# backend/ai/llm_client.py
import os
from dotenv import load_dotenv
import os.path as osp
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


BASE_DIR = osp.abspath(osp.join(osp.dirname(__file__), "..", ".."))
load_dotenv(osp.join(BASE_DIR, ".env"))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "openai")

# model names
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

def get_chat_llm():
    provider = LLM_PROVIDER.lower()
    if provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model=os.getenv("OLLAMA_LLM_MODEL", "mistral"))
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model_name=os.getenv("GROQ_LLM_MODEL", "llama-3.1-8b-instant"))
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_LLM_MODEL", "gemini-1.5-flash"))
    if provider == "openai":
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), temperature=0.2)
    # fallback
    from langchain_community.chat_models import ChatOllama
    return ChatOllama(model=os.getenv("OLLAMA_LLM_MODEL", "mistral"))


def get_embedding_model():
    """Return an embeddings object compatible with LangChain/Chroma."""
    provider = EMBED_PROVIDER.lower()

    if provider == "openai":
        # LangChain OpenAIEmbeddings
        from langchain.embeddings import OpenAIEmbeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment")
        return OpenAIEmbeddings(model=OPENAI_EMBED_MODEL, openai_api_key=api_key)

    if provider == "gemini":
        # Google (Gemini) embeddings via LangChain Google wrapper
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        api_key = os.getenv("GOOGLE_API_KEY")
        model=os.getenv("GEMINI_EMBED_MODEL")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set in environment")
        return GoogleGenerativeAIEmbeddings(model=model)

    if provider == "local":
        return LocalSentenceTransformerEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

    # fallback: Ollama (local)
    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=os.getenv("OLLAMA_EMBED_MODEL"))

    # final fallback to OpenAI
    from langchain.embeddings import OpenAIEmbeddings
    return OpenAIEmbeddings(model=OPENAI_EMBED_MODEL)

class LocalSentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        ).tolist()

    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True).tolist()
