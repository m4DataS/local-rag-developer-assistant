import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# ----- CONFIG -----
NOTES_DIR = "./dev_notes"
EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ----- INIT DB -----
client = PersistentClient(path="./db")
collection = client.get_or_create_collection(name="notes")

# ----- LOAD & INGEST FILES -----
for filename in os.listdir(NOTES_DIR):
    if not filename.endswith(".txt"):
        continue

    file_path = os.path.join(NOTES_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    embedding = EMBED_MODEL.encode(text).tolist()

    collection.add(
        ids=[filename],
        embeddings=[embedding],
        documents=[text]
    )

    print(f"Ingested {filename}")

print("✅ Ingestion complete!")
