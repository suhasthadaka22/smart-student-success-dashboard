from backend.ai.llm_client import get_embedding_model

emb = get_embedding_model()
vec = emb.embed_query("hello world")

print("Embedding length:", len(vec))
