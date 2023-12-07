# MiniProject 2 - eCommerce Product Management Site
# This Flask app is to be deployed through oracle to an online server

# import necessary libraries for app/website development
from flask import Flask, render_template, request, redirect
# import sql to handle database management
import sqlite3

# normal flask notation to initialize app and make sure it works right
app = Flask(__name__)

# this function initializes the database called 'product_db.db'
def initialize_database():
    with sqlite3.connect("product_db.db") as con:
        # this creates the actual table itself - be careful not to change db name! 
        con.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                description TEXT,
                price REAL,
                code TEXT
            )
        ''')
        con.commit()

# app route for home page that calls home.html file for formatting 
@app.route('/')
def home():
    return render_template('home.html')

# app route for adding new product to db
@app.route('/add_product', methods=['GET', 'POST']) # note: the GET and POST methods help sent and retrieve data to server
def add_product():
    # if statement retrieves the data from the user that correspond to each of variables required for product
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        price = float(request.form['price'])
        code = request.form['code']
    
        # adds each of the newly entered products into existing database
        with sqlite3.connect("product_db.db") as con:
            con.execute('''
                INSERT INTO products (category, description, price, code)
                VALUES (?, ?, ?, ?)
            ''', (category, description, price, code))
            con.commit()

        return redirect('/')
    
    return render_template('add_product.html')

# app route to view existing product and search based on category
@app.route('/view_product', methods=['GET', 'POST'])
# function to view existing product in the database
def view_product():
    # allows user to interact with page and enter in a specific category to search for
    if request.method == 'POST':
        category = request.form['category']
        with sqlite3.connect("product_db.db") as con:
            if category:
                cursor = con.execute('SELECT * FROM products WHERE category=?', (category,))
            else:
                cursor = con.execute('SELECT * FROM products')
            products = cursor.fetchall()
            return render_template('view_product.html', products=products)

    return render_template('view_product.html')

# app route will delete items in the database
@app.route('/delete_product/<int:prod_id>',methods=['POST'])
# function to delete the product 
def delete_product(prod_id):
    with sqlite3.connect('product_db.db') as con: 
        con.execute('DELETE FROM products WHERE id = ?',(prod_id,))

        return redirect('/view_product')

# debugger makes sure there's no kinks when the code runs
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
