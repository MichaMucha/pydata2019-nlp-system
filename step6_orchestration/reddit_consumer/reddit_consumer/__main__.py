from time import sleep
from os import getenv

from reddit_consumer.reddit import get_subreddit, extract_comment, extract_post
from reddit_consumer.preprocessing import message_to_sentences, replace_urls
from tqdm import tqdm
from praw.exceptions import APIException, ClientException
import fire
import redis
import ujson

REDIS_HOST = getenv('REDIS_URL', 'localhost')

class StreamConsumer:

    def __init__(self):
        self.sub = get_subreddit()
        self.__retries = 10
        self.__delay_before_retry = 360 # seconds

    def stdout(self, stream='comments'):
        try:
            s = self.sub.stream
            s = s.comments if stream == 'comments' else s.submissions
            f = extract_comment if stream == 'comments' else extract_post
            for c in tqdm(s()):
                print(f(c))
        except KeyboardInterrupt:
            print('\nShutting down..')
    
    def redis(self, stream='comments'):
        r : redis.Redis = redis.Redis(host=REDIS_HOST)
        try:
            s = self.sub.stream
            s = s.comments if stream == 'comments' else s.submissions
            f = extract_comment if stream == 'comments' else extract_post
            for c in tqdm(s()):
                msg = f(c)
                text = replace_urls(msg['text'])
                sentences = message_to_sentences(text)
                for s in sentences:
                    r.publish(stream, ujson.dumps(s))

                author = msg['author']
                key = f'{stream}:{author}'
                r.incr(key)
                r.expire(key, 3600*24)

        except APIException as e:
            print(e)
            self.__retry()
        except ClientException as e:
            print(e)
            self.__retry()
    
    def __retry(self):
        if self.__retries == 0:
            exit(0)
        self.__retries -= 1
        sleep(self.__delay_before_retry)
        self.redis()
        


def main():
    fire.Fire(StreamConsumer)

if __name__ == "__main__":
    main()
