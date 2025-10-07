import pandas as pd 

class Insights_Engine:

    def __init__(self, client):
        self.client = client

    def generate(self, df: pd.DataFrame, question: str):
        if df.empty:
            return "No data returned from the query"
        
        sample = df.head(200).to_markdown(index=False)

        prompt = (
            f"Analyze this sample to answer the question: {question}"
            f"Heres a sample: {sample}"
            f"Provide 3 key insights and concise explanations"
        )

        resp = self.client.chat.completions.create(
            model = "gpt-4o",
            messages =[
                
                {"role":"system", "content": "You are a senior data analyst"},
                {"role":"user", "content": prompt}
                
            ]
        )
        return resp.choices[0].message.content.strip()