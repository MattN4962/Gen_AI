from config import DEFAULT_MODEL


class SQL_Agent:
    def __init__(self, client):
        self.client = client
    
    def generate_sql(self, user_query, schema):
        response = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                "role": "system",
                "content": f"""
                You will take the user query in natural language and produce a SINGLE SQL query using only SELECT statements written in SQL Server syntax.
                Return ONLY the SQL query — no explanations.

                This is the table schema: {schema}

                Important rules:
                1. Only use columns that exist in the provided schema. Do NOT assume additional columns.
                2. Prefer columns that contain actual data (non-NULL for most records). Avoid using columns that are known or likely to be NULL for all rows.
                3. If unsure whether a column contains data, you may exclude it.
                4. Always ensure joins and filters compare columns of the same data type.
                5. If joining numeric and string columns, use TRY_CAST on both sides to avoid conversion errors.
                6. If a column has a datetimeoffset data type, CAST it as DATETIME in the query for pyodbc and Python compatibility.
                7. If the user’s intent is unclear, focus on returning a valid, meaningful query using non-null, relevant columns only.
                8. Only use tables with the schema name CustomerHub or OrderHub, use no other tables
                9. If a column has a datetimeoffset or datetime2 data type, CAST it as DATETIME in the query for pyodbc and Python compatibility.
                """
                }
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()