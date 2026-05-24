# import flask and other necessary libraries
from flask import Flask, render_template
import sqlite3

# create a Flask application

app = Flask(__name__)

#the path and file name for the database
DATABASE = 'database.db'

# cool function to automatically connect and query
def query_db(sql, args=(), one=False):
    '''connecct and query- will return one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

# routes
@app.route('/')
def index():
    results = query_db('SELECT * FROM "PC-parts"')
    return render_template('base.html', results=results)

