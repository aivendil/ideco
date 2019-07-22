import datetime
import json

from aiohttp import web

from test_task.settings import all_comments, all_news


def check_news_available(news):
    """
    Check, that news is not deleted and it's date earlier than now
    :param news: News dict
    :type news: dict
    :rtype: bool
    """
    return not news['deleted'] and datetime.datetime.fromisoformat(news['date']) < datetime.datetime.now()


async def find_comments_by_news_id(news_id, comments):
    filtered = filter(lambda comment: comment['news_id'] == news_id, comments)
    return list(filtered)


async def find_news(news_id, all_news, comments):
    filtered_news = list(filter(lambda news: news['id'] == news_id, all_news))
    if len(filtered_news) == 0:
        return None
    else:
        news = filtered_news[0]
        comments = await find_comments_by_news_id(news_id, comments)
        news['comments'] = comments
        news['comments_count'] = len(comments)
        return news


async def get_all_news(request):
    for news in all_news:
        news['comments_count'] = len(await find_comments_by_news_id(news['id'], all_comments))
    filtered_news = list(
        filter(check_news_available, all_news))
    return web.json_response({'news': filtered_news})


async def get_news_by_id(request):
    news_id = int(request.match_info['news_id'])
    news = await find_news(news_id, all_news, all_comments)
    if news is None or not check_news_available(news):
        return web.HTTPNotFound()
    return web.json_response({'news': news})


