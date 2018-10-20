#每个词项的结构
class Node:
    def __init__(self, word, id):
        self.word = word
        self.id = [id]
        self.df = 1

    #在该词项中添加一个歌曲ID
    def addID(self, Sid):
        if self.id.count(Sid) == 0:
            self.id.append(Sid)
            self.df += 1

    def getJson(self):
        return {
            'term': self.word,
            'IDS': self.id,
            'DF': self.df
        }


#倒排索引表的结构
class IndexList:
    def __init__(self):
        self.list = []

    def addword(self, word, Sid):
        self.list.append(Node(word, Sid))

    #添加词组
    def insert(self, word, Sid):
        for node in self.list:
            if word == node.word:
                node.addID(Sid)
                return
        self.addword(word, Sid)

    def getJson(self):
        jList = []
        for node in self.list:
            t = node.getJson()
            jList.append(t)
        return jList

    def appendsong(self, words, id):
        for word in words:
            self.insert(word, id)


# t = Node('二年', 1)
# t.addID(23)
# print(t.getJson())
# print(json.dumps(t.getJson()))
# file = open('test.json', 'x')
# file.write(json.dumps(t.getJson()))
# file.write(json.dumps(t.getJson()))
