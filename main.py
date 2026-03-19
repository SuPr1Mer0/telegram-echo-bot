import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

import db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

bot = telebot.TeleBot(TOKEN)


def make_start_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 Статистика", callback_data="stats"),
        InlineKeyboardButton("🕒 Последние сообщения", callback_data="history")
    )
    markup.add(
        InlineKeyboardButton("ℹ️ О боте", callback_data="about"),
        InlineKeyboardButton("🔄 Обновить", callback_data="refresh")
    )
    return markup


@bot.message_handler(commands=['start'])
def cmd_start(message):
    text = (
        "Привет! 👋 Я эхо-бот.\n"
        "Пиши мне что угодно — я повторю и сохраню.\n\n"
        "Или нажми на кнопки ниже:"
    )
    bot.reply_to(message, text, reply_markup=make_start_inline_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user
    uid = user.id
    username = user.username or "без имени"

    if call.data == "stats":
        count = db.get_message_count(uid)
        text = f"@{username}, от тебя сохранено сообщений: **{count}**"
        bot.answer_callback_query(call.id, "Статистика готова!")
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    elif call.data == "history":
        rows = db.get_last_messages(uid, 5)
        if not rows:
            text = "У тебя пока нет сообщений в базе."
        else:
            text = "Твои последние сообщения:\n\n"
            for i, (msg_text, dt) in enumerate(rows, 1):
                text += f"{i}. {msg_text}\n   _{dt}_\n\n"

        bot.answer_callback_query(call.id, "История загружена!")
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    elif call.data == "about":
        text = (
            "Это демонстрационный эхо-бот для портфолио.\n"
            "• Сохраняет все сообщения в SQLite\n"
            "• Inline-кнопки\n"
            "• Статистика и история\n\n"
            "Создан для примера — могу сделать под твой проект!"
        )
        bot.answer_callback_query(call.id, "О боте")
        bot.send_message(call.message.chat.id, text)

    elif call.data == "refresh":
        bot.answer_callback_query(call.id, "Клавиатура обновлена")
        bot.send_message(
            call.message.chat.id,
            "Обновлённое меню:",
            reply_markup=make_start_inline_keyboard()
        )


@bot.message_handler(func=lambda m: True)
def echo_and_save(message):
    # Пропускаем служебные сообщения (если нужно)
    if message.text.startswith('/'):
        return

    user = message.from_user
    username = user.username
    uid = user.id
    text = message.text

    # Сохраняем в БД
    db.save_message(uid, username, text)

    # Отвечаем эхом
    reply = f"\n{text}\n\n"
    bot.reply_to(message, reply)


if __name__ == "__main__":
    print("Запуск бота...")
    db.init_db()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)