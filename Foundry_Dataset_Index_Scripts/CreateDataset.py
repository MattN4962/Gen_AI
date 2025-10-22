import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
api_key = os.getenv("AI_FOUNDRY_API_KEY")
version = os.getenv("API_VERSION")
model = "gpt-4o-2"

url = endpoint

headers = {
    "Content-Type":"application/json",
    "api-key": api_key
}

payload = {
    "messages": [
        {
            "role": "system", "content": "You are an assistent"
        },
        {
            "role": "user", "content": "Confirm this endpoint is working"
        }
    ],
    "temperature": .3
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Success")
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Failed {response.status_code}")