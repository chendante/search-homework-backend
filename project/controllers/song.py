import json
import time
from project.models.song_list import SongList
from project import app
from bottle import template, request, response


@app.route('/song/number', method='GET')
# @app.hook('after_request')
def get_song_number():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(SongList.song_number())


@app.route('/song/list', method='GET')
# @app.hook('after_request')
def get_song_list():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(SongList.song_name_list())


@app.route('/song/one', method='GET')
# @app.hook('after_request')
def get_one_song():
    response.headers['Access-Control-Allow-Origin'] = '*'
    id = request.query.id
    return json.dumps(SongList.get_one_song(id))


@app.route('/song/index', method='POST')
# @app.hook('after_request')
def update_index():
    response.headers['Access-Control-Allow-Origin'] = '*'
    begin = time.time()
    SongList.updateIndex()
    end = time.time()
    return json.dumps(end-begin)


@app.route('/song/vector-index', method='POST')
def update_vector_index():
    response.headers['Access-Control-Allow-Origin'] = '*'
    begin = time.time()
    SongList.update_vector_index()
    end = time.time()
    return json.dumps(end - begin)
