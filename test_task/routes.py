from aiohttp import web

from test_task.views import get_all_news, get_news_by_id


def setup_routes(app):
    """
    Set routes path.
    :param app: wsgi application
    :type app: aiohttp.web_app.Application
    :return:
    """
    app.add_routes([web.get('/', get_all_news),
                    web.get(r'/news/{news_id:\d+}', get_news_by_id)])
