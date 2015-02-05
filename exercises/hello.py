from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello():
    return '<h1>Hello, Flask!</h1>'

@app.route('/hello2')
@app.route('/hello2/<name>')
def hello2(name = 'FLASK'):
    return '<h1>Hello, %s!</h1>' % name

if __name__ == '__main__':
    app.run()