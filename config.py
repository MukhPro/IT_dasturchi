from aiogram import Bot, Dispatcher
import os


BOT_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
