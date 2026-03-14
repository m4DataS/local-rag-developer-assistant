from chromadb import PersistentClient

# 1️⃣ Connect to your ChromaDB
client = PersistentClient(path="./db")

# 2️⃣ Get your collection
collection = client.get_collection("notes")

# 3️⃣ Define your query
query = "How do I use venv in Python?"

# 4️⃣ Retrieve top 3 relevant documents
results = collection.query(
    query_texts=[query],
    n_results=3
)

# 5️⃣ Print retrieved documents
for i, doc in enumerate(results["documents"][0]):
    print(f"\n--- Document {i+1} ---\n")
    print(doc)
