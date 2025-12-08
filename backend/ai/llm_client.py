# backend/ai/llm_client.py

"""
Single place to configure all LLM + Embeddings providers.

Change only the constants at the top (or env vars) to switch models.
All other modules should import get_chat_llm() and get_embedding_model().
"""

import os
from dotenv import load_dotenv


# ------------ CONFIGURATION ------------

# Load .env from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

# You can also set these via environment variables if you want.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")        # 'ollama', 'gemini', 'groq', 'openai' (future)
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "ollama")    # usually same as LLM_PROVIDER

# Default model names (can be overridden with env vars)
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "mistral")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Example placeholders if you later use these:
# GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL", "gemini-1.5-flash")
# GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")

GROQ_LLM_MODEL = os.getenv("GROQ_LLM_MODEL", "llama-3.1-8b-instant")


# ------------ CHAT LLM FACTORY ------------

def get_chat_llm():
    """
    Returns a LangChain chat model depending on LLM_PROVIDER.
    Only this function needs to change when you switch providers.
    """
    provider = LLM_PROVIDER.lower()

    if provider == "ollama":
        # Local model via Ollama
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(model=OLLAMA_LLM_MODEL)

    elif provider == "gemini":
        # Requires: pip install google-generativeai langchain-google-genai
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set for Gemini.")
        return ChatGoogleGenerativeAI(
            model=GEMINI_LLM_MODEL,
            temperature=0.3,
        )

    elif provider == "groq":
        # Requires: pip install langchain-groq
        from langchain_groq import ChatGroq
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set for Groq.")
        return ChatGroq(
            model_name=GROQ_LLM_MODEL,
            temperature=0.3,
        )

    # You can add 'openai', 'anthropic', etc. here later in the same pattern.

    # Fallback: Ollama
    from langchain_community.chat_models import ChatOllama
    return ChatOllama(model=OLLAMA_LLM_MODEL)


# ------------ EMBEDDINGS FACTORY ------------

def get_embedding_model():
    """
    Returns a LangChain embeddings model depending on EMBED_PROVIDER.
    Used by vector_store.py to build the Chroma DB.
    """
    provider = EMBED_PROVIDER.lower()

    if provider == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)

    elif provider == "gemini":
        # Requires: pip install google-generativeai langchain-google-genai
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set for Gemini embeddings.")
        return GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBED_MODEL,
        )

    # If you later want OpenAI embeddings, add here.
    # elif provider == "openai":
    #     from langchain_openai import OpenAIEmbeddings
    #     return OpenAIEmbeddings(model="text-embedding-3-small")

    # Fallback: Ollama embeddings
    from langchain_community.embeddings import OllamaEmbeddings
    return OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
