import pandas as pd 
from .synapse_connector import get_db_connection

def run_sql_query(query: str) -> pd.DataFrame:
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"SQL Error: {e}")
        return pd.DataFrame()
    finally: 
        conn.close()