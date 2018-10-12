from bottle import route, run, template
from project import app


@app.route('/', method='GET')
def index():
    return template('index')


if __name__ == '__main__':
    run(app, reloader=True, host='localhost', port=8080)