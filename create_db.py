#!/usr/local/bin/python3
# coding: utf-8

# BagAndDrag - create_db.py
# 1/10/21 15:23
#

__author__ = "Benny <benny.think@gmail.com>"

import pymysql

con = pymysql.Connect(host="127.0.0.1", user="root", password="root", database="yyets", charset="utf8mb4")

sql = [
    """
    create table resource
    (
        id         int primary key,
        url        varchar(255) null unique ,
        name       text         null,
        expire     int          null,
        expire_cst varchar(255) null,
        data       longtext     null
    
    );
    
    
    """,

    """
    create table failure
    (
        id        int primary key not null,
        traceback longtext        null
    );
    """,

]
cur = con.cursor()
for s in sql:
    cur.execute(s)
con.close()