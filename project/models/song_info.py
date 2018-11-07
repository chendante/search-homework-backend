import jieba
from project.models.inverted_index import InvertedIndex
from collections import Counter


stopwords = set(['\n', ' ', ':', '这', '作曲', '作词', '我', '你'])

num_song = 99

class song:
    def __init__(self, id, text):
        self.id = id
        self.lyric = text

    #用jieba将文本分解
    def getwords(self):
        return jieba.cut_for_search(self.lyric)

    def getid(self):
        return self.id

    def getwordlist(self):
        w_list = ()
        words = self.getwords()
        for word in words:
            if (word in stopwords) \
                    or (word in w_list):
                continue
            w_list += (word,)
        return w_list

    #获取歌词tf
    def get_tf(self):
        tf = Counter()
        words = self.getwords()
        for word in words:
            if word in stopwords:
                continue
            tf[word] += 1
        return tf

    def get_df(self, kind=0):
        words = list(self.get_tf())
        df = Counter()
        for word in words:
            num = InvertedIndex.search_lyric(word, kind)
            if num == 0:
                df[word] = 0
            else:
                df[word] = num_song/num
        return df


