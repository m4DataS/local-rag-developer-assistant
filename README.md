# local-rag-developer-assistant (Local Document RAG [Llama 3.2 + ChromaDB])

A completely local, private Retrieval-Augmented Generation (RAG) system running on macOS. This system ingests personal text notes, embeds them into a vector database (ChromaDB), and answers questions against them using Ollama's `llama3.2:3b` model.

## Prerequisites

1. **[Ollama](https://ollama.com/)**: Installed and running locally.
2. **Model**: Pull the Llama 3.2 3B model via terminal:

   ```bash
   ollama pull llama3.2:3b
   ```

3. **Python 3.9+**

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd perso_data-eng_RAG
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv rag_env
source rag_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your Notes Directory

Create the folder where your personal `.txt` notes will live:

```bash
mkdir dev_notes
```

*(Place any initial `.txt` files containing your notes into this folder.)*

---

## 🚀 Usage Guide

This project consists of two distinct components: the Data Ingestion pipeline and the LLM Chat interface.

### Step 1: Initial Data Ingestion

Run the ingestion script to parse all `.txt` files in `dev_notes/` and embed them into the local ChromaDB database:

```bash
python ingestion_script.py
```

*Note: This will automatically create a `db/` folder in your project directory containing the vector embeddings. This folder is ignored in version control to protect your data.*

*(Optional)* You can verify that your notes were successfully embedded by running:

```bash
python ingestion_checker.py
```

### Step 2: Querying the LLM

Once the database is populated, you can ask questions! The script will retrieve the top 3 most relevant notes and stream the AI's answer in real-time.

```bash
python model_connection_v2.py ask "Your custom question here"
```

*Example:* `python model_connection_v2.py ask "How do I configure git redirection?"`

### Step 3: Real-time Notes Syncing (Background Watcher)

If you are actively taking notes and want the RAG system to update automatically when you save a `.txt` file, run the watcher script in a separate terminal:

```bash
# Keep this running in the background while you work
python ingestion_watcher.py
```

## Useful Debugging Scripts

- `query_simple.py`: A barebones test script to search the ChromaDB vector store directly, completely bypassing the LLM. Useful for testing if the embedding model is finding the correct notes.


## 🔮 Future Improvements

- **User Interface**: Add a web UI using [Streamlit](https://streamlit.io/) for a more interactive and user-friendly experience.
- **Improved Resilience**: Refactor the backend to use [LangChain](https://www.langchain.com/) for more robust pipeline management, memory, and advanced RAG retrieval strategies.
- **Model Experimentation**: Evaluate the DeepSeek model family, which are known to be lighter in token processing to further speed up local inference.
- **Deployment & Cloud Proficiency**:
  - Deploy the RAG on a private server accessible from the local network.
  - Deploy the RAG on various cloud platforms to compare their offerings and improve cloud proficiency (e.g., Databricks, Azure, GCP).