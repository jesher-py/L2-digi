# import flask and other necessary libraries
from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

#  initialise Flask application
app = Flask(__name__)

#the path and file name for the database


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

# routes go here
@app.route('/')
def home():
    # home page- will display all the PC parts in the database
    # query to select all the PC parts from the database, name, brand, category and price

    sql = """ SELECT name, brand, category, price, imgURL FROM "PC-parts" """

    results = query_db(sql)
    return render_template('home.html',results=results)

if __name__ == '__main__':
    app.run(debug=True)