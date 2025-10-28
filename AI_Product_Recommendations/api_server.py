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

def diversify_results(results, max_per_product=2):
    seen = {}
    diversified = []

    for res in results:
        if isinstance(res, dict):
            product = res.get("Display Name", None)
        elif isinstance(res, str):
            product = res
        
        if product not in seen:
            seen[product] = 0
        if seen[product] < max_per_product:
            diversified.append(res)
            seen[product] += 1

    return diversified    

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
    diversifed_response = diversify_results(response, max_per_product=2)
    
    return {"query": request.query, "results": diversifed_response}

@app.post("/generate_regimen")
async def generate_regimen(request: QueryRequest):
    results = query_vectorstore(collection, request.query, top_k=request.top_k)
    products = []

    for i, doc in enumerate(results["documents"][0]):
        parts = [p.strip() for p in doc.split("|")]
        display_name = parts[0].strip() if len(parts) > 0 else "Unknown Product"
        division = parts[2] if len(parts) > 0 else "No Data"
        category = parts[3] if len(parts) > 0 else "No Data"
        products.append(f"{display_name} ({category})")
    
    diversify_results(products, max_per_product=3)

    #Generate Regimen with GPT
    product_context = "\n".join(products)
    prompt = f"""
        The user wants a personalized supplement regimen to achieve their goal: "{request.query}",
        Based on these available products:
        {product_context}

        Create a clear, structured daily plan using these products.
        Include timing(morning, pre-workout, post-workout, evening), dosage guidance, and rationale.
        Keep the explanation minimal and only provide necessary information - this may be used in a store setting by an associate 
        """

        # Define Open AI connection
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("API_VERSION")
    )

    llm_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert fitness and supplement advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=600
    )

    regimen = llm_response.choices[0].message.content

    return {
        "query": request.query,
        "products": products,
        "regimen": regimen
    }