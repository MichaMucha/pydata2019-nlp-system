from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import CantParseEntities
from dotenv import load_dotenv, find_dotenv
from signal import signal, SIGINT
from tqdm import tqdm
from os import getenv
import sys
import fire
import uvloop
import redis

load_dotenv(find_dotenv('.telegram'))
uvloop.install()

REDIS_HOST = getenv('REDIS_URL', 'localhost')
channel_id = getenv('MY_TELEGRAM_NUMBER')

async def push_update(content, bot):
    try:
        return await bot.send_message(
            channel_id, content, parse_mode='Markdown')
    except CantParseEntities:
        return await bot.send_message(channel_id, content)


async def listen(source):
    r_conn = redis.Redis(REDIS_HOST)
    p = r_conn.pubsub(ignore_subscribe_messages=True)
    p.subscribe(source)
    for message in tqdm(p.listen()):
        yield message['data']


async def subscribe_and_listen(bot, channel_name='processed'):
    async for message in listen(channel_name):
        await push_update(message, bot)

def main():
    fire.Fire(TelegramPublisher)

class TelegramPublisher:
    def publish(self, channel_name='processed'):
        signal(SIGINT, interrupt_handler)
        try:
            loop = uvloop.new_event_loop()
            bot = Bot(token=getenv('TELEGRAM_KEY'), loop=loop)
            task = loop.create_task(subscribe_and_listen(bot, channel_name))
            loop.run_until_complete(task)
        finally:
            task.cancel()
            loop.run_until_complete(bot.close())
            loop.close()


def interrupt_handler(signal, frame):
    print('\nYou pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    main()
