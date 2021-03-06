#!/usr/bin/env python
# coding: UTF-8

# import inspect

from feedparser import parse
from urllib import request
from bs4 import BeautifulSoup

# 取得するRSSのURL
RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"

# RSSから取得する
# print(inspect.getargspec(parse))
# ArgSpec(args=['url_file_stream_or_string', 'etag', 'modified', 'agent', 'referrer', 'handlers', 'request_headers', 'response_headers', 'resolve_relative_uris', 'sanitize_html'], varargs=None, keywords=None, defaults=(None, None, None, None, None, None, None, None, None))
feeds = parse(url_file_stream_or_string=RSS_URL)

# 記事の情報をひとつずつ取り出す
for entry in feeds.entries:

    print(entry.title)

    instance = request.urlopen(url=entry.link)

    soup = BeautifulSoup(instance, "html.parser")

    # 例としてタイトル要素のみを出力する
    print(soup.title)
