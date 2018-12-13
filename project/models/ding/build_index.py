from whoosh.index import create_in, open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import os.path
from project.models.base import Database
import shutil


class IndexBuilder:
    analyzer = ChineseAnalyzer()
    index_path = "./index_dir2"
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer)
                    , url=ID(stored=True, unique=True)
                    , content=TEXT(stored=True, analyzer=analyzer)
                    , site=ID(stored=True)
                    , wid=NUMERIC(stored=True)
                    , time=ID(stored=True)
                    , pagerank=NUMERIC(stored=True))
    # 这里是一个大坑
    if not os.path.exists(index_path):
        os.mkdir(index_path)
        ix = create_in(index_path, schema)
    else:
        ix = open_dir(index_path)

    @staticmethod
    def insert_index(title, url, content, m_type, wid, the_time, page_rank):
        # 写索引
        writer = IndexBuilder.ix.writer()
        writer.add_document(title=str(title)
                            , url=str(url)
                            , content=str(content)
                            , site=str(m_type)
                            , wid=wid
                            , time=the_time
                            , pagerank=page_rank)
        writer.commit()

    @staticmethod
    def insert_list(info_list, site_type):
        for info in info_list:
            content = info[4].strip("\"")
            title = info[2].strip("\"")
            url = info[1].strip("\"")
            the_time = info[3].strip("\"")
            id = info[0]
            page_rank = info[5]
            if page_rank == '':
                page_rank = 0
            IndexBuilder.insert_index(title=title, url=url
                                      , content=content, m_type=site_type
                                      , wid=id, the_time=the_time
                                      , page_rank=page_rank)

    @staticmethod
    def rebuild_index():
        if os.path.exists(IndexBuilder.index_path):
            shutil.rmtree(IndexBuilder.index_path)
        os.mkdir(IndexBuilder.index_path)
        IndexBuilder.ix = create_in(IndexBuilder.index_path, IndexBuilder.schema)
        for i in range(1, 6):
            j = 0
            while True:
                data_list = ()
                try:
                    if i is IndexData.wxy_type:
                        data_list = IndexData.get_10_wxy(j)
                    elif i is IndexData.soft_type:
                        data_list = IndexData.get_10_soft(j)
                    elif i is IndexData.sms_type:
                        data_list = IndexData.get_10_sms(j)
                    elif i is IndexData.law_type:
                        data_list = IndexData.get_10_law(j)
                    elif i is IndexData.physics_type:
                        data_list = IndexData.get_10_physics(j)
                    if data_list is ():
                        break
                    j += 10
                    IndexBuilder.insert_list(data_list, i)
                    print(i, j)
                except Exception as e:
                    print(e)

    @staticmethod
    def test_build():
        if os.path.exists(IndexBuilder.index_path):
            shutil.rmtree(IndexBuilder.index_path)
        os.mkdir(IndexBuilder.index_path)
        IndexBuilder.ix = create_in(IndexBuilder.index_path, IndexBuilder.schema)
        data = IndexData.get_10_wxy(0)
        IndexBuilder.insert_list(data, 1)


class IndexData:
    wxy_type = 1
    soft_type = 2
    sms_type = 3
    law_type = 4
    physics_type = 5

    @staticmethod
    def get_10_wxy(begin_id):
        sql = "SELECT ID,url,title,time,content,pagerank from Wxy" \
              " WHERE id > %d LIMIT 10" % begin_id
        Database.cursor.execute(sql)
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def get_10_soft(begin_id):
        sql = "SELECT ID,url,title,time,content,pagerank from Soft" \
              " WHERE id > %d LIMIT 10" % begin_id
        Database.cursor.execute(sql)
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def get_10_sms(begin_id):
        sql = "SELECT ID,url,title,time,content,pagerank from Sms" \
              " WHERE id > %d LIMIT 10" % begin_id
        Database.cursor.execute(sql)
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def get_10_law(begin_id):
        sql = "SELECT ID,url,title,time,content,pagerank from Law" \
              " WHERE id > %d LIMIT 10" % begin_id
        Database.cursor.execute(sql)
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def get_10_physics(begin_id):
        sql = "SELECT ID,url,title,time,content,pagerank from Physics" \
              " WHERE id > %d LIMIT 10" % begin_id
        Database.cursor.execute(sql)
        res = Database.cursor.fetchall()
        return res

    @staticmethod
    def ids_to_str(id_list):
        id_str = str(id_list[0])
        for val in id_list[1:]:
            id_str += ',' + str(val)
        return id_str

    @staticmethod
    def get_wxy(the_id):
        m_d = Database()
        sql = "SELECT * from Wxy" \
              " WHERE id = %d" % the_id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data

    @staticmethod
    def get_soft(the_id):
        m_d = Database()
        sql = "SELECT * from Soft" \
              " WHERE id = %d" % the_id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data

    @staticmethod
    def get_sms(the_id):
        m_d = Database()
        sql = "SELECT * from Sms" \
              " WHERE id = %d" % the_id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data

    @staticmethod
    def get_law(the_id):
        m_d = Database()
        sql = "SELECT * from Wxy" \
              " WHERE id = %d" % the_id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data

    @staticmethod
    def get_physics(the_id):
        m_d = Database()
        sql = "SELECT * from Wxy" \
              " WHERE id = %d" % the_id
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        m_d.db.close()
        return data

    @staticmethod
    def get_info(the_id, site):
        res = ()
        try:
            if site is IndexData.wxy_type:
                res = IndexData.get_wxy(the_id)
            elif site is IndexData.soft_type:
                res = IndexData.get_soft(the_id)
            elif site is IndexData.sms_type:
                res = IndexData.get_sms(the_id)
            elif site is IndexData.law_type:
                res = IndexData.get_law(the_id)
            elif site is IndexData.physics_type:
                res = IndexData.get_physics(the_id)
            if res is not ():
                return {'success': True, 'data': res}
            else:
                return {'success': False, 'data': res}
        except Exception as e:
            print(e)
            return {'success': False, 'data': res}


if __name__ == '__main__':
    # IndexBuilder.rebuild_index()

    # 测试
    data = IndexData.get_10_wxy(0)
    IndexBuilder.insert_list(data, 1)
