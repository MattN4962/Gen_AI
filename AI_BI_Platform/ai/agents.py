from openai import AzureOpenAI
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_API_VERSION, DEFAULT_MODEL
from .anomoly_detector import Anomoly_Detector
from .insight_engine import Insights_Engine
from .strategy_advisor import Strategy_Advisor
from .forcaster import Forcaster


class SQL_Agent:
    def __init__(self, client):
        self.client = client
    
    def generate_sql(self, user_query, schema):
        response = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role":"system",
                "content":f"""You will take the user query in natural language and produce a a SINGLE SQL query using only SELECT statements using SQL Server query syntax."
                " This is the table schema: {schema}, and the field is_Pro is either True or False."
                "When placing brackets around schema and table names, make sure that ONLY table and schema names are in []'s" 
                "Always ensure joins and filters compare columns of the same data type. "
                "If joining numeric and string columns, use TRY_CAST on both sides to avoid conversion errors."
                "If a column has a datetimeoffset data type, always CAST it as DATETIME in the query "
                "to ensure compatibility with pyodbc and Python."
                "Only use columns that you know exist in the provided schema. Do NOT assume and columns exist if they are not listed"  
                """
                }
            ]
            temperature=0
        )
        return response.choices[0].message.content.strip()