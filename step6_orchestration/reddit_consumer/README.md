# Reddit comments consumer

## Getting started with docker

Set your reddit keys and the desired subreddit in `.env`

```sh
docker build -t reddit_consumer .
docker run -it --env-file='./.env' reddit_consumer
```