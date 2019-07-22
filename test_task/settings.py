import json

NEWS_FILENAME = 'news.json'
with open(NEWS_FILENAME) as news_file:
    all_news = json.load(news_file)['news']
COMMENTS_FILENAME = 'comments.json'
with open(COMMENTS_FILENAME) as comments_file:
    all_comments = json.load(comments_file)['comments']
