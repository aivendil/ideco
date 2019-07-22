from aiohttp import web

from test_task.routes import setup_routes

app = web.Application()
setup_routes(app)
web.run_app(app)
