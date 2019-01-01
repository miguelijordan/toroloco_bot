import telebot

TOKEN = "714529585:AAHi_JisI_7ztewDLZeaoHsUUSrDRMlR2VY"
PHOTOS_FOLDER = "/photos"
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

if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)

    chats = load_chats()
    updates = bot.get_updates()
    chats |= set([u.message.chat.id for u in updates])


    save_chats(chats)
    print(chats)

    # updates = bot.get_updates()
    # print([u.message.chat.title for u in updates])
    # chat_id = bot.get_updates()[-1].message.chat.id
    # print(updates[-1].message.chat)
