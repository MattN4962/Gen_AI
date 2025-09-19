import mysql.connector
import pandas as pd
#This file is just to test the connection and a simple query
# Database connection configuration
config = {
    'user': 'root',
    'password': 'mysqlserver',
    'host': 'localhost',
    'port': 3306,
    'database':'Main'
}

# Connect to the database
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
print("Connected to the database.")

records = cursor.execute("SELECT * FROM customers limit 10;")
records = cursor.fetchall()
print(records)