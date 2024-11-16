import telebot
import os
import subprocess

with open("token.txt",'r') as f:
	API_TOKEN = f.readline()
bot = telebot.TeleBot(API_TOKEN)


BEATS_FOLDER = 'beats/'

@bot.message_handler(content_types=['document', 'audio'])
def save_beats(message):
    file = message.audio or message.document
    if file:
        file_id = file.file_id
        new_file = bot.get_file(file_id)
        
        downloaded_file = bot.download_file(new_file.file_path)
        
        with open(f'{BEATS_FOLDER}{file.file_name}', 'wb') as f:
            f.write(downloaded_file)

        bot.reply_to(message, f'Файл {file.file_name} сохранен в папку beats.')


def run_send_script(argument):
    subprocess.run(['python', 'send.py', argument])

def run_clear_script():
    subprocess.run(['python', 'clear.py'])

def send_buttons(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        telebot.types.KeyboardButton("Добавить биты"),
        telebot.types.KeyboardButton("Заслать только артистам, которым уже отправляли"),
        telebot.types.KeyboardButton("Отправить биты только новеньким"),
        telebot.types.KeyboardButton("Сначала отправить артистам, которым отправляли, а потом новеньким"),
        telebot.types.KeyboardButton("Очистить папку с битами")
    )
    bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    send_buttons(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_button(call):
    if call.data == 'add_beats':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправьте биты, которые хотите добавить.")
    elif call.data == 'send_existing':
        run_send_script('2')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправка артистам, которым уже отправляли, началась.")
    elif call.data == 'send_new':
        run_send_script('1')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправка новеньким началась.")
    elif call.data == 'send_all':
        run_send_script('2')
        run_send_script('1')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправка артистам, которым отправляли, и новеньким началась.")
    elif call.data == 'clear_beats':
        run_clear_script()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Папка с битами очищена.")

if not os.path.exists(BEATS_FOLDER):
    os.makedirs(BEATS_FOLDER)

bot.polling(none_stop=True)
