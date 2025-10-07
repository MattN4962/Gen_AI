import pyodbc
from config import CONN_STR


def get_db_connection():
    """
    Gets the DB connection to be used throughout the app
    """
    try:
        conn = pyodbc.connect(CONN_STR)
        print("Connected To Database")
        return conn
    except Exception as e:
        print("Unable to Connect:\n{e}")
        return None 
