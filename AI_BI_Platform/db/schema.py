import pandas as pd
from .synapse_connector import get_db_connection


def get_schema():
    query = """
        SELECT
            TABLE_NAME   AS table_name,
            COLUMN_NAME  AS column_name,
            DATA_TYPE    AS data_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
    """
    
    conn, cursor = get_db_connection()
    if not conn or not cursor:
        return {}
    
    cursor.execute(query)
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["table_name", "column_name", "data_type"])
    #print(df)
    schema_dict = (
            df.groupby("table_name")
              .apply(lambda g: [f"{col} ({dtype})" for col, dtype in zip(g.column_name, g.data_type)])
              .to_dict()
        )
    return schema_dict