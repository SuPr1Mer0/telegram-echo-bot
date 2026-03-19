# Telegram Echo Bot с базой данных

Простой, но демонстрационный Telegram-бот на Python, который:
- отвечает эхом
- сохраняет все сообщения в SQLite
- показывает статистику и историю

## Возможности
- Команды: /start, /stats, /history
- Сохранение user_id, username, текст, timestamp
- Reply-клавиатура

## Стек
- pyTelegramBotAPI
- SQLite3
- python-dotenv

## Запуск

```bash
pip install -r requirements.txt
# создай .env с BOT_TOKEN=...
python main.py
