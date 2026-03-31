from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import mysql.connector
from backend.searching import search_products
from backend.sorting import quicksort_products

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("db_host"),
    port=int(os.getenv("db_port")),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name")
)

cursor = db.cursor(dictionary=True)

category_map = {
    1: ("books", "images/books.png"),
    2: ("clothes", "images/clothes.jpeg"),
    3: ("groceries", "images/groceries.jpeg"),
    4: ("toys", "images/toys.jpg"),
    5: ("accessories", "images/accessories.jpg"),
    6: ("home", "images/home_appliances.jpg")
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', categories=category_map)

def fetch_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

@app.route('/products', methods=['GET'])
def show_products():
    products_list = fetch_products()
    
    category = request.args.get('category')
    if category and category.isdigit():
        products_list = [p for p in products_list if p['category_id'] == int(category)]

    query = request.args.get('search')
    if query:
        products_list = search_products(products_list, query)
        
    sort = request.args.get('sort')
    if sort == 'price_asc':
        products_list = quicksort_products(products_list.copy(), ascending=True)
    elif sort == 'price_desc':
        products_list = quicksort_products(products_list.copy(), ascending=False)
        
    folder_map = {
        1: "books",
        2: "clothes",
        3: "groceries",
        4: "toys",
        5: "accessories",
        6: "home"
    }

    for product in products_list:
        category_id = product['category_id']
        product_id = product['id']
        folder = folder_map.get(category_id, "misc")
        product['image_url'] = f"images/{folder}/{(product_id % 50)}.jpg"
        
    return render_template('products.html', products=products_list)


if __name__ == '__main__':
    app.run(debug=True)