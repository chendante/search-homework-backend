import jieba


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
        list = ()
        words = self.getwords()
        for word in words:
            if (word in stopwords) or (word in list):
                continue
            list += (word,)
        return list
