import os.path
import json


class Compress:
    word_list = []
    word_list_str = ""
    # 压缩后的结果
    # 格式：[id, point, tf]
    compressed_dic = []
    index_list = []
    compressed_index = []

    def __init__(self):
        # 加载词典
        file_name = "./word_list.json"
        f = open(file_name, 'r')
        self.word_list = json.load(f)
        f.close()
        # 压缩词典
        self.compress_word_list()
        f2 = open("./BlockedSort/index_list_8_0.txt")
        for line in f2:
            if line != "":
                x, y = line.split()
                self.index_list.append([int(x), int(y)])
        self.calculate_tf()

    def calculate_tf(self):
        last = 0
        count = 0
        for v in self.index_list:
            if last != v[0]:
                self.add_tf(last, count)
                last = v[0]
                count = 1
            else:
                count += 1
        self.add_tf(last, count)

    def add_tf(self, id, count):
        for i in range(len(self.compressed_dic)):
            if id == self.compressed_dic[i][0]:
                self.compressed_dic[i].append(count)
                break

    def save_dic(self):
        f1 = open("./compressed_str.json", 'w+')
        f1.write(json.dumps(self.word_list_str))
        f1.close()
        f2 = open("./compressed_dic.json", 'w+')
        f2.write(json.dumps(self.compressed_dic))
        f2.close()
        f3 = open("./compressed_index.json", 'w+')
        f3.write(json.dumps(self.compressed_index))
        f3.close()

    def compress_word_list(self):
        point = 0
        i = 0
        for word in self.word_list:
            self.compressed_dic.append([i, point])
            point += len(word) + 1
            i += 1
            self.word_list_str += word + " "

    def find_word(self, word_id):
        word_point = -1
        for term in self.compressed_dic:
            if term[0] == word_id:
                word_point = term[1]
        word = ""
        if word_point == -1:
            return word
        for letter in self.word_list_str[word_point:]:
            if letter != " ":
                word += letter
            else:
                break
        return word

    def find_word_id(self, word):
        point = 0
        for v in self.word_list_str.split(" "):
            if v != word:
                point += 1
            else:
                return point
        return -1

    def compress_index(self):
        last_term_id = 0
        last_doc_id = 0
        data_line = []
        for v in self.index_list:
            if last_term_id != v[0]:
                self.compressed_index.append([last_term_id, data_line])
                last_term_id = v[0]
                data_line = []
                last_doc_id = 0
            data_line.append(v[1] - last_doc_id)
            last_doc_id = v[1]
        self.compressed_index.append([last_term_id, data_line])

    def find_doc_list(self, word):
        word_id = self.find_word_id(word)
        if word_id == -1:
            return []
        doc_list = []
        for v in self.compressed_index:
            if v[0] == word_id:
                doc_list = v[1]
        res = []
        value = 0
        for v in doc_list:
            value += v
            res.append(value)
        return res


if __name__ == '__main__':
    test = Compress()
    test.compress_index()
    print(test.find_doc_list("家"))
    # test.save_dic()
