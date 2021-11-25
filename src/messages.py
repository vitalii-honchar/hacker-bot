from domain import Article
from typing import List
from datetime import date

def _escape_str(s):
    return s.translate(str.maketrans({'-': '\-', '(': '\(', ')': '\)', '.': '\.'}))

def _create_link(title, link):
    return f'[{_escape_str(title)}]({_escape_str(link)})'

def create_message(articles: List[Article]) -> str:
    msg = f'*News for {date.today().strftime("%B %d, %Y")}*'
    counter = 1
    for article in articles:
        msg += f'\n{counter}\. {_create_link(article.title, article.link)}'
        counter += 1
    return msg
