# ingest_data.py
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
# We are now using DirectoryLoader to read from a local folder
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
# We are using Ollama for local embeddings
from langchain_community.embeddings import OllamaEmbeddings
# We import from our config file
from config import REPO_PATH, VECTOR_DB_PATH, EMBEDDING_MODEL

load_dotenv()

def ingest_codebase():
    # Load code from the local cloned_repo directory
    print(f"Loading documents from the local '{REPO_PATH}' directory...")
    
    # --- THIS IS THE FINAL FIX for encoding and file type ---
    loader = DirectoryLoader(
        REPO_PATH, 
        glob="**/*.py", # We now load Python files
        loader_cls=TextLoader, 
        use_multithreading=True, 
        loader_kwargs={'encoding': 'utf-8'} # We explicitly use utf-8 encoding
    )
    # --------------------------
    
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")
    
    # We'll only process the first 20 documents for a quick start.
    documents = documents[:20]
    print(f"Processing a smaller subset of {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks.")

    print("Creating Ollama embeddings and ingesting into ChromaDB...")
    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=VECTOR_DB_PATH)
    print("Ingestion complete. Vector database is ready.")

if __name__ == "__main__":
    ingest_codebase()