from project.models.base import Database
import project.models.indexlist as indexlist
import project.models.song_info as songInfo
import json


# 获取最大ID
def maxid():
    sql = "SELECT MAX(ID) from song_list"
    Database.cursor.execute(sql)
    data = Database.cursor.fetchall()
    return data[0][0]


# 获取某个ID的歌曲信息
def getinfo(i):
    sql = "SELECT * from song_list " \
          "where song_list.ID = '%d'" % i
    Database.cursor.execute(sql)
    data = Database.cursor.fetchall()
    return data


class song_list:

    #更新歌曲名称和歌词的索引
    @staticmethod
    def updateIndex():
        lyric_index = indexlist.IndexList()
        name_index = indexlist.IndexList()
        for i in range(maxid()):
            str = getinfo(i)
            if not str == ():
                lyric = songInfo.song(str[0][2], str[0][3])
                lyric_index.appendsong(lyric.getwordlist(), lyric.getid())
                name = songInfo.song(str[0][2], str[0][1])
                name_index.appendsong(name.getwordlist(), name.getid())
        file1 = open('song_lyric_index.json', 'w+')
        file1.write(json.dumps(lyric_index.getJson()))
        file2 = open('song_name_index.json', 'w+')
        file2.write(json.dumps(name_index.getJson()))

    @staticmethod
    def song_number():
        Database.cursor.execute("SELECT COUNT(ID) from song_list")
        data = Database.cursor.fetchall()
        return data[0][0]

    @staticmethod
    def song_name_list():
        Database.cursor.execute("SELECT song_id,song_name,id from song_list")
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def lyric_inverted_index_list():
        Database.cursor.execute("SELECT * from lyric_inverted_index")
        data = Database.cursor.fetchall()
        return data

    #给一个词，返回对应的id列表
    @staticmethod
    def search_lyric(search_word):
        sql = "SELECT * FROM lyric_inverted_index WHERE lyric_inverted_index.word='%s'" % search_word
        Database.cursor.execute(sql)
        # 获取所有记录列表
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def search_name(search_word):
        sql = "SELECT * FROM name_inverted_index WHERE name_inverted_index.word='%s'" % search_word
        Database.cursor.execute(sql)
        # 获取所有记录列表
        data = Database.cursor.fetchall()
        return data
