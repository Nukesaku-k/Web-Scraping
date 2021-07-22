#!/usr/bin/env python
# coding: UTF-8

# Usage: python headless_lambda.py

import os
import urllib.parse
import urllib.request
import shutil

from bs4 import BeautifulSoup
# import chromedriver_binary
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys

line_notify_endpoint = 'https://notify-api.line.me/api/notify'
# Environment variables used in lambda.
line_notify_token = os.environ.get('line_notify_token')
# line_notify_token = '___to_be_set___'  # Loacal test.


URL = 'https://www.nikkei.com/markets/kabu/'

CHROME_HOME = '/tmp/bin'
CHROME_PATH = f'{CHROME_HOME}/chromium-browser'
DRIVER_PATH = f'{CHROME_HOME}/chromedriver'

MESSAGE = '\n日経平均(円): {jp_stk_price}'


def setup_driver():
    try:
        os.mkdir(path=CHROME_HOME)
        os.chmod(CHROME_HOME, 0o777)
        shutil.copy2('/usr/bin/chromium-browser', CHROME_HOME)
        shutil.copy2('/usr/bin/chromedriver', CHROME_HOME)
    except FileExistsError:
        pass


def headless_lambda():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--single-process')

    driver = webdriver.Chrome(
        options=options,
        service_log_path='/tmp/chromedriver.log',
    )
    driver.get(URL)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    jp_stk_price = soup.select('.mkc-stock_prices')
    driver.quit()
    try:
        return MESSAGE.format(jp_stk_price=jp_stk_price[0].string)
    except IndexError:
        return ''


def notify_to_line(message):
    if not has_message(message):
        return None
    method = 'POST'
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    payload = {'message': message}
    try:
        payload = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(line_notify_endpoint, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
        return message
    except Exception as e:
        return e


def has_message(str=''):
    if len(str) == 0:
        return False
    return True


def lambda_handler(event, context):
    setup_driver()
    message = headless_lambda()
    print(message)
    return notify_to_line(message)


# Loacal test.
#if __name__ == '__main__':
#    lambda_handler('', '')
