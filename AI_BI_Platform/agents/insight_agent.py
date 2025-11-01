import pandas as pd 
from openai import AzureOpenAI
from config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, API_VERSION

# Initialize OpenAi client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version = API_VERSION
)

class InsightAgent:
    def __init__(self):
        self.name = "InsightAgent"

    def run(self, df: pd.DataFrame, user_question: str) -> str:
        if df.empty:
            return "No data available for insights."
        
        sample_data = df.head(50).to_markdown(index=False)

        prompt = f"""
                    You are an expert data analayst. Answer the question '{user_question}'.
                    Use this data sample: {sample_data}
                    Provide, actionable insights, trends, and give recommendations how to maximize profits using current strategies 
                    in the nutrition / supplement retail market.
                  """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are and enterprise insights generator."},
                {"role": "user", "content": prompt}
            ],
            temperature= 0.6,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()