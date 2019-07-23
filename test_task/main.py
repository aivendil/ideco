from aiohttp import web

from test_task.read_json import read_json
from test_task.routes import setup_routes

app = web.Application()
setup_routes(app)
app.on_startup.append(read_json)
web.run_app(app)
