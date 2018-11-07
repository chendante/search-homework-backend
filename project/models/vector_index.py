from collections import Counter
from project.models.song_info import song
import project.models.song_list as ii
from project.models.inverted_index import InvertedIndex
import math

num_of_song = ii.SongList.song_number()


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
    def deal(self, kind=0):
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
