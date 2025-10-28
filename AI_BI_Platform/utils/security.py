import re
import pandas as pd

forbidden_keywords = [
    "DROP", "DELETE", "INSERT", "TRUNCATE", "UPDATE", "ALTER", "EXEC", "CREATE", "EXECUTE"
]

def is_sql_safe(query: str) -> bool:
    #Check that sql is read-only
    clean_sql = re.sub(r"```sql|```", "", query, flags=re.IGNORECASE).strip().upper()
    if any(word in clean_sql for word in forbidden_keywords):
        return False
    if not clean_sql.startswith("SELECT"):
        return False
    return True

def dataframe_to_markdown(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df is None or df.empty:
        return "No Data"
    return df.head(max_rows).to_markdown(Index=False)