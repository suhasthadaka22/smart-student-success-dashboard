# backend/ai/rebuild_vectorstore.py

from backend.ai.vector_store import build_vectorstore, VECTOR_DIR
import shutil
import os

if __name__ == "__main__":
    print("🔥 Rebuilding Vectorstore...")

    # Delete old vectorstore dir
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)
        print("🗑 Deleted old vectorstore folder.")

    # Rebuild
    vs = build_vectorstore()
    print("✅ New vectorstore built successfully.")