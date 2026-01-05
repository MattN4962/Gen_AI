import tempfile
import pandas as pd
import os, io
from dotenv import load_dotenv
from azure.storage.blob import BlobClient, BlobServiceClient
import chromadb
from tqdm import tqdm
from openai import AzureOpenAI
import hashlib


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

def check_vectorstore_exists_in_blob(container_name, blob_prefix):
    """Check if ChromaDB vectorstore exists in blob storage"""
    try:
        container_client = blob_service.get_container_client(container_name)
        blobs = list(container_client.list_blobs(name_starts_with=blob_prefix))
        return len(blobs) > 0
    except Exception as e:
        print(f"Error checking blob storage: {e}")
        return False

def download_csv_from_blob(container, blob_name):
    """Download CSV file from Azure Blob Storage"""
    print(f"Downloading CSV from Azure Blob: {blob_name}")
    blob_client = blob_service.get_blob_client(
        container=container,
        blob=blob_name
    )
    
    # Download blob data
    blob_data = blob_client.download_blob().readall()
    
    # Load into pandas DataFrame
    df = pd.read_csv(io.BytesIO(blob_data))
    print(f"Downloaded {len(df)} products from blob storage")
    
    return df

# Download Product Catalog
def download_chroma_from_blob(container_name, blob_prefix):
    print(f"Downloading Vectorstore From Azure Blob {blob_prefix}")
    container_client = blob_service.get_container_client(container_name)

    base_temp = os.getenv("TEMP_FOLDER_BASE", "./temp")
    temp_dir = os.path.join(base_temp, "chroma_store")

    os.makedirs(temp_dir, exist_ok=True)
    
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

def embed_products(df, collection, batch_size=500):
    """Embed products from DataFrame into ChromaDB collection"""
    print(f"Embedding {len(df)} products into ChromaDB...")
    
    # Convert DataFrame to list of dicts
    products = df.to_dict('records')
    
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

    for i in tqdm(range(0, len(vectorstore), batch_size), desc="Embedding batches"):
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
    
    print(f"Successfully embedded {len(vectorstore)} products")
    return collection


def persist_to_blob(upload_dir):
    """Upload ChromaDB files to Azure Blob Storage"""
    print("Uploading ChromaDB to Azure Blob Storage...")

    for root, _, files in os.walk(upload_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Create blob path relative to upload_dir
            relative_path = os.path.relpath(file_path, upload_dir)
            blob_path = f"{blob_prefix}{relative_path}".replace("\\", "/")
            
            blob_client = blob_service.get_blob_client(container=root_container, blob=blob_path)

            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded: {blob_path}")
    
    print("ChromaDB successfully persisted to blob storage")

def load_collection(path=os.getenv("TEMP_FOLDER_BASE"), collection_name="Products_Collection"):
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

def initialize_vectorstore():
    """Initialize vectorstore: download from blob if exists, otherwise create from CSV"""
    local_chroma_dir = os.path.join(os.getenv("TEMP_FOLDER_BASE"), "chroma_store")
    collection_name = "Products_Collection"
    
    # Check if vectorstore exists in blob storage
    vectorstore_exists = check_vectorstore_exists_in_blob(root_container, blob_prefix)
    
    if vectorstore_exists:
        print("Vectorstore found in blob storage, downloading...")
        # Download existing vectorstore from blob
        local_chroma_dir = download_chroma_from_blob(root_container, blob_prefix)
        collection = load_collection(local_chroma_dir, collection_name)
        print(f"Loaded existing collection with {collection.count()} embeddings")
    else:
        print("Vectorstore not found in blob storage, creating new one...")
        # Download CSV and create embeddings
        df = download_csv_from_blob(root_container, blob_path)
        
        # Create new ChromaDB collection
        os.makedirs(local_chroma_dir, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=local_chroma_dir)
        collection = chroma_client.get_or_create_collection(collection_name)
        
        # Check if collection is empty before embedding
        if collection.count() == 0:
            print("Collection is empty, embedding products...")
            embed_products(df, collection)
            
            # Persist to blob storage
            persist_to_blob(local_chroma_dir)
        else:
            print(f"Collection already has {collection.count()} embeddings, skipping embedding step")
    
    return collection, local_chroma_dir

if __name__ == "__main__":
    collection, local_chroma_dir = initialize_vectorstore()
    
    # Test query
    print("\n" + "="*50)
    print("Testing vectorstore with sample query...")
    print("="*50)
    query_vectorstore(collection, "protein powder for muscle building", top_k=5)
