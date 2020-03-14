import requests
import random
import telebot
from telebot.types import InlineKeyboardButton as Button
from telebot.types import InlineKeyboardMarkup as Markup
from telebot.types import ReplyKeyboardRemove
from PIL import Image, ImageFont, ImageDraw

DEMOTIVATOR_TEMPLATE_PATH = 'template.png'
FONT_PATH = 'times.ttf'
PHRASES_PATH = 'phrases.txt'
DEMOTIVATOR_PICTURE_POS = (23,22)
DEMOTIVATOR_TEXT_POS = (250,540)
DEMOTIVATOR_PICTURE_SIZE = (454,454)
token = "1110888415:AAFSA3wSGrrbrwUj4kc_lY5NgBI4shZzD4o"
bot = telebot.TeleBot(token)

def answer(id, text, alert = False):
    try:
        return bot.answer_callback_query(
            id,
            text,
            alert
        )
    except: pass

def delete(message):
    try:
        bot.delete_message(
            message.chat.id,
            message.message_id
        )
    except: pass

def send(id, text, markup = None):
    try:
        return bot.send_message(
            id,
            text,
            parse_mode = 'html',
            reply_markup = markup,
            disable_web_page_preview = True
        )
    except: pass

def edit(chatid, messageid, text, markup = None):
    try:
        return bot.edit_message_text(
            text,
            chatid,
            messageid,
            parse_mode = 'html',
            reply_markup = markup,
            disable_web_page_preview = True
        )
    except: pass

def random_text():
    with open(PHRASES_PATH, 'rt', encoding='utf-8') as file:
        return random.choice(file.readlines()).strip()

def format(text, params = {}):
    for key, value in params.items():
        text = text.replace(f"${key}", str(value))
    return text

def generate_demotivator(path, text):
    id = random.randint(0,10000000)
    demotivator = Image.open(DEMOTIVATOR_TEMPLATE_PATH).convert('RGBA')
    picture = Image.open(path).convert('RGBA')
    picture = picture.resize(DEMOTIVATOR_PICTURE_SIZE, Image.ANTIALIAS)
    demotivator.paste(picture, DEMOTIVATOR_PICTURE_POS)
    font = ImageFont.truetype(FONT_PATH, 36)
    draw = ImageDraw.Draw(demotivator)
    text = text.replace(' - ', "\n")
    width, height = draw.textsize(text, font = font)
    draw.text(
        (
            DEMOTIVATOR_TEXT_POS[0] - width/2,
            DEMOTIVATOR_TEXT_POS[1] - height/2
        ),
        text,
        (255,255,255),
        font = font,
        align = 'center'
    )
    path = f"out/{id}.png"
    demotivator.save(open(path, 'wb'), "PNG")
    return path

@bot.message_handler(content_types = ['photo'])
def handle_photo(message):
    sender = message.from_user
    photo = message.photo[0].file_id
    filepath = bot.get_file_url(photo)
    data = requests.get(filepath)
    filename = filepath.split('/')[-1]
    path = f"temp/{filename}"
    open(path, 'wb').write(data.content)
    out = generate_demotivator(path, text = random_text())
    try: bot.send_photo(sender.id, open(out, 'rb'))
    except Exception as e: print(e)

bot.polling()
