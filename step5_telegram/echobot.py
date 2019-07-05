import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
load_dotenv()


API_TOKEN = os.getenv('TELEGRAM_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    sender = message.chat.id
    await bot.send_message(
        sender, f'Hi! Your id is {sender}'
    )

executor.start_polling(dp, skip_updates=True)#, loop=loop)