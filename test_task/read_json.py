import json
import os

from test_task.settings import NEWS_FILENAME, COMMENTS_FILENAME


async def read_json(app, news_filename=NEWS_FILENAME, comments_filename=COMMENTS_FILENAME):
    """
    Add news and comments to app
    :param comments_filename: Path to comments json file
    :type comments_filename: str
    :param news_filename: Path to news json file
    :type news_filename: str
    :param app: aiohttp Application
    :type app: aiohttp.web_app.Application
    """
    print(os.getcwd())
    with open(news_filename) as news_file:
        app['news'] = json.load(news_file)['news']
    with open(comments_filename) as comments_file:
        app['comments'] = json.load(comments_file)['comments']
