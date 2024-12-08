import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

API_TOKEN = '8180343293:AAEnH5aGstLSYZ0RvBRrr8Wx1AQRubRsat4'  # Ваш токен API
ADMIN_ID = '7018589360'  # Ваш Telegram ID

bot = telebot.TeleBot(API_TOKEN)

# Хранилище для заблокированных пользователей
blocked_users = set()
user_messages = {}  # Хранилище для сообщений пользователей

# Функция для блокировки пользователя
def block_user(user_id):
    blocked_users.add(user_id)

# Функция для отправки сообщения админу с кнопками
def send_message_to_admin(message, user_id):
    forwarded_message = f"Сообщение от @{message.from_user.username or message.from_user.first_name} (ID: {user_id}): {message.text}"
    
    markup = InlineKeyboardMarkup()
    block_button = InlineKeyboardButton(text="Заблокировать", callback_data=f"block_{user_id}")
    reply_button = InlineKeyboardButton(text="Ответить", callback_data=f"reply_{user_id}")
    markup.add(block_button, reply_button)

    try:
        bot.send_message(chat_id=ADMIN_ID, text=forwarded_message, reply_markup=markup)
    except Exception as e:
        pass  # Подавляем вывод ошибок

# Хэндлер для приема сообщений от пользователей
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id

    # Проверяем, не заблокирован ли пользователь
    if user_id in blocked_users:
        try:
            bot.send_message(message.chat.id, "Вы были убиты TERRIFIERом")
        except:
            pass  # Подавляем ошибки
        return

    # Сохраняем сообщение пользователя
    user_messages[user_id] = message.text

    # Пересылаем сообщение администратору
    send_message_to_admin(message, user_id)

    # Подтверждение пользователю
    bot.send_message(message.chat.id, "Сообщение отправлено, жди")

    # Отправка сообщения с инлайн-кнопкой "БИО TERRIFIERа"
    bio_markup = InlineKeyboardMarkup()
    bio_button = InlineKeyboardButton(text="БИО TERRIFIERа", url="https://t.me/+s6yAr9ehsGQ1NjBi")
    bio_markup.add(bio_button)
    
    bot.send_message(message.chat.id, "НЕ ЗАБУДЬ ПОСЕТИТЬ БИО TERRIFIERа:", reply_markup=bio_markup)

# Обработчик для кнопки "Заблокировать"
@bot.callback_query_handler(func=lambda call: call.data.startswith('block_'))
def handle_block(call):
    user_id = int(call.data.split('_')[1])
    block_user(user_id)

    try:
        bot.send_message(ADMIN_ID, f"Пользователь с ID {user_id} был заблокирован.")
    except:
        pass  # Подавляем ошибки

    bot.answer_callback_query(call.id, "Пользователь заблокирован.")

# Обработчик для кнопки "Ответить"
@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def handle_reply(call):
    user_id = int(call.data.split('_')[1])
    bot.send_message(call.message.chat.id, "Введите ваше сообщение для пользователя:")
    bot.register_next_step_handler(call.message, lambda message: send_reply(message, user_id))

def send_reply(message, user_id):
    try:
        bot.send_message(user_id, f"TERRIFIER: {message.text}")
        bot.send_message(ADMIN_ID, "Ответ успешно отправлен пользователю.")
    except:
        pass  # Подавляем ошибки

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)  # Запуск бота
        except Exception as e:
            time.sleep(5)  # Ждем 5 секунд перед новой попыткой