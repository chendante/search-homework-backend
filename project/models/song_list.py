from project.models.base import Database
import project.models.indexlist as indexlist
import project.models.song_info as songInfo
import json


# 获取最大ID
def maxid():
    m_d = Database()
    sql = "SELECT MAX(ID) from song_list"
    m_d.cursor.execute(sql)
    data = m_d.cursor.fetchall()
    return data[0][0]


# 获取某个ID的歌曲信息
def getinfo(i):
    m_d = Database()
    sql = "SELECT * from song_list " \
          "where song_list.ID = '%d'" % i
    m_d.cursor.execute(sql)
    data = m_d.cursor.fetchall()
    return data


class SongList:

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
        file1.close()
        file2.close()

    @staticmethod
    def song_number():
        m_d = Database()
        m_d.cursor.execute("SELECT COUNT(ID) from song_list")
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data[0][0]

    @staticmethod
    def song_name_list():
        m_d = Database()
        m_d.cursor.execute("SELECT song_id,song_name,id from song_list")
        data = m_d.cursor.fetchall()
        return data

    #给一个词，返回对应的id列表
    @staticmethod
    def search_lyric(search_word):
        m_d = Database()
        sql = "SELECT * FROM lyric_inverted_index WHERE lyric_inverted_index.word='%s'" % search_word
        m_d.cursor.execute(sql)
        # 获取所有记录列表
        data = m_d.cursor.fetchall()
        return data

    @staticmethod
    def get_one_song(id):
        m_d = Database()
        sql = "SELECT * from song_list WHERE id = '%s'" % id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        return data[0]

    #获取id列表的所有歌曲
    @staticmethod
    def get_search_list(id_list):
        m_d = Database()
        id_str = str(id_list[0])
        for val in id_list[1:]:
            id_str += ',' + str(val)
        sql = "SELECT * from song_list WHERE id in (%s)" % id_str
        print(sql)
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        return data
