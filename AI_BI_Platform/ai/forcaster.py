import pandas as pd
from openai import AzureOpenAI

class Forcaster:
    def __init__(self, client):
        self.client = client

    def forcast(self, df: pd.DataFrame):
        if df.empty:
            return "No data available for forcasting"
        
        prompt = {
            "Based on the historical data, generate a 3-month projection"
            "of key numerical metrics and describe expected trends"
        }
        response = self.client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {
                    "role":"system", "content": "You are a forcasting analyst."
                },
                {
                    "role": "user", "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()