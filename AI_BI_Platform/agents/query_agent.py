from openai import AzureOpenAI
from config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, API_VERSION

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=API_VERSION
)

class QueryAgent:
    def __init__(self):
        self.name = "QueryAgent"

def run(self, user_query: str, schema: dict) -> str:
    prompt = f"""
    Your are a SQL Expert.
    Create a single SQL query and return only the SQL code, no explaination.
    Only use SELECT statements. DO NOT use queries that start with - INSERT, UPDATE, DELETE, DROP, ALTER, EXEC, MERGE or CREATE
    This is the schema: {schema}
    User question: {user_query}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert SQL generator"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=300
    )

    sql = response.choices[0].messages.content.strip()
    sql = sql.replace("```sql","").replace("```", "").strip()
    return sql