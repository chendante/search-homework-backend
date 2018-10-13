import json
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
