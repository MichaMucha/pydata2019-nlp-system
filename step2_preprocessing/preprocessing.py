import re
import html
from typing import Collection, Dict

from praw.models import Comment, Submission

__all__ = [
     'extract_post',
     'extract_comment',
     'message_to_sentences',
     'replace_urls',
     'spec_add_spaces',
     'rm_useless_spaces',
     'replace_rep',
     'replace_wrep',
     'fix_html',
     'replace_all_caps',
     'deal_caps'
]

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

def message_to_sentences(message:Dict, minimum_characters:int=5) -> str:
    text = message['text']
    sentences = []
    for line in text.split('\n'):
        sentences += line.split('.')
    return [s for s in sentences if len(s) > minimum_characters]

def replace_urls(text:str) -> str:
    MARKDOWN_URL_REGEX = (
        r'((\[.+?\]\()?(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)(?:\))?)'
    )
    return text.replace(
        MARKDOWN_URL_REGEX,
        __re_sub_urls
    )

def __re_sub_urls(match):
    url = match.group(2)[1:-2]
    if match.group(3)[:-1] == match.group(2)[1:-2].replace('\_', '_'):
        return "<URL>"
    else:
        return f"{url} <URL>"

# Adopted from fast.ai
# https://github.com/fastai/fastai/blob/master/fastai/text/transform.py

BOS,EOS,FLD,UNK,PAD = 'xxbos','xxeos','xxfld','xxunk','xxpad'
TK_MAJ,TK_UP,TK_REP,TK_WREP = 'xxmaj','xxup','xxrep','xxwrep'

def spec_add_spaces(t:str) -> str:
    "Add spaces around / and # in `t`. \n"
    return re.sub(r'([/#\n])', r' \1 ', t)

def rm_useless_spaces(t:str) -> str:
    "Remove multiple spaces in `t`."
    return re.sub(' {2,}', ' ', t)

def replace_rep(t:str) -> str:
    "Replace repetitions at the character level in `t`."
    def _replace_rep(m:Collection[str]) -> str:
        c,cc = m.groups()
        return f' {TK_REP} {len(cc)+1} {c} '
    re_rep = re.compile(r'(\S)(\1{3,})')
    return re_rep.sub(_replace_rep, t)

def replace_wrep(t:str) -> str:
    "Replace word repetitions in `t`."
    def _replace_wrep(m:Collection[str]) -> str:
        c,cc = m.groups()
        return f' {TK_WREP} {len(cc.split())+1} {c} '
    re_wrep = re.compile(r'(\b\w+\W+)(\1{3,})')
    return re_wrep.sub(_replace_wrep, t)

def fix_html(x:str) -> str:
    "List of replacements from html strings in `x`."
    re1 = re.compile(r'  +')
    x = x.replace('#39;', "'").replace('amp;', '&').replace('#146;', "'").replace(
        'nbsp;', ' ').replace('#36;', '$').replace('\\n', "\n").replace('quot;', "'").replace(
        '<br />', "\n").replace('\\"', '"').replace('<unk>',UNK).replace(' @.@ ','.').replace(
        ' @-@ ','-').replace(' @,@ ',',').replace('\\', ' \\ ')
    return re1.sub(' ', html.unescape(x))

def replace_all_caps(x:Collection[str]) -> Collection[str]:
    "Replace tokens in ALL CAPS in `x` by their lower version and add `TK_UP` before."
    res = []
    for t in x:
        if t.isupper() and len(t) > 1: res.append(TK_UP); res.append(t.lower())
        else: res.append(t)
    return res

def deal_caps(x:Collection[str]) -> Collection[str]:
    "Replace all Capitalized tokens in `x` by their lower version and add `TK_MAJ` before."
    res = []
    for t in x:
        if t == '': continue
        if t[0].isupper() and len(t) > 1 and t[1:].islower(): res.append(TK_MAJ)
        res.append(t.lower())
    return res
