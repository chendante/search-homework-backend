import json
import time
from project.models.inverted_index import InvertedIndex
from project.models.song_list import SongList
from project import app
from bottle import template, request, response


#获取两个倒排索引表
@app.route('/search/lyric-index', method='GET')
# @app.hook('after_request')
def get_lyric_index():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(InvertedIndex.lyric_inverted_index_list())


@app.route('/search/name-index', method='GET')
# @app.hook('after_request')
def get_name_index():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(InvertedIndex.name_inverted_index_list())


@app.route('/search/name', method='GET')
# @app.hook('after_request')
def get_song_list():
    response.headers['Access-Control-Allow-Origin'] = '*'
    word = request.query.word
    return json.dumps(InvertedIndex.search_name(word))


@app.route('/search/boolean', method='GET')
# @app.hook('after_request')
def get_search_boolean():
    response.headers['Access-Control-Allow-Origin'] = '*'
    boolean_str = request.query.boolean
    if len(boolean_str) == 0:
        return json.dumps("请输入正确格式的布尔表达式")
    not_str = request.query.dont
    id_list = InvertedIndex.search_boolean(boolean_str, not_str)
    if id_list == []:
        search_list = []
    else:
        search_list = SongList.get_search_list(id_list)
    return json.dumps({'id_list': id_list, 'song_list': search_list})



