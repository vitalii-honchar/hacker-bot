import requests
from typing import List
from domain import Article
from bs4 import BeautifulSoup

RESOURCE_URL = 'https://news.ycombinator.com/'

def _parse_response(html: str) -> List[Article]:
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    for itemNode in soup.find_all('tr', class_='athing'):
        linkNode = itemNode.find('a', class_='titlelink')
        scoreNode = soup.find('span', id='score_' + itemNode['id'])

        article = Article(
            rank=itemNode.find('span', class_='rank').text.replace('.', ''),
            link=linkNode['href'],
            title=linkNode.text,
            score=int(scoreNode.text.split()[0]) if scoreNode is not None else 0
        )
        articles.append(article)

    return articles

def get_top_arcticles(limit: int = 10):
    res = requests.get(RESOURCE_URL)
    if res.status_code != 200:
        raise ResourceError(f'Invalid status code: status_code = {res.status_code}')
    return sorted(_parse_response(res.text), key=lambda i: i.score, reverse=True)[:limit]

class ResourceError(Exception):
    pass