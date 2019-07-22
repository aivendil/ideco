import datetime
import json

from aiohttp import web

from test_task.settings import comments, all_news


async def get_comments(news_id):
    filtered = filter(lambda comment: comment['news_id'] == news_id, comments)
    return list(filtered)


async def get_all_news(request):
    for news in all_news:
        news['comments_count'] = len(await get_comments(news['id']))
    filtered_news = list(
        filter(lambda news: not news['deleted'] and
                            datetime.datetime.fromisoformat(news['date']) < datetime.datetime.now(),
               all_news))
    return web.json_response({'news': filtered_news})


