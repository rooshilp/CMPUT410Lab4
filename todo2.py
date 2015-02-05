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
    return (result[0] if result else None) if one else result

def add_task(category):
    tasks = query_db('insert into task(category) values(?)', [category], one=True)
    get_conn().commit()
    
def print_tasks():
    tasks = query_db('select * from task')
    for task in tasks:
        print("task(category): %s " %task['category'])
        
    print("%d tasks in total." % len(tasks))


if __name__ == '__main__':
    query_db('delete from task')
    print_tasks()
    add_task('CMPUT410')
    add_task('abs')
    add_task('C10')
    print_tasks()