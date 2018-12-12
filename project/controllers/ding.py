import json
from project import app
from bottle import template, request, response
from project.models.ding.ding_search import DingSearch
from project.models.ding.build_index import *


@app.route('/ding/search', method='GET')
def search():
    response.headers['Access-Control-Allow-Origin'] = '*'
    keyword = request.query.keyword
    site_type = request.query.type
    page = int(request.query.page)
    site_type = int(site_type)
    return json.dumps(DingSearch.search(keyword, site_type, page))


@app.route('/ding/copy/<site>/<id>', method='GET')
def copy(site, id):
    site_type = int(site)
    id = int(id)
    info = IndexData.get_info(id, site_type)
    if info['success']:
        return info['data'][0][5].strip("\"")
    else:
        return "page not found 404"


@app.route('/ding/build/test', method='POST')
def build_test():
    IndexBuilder.test_build()
    return "success"


@app.route('/ding/build/real', method='POST')
def build_index():
    IndexBuilder.rebuild_index()
    return "success"
