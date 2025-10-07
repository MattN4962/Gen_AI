import pyodbc
from config import CONN_STR

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