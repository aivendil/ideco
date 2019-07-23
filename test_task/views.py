import datetime

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
    """
    Find all comments, related with given news
    :param news_id: Id of news
    :type news_id: int
    :param comments: List of comment in which will be searched
    :type comments: list of dict
    :return: List of found comments
    :rtype: list of dict
    """
    filtered = filter(lambda comment: comment['news_id'] == news_id, comments)
    return list(filtered)


async def find_news(news_id, all_news, comments):
    """
    Find news with given id. In founded news will be added related comments and count of comments.
    :param news_id: Id of news
    :type news_id: int
    :param all_news: List of news in which will be searched
    :type all_news: list of dict
    :param comments: List of comment in which will be searched
    :return: First news with given id if it exist else None.
    :rtype: dict or None
    """
    filtered_news = list(filter(lambda news: news['id'] == news_id, all_news))
    if len(filtered_news) == 0:
        return None
    else:
        news = filtered_news[0]
        comments = await find_comments_by_news_id(news_id, comments)
        comments.sort(key=lambda comment: datetime.datetime.fromisoformat(comment['date']))
        news['comments'] = comments
        news['comments_count'] = len(comments)
        return news


async def get_all_news(request):
    """
    View for list of all available news.
    :param request: Http request
    :type request: aiohttp.web_request.Request
    :return: Json with list of all news
    """
    for news in all_news:
        news['comments_count'] = len(await find_comments_by_news_id(news['id'], all_comments))
    filtered_news = list(
        filter(check_news_available, all_news))
    filtered_news.sort(key=lambda news: datetime.datetime.fromisoformat(news['date']))
    return web.json_response({'news': filtered_news, 'news_count': len(filtered_news)})


async def get_news_by_id(request):
    """
    View for news with given id.
    :param request: http request
    :type request: aiohttp.web_request.Request
    :return: Json with news if it exist and available else 404
    """
    news_id = int(request.match_info['news_id'])
    news = await find_news(news_id, all_news, all_comments)
    if news is None or not check_news_available(news):
        return web.HTTPNotFound()
    return web.json_response({'news': news})


