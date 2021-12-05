import asyncio, aiohttp, datetime

URL_STORIES = 'https://hacker-news.firebaseio.com/v0/newstories.json'
URL_STORY = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

def story_filter(story):
    return story is not None and 'title' in story and 'url' in story and 'score' in story

async def get(session, url):
    async with session.get(url, ssl=False) as r:
        return await r.json()

async def main():
    async with aiohttp.ClientSession() as session:
        ids = await get(session, URL_STORIES)
        requests = [get(session, URL_STORY.format(id)) for id in ids]
        print('Request stories')
        stories = await asyncio.gather(*requests)
        stories = filter(story_filter, stories)
        stories = sorted(stories, key=lambda s: int(s['score']), reverse=True)
        return stories
        

event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)
stories = event_loop.run_until_complete(main())

for story in stories[:10]:        
    print('title =', story['title'])
    print('url =', story['url'])
    print('score =', story['score'])
    print('time =', datetime.datetime.fromtimestamp(int(story['time'])))
    print('-' * 10)