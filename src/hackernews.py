import aiohttp, asyncio
from typing import List
from domain import Article

URL_NEWSTORIES = 'https://hacker-news.firebaseio.com/v0/newstories.json'
URL_STORY = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

async def get(session, url):
    async with session.get(url, ssl=False) as r:
        return await r.json()

async def _get_top_articles():

    async with aiohttp.ClientSession() as session:
        ids = await get(session, URL_NEWSTORIES)
        requests = [get(session, URL_STORY.format(id)) for id in ids]
        stories = await asyncio.gather(*requests)
        stories = filter(_story_filter, stories)
        stories = sorted(stories, key=lambda s: int(s['score']), reverse=True)
        return stories

def _story_filter(story):
    return story is not None and 'title' in story and 'url' in story and 'score' in story

async def get_top_arcticles(limit: int = 5) -> list[Article]:
    articles_json = await _get_top_articles()
    articles = []
    for article_json in articles_json[:limit]:
        articles.append(
            Article(
                title=article_json['title'],
                link=article_json['url'],
                score=article_json['score']
            )
        )
    return articles
