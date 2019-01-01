import telebot
import os
import random

# CONSTANTS
TOKEN = "714529585:AAHi_JisI_7ztewDLZeaoHsUUSrDRMlR2VY"
PHOTOS_DIR = "./photos"
CHATS_DB = "Chats.dat"


def load_chats():
    """ Load chats' identifiers from a file. """
    try:
        with(open(CHATS_DB, 'r')) as f:
            chats = set(map(int, f.read().splitlines()))
    except Exception as error:
        print(error)
        chats = set()
    return chats

def save_chats(chats):
    """ Save chats' identifiers in a file. """
    try:
        with(open(CHATS_DB, 'w+')) as f:
            for c in chats:
                f.write("%s\n" % c)
    except Exception as error:
        print(error)

def get_photos():
    """ Load photos on a directory. """
    try:
        photos = os.listdir(PHOTOS_DIR)
    except Exception as error:
        print(error)
        photos = []
    return photos

def get_random_photo():
    """ Get a random photo from the photos directory. """
    try:
        photos = get_photos()
        sample = random.sample(photos, 1)[0]
    except Exception as error:
        print(error)
        sample = None
    return sample

def send_photo(bot, chats, photo):
    """ Send a photo to all chats.
    Return the set of chats that do not exist anymore. """
    invalid_chats = []
    image = open(PHOTOS_DIR + '/' + photo, 'rb')
    for c in chats:
        try:
            bot.send_photo(c, image)
        except Exception as error:
            print("Error: " + str(c))
            print(error)
            invalid_chats.append(c)
    image.close()
    return set(invalid_chats)


if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)

    chats = load_chats()
    updates = bot.get_updates()
    chats |= set([u.message.chat.id for u in updates if u.message.chat.type == 'group'])

    photo = get_random_photo()
    print("Chats: " + str(chats))
    print("Photo: " + str(photo))
    invalid_chats = send_photo(bot, chats, photo)
    chats -= invalid_chats

    save_chats(chats)
