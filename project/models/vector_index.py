from collections import Counter
from project.models.song_info import song
from project.models.inverted_index import InvertedIndex, convert_list
import math

num_of_song = 99

def get_weight_list(text):
    str_list = convert_list(text)
    res = Counter()
    for value in str_list:
        id_w = value.lstrip().rstrip().split(":")
        res[id_w[0]] = id_w[1]
    return res


# 该类用于处理向量空间模型搜索内容的处理
class VectorSearch:
    def __init__(self, text):
        self.text = text
        self.song = song(-1, text)
        self.tf = Counter()
        self.lyric_tf_idf = Counter()
        self.name_tf_idf = Counter()
        self.lyric_list = []
        self.name_list = []

    def get_tf(self):
        self.tf = self.song.get_tf()

    # 处理得出其各个词项的tf-idf值
    def get_tf_idf(self, kind=0):
        words = self.song.getwords()
        for word in words:
            data = InvertedIndex.get_word_info(word, kind)
            print(word)
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

    def get_cos_list(self):
        for sid in self.lyric_list:



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
        print(tf_idf_list)
        res = 0
        for value in tf_idf_list:
            print(value)
            res += value[1]*value[1]
        res = math.sqrt(res/len(tf_idf_list))
        return res

    def get_json(self):
        return {
            'id': self.id,
            'tf-idf-matrix': list(self.get_index()),
            'length': self.get_length()
        }
