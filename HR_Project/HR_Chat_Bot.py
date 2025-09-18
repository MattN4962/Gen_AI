import os
from dotenv import load_dotenv
import gradio as gr
from langchain_huggingface import ChatHuggingFace, HuggingFaceEmbeddings, HuggingFaceEndpoint

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
    loader = PyPDFLoader("Nestle_Policy.pdf")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 50,
        chunk_overlap = 10
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorStore = Chroma.from_documents(chunks, embeddings)

    return f"Loaded {len(chunks)} text chunks into Chroma DB"
# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful HR assistant. Use the context from Nestle's HR policy
to answer the question clearly and concisely.

Context:
{context}

Question:
{question}

Answer:
"""
)

llm = ChatHuggingFace(
    llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="conversational",
    huggingfacehub_api_token=api_key,
    temperature=0.3,
    max_new_tokens=1000
    )
)

# Answer questions using vecto search + GPT
def huggingface_chat(message, history):
    global vectorStore
    if not vectorStore:
        reply = "Please upload the HR Policy PDF!"
        history.append((message, reply))
    # Retrieve most relevant chunks
    chunks = vectorStore.similarity_search(message, k=3)
    context = "\n\n".join([c.page_content for c in chunks])
    # Build final prompt
    prompt = prompt_template.format(context=context, question=message)
    
    # Call Hugging Face model
    response = llm.invoke(prompt)
    reply = response.content
    #print(response) For debugging

    history.append((message, reply))
    return history, history

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Nestlé HR Policy Assistant (Hugging Face Edition)")

    with gr.Row():
        with gr.Column(scale=1):
            pdf_file = gr.File(label="Upload Nestlé HR Policy PDF", type="filepath")
            load_btn = gr.Button("Load PDF")
            status = gr.Textbox(label="Status")

        with gr.Column(scale=2):
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Ask about Nestlé HR Policy...")
            clear = gr.Button("Clear Chat")

    load_btn.click(loadPDF, pdf_file, status)

    def user_input(user_message, history):
        return "", history + [[user_message, None]]

    msg.submit(user_input, [msg, chatbot], [msg, chatbot], queue=False).then(
        huggingface_chat, [msg, chatbot], [chatbot, chatbot]
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
