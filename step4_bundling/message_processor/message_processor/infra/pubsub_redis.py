from multiprocessing import Process
import sys
import redis
import uvloop
import ujson
from signal import signal, SIGINT
from typing import Callable
from dotenv import load_dotenv, find_dotenv
from os import getenv
from tqdm import tqdm
load_dotenv(find_dotenv())

REDIS_HOST = getenv('REDIS_URL', 'localhost')
SUBREDDIT = getenv('SUBREDDIT')
uvloop.install()

def launch_pubsub_task(func: Callable, 
        source='comments', sink='processed', subprocess=False):
    async def pubsub_func():
        r = redis.Redis(REDIS_HOST)
        async for message in listen(source):
            if message is StopAsyncIteration:
                break
            output = func(message['data'])
            if output is not None:
                await publish(r, sink, output)

    def run_task():
        loop = uvloop.new_event_loop()
        task = loop.create_task(pubsub_func())    
        try:
            loop.run_until_complete(task)
        finally:
            print('Stopping...')
            task.cancel()
            loop.stop()
            loop.close()

    signal(SIGINT, interrupt_handler)

    if subprocess:
        process = Process(target=run_task)
        process.start()
    else:
        run_task()
        
    

async def listen(source):
    r_conn = redis.Redis(REDIS_HOST)
    p = r_conn.pubsub(ignore_subscribe_messages=True)
    p.subscribe(source)
    for message in tqdm(p.listen()):
        yield message


async def publish(r, sink, message):
    r.publish(sink, message)


def interrupt_handler(signal, frame):
    print('\nYou pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    @launch_pubsub_task
    def test(a):
        a = ujson.loads(a)
        text = a['text']
        author = a['author']
        c_id = a['id']
        return (f'Message size: {len(text)}, '
                f'author: {author}, [id: {c_id}]'
                f'(https://www.reddit.com/r/{SUBREDDIT}/comments/{c_id}/)')
