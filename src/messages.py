from domain import Article
from typing import List

def _escape_str(s):
    return s.translate(str.maketrans({'-': '\-', '(': '\(', ')': '\)', '.': '\.'}))

def create_message(articles: List[Article]) -> str:
    msg = ''
    for article in articles:
        if len(msg) > 0:
            msg += '\n'
        msg += f'{article.rank}\. [{_escape_str(article.title)}]({_escape_str(article.link)}) \- {article.score}'
    return msg
