# import flask and other necessary libraries
from flask import Flask, g, render_template, request
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
    # home page- will display th latest PC parts in the database, name, brand, price and image
    sql = """ 
    SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
    FROM "PC-parts"
    join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id
    WHERE rating >= 5
    ORDER BY releaseYear DESC
    """
    results = query_db(sql)
    return render_template('home.html',results=results)

@app.route('/parts')
def parts():

    #getting values from forms and passing them to the query
    brand = request.args.get('brand')
    price_point = request.args.get('price_tier')

    # parts page- will display all the PC parts in the database
    # query to select all the PC parts from the database, name, brand, category and price
    sql = """ SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
             FROM "PC-parts" 
             join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id 
             WHERE 1=1"""
    

    # list to hold the values for the query
    parameters = []
    if brand:
        sql += " AND manufacturers.name = ?"
        parameters.append(brand)
    if price_point:
       sql += " AND price_tier = ?"
       parameters.append(price_point)
       
    results = query_db(sql, tuple(parameters))
    return render_template('parts.html',results=results)


@app.route('/parts/cpu')
def cpu():
    # CPU page- will display all the CPUs in the database
    # query to select all the CPUs from the database, id, name, brand, price, category and release year

    sql = """ SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
             FROM "PC-parts" 
             join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id
             WHERE category = 'CPU'
    """

    results = query_db(sql)
    return render_template('parts.html',results=results)

@app.route('/parts/gpu')
def gpu():
    # GPU page- will display all the GPUs in the database
    # query to select all the GPUs from the database, id, name, brand, price, category and release year

    sql = """ 
    SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
    FROM "PC-parts" 
    join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id
    WHERE category = 'GPU' 
    """

    results = query_db(sql)
    return render_template('parts.html',results=results)

@app.route('/parts/ram')
def ram():
    # RAM page- will display all the RAMs in the database
    # query to select all the RAMs from the database, id, name, brand, price, category and release year

    sql = """ 
    SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
    FROM "PC-parts" 
    join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id WHERE category = 'RAM' """
    results = query_db(sql)
    return render_template('parts.html',results=results)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # search page- will display search results based on user input in the search bar
    results = []
    if request.method == 'POST':
        search_term = request.form['search']
        sql = """
        SELECT "PC-parts".id, "PC-parts".imgURL, "PC-parts".name, "manufacturers".name as brand, category, price
        FROM "PC-parts"
        join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id
        WHERE "PC-parts".name LIKE ?
        """
        results = query_db(sql, ['%' + search_term + '%'])
    return render_template('search.html', results=results)



@app.route('/detail/<int:id>')
def detail(id):
    # detail page- will display the details of a specific part
    # query to select the details of a specific part from the database, name, brand, price and image, specifications, and description

        sql = """ 
        SELECT "PC-parts".name, "manufacturers".name as brand, category, price, specs, description, price_tier, rating, releaseYear, imgURL, stockQuantity, compatibility
        FROM "PC-parts" 
        join manufacturers ON "PC-parts".manufacturers_id = manufacturers.id
        WHERE "PC-parts".id = ? 
        """
        results = query_db(sql, [id], one=True)
        return render_template('detail.html',part=results)
    
@app.route('/about')
def about():
    # about page- will display information about the website and the creator
    return render_template('about.html')

@app.route('/contact')
def contact():  
    # contact page- will display contact information for the creator
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)

