# script1_ingest_index.py

import os
import nest_asyncio
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.gemini import Gemini
from gitingest import ingest # Assuming gitingest is installed and importable

# --- Configuration ---
# IMPORTANT: Replace with your actual Google API Key
GOOGLE_API_KEY = "YOUR_ACTUAL_GOOGLE_API_KEY_HERE"
# The GitHub repository you want to index
REPO_URL = "https://github.com/crewAIInc/crewAI" # Example: crewAI repo (CHANGE THIS!)
# Directory to save the generated index
PERSIST_DIR = "./index_store"
# Temporary file to store fetched repo data
DATA_FILE = "repo_data.txt"
# Embedding model to use
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
# LLM model to use (ensure compatibility with your API key)
LLM_MODEL_NAME = "models/gemini-1.5-flash-8b" # Or other compatible Gemini model

# --- Helper Function to Save Data ---
def save_string_to_txt(content: str, filename: str):
    """Saves the given string content to a text file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Successfully saved repository data to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")
        raise

# --- Main Ingestion and Indexing Logic ---
def main():
    print("Starting ingestion and indexing process...")

    # 1. Validate Google API Key
    if GOOGLE_API_KEY == "YOUR_ACTUAL_GOOGLE_API_KEY_HERE" or not GOOGLE_API_KEY:
        raise ValueError(
            "Please replace 'YOUR_ACTUAL_GOOGLE_API_KEY_HERE' with your "
            "actual Google API Key obtained from https://aistudio.google.com/app/apikey"
        )
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print("Google API Key configured.")

    # 2. Apply nest_asyncio
    nest_asyncio.apply()

    # 3. Configure LlamaIndex Settings
    print(f"Configuring embedding model: {EMBEDDING_MODEL_NAME}")
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)
    print(f"Configuring LLM: {LLM_MODEL_NAME}")
    Settings.llm = Gemini(model=LLM_MODEL_NAME)
    print("LlamaIndex Settings configured.")

    # 4. Fetch Data from GitHub Repository
    print(f"Fetching data from repository: {REPO_URL}")
    try:
        _summary, _tree, repo_content = ingest(REPO_URL)
        if not repo_content:
            print("Warning: No content fetched from the repository.")
            return
        print(f"Successfully fetched content (length: {len(repo_content)} characters).")
    except Exception as e:
        print(f"Error fetching repository data using gitingest: {e}")
        return

    # 5. Save Fetched Data Temporarily
    save_string_to_txt(repo_content, DATA_FILE)

    # 6. Load Data using SimpleDirectoryReader
    print(f"Loading data from temporary file: {DATA_FILE}")
    try:
        documents = SimpleDirectoryReader(input_files=[DATA_FILE]).load_data()
        if not documents:
            print("Error: No documents were loaded.")
            return
        print(f"Successfully loaded {len(documents)} document chunk(s).")
    except Exception as e:
        print(f"Error loading data with SimpleDirectoryReader: {e}")
        return

    # 7. Create Vector Store Index
    print("Creating vector store index... (This may take a while)")
    try:
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        print("Index creation complete.")
    except Exception as e:
        print(f"Error creating vector store index: {e}")
        return

    # 8. Persist Index to Disk
    print(f"Persisting index to directory: {PERSIST_DIR}")
    try:
        if not os.path.exists(PERSIST_DIR): os.makedirs(PERSIST_DIR)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print(f"Index successfully persisted to {PERSIST_DIR}")
    except Exception as e:
        print(f"Error persisting index: {e}")

    # 9. Clean up temporary file
    try:
        os.remove(DATA_FILE)
        print(f"Removed temporary data file: {DATA_FILE}")
    except OSError as e:
        print(f"Error removing temporary file {DATA_FILE}: {e}")

    print("\nScript 1 finished: Ingestion and Indexing complete.")
    print(f"You can now run Script 2 to query the index stored in '{PERSIST_DIR}'.")

if __name__ == "__main__":
    main()
