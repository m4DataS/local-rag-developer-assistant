import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# ----- CONFIG -----
NOTES_DIR = "./dev_notes"
EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ----- INIT DB -----
client = PersistentClient(path="./db")
collection = client.get_or_create_collection(name="notes")

# ----- EVENT HANDLER -----
class NotesHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".txt"):
            return
        self.ingest_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".txt"):
            return
        self.ingest_file(event.src_path)

    def ingest_file(self, file_path):
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        embedding = EMBED_MODEL.encode(text).tolist()

        # Remove old entry if exists
        if filename in collection.get()["ids"]:
            collection.delete(ids=[filename])

        # Add new/updated note
        collection.add(
            ids=[filename],
            embeddings=[embedding],
            documents=[text]
        )
        print(f"✅ Ingested {filename}")

# ----- START WATCHER -----
if __name__ == "__main__":
    event_handler = NotesHandler()
    observer = Observer()
    observer.schedule(event_handler, NOTES_DIR, recursive=False)
    observer.start()
    print(f"Watching folder {NOTES_DIR} for new or updated notes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
