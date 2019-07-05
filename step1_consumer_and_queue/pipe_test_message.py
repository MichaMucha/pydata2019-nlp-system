import redis
import fire
import mq

def send_test_message(text:str='Pigs in space!'):
    test_comment = {
        'created_utc': 1562368219.0,
        'text': text,
        'id': 'eszutd4',
        'score': 9001,
        'author': 'Josh McTester'
    }

    r = redis.Redis()

    r.publish(
        'comments', 
        mq.serialize_message_data(test_comment)
    )

if __name__ == "__main__":
    fire.Fire(send_test_message)