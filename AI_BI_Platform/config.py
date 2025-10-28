import os
from dotenv import load_dotenv

"""
Central configuration for the AI BI Platform.
This file stores connection strings, model names, and report paths.
"""

# Load environment variables from .env file if present
load_dotenv()


# Azure Synapse / SQL Database connection
AZURE_SYNAPSE_SERVER = os.getenv("AZURE_SYNAPSE_SERVER")
AZURE_SYNAPSE_DB = os.getenv("AZURE_SYNAPSE_DB")
#AZURE_SYNAPSE_USERNAME = os.getenv("AZURE_SYNAPSE_USERNAME", "readonly_user")
#AZURE_SYNAPSE_PASSWORD = os.getenv("AZURE_SYNAPSE_PASSWORD", "<password>")
DEFAULT_MODEL="gpt-4o"

#Connection String
CONN_STR = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{AZURE_SYNAPSE_SERVER},1433;"
    f"Database={AZURE_SYNAPSE_DB};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
    "Authentication=ActiveDirectoryDefault;"
)

# Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "<your-endpoint>")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "<key>")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")


# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


# Other settings
MAX_QUERY_ROWS = int(os.getenv("MAX_QUERY_ROWS", "100000"))
