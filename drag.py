#!/usr/local/bin/python3
# coding: utf-8

# BagAndDrag - drag.py
# 1/10/21 15:38
#

__author__ = "Benny <benny.think@gmail.com>"

import argparse
import logging
import time
import requests
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import trange

from bag import SHARE_URL, API_DATA, load_cookies, is_cookie_valid, login, insert_db, insert_error

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s [%(levelname)s]: %(message)s')
s = requests.session()

parser = argparse.ArgumentParser()
# start_id, end_id, interval, concurrency
parser.add_argument("-s", help="Start id", type=int, default=36736)
parser.add_argument("-e", help="End id", type=int, default=36740)
parser.add_argument("-i", help="Interval", default=10, type=int)
parser.add_argument("-c", help="Concurrency", default=2, type=int)
args = parser.parse_args()

executor = ThreadPoolExecutor(max_workers=args.c)


def get_api_json(resource_id):
    try:
        if not is_cookie_valid():
            login()
        logging.info("resource id is %s", resource_id)
        res = s.post(SHARE_URL, data={"rid": resource_id}, cookies=load_cookies()).json()
        share_code = res['data'].split('/')[-1]
        logging.info("Share code is %s", share_code)
        data = s.get(API_DATA.format(code=share_code)).json()

        insert_db(data)
        time.sleep(args.i)
    except Exception:
        insert_error(resource_id, traceback.format_exc())


def main():
    from tqdm import tqdm
    total = args.e + 1 - args.s
    list(tqdm(executor.map(get_api_json, range(args.s, args.e + 1)), total=total))


if __name__ == '__main__':
    main()
