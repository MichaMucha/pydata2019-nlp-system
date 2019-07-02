import redis

def most_active_commenters(r: redis.Redis, n=10):
    result = sorted(
        (int(r.get(k)), k.decode()) 
        for k in r.keys('comments:*')
        )[-n:]
    return list(reversed(result))