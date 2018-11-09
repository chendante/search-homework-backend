from collections import Counter
from project.models.song_info import song
from project.models.inverted_index import InvertedIndex, convert_list
from project.models.base import Database
import math

num_of_song = 99
name_weight = 2


def get_weight_list(text):
    str_list = convert_list(text)
    res = Counter()
    for value in str_list:
        id_w = value.lstrip().rstrip().split(":")
        res[int(id_w[0])] = float(id_w[1])
    return res


# 将counter类数据排序并返回list格式
def counter_to_list(co):
    res = {"id_list": [], "w_list": []}
    for sid in list(co.most_common()):
        res["id_list"].append(sid[0])
        res["w_list"].append(sid[1])
    return res


# 该类用于处理向量空间模型搜索内容的处理
class VectorSearch:
    def __init__(self, text):
        self.text = text
        self.song = song(-1, text)
        self.tf = Counter()
        # 格式：{ sid: tf-idf, sid: tf-idf}
        self.lyric_tf_idf = Counter()
        self.name_tf_idf = Counter()
        self.lyric_list = []
        self.name_list = []
        self.lyric_cos = Counter()
        self.name_cos = Counter()

    def get_tf(self):
        self.tf = self.song.get_tf()

    # 处理得出其各个词项的tf-idf值
    def get_tf_idf(self, kind=0):
        words = self.song.getwords()
        for word in words:
            data = InvertedIndex.get_word_info(word, kind)
            if data['num'] != 0:
                if kind == 0:
                    self.lyric_tf_idf[data['id']] = (1+math.log10(self.tf[word]))*math.log10(num_of_song/data['num'])
                    self.lyric_list = list(set(self.lyric_list).union(set(data['list'])))
                else:
                    self.name_tf_idf[data['id']] = (1 + math.log10(self.tf[word])) * math.log10(num_of_song / data['num'])
                    self.name_list = list(set(self.name_list).union(set(data['list'])))

    def deal(self):
        self.get_tf()
        self.get_tf_idf(0)
        self.get_tf_idf(1)

    def get_one_cos(self, sid, kind=0):
        vector_space = VectorSpace(sid, kind)
        res = 0
        for tf_idf_value in vector_space.w_list.items():
            if kind == 0:
                res += self.lyric_tf_idf[tf_idf_value[0]]*tf_idf_value[1]
            else:
                res += self.name_tf_idf[tf_idf_value[0]]*tf_idf_value[1]
        return res/vector_space.length

    def get_cos_list(self, kind=0):
        if kind == 0:
            the_list = self.lyric_list
        else:
            the_list = self.name_list
        for sid in the_list:
            if kind == 0:
                self.lyric_cos[sid] = self.get_one_cos(sid, kind)
            else:
                self.name_cos[sid] = self.get_one_cos(sid, kind)

    def get_sort(self, kind=0):
        self.deal()
        self.get_cos_list(0)
        self.get_cos_list(1)
        if kind == 0:
            return counter_to_list(self.lyric_cos)
        elif kind == 1:
            return counter_to_list(self.name_cos)
        w_list = Counter()
        keys = set(self.lyric_cos).union(self.name_cos)
        for key in keys:
            w_list[key] = self.name_cos[key]*name_weight + self.lyric_cos[key]
        return counter_to_list(w_list)


# 该类用于将一个歌曲的内容处理为数据库所需要的形式
# 形式： 歌曲id，tf-idf列表             ,歌曲tf-idf空间长度
# 例子：   4     1:2.34 2:4.113 5:1.341   3.1435
class VectorIndex:
    def __init__(self, text, id, kind=0):
        self.vector_search = VectorSearch(text)
        self.vector_search.deal()
        self.kind = kind
        self.id = id

    def get_index(self):
        if self.kind == 0:
            return self.vector_search.lyric_tf_idf.items()
        else:
            return self.vector_search.name_tf_idf.items()

    def get_length(self):
        tf_idf_list = self.get_index()
        res = 0
        for value in tf_idf_list:
            res += value[1]*value[1]
        res = math.sqrt(res/len(tf_idf_list))
        return res

    def get_json(self):
        return {
            'id': self.id,
            'tf-idf-matrix': list(self.get_index()),
            'length': self.get_length()
        }


# 该类用于将数据库中的vector_index处理成为需要的格式
class VectorSpace:
    def __init__(self, sid, kind=0):
        self.id = sid
        self.kind = kind
        m_d = Database()
        if kind == 0:
            sql = "SELECT * from lyric_vector_index where sid = %d" % int(sid)
        else:
            sql = "SELECT * from name_vector_index where sid = %d" % int(sid)
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        if not data == ():
            self.w_list = get_weight_list(data[0][1])
            self.length = data[0][2]
        else:
            self.w_list = Counter()
            self.length = 0

    @staticmethod
    def get_vector_list(kind=0):
        m_d = Database()
        if kind == 0:
            sql = "SELECT * from lyric_vector_index " \
                  "INNER JOIN song_list " \
                  "on song_list.ID = lyric_vector_index.Sid limit 10"
        else:
            sql = "SELECT * from name_vector_index " \
                  "INNER JOIN song_list " \
                  "on song_list.ID = name_vector_index.Sid limit 10"
        m_d.cursor.execute(sql)
        data = m_d.cursor.fetchall()
        return data
