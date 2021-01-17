#!/usr/local/bin/python3
# coding: utf-8

# BagAndDrag - cfkv.py
# 1/17/21 12:08
#

__author__ = "Benny <benny.think@gmail.com>"

import pymysql
import json
import os

con = pymysql.Connect(host="127.0.0.1", user="root", password="root", charset="utf8mb4", database="yyets",
                      cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

SIZE = 3000
cur.execute("select count(id) from resource")
count = cur.fetchall()[0]["count(id)"]
LIMIT = count // SIZE + 1


def convert_kv():
    for i in range(1, LIMIT + 1):
        SQL = "select id,data from resource limit %d offset %d" % (SIZE, (i - 1) * SIZE)
        print(SQL)
        cur = con.cursor()
        cur.execute(SQL)
        data = cur.fetchall()
        write_data = []
        for datum in data:
            write_data.append({
                "key": datum["id"],
                "value": json.loads(datum['data'])}
            )
        with open(f"kv/kv_data{i - 1}.json", "w") as f:
            json.dump(write_data, f, ensure_ascii=False)

    con.close()


def verify_kv_data():
    files = os.listdir("kv")
    rows = 0
    for file in files:
        with open(f"kv/{file}") as f:
            data = json.load(f)
            rows += len(data)
    assert rows == count


def dump_index():
    cur = con.cursor()
    a = {"index":
        {
            "name": 12345,
            "name2": 1234,
        }
    }
    indexes = {}
    cur.execute("select name, id from resource")
    data = cur.fetchall()
    for datum in data:
        name = datum["name"]
        rid = datum["id"]
        indexes[name] = rid
    with open("kv/index.json", "w") as f:
        write_data = [dict(index=indexes)]
        json.dump(write_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # convert_kv()
    # verify_kv_data()
    dump_index()