from backend.ai.llm_client import get_chat_llm

def main():
    llm = get_chat_llm()
    print("Using LLM:", llm)

    question = "In one sentence, explain what this project does."
    resp = llm.invoke(question)
    print("\nResponse:\n", resp.content if hasattr(resp, "content") else resp)

if __name__ == "__main__":
    main()