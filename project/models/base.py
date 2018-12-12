import pymysql


class Database:
    db = pymysql.connect("47.95.200.233", "dante", "528031", "search_homework")
    cursor = db.cursor()

    def getdb(self):
        self.db = pymysql.connect("47.95.200.233", "dante", "528031", "search_homework")
        self.cursor = self.db.cursor()

    def __init__(self):
        self.db = pymysql.connect("47.95.200.233", "dante", "528031", "search_homework")
        self.cursor = self.db.cursor()
