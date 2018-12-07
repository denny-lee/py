#!/usr/bin/env python
# _*_ coding: utf-8
import re
import pymongo
import os


HELP = ('?', 'h')
Q = ('q', 'Q')
ADD = 'i '
SEARCH = 'f '
showDb = ('db', 'DB')
help_doc = 'Usage:\n--------------------Cmd--------------------\n' \
           'i {data seperated with comma}\n' \
           'f {key:value pair seperated with comma}\n' \
           'db  show current db\n' \
           '? or h for HELP\n' \
           'q or Q for Quit\n' \
           '---------------------------------------------------\n\n'


class DbWorker:

    client = None
    db = None
    currdb = ''

    def __init__(self, url):
        self.client = pymongo.MongoClient(url)

    def useDb(self, db):
        if not self.client:
            print('Client not connected to db.')
            return
        self.db = self.client[db]
        self.currdb = db

    def showDb(self):
        print(self.currdb)

    def _save(self, coll, data):
        self.db[coll].insert_one(data)

    def save(self, coll, data):
        if not coll or not data:
            return
        self._save(coll, data)

    def search(self, coll, sql):
        if not coll or not sql:
            return None
        self.db[coll].find(sql)



    def execute(self, c):
        if not c:
            return
        c = c.strip()
        if c in HELP:
            print(help_doc)
        elif c.startswith(ADD):
            print('add things')
        elif c.startswith(SEARCH):
            self.
        elif c == 'cls':
            os.system(c)


url = "mongodb://localhost:27017/"
dbName = "word_book"


app = DbWorker(url)
app.useDb(dbName)

while True:
    cmd = input(">> ")
    if cmd in Q:
        break
    else:
        # print('Command: '+cmd+'\n')
        app.execute(cmd)

print("Bye~")
