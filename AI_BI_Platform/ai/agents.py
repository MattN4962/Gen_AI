from openai import AzureOpenAI
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_API_VERSION, DEFAULT_MODEL
from .anomoly_detector import Anomoly_Detector
from .insight_engine import Insights_Engine
from .strategy_advisor import Strategy_Advisor
from .forcaster import Forcaster


class SQL_Agent:
    