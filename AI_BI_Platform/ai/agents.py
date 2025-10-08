from openai import AzureOpenAI
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_API_VERSION, DEFAULT_MODEL
from .anomoly_detector import Anomoly_Detector
from .insight_engine import Insights_Engine
from .strategy_advisor import Strategy_Advisor
from .forcaster import Forcaster


class SQL_Agent:
    def __init__(self, client):
        self.client = client
    
    def generate_sql(self, user_query):
        response = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system", "content": f"You are a SQL exper"
                }
            ]
        )