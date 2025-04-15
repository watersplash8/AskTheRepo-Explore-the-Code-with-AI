# script2_query_assistant.py

import os
import nest_asyncio
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms.gemini import Gemini
from llama_index.core.prompts import PromptTemplate

# --- Configuration ---
# IMPORTANT: Replace with your actual Google API Key
GOOGLE_API_KEY = "YOUR_ACTUAL_GOOGLE_API_KEY_HERE"
# Directory where the index was saved by Script 1
PERSIST_DIR = "./index_store"
# Embedding model used during indexing (MUST MATCH SCRIPT 1)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
# LLM model used during indexing (MUST MATCH SCRIPT 1)
LLM_MODEL_NAME = "models/gemini-1.5-flash-8b" # Or other compatible Gemini model

# --- Custom Prompt Template ---
QA_PROMPT_TMPL_STR = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query in a step-by-step manner.\n"
    "Include code snippets when relevant. If you don't know the "
    "answer based on the context, say 'Based on the provided context, I don't know!'.\n"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt_tmpl = PromptTemplate(QA_PROMPT_TMPL_STR)

# --- Main Querying Logic ---
def main():
    print("Starting Query Assistant...")

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

    # 3. Configure LlamaIndex Settings (MUST MATCH SCRIPT 1)
    print(f"Configuring embedding model: {EMBEDDING_MODEL_NAME}")
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)
    print(f"Configuring LLM: {LLM_MODEL_NAME}")
    Settings.llm = Gemini(model=LLM_MODEL_NAME)
    print("LlamaIndex Settings configured.")

    # 4. Check if the Index Directory Exists
    if not os.path.exists(PERSIST_DIR):
        print(f"Error: Index directory '{PERSIST_DIR}' not found.")
        print("Please run Script 1 first to create and persist the index.")
        return

    # 5. Load the Index from Disk
    print(f"Loading index from directory: {PERSIST_DIR}")
    try:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print("Index loaded successfully.")
    except Exception as e:
        print(f"Error loading index from storage: {e}")
        return

    # 6. Create Query Engine
    print("Creating query engine...")
    query_engine = index.as_query_engine()
    print("Query engine created.")

    # 7. Update Query Engine with Custom Prompt
    print("Applying custom prompt template...")
    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
    )
    print("Custom prompt applied.")

    # 8. Start Query Loop
    print("\n--- GitHub Repo Assistant Ready ---")
    print(f"Ask questions about the content indexed from {PERSIST_DIR}.")
    print("Type 'quit' or 'exit' to stop.")

    while True:
        user_query = input("\nYour Question: ")
        if user_query.lower() in ['quit', 'exit']:
            print("Exiting assistant.")
            break
        if not user_query.strip():
            print("Please enter a question.")
            continue

        print("Processing your query...")
        try:
            response = query_engine.query(user_query)
            print("\nAI Assistant Response:")
            print("----------------------")
            print(str(response)) # Using str() for safe printing
            print("----------------------")
        except Exception as e:
            print(f"\nAn error occurred during querying: {e}")
            print("Please try again or check the configuration/API key.")

if __name__ == "__main__":
    main()
