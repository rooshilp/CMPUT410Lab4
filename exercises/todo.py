from flask import Flask, request, url_for, redirect
import sqlite3

dbFile = 'task.db'
conn = None

def get_conn():
    global conn
    if conn is None:
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
    return conn

def close_connection():
    global conn
    if conn is not None:
        conn.close()
        conn = None
        
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    cur.close()
    return r[0] if one else r

def add_task(category):
    tasks = query_db('insert into tasks(category) values(?)', [category], one=true)
    get_conn().commit()

    
app = Flask(__name__)
tasks = []

@app.route('/')
def welcome():
    return '<h1>Welcome to the Flask lab!</h1>'

@app.route('/task1', methods = ['GET', 'POST'])
def task():
    #POST:
    if request.method == 'POST':
        category = request.form['category']
        tasks.append({'category':category})
        #return redirect('/task1')
        return redirect(url_for('task'))        
    
    #GET:
    resp = '''
    <form action="" method =post>
    <p>Category: <input type=text name=category></p>
    <p><input type=submit name=Add></p>
    '''
 
    #show table:
    resp = resp + '''
    <table border="1" cellpadding="3">
        <body>
            <tr>
                <th>Category</th>
            </tr>
    '''
    for task in tasks:
        resp = resp + "<tr><td>%s</td></tr>" %(task['category'])
        
    resp = resp + "</body></table>"
    return resp

if __name__ == '__main__':
    app.run()