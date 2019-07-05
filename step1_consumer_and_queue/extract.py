from typing import Dict
from praw.models import Comment, Submission


def extract_post(post: Submission) -> Dict:
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

def extract_comment(comment: Comment, sub_id=None) -> Dict:
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