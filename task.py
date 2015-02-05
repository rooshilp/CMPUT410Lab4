import os
import sqlite3
from flask import Flask, request, url_for, redirect
app = Flask(__name__)

dbFile = 'task.db'
conn = None

def get_conn():
    global conn
    if conn is None:
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    global conn
    if conn is not None:
        conn.close()
        conn = None
        
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    cur.close()
    return (result[0] if result else None) if one else result
    
@app.route('/')
def welcome():
    return '<h1>Welcome to the Flask lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
    #POST:
    if request.method == 'POST':
        query_db("insert into task (category, priority, description) values (?, ?, ?)", 
                 [request.form['category'], int(request.form['priority']), request.form['description']])
        get_conn().commit()
        #return redirect('/task1')
        return redirect(url_for('task'))        
    
    #GET:
    resp = '''
    <form action="" method =post>
    <p>Category: <input type=text name=category></p>
    <p>Priority: <input type=number name=priority></p>
    <p>Description: <input type=text name=description></p>
    <p><input type=submit name=Add></p>
    '''
 
    #show table:
    resp = resp + '''
    <table border="1" cellpadding="3">
        <body>
            <tr>
                <th>Category</th>
                <th>Priority</th>
                <th>Description</th>
            </tr>
    '''
    tasks = query_db('select * from task')
    for task in tasks:
        resp = resp + "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (task['category'], task['priority'], task['description'])
        
    resp = resp + "</body></table>"
    return resp    


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)