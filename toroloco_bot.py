"""
Telegram bot that sends photos to chat groups.
"""
import telebot
import os
import random
import logging

# CONSTANTS
TOKEN = ""
PHOTOS_DIR = "./photos"
CHATS_DB = "Chats.dat"


def load_chats():
    """ Load chats' identifiers from a file. """
    try:
        with(open(CHATS_DB, 'r')) as f:
            chats = set(map(int, f.read().splitlines()))
    except Exception as error:
        logging.error("Error loading chats.\n%s" % error)
        chats = set()
    return chats

def save_chats(chats):
    """ Save chats' identifiers in a file. """
    try:
        with(open(CHATS_DB, 'w+')) as f:
            for c in chats:
                f.write("%s\n" % c)
    except Exception as error:
        logging.error("Error saving chats.\n%s" % error)

def get_photos():
    """ Load photos on a directory. """
    try:
        photos = os.listdir(PHOTOS_DIR)
    except Exception as error:
        logging.error("Error getting photos.\n%s" % error)
        photos = []
    return photos

def get_random_photo():
    """ Get a random photo from the photos directory. """
    try:
        photos = get_photos()
        logging.info("#Photos: %i" % len(photos))
        sample = random.sample(photos, 1)[0]
    except Exception as error:
        logging.error("Error getting random photo.\n%s" % error)
        sample = None
    return sample

def send_photo(bot, chats, photo_path):
    """ Send a photo to all chats.
    Return the set of chats that do not exist anymore. """
    invalid_chats = []
    for c in chats:
        try:
            image = open(photo_path, 'rb')
            bot.send_photo(c, image)
            image.close()
        except Exception as error:
            logging.error("Invalid chat: %i.\n%s" % (c, error))
            print(error)
            invalid_chats.append(c)
    return set(invalid_chats)

def get_photo_path(photo):
    return PHOTOS_DIR + '/' + photo

def remove_photo(photo_path):
    os.remove(photo_path)


if __name__ == '__main__':
    logging.basicConfig(filename='toro.log', filemode='a+', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',)
    logging.info("Toro Loco running...")

    bot = telebot.TeleBot(TOKEN)

    chats = load_chats()
    updates = bot.get_updates()
    chats |= set([u.message.chat.id for u in updates if u.message.chat.type == 'group'])
    logging.info("#Chat groups: %i" % len(chats))

    photo = get_random_photo()
    if photo is not None:
        photo_path = get_photo_path(photo)
        invalid_chats = send_photo(bot, chats, photo_path)
        remove_photo(photo_path)

        chats -= invalid_chats
        logging.info("#Photo (%s) sent to %i chat groups." % (photo_path, len(chats)))
        logging.info("#Invalid chat groups: %i" % len(invalid_chats))

        save_chats(chats)

    logging.info("Toro Loco finished!")
