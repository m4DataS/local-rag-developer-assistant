from chromadb import PersistentClient

client = PersistentClient(path="./db")
collection = client.get_collection("notes")

# List all document IDs
print(collection.get()["ids"])
