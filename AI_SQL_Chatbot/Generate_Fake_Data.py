import pandas as pd
from faker import Faker
import random

fake = Faker()

# Config
NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000   
NUM_PRODUCTS = 100

# Generate Customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'address': fake.address().replace('\n', ', ')
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv('customers.csv', index=False)

# Generate Products
products = {"Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch"],
            "Home Appliances": ["Refrigerator", "Microwave", "Washing Machine", "Air Conditioner", "Vacuum Cleaner"],
            "Books": ["Fiction Book", "Non-Fiction Book", "Science Book", "History Book", "Biography"],
            "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers"],
            "Toys": ["Action Figure", "Doll", "Puzzle", "Board Game", "Building Blocks"]}

product_list = list(products.items())

products = []
for i in range(1, NUM_PRODUCTS + 1):
    category, names = random.choice(product_list)
    product_name = random.choice(names)
    products.append({
        'product_id': i,
        'category': category,
        'product_name': product_name,
        'price': round(random.uniform(5.0, 500.0), 2)
    })
products_df = pd.DataFrame(products)
products_df.to_csv('products.csv', index=False)

# Generate Orders
orders = []
for i in range(1, NUM_ORDERS + 1):
    orders.append({
        'order_id': i,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'product_id': random.randint(1, NUM_PRODUCTS),
        'quantity': random.randint(1, 10),
        'order_date': fake.date_this_year()
    })
orders_df = pd.DataFrame(orders)
orders_df.to_csv('orders.csv', index=False)
print("Fake data generated and saved to CSV files.")
