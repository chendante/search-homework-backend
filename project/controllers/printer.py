# -*- coding: utf-8 -*-
import json
from project import app
from bottle import template, request


@app.route('/', method='GET')
def index():
    return template('printer/index', message='')


@app.route('/print', method=['GET', 'POST'])
def printer():
    if request.method == 'POST':
        message = request.forms.get('text')
        message = message+'22'
        return json.dumps(message)
        # return template('printer/index', message=message)
    return template('printer/print', message='')
