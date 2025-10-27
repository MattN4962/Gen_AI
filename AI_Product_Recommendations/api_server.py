from fastapi import FastAPI
from pydantic import BaseModel
from Vectorstore_Utils import load_collection, query_vectorstore, download_chroma_from_blob
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI(title="GNC Fitness GPT")

VECTORSTORE_PATH = os.getenv("TEMP_FOLDER_BASE")
COLLECTION_NAME = "Products_Collection"

print(f"Loading Chroma Store from: {VECTORSTORE_PATH}")
collection = load_collection(path=VECTORSTORE_PATH, collection_name=COLLECTION_NAME)

# Request Body Model
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# Endpoint to query
@app.post("/query")
async def query_vectorstore_endpoint(request: QueryRequest):
    results = query_vectorstore(collection, request.query, top_k=request.top_k)

    #Format results
    response = []
    for i, doc in enumerate(results["documents"][0]):
        parts = [p.strip() for p in doc.split("|")]
        display_name = parts[0] if len(parts) > 0 else "Unknown Product"
        division = parts[2] if len(parts) > 0 else "No Data"
        category = parts[3] if len(parts) > 0 else "No Data"
        response.append({
            "Rank": i + 1,
            "Display Name": display_name,
            "Division": division,
            "Category": category,
            "Score": results["distances"][0][i] if "distances" in results else None
        })

    return {"query": request.query, "results": response}
