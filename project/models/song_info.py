import jieba
from collections import Counter


stopwords = set(['\n', ' ', ':', '这', '作曲', '作词', '我', '你'])


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


