import pyodbc
from config import CONN_STR

<<<<<<< Updated upstream
def get_connection():
    """Establish a connection to Azure Synapse."""
    try:
        conn = pyodbc.connect(CONN_STR)
        print("✅ Connected to Azure Synapse")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None
get_connection()
=======
def get_db_connection():
    """
    Gets the DB connection to be used throughout the app
    """
    try:
        conn = pyodbc.connect(CONN_STR)
        print("Connected To Database")
        return conn
    except Exception as e:
        print("Unable to Connect")
        return None 
>>>>>>> Stashed changes
