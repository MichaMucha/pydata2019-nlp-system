from bs4 import BeautifulSoup
from pathlib import Path
import requests


def get_imgur_gallery_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    img_ids = [
        i['id'] for i in
        soup.select('.post-image-container')
    ]
    return [
        f'https://i.imgur.com/{img_id}.png'
        for img_id in img_ids
    ]


def parse_url(url):
    if Path(url).suffix[1:] in ['jpg', 'png', 'jpeg']:
        parsed = url
        is_photo = True
    elif 'imgur.com' in url:
        if 'gallery' in url:
            parsed = get_imgur_gallery_images(url)
        else:
            img_id = Path(url).name
            parsed = f'https://i.imgur.com/{img_id}.png'
        is_photo = True
    else:
        parsed = url
        is_photo = False
    return parsed, is_photo
