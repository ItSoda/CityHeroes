import urllib.request
from io import BytesIO

import requests
import telebot
from django.conf import settings
from django.core.files import File
from telebot import types

from .models import News, Tg_Bot

# Вставляем токен бота
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        if Tg_Bot.objects.get(user_id=user_id):
            bot.reply_to(
                message,
                f"Мы всегда с вами {first_name}! Воспользуйся /help для подробной информации",
            )

    except Tg_Bot.DoesNotExist:
        Tg_Bot.objects.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.send_message(
            message.chat.id,
            f"Привет, {first_name}! Воспользуйся /help для подробной информации",
        )


# Рассылка всем пользователям от лица админа
@bot.message_handler(commands=["send_message"])
def send_message(message):
    if int(settings.ADMIN_ID) == int(message.chat.id):
        markup = types.ForceReply(selective=False)
        bot.send_message(
            message.chat.id,
            "Введите текст сообщения, которое хотите отправить:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(message, process_text)
    else:
        bot.send_message(message.chat.id, "Вы не администратор")


def process_text(message):
    text = message.text.strip()
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        "Теперь отправьте фотографию для этого сообщения: \nЕсли не хотите то '-'",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, process_photo, text)


def process_photo(message, text):
    if message.photo:
        photo = message.photo[-1].file_id  # Получаем file_id фотографии
        users = Tg_Bot.objects.all()

        for user in users:
            try:
                bot.send_photo(user.user_id, photo, caption=text)
                News.objects.create(text=text, photo=photo)
            except Exception as e:
                print(f"Произошла ошибка {e}")
        else:
            bot.send_message(message.chat.id, "Рассылка завершена")
    else:
        users = Tg_Bot.objects.all()

        for user in users:
            try:
                bot.send_message(user.user_id, text)
                News.objects.create(
                    text=text,
                )
            except Exception as e:
                print(f"Произошла ошибка {e}")


@bot.message_handler(commands=["news"])
def news(message):
    news = News.objects.all()

    for new in news:
        if new.photo is not None:
            photo_path = new.photo.path
            caption = new.text
            send_photo_with_caption(bot, message.chat.id, photo_path, caption)
        else:
            bot.send_message(message.chat.id, f"{new.text}")


def send_photo_with_caption(bot, chat_id, photo_path, caption):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id, photo, caption=caption)


@bot.message_handler(commands=["app"])
def app(message):
    bot.send_message(
        message.chat.id, "Скачайте наше бесплатное приложение по ссылке: https.."
    )


@bot.message_handler(commands=["help"])
def help(message):
    text = "Команды:\n/start - перезапуск бота \n/help - Помощь \n/app - ссылка на наше приложение \n/news - новости нашего проекта"
    bot.send_message(
        message.chat.id,
        f"Приветствую {message.from_user.first_name}\n \n{text}",
        parse_mode="html",
    )


# Ловит любое сообщение
@bot.message_handler()
def info(message):
    if message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")
    bot.reply_to(message, f"Лучше взгляните на наших животных ;)")


def start_bot():
    bot.polling(non_stop=True)


def stop_bot():
    bot.stop_polling()
