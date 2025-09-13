import os
from dotenv import load_dotenv
import gradio as gr
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI

# LangChain tools
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
#print(api_key)

# Define Globals
vectorStore = None
# Load PDF, split, store in Chroma
def loadPDF(file):
    global vectorStore
    loader = PyPDFLoader(file.name)
    documents = loader.load

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 50,
        chunk_overlap = 10
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorStore = Chroma.from_documents(chunks, embeddings)

    return f"Loaded {(chunks)} text chunks into Chroma DB"
# Define prompt template

# Answer questions using vecto search + GPT

    # Retrieve most relevant chunks

    # Build final prompt

    # Call GPT model


# Gradio UI

