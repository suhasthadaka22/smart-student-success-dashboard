import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.ai.llm_client import get_embedding_model

# ----- Correct project paths -----
# vector_store.py is in backend/ai
# project root is two levels up: ../../
# Base directory = project root (adjust if needed)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DOCS_DIR = os.path.join(BASE_DIR, "docs")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")  
os.makedirs(VECTOR_DIR, exist_ok=True)


def build_vectorstore():
    """
    Load markdown docs from docs/, split into chunks,
    create embeddings using Ollama, and store them in an in-memory Chroma collection.
    """
    loaders = [
    TextLoader(os.path.join(DOCS_DIR, "attendance_rules.md"), encoding="utf-8"),
    TextLoader(os.path.join(DOCS_DIR, "study_tips.md"), encoding="utf-8"),
    TextLoader(os.path.join(DOCS_DIR, "events.md"), encoding="utf-8"),
    TextLoader(os.path.join(DOCS_DIR, "library_resources.md"), encoding="utf-8")
    ]

    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    # Use provided embeddings with explicit model (you already pulled this)
    embeddings = get_embedding_model()

    # In-memory Chroma – no persist_directory, no dimension conflicts
    vectorstore = Chroma.from_documents(
        split_docs,
        embedding=embeddings,
        persist_directory=VECTOR_DIR,
    )
    return vectorstore


def get_vectorstore():
    # For our small demo, rebuilding each time is fine.
    # If you want, we can later cache this with functools.lru_cache or Streamlit cache.
    return build_vectorstore()
