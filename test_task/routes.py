from test_task.views import get_all_news


def setup_routes(app):
    app.router.add_get('/', get_all_news)
