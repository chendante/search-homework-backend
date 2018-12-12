from whoosh.qparser import QueryParser, OrGroup
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh import scoring
from project.models.ding.build_index import IndexBuilder
from whoosh.index import open_dir
import math


class DingSearch:
    try:
        ix = open_dir(IndexBuilder.index_path)
    except Exception as e:
        print(e)

    @staticmethod
    def search(keyword, type_id, page):
        searcher = DingSearch.ix.searcher(weighting=scoring.BM25F)
        m_parser = MultifieldParser(["content", "title"], IndexBuilder.schema, group=OrGroup)
        m_query = m_parser.parse(keyword)
        # m_query = And(Term("wid", 11))
        if type_id in [1, 2, 3, 4, 5]:
            m_query = m_query.__and__(Term("site", str(type_id)))
        res = searcher.search(m_query)
        # 得到查询总条数
        res_total = len(res)
        # 分页查询
        res = searcher.search_page(m_query, page, 15)
        try:
            rr = []
            for hit in res:
                if hit.highlights("title"):
                    title = hit.highlights("title")
                else:
                    title = hit["title"]
                if hit.highlights("content"):
                    content = hit.highlights("content")
                else:
                    content = hit["content"]
                rr.append(
                    {"id": hit['wid'], "url": hit['url'], "title": title, "content": content
                        , "score": hit.score, "site": hit['site'], "pagerank": hit['pagerank']})
            return {'data': DingSearch.re_sort(rr), 'res_total': res_total}
        except Exception as e:
            print(e)
            return {'data': [], 'res_total': 0}

    @staticmethod
    def re_sort(rr):
        sort_list = []
        for v in rr:
            score = math.log10(v["pagerank"]) + v["score"]
            sort_list.append(SortElement(score=score, info=v))
        sort_list.sort()
        res = []
        for new_element in sort_list:
            res.append(new_element.info)
        return res


# 重载运算符用于排序
class SortElement(object):
    def __init__(self, score="", info=""):
        self.score = score
        self.info = info

    def __lt__(self, other):  # override <操作符
        if self.score < other.score:
            return True
        return False


if __name__ == '__main__':
    print(DingSearch().search("南开大学", 1, 1000))
