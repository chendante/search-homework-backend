from project.models.base import Database

#将字符串格式的id列表转换为列表
def convert_list(num_str):
    data = num_str.lstrip().rstrip().split(" ")
    res = []
    for val in data:
        if val != '':
            res.append(val)
    return res


#把所有运算符都当成右运算符
def deal_boolean_list(boolean_list, kind=0):
    single_word_list = InvertedIndex.search_lyric(boolean_list[0], kind)
    if len(boolean_list) > 1:
        if boolean_list[1] == 'AND':
            return list(set(single_word_list).intersection(set(deal_boolean_list(boolean_list[2:], kind))))
        elif boolean_list[1] == 'OR':
            return list(set(single_word_list).union(set(deal_boolean_list(boolean_list[2:], kind))))
    else:
        return single_word_list


#将所有词项的倒排记录表取并集
def deal_not_list(not_list, kind=0):
    t = []
    for word in not_list:
        t = list(set(t).union(set(InvertedIndex.search_lyric(word, kind))))
    return t


class InvertedIndex:
    @staticmethod
    def lyric_inverted_index_list():
        Database.cursor.execute("SELECT * from lyric_inverted_index limit 100")
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def name_inverted_index_list():
        Database.cursor.execute("SELECT * from name_inverted_index limit 100")
        data = Database.cursor.fetchall()
        return data

    @staticmethod
    def search_name(search_word):
        sql = "SELECT * FROM name_inverted_index WHERE name_inverted_index.word='%s'" % search_word
        Database.cursor.execute(sql)
        # 获取所有记录列表
        data = Database.cursor.fetchall()
        if data == ():
            return []
        return convert_list(data[0][2])

    @staticmethod
    def search_lyric(search_word, kind=0):
        if kind == 0:
            sql = "SELECT * FROM lyric_inverted_index " \
                  "WHERE lyric_inverted_index.word='%s'" \
                  % search_word
        else:
            sql = "SELECT * FROM name_inverted_index " \
                  "WHERE name_inverted_index.word='%s'" \
                  % search_word
        Database.cursor.execute(sql)
        # 获取所有记录列表
        data = Database.cursor.fetchall()

        if data == ():
            return []
        return convert_list(data[0][2])

    @staticmethod
    def search_boolean(boolean_str, not_str, kind=0):
        boolean_list = convert_list(boolean_str)
        if len(not_str) == 0:
            not_list = []
        else:
            not_list = deal_not_list(convert_list(not_str), kind)
        return list(set(deal_boolean_list(boolean_list, kind)).difference(set(not_list)))
