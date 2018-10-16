import json
import time
from project.models.inverted_index import InvertedIndex
from project import app
from bottle import template, request, response


@app.route('/search', method='GET')
@app.hook('after_request')
def get_song_list():
    response.headers['Access-Control-Allow-Origin'] = '*'
    word = request.query.word
    print(word)
    return json.dumps(InvertedIndex.search_lyric(word))


@app.route('/search/boolean', method='GET')
@app.hook('after_request')
def get_search_boolean():
    response.headers['Access-Control-Allow-Origin'] = '*'
    word = request.query.word
    print(word)
    return json.dumps(InvertedIndex.search_boolean(word))
