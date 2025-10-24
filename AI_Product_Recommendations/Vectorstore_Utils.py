import tempfile
import pandas as pd
import os, io
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import chromadb
from tqdm import tqdm
from openai import AzureOpenAI


load_dotenv()

# Load Environment Variables For Blob Storage
blob_service = BlobServiceClient.from_connection_string(os.getenv("AZURE_BLOBSTORE_CONNECTION_STRING"))
root_container = os.getenv("ROOT_CONTAINER")
blob_path = os.getenv("BLOB_PATH")
blob_prefix = os.getenv("BLOB_PREFIX")



client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("API_VERSION")
)

# Download Product Catalog
def download_chroma_from_blob(container_name, blob_prefix):
    print(f"Downloading Vectorstore From Azure Blob {blob_prefix}")
    container_client = blob_service.get_container_client(container_name)
    temp_dir = tempfile.mkdtemp(prefix="chroma_")
    blobs = container_client.list_blobs(name_starts_with=blob_prefix)
    for blob in blobs:
        local_path = os.path.join(temp_dir, os.path.relpath(blob.name, blob_prefix))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, "wb") as f:
            data = container_client.download_blob(blob.name).readall()
            f.write(data)
        
    print(f"Chroma files downloaded to: {temp_dir}")
    
    return temp_dir


# persist_dir = "./vector_store/Product_Chroma_Collection/"
# chroma_client = chromadb.PersistentClient(path=persist_dir)
# collection = chroma_client.get_or_create_collection("Products_Collection")

def embed_blob(products, batch_size=500) -> chromadb.Collection:
    vectorstore = []
    pIds = []

    for p in products:
        id = str(p.get("ProductId", ""))
        description = str(p.get("ProductLongDescription", ""))
        display_name = str(p.get("ProductDisplayName", ""))
        p_division = str(p.get("ProductDivision", ""))
        p_category = str(p.get("ProductCategory", ""))
        p_class = str(p.get("ProductClass", ""))
        p_subclass = str(p.get("ProductSubClass", ""))
        p_isVegetarian = str(p.get("Vegetarian", ""))
        p_isVegan = str(p.get("Vegan", ""))
        p_price = str(p.get("BaseRetailPrice", ""))
    
        text = f"{display_name} | {description} | Division: {p_division} | Category: {p_category} | Class: {p_class} | SubClass: {p_subclass} | IsVegitarian: {p_isVegetarian} | IsVegan {p_isVegan} | Price: {p_price}"
        pIds.append(id)
        vectorstore.append(text)

    for i in tqdm(range(0, len(vectorstore), batch_size)):
        batch_texts = vectorstore[i:i+batch_size]
        batch_ids = pIds[i:i+batch_size]

        response = client.embeddings.create(
            input=batch_texts,
            model="embedding-small"
        )

        embeddings = [d.embedding for d in response.data]

        collection.add(
            ids=batch_ids,
            embeddings=embeddings,
            documents=batch_texts
        )
    return collection


def persist_to_blob(upload_dir="./vector_store/Product_Chroma_Collection/"):
    print("Uploading ChromaDB to Foundry Blob Storage")

    for root, _, files in os.walk(upload_dir):
        for file in files:
            file_path = os.path.join(root, file)
            blob_path = f"vectorstore/Product_Chroma_Collection/{os.path.relpath(file_path, upload_dir)}"
            blob_client = blob_service.get_blob_client(container=root_container, blob=blob_path)

            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

def load_collection(path="./vectorstore/Product_Chroma_Collection/", collection_name="Products_Collection"):
    client = chromadb.PersistentClient(path=path)
    collection_list = client.list_collections()
    collection = client.get_collection(collection_name)
    return collection

def query_vectorstore(collection, query_text, top_k=5):
    # Embed the query
    response = client.embeddings.create(
        input=query_text,
        model="embedding-small"
    )

    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k
    )

    print("Top matches")
    for i, doc in enumerate(results["documents"][0]):
        print(f"\nResult {i + 1}:")
        print(doc)
    
    return results

if __name__ == "__main__":

    local_chroma_dir = r"C:\Users\rt1mxn\AppData\Local\Temp"
    chroma_folders = [f for f in os.listdir(local_chroma_dir) if f.startswith("chroma") and os.path.isdir(os.path.join(local_chroma_dir, f))]

    if not chroma_folders:
        local_chroma_dir = download_chroma_from_blob(root_container, blob_prefix)

    local_chroma_dir = f"{local_chroma_dir}\\{chroma_folders[0]}"
    collection = load_collection(local_chroma_dir, "Products_Collection")

    query = "I want to build lean muscle and recover faster"
    query_vectorstore(collection, query)

