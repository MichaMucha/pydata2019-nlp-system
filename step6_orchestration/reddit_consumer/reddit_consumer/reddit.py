import os
import requests
from os import getenv
from pathlib import Path

import pandas as pd
import praw
from praw.models import Comment, Submission, MoreComments
from tqdm import tqdm
from dotenv import load_dotenv

from reddit_consumer.parse_url import parse_url

load_dotenv()

REDDIT_ID = getenv('REDDIT_ID')
REDDIT_SECRET = getenv('REDDIT_SECRET')
REDDIT_USER = getenv('REDDIT_USER')

def get_reader():
    return praw.Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER
    )

def get_subreddit(sub=None, reader=None):
    if reader is None:
        reader = get_reader()
    if sub is None:
        sub = getenv('SUBREDDIT')

    return reader.subreddit(sub)

def extract_post(post: Submission):
    sub = post
    link, is_photo = parse_url(sub.url)
    return {
        'author': sub.author.name,
        'title': sub.title,
        'flair': sub.link_flair_text,
        'link': link,
        'text': sub.selftext,
        'created_utc': sub.created_utc,
        'url_is_photo': is_photo,
        'id': sub.id,
        'score': sub.score
    }


def extract_comment(comment: Comment, sub_id=None):
    c = comment
    author = c.author.name if c.author != None else ''
    r = dict(
        created_utc=c.created_utc,
        text=c.body,
        id=c.id,
        score=c.score,
        author=author
    )
    if sub_id != None:
        r.update({'parent': sub_id})
    return r


def search_and_download_by_flair(flair, subreddit, 
                                 path=Path('data/posts')):
    flair_posts = subreddit.search(f'flair:"{flair}"', limit=1000)
    posts = [extract_post(post) for post in tqdm(flair_posts)]
    posts = pd.DataFrame(posts)
    posts['created_utc'] = pd.to_datetime(posts.created_utc, unit='s')
    posts.to_csv(path / f'{flair}.csv')
    return posts


def download_images(flair, posts: pd.DataFrame, path=Path('data/posts')):
    links = posts[posts.url_is_photo].set_index('id').link
    os.makedirs(path / flair, exist_ok=True)
    links = unroll_galleries(links)
    for post_id, link in tqdm(links.iteritems()):
        img = requests.get(link)
        if img.status_code != 200:
            print('problem with', post_id, img.status_code)
            continue
        save_image(
            path / flair,
            f'{post_id}{Path(link).suffix}',
            img.content
        )


def unroll_galleries(links):
    galleries = links[links.apply(type) == list]
    links = links.drop(galleries.index)
    for p, l in galleries.iteritems():
        links = links.append(
            pd.Series({
                f'{p}-{i}': link
                for i, link in enumerate(l, 1)
            })
        )
    return links


def save_image(path, filename, image_bytes):
    (path / filename).write_bytes(image_bytes)
