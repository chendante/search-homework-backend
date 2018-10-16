import json
import time
from project.models.song_list import song_list
from project import app
from bottle import template, request, response


@app.route('/song/number', method='GET')
@app.hook('after_request')
def get_song_number():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(song_list.song_number())


@app.route('/song/list', method='GET')
@app.hook('after_request')
def get_song_list():
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(song_list.song_name_list())


@app.route('/song/index', method='POST')
@app.hook('after_request')
def update_index():
    response.headers['Access-Control-Allow-Origin'] = '*'
    begin = time.time()
    song_list.updateIndex()
    end = time.time()
    return json.dumps(end-begin)
