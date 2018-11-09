import json
import time
import project.models.vector_index as Vector
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
    kind = int(request.query.kind)
    if len(boolean_str) == 0:
        return json.dumps({'id_list': [], 'song_list': []})
    not_str = request.query.dont
    if kind == 2:
        id_list = list(set(InvertedIndex.search_boolean(boolean_str, not_str, 1)).
                       union(InvertedIndex.search_boolean(boolean_str, not_str)))
    else:
        id_list = InvertedIndex.search_boolean(boolean_str, not_str, kind)
    if id_list == []:
        search_list = []
    else:
        search_list = SongList.get_search_list(id_list)
    return json.dumps({'id_list': id_list, 'song_list': search_list})


@app.route('/search/vector', method='GET')
def get_search_vector():
    response.headers['Access-Control-Allow-Origin'] = '*'
    search_str = request.query.text
    kind = int(request.query.kind)
    if len(search_str) == 0:
        return json.dumps({'id_list': [], 'song_list': []})
    vector_search = Vector.VectorSearch(search_str)
    id_list = vector_search.get_sort(kind)
    if id_list == []:
        search_list = []
    else:
        search_list = SongList.get_search_list(id_list)
    return json.dumps({'id_list': id_list, 'song_list': search_list})


@app.route('/search/vector-list', method='GET')
def get_search_vector():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(Vector.VectorSpace.get_vector_list())
