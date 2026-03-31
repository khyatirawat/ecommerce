def search_products(products, query):
    query = query.lower()
    return [
        product for product in products 
        if query in product['product_name'].lower()
        or query in product['descrip'].lower()
    ]