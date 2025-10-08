

class Strategy_Advisor:
    def __init__(self, client):
        self.client = client

    def suggest_strategy(self, insights, forcast, anomalies):
        prompt =(
            f"Givent these insights:\n{insights}\n"
            f"Forcast:\n{forcast}\n"
            f"Anomalies:\n{anomalies}\n\n"
            "Provide actionable business strategies or optimizations."
        )

        response = self.client.chat.completions.create(
            model = "gpt-4o",
            messages=[{"role": "system", "content": "You are a business strategist."},
                      {"role": "user","content": prompt}]
        )

        return response.choices[0].message.content.strip()