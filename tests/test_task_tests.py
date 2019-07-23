import os

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from test_task.read_json import read_json
from test_task.routes import setup_routes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_FILENAME = os.path.join(BASE_DIR, 'news.json')
COMMENTS_FILENAME = os.path.join(BASE_DIR, 'comments.json')


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = web.Application()
        setup_routes(app)
        await read_json(app, NEWS_FILENAME, COMMENTS_FILENAME)
        return app

    @unittest_run_loop
    async def test_deleted_news(self):
        resp = await self.client.request("GET", "/news/2")
        assert resp.status == 404

    @unittest_run_loop
    async def test_future_news(self):
        resp = await self.client.request("GET", "/news/3")
        assert resp.status == 404

    @unittest_run_loop
    async def test_not_existed_news(self):
        resp = await self.client.request("GET", "/news/9")
        assert resp.status == 404
        resp = await self.client.request("GET", "/news/w")
        assert resp.status == 404

    @unittest_run_loop
    async def test_all_news(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        news = await resp.json()
        correct = {"news": [
            {"id": 4,
             "title": "news_1",
             "date": "2018-01-01T20:56:35",
             "body": "The news",
             "deleted": False,
             "comments_count": 0},
            {"id": 1,
             "title": "news_1",
             "date": "2019-01-01T20:56:35",
             "body": "The news",
             "deleted": False,
             "comments_count": 2}],
            "news_count": 2}
        assert news == correct

    @unittest_run_loop
    async def test_one_news(self):
        resp = await self.client.request("GET", "/news/1")
        assert resp.status == 200
        news = await resp.json()
        correct = {"news":
                       {"id": 1,
                        "title": "news_1",
                        "date": "2019-01-01T20:56:35",
                        "body": "The news",
                        "deleted": False,
                        "comments_count": 2,
                        "comments": [{"id": 2,
                                      "news_id": 1,
                                      "title": "comment_2",
                                      "date": "2018-01-02T21:58:25",
                                      "comment": "Comment"},
                                     {"id": 1,
                                      "news_id": 1,
                                      "title": "comment_1",
                                      "date": "2019-01-02T21:58:25",
                                      "comment": "Comment"}
                                     ]
                        }
                   }
        assert news == correct
