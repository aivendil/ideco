import json

from test_task.settings import NEWS_FILENAME, COMMENTS_FILENAME


async def read_json(app):
    """
    Add news and comments to app
    :param app: aiohttp Application
    :type app: aiohttp.web_app.Application
    """
    with open(NEWS_FILENAME) as news_file:
        app['news'] = json.load(news_file)['news']
    with open(COMMENTS_FILENAME) as comments_file:
        app['comments'] = json.load(comments_file)['comments']
