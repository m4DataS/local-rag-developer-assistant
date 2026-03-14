import requests
import json
import argparse
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# ----- CONFIG -----
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b" # changed from llama3:latest for faster local performance
TOP_K = 3  # number of most relevant notes to provide as context

# ----- INIT DB & EMBEDDING MODEL -----
client = PersistentClient(path="./db")
collection = client.get_collection("notes")
EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve_context(question: str, top_k: int = TOP_K) -> str:
    """
    Retrieves the top_k most relevant notes from Chroma based on the question.
    """
    question_embedding = EMBED_MODEL.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    docs = results['documents'][0]
    context = "\n\n".join(docs)
    return context

def ask_model(question: str) -> str:
    """
    Sends the question + retrieved context to the model and returns the answer.
    """
    context = retrieve_context(question)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}"

    print("\n--- MODEL ANSWER ---\n")
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "options": {
                "num_predict": 150 # correct parameter for limiting answer length
            }
        },
        stream=True # stream the response instead of blocking
    )
    response.raise_for_status()

    # Assemble and stream answer from JSON lines
    answer = ""
    for line in response.iter_lines():
        if line:
            try:
                obj = json.loads(line)
                if "response" in obj:
                    chunk = obj["response"]
                    answer += chunk
                    print(chunk, end="", flush=True)
            except json.JSONDecodeError:
                continue

    print("\n")
    return answer

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query your RAG with Llama + Chroma")
    parser.add_argument("mode", choices=["demo", "ask"], help="demo: use test question, ask: provide your question")
    parser.add_argument("question", nargs="?", help="Your custom question (required if mode is 'ask')")
    args = parser.parse_args()

    if args.mode == "demo":
        question = "How do I activate a venv on Mac?"
    elif args.mode == "ask":
        if not args.question:
            print("Error: You must provide a question when using 'ask' mode.")
            exit(1)
        question = args.question

    # we no longer need to print here since we stream inline
    ask_model(question)
