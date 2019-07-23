import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_FILENAME = os.path.join(BASE_DIR, 'news.json')
COMMENTS_FILENAME = os.path.join(BASE_DIR, 'comments.json')
