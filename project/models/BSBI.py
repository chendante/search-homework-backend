import project.models.song_list as song_list
import os.path
import project.models.song_info as songInfo
import numpy as np
import json
import time


class BlockedSort:
    # 词典
    word_list = []
    # 倒排记录（不允许超过100条）
    # 每条记录的格式：(termId,docId)
    index_list = []
    save_time = 89
    max_index_num = 100
    file_base_name = "./BlockedSort/index_list"
    level = 0
    num = 0
    merge_index1 = []
    merge_index2 = []

    def save_word_list(self):
        file = open("./word_list.json", 'w+')
        file.write(json.dumps(self.word_list))

    # 根据层级和编号存储文件
    def save_index_list(self):
        level = str(self.level)
        num = str(self.num)
        file_name = self.file_base_name + "_" + level + "_" + num + ".txt"
        # 从后追加，不存在的话新建
        file = open(file_name, 'a+')
        for index in self.index_list:
            line = str(index[0]) + " " + str(index[1]) + "\n"
            file.write(line)
        file.close()
        self.index_list = []
        self.num += 1

    def load_index_list(self, no, start):
        level = str(self.level)
        num = str(self.num)
        file_name = self.file_base_name + "_" + level + "_" + num + ".txt"
        if not os.path.exists(file_name):
            return False
        f = open(file_name, 'r')
        data = []
        for line in f:
            if line != "":
                x, y = line.split()
                data.append([int(x), int(y)])
        if no == 1:
            self.merge_index1 = data
        else:
            self.merge_index2 = data
        if not data:
            return False
        f.close()
        return True
        # level = str(self.level)
        # num = str(self.num)
        # file_name = self.file_base_name + "_" + level + "_" + num + ".txt"
        # if not os.path.exists(file_name):
        #     return False
        # f = open(file_name, 'r')
        # data = []
        # start = 50 * start
        # end = start + 50
        # i = start
        # for line in f:
        #     # 最多加载50条
        #     i += 1
        #     if i <= start:
        #         continue
        #     if i > end:
        #         break
        #     x, y = line.split()
        #     data.append([int(x), int(y)])
        # if no == 1:
        #     self.merge_index1 = data
        # else:
        #     self.merge_index2 = data
        # if not data:
        #     return False
        # f.close()
        # return True

    # 构建倒排索引
    def pre_process(self):
        self.level = 0
        for i in range(song_list.maxid()):
            time.sleep(1)
            print(i)
            song_info_str = song_list.getinfo(i)
            if not song_info_str == ():
                lyric = songInfo.song(song_info_str[0][2], song_info_str[0][3])
                self.append_song(lyric.getwordlist(), lyric.getid())
        self.save_index_list()
        self.save_word_list()

    # 添加新歌
    def append_song(self, song_word_list, song_id):
        for word in song_word_list:
            if word not in self.word_list:
                self.word_list.append(word)
            term_id = self.word_list.index(word)
            self.index_list.append((term_id, song_id))
            if len(self.index_list) == self.max_index_num:
                self.save_index_list()

    # 根据termID合并
    def base_merge(self):
        merge = self.merge_index1 + self.merge_index2
        sort_list = np.array(merge)
        sort_list1 = sort_list[:, ::-1].T
        sort_list2 = np.lexsort(sort_list1)
        sort_list3 = sort_list[sort_list2]
        self.index_list = sort_list3

    # 将两个Block合并，并写入文件
    def block_merge(self, num1, num2, num_next):
        self.num = num1
        self.load_index_list(1, num1)
        self.num = num2
        self.load_index_list(2, num2)
        self.base_merge()
        self.level += 1
        self.num = num_next
        self.save_index_list()
        self.level -= 1
        # load1 = 0
        # load2 = 0
        # start = 0
        # self.num = num1
        # flag1 = self.load_index_list(1, load1)
        # self.num = num2
        # flag2 = self.load_index_list(2, load2)
        # while True:
        #     self.base_merge()
        #     self.index_list = BlockedSort.remove_unload_term(self.index_list, start)
        #     self.level += 1
        #     self.num = num_next
        #     self.save_index_list()
        #     self.level -= 1
        #     if flag1 and flag2:
        #         if self.merge_index1[-1][0] > self.merge_index2[-1][0]:
        #             start = self.merge_index2[-1][0]
        #             load2 += 1
        #             self.merge_index1 = BlockedSort.remove_load_term(self.merge_index1, start)
        #             self.num = num2
        #             flag2 = self.load_index_list(2, load2)
        #         else:
        #             start = self.merge_index1[-1][0]
        #             load1 += 1
        #             self.merge_index2 = BlockedSort.remove_load_term(self.merge_index2, start)
        #             self.num = num1
        #             flag1 = self.load_index_list(1, load1)
        #     elif flag1:
        #         load1 += 1
        #         self.num = num1
        #         flag1 = self.load_index_list(1, load1)
        #     elif flag2:
        #         load2 += 1
        #         self.num = num2
        #         flag2 = self.load_index_list(2, load2)
        #     else:
        #         break

    @staticmethod
    def remove_load_term(m_list, start):
        data = []
        for line in m_list:
            if line[0] > start:
                data.append([line[0], line[1]])
        m_list = data
        return data

    @staticmethod
    def remove_unload_term(m_list, start):
        data = []
        for line in m_list:
            if line[0] <= start:
                data.append([line[0], line[1]])
        m_list = data
        return data

    def block_sort(self):
        self.level = 1
        self.num = 0
        for i in range(self.save_time):
            file_name = self.file_base_name + "_0_" + str(i) + ".txt"
            f = open(file_name, 'r')
            data = []
            for line in f:
                if line != "":
                    x, y = line.split()
                    data.append([int(x), int(y)])
            sort_list = np.array(data)
            sort_list1 = sort_list[:, ::-1].T
            sort_list2 = np.lexsort(sort_list1)
            sort_list3 = sort_list[sort_list2]
            self.index_list = sort_list3
            self.save_index_list()

    def merge_start(self):
        self.level = 1
        while True:
            print(self.level)
            num_max = 0
            while True:
                self.num = num_max
                if self.load_index_list(1, 0):
                    self.merge_index1 = []
                    self.merge_index2 = []
                    self.block_merge(num_max, num_max + 1, int(num_max/2))
                    print(self.level, "  ", self.num)
                else:
                    break
                num_max += 2
            if num_max <= 2:
                break
            self.level += 1


if __name__ == '__main__':
    test = BlockedSort()
    # test.pre_process()
    # test.block_sort()
    test.merge_start()
    data = []
    data.append([2, 14])
    data.append([35, 12])
    data.append([22, 12])
    a = np.array(data)
    # a = np.array(
    #     [[2, 14],
    #      [35, 9],
    #      [22, 12],
    #      [4, 8]]
    # )
    a1 = a[:, ::-1].T
    a2 = np.lexsort(a1)
    a3 = a[a2]
    k = list(a3)
    for v in k:
        print(v)
    print(k)
