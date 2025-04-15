# AskTheRepo: Explore the Code with AI 🤖

Navigate and understand complex GitHub repositories by simply asking questions! AskTheRepo allows you to turn any public GitHub repository into a conversational AI assistant.

This project uses a two-step process:
1.  **Ingest & Index:** Fetches repository content and builds a searchable vector index (run once per repo).
2.  **Query:** Loads the index and lets you ask questions about the code, documentation, and structure using an AI assistant powered by Google Gemini.

## 🌟 Features

*   **Conversational Interface:** Ask questions about repository content in natural language.
*   **Deep Code Understanding:** Leverages AI to analyze code, documentation, dependencies, and more.
*   **Efficient:** Ingests and indexes repositories once, allowing for fast querying afterwards.
*   **Customizable:** Easily point it to different public GitHub repositories.
*   **Powered by Leading AI:** Utilizes LlamaIndex, Google Gemini, and Hugging Face embeddings.

## 🛠️ Technology Stack

*   **Python** (3.8+)
*   **LlamaIndex:** Core framework for data indexing and retrieval.
*   **Google Gemini:** Large Language Model for understanding and generation.
*   **Hugging Face Sentence Transformers:** For generating text embeddings (`BAAI/bge-small-en-v1.5`).
*   **gitingest:** Utility to fetch content from GitHub repositories.
*   **nest_asyncio:** For compatibility in certain environments.

## 🚀 Getting Started

Follow these steps to set up and run AskTheRepo.

### Prerequisites

1.  **Python:** Ensure you have Python 3.8 or newer installed. Check with `python --version` or `python3 --version`.
2.  **Pip:** Python's package installer (usually comes with Python).
3.  **Git:** Required to clone this repository.
4.  **Internet Connection:** Needed for installing packages, downloading models, fetching repo data, and using the Google Gemini API.
5.  **Google API Key:** You **MUST** obtain an API key for Google Gemini from [Google AI Studio](https://aistudio.google.com/app/apikey). Follow the instructions there. Keep this key secure!

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/AskTheRepo.git # Replace YOUR_USERNAME
    cd AskTheRepo
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # Create the environment
    python -m venv venv
    # Activate it (example for Linux/macOS)
    source venv/bin/activate
    # On Windows, use: .\venv\Scripts\activate
    ```

3.  **Install Required Libraries:**
    ```bash
    pip install llama-index gitingest nest_asyncio llama-index-llms-gemini llama-index-embeddings-huggingface
    ```

## ⚙️ Usage

AskTheRepo uses two main scripts. Run them in sequence.

### Step 1: Ingest and Index the Repository (`script1_ingest_index.py`)

This script fetches the target repository's content, processes it, and saves a local vector index. **Run this script once for each repository you want to analyze.**

1.  **Configure Script 1:**
    *   Open `script1_ingest_index.py` in a text editor.
    *   **Replace `"YOUR_ACTUAL_GOOGLE_API_KEY_HERE"`** with your actual Google API Key.
    *   **Change the `REPO_URL`** variable to the URL of the public GitHub repository you want to index (e.g., `"https://github.com/facebook/react"`).
    *   (Optional) Modify `PERSIST_DIR` if you want to save the index in a different location.

2.  **Run the Ingestion Script:**
    *   Make sure your virtual environment is activated.
    *   Run the script from your terminal:
    ```bash
    python script1_ingest_index.py
    ```
    *   This may take some time, especially for large repositories or on the first run (model download).
    *   Upon success, a directory named `index_store` (or your custom `PERSIST_DIR`) will be created containing the index files.

### Step 2: Query the AI Assistant (`script2_query_assistant.py`)

This script loads the previously generated index and starts the interactive chat session. **Run this script whenever you want to ask questions about the indexed repository.**

1.  **Configure Script 2:**
    *   Open `script2_query_assistant.py`.
    *   **Replace `"YOUR_ACTUAL_GOOGLE_API_KEY_HERE"`** with your Google API Key (must be the same key used in Script 1).
    *   **Ensure** that `PERSIST_DIR`, `EMBEDDING_MODEL_NAME`, and `LLM_MODEL_NAME` **match the settings used in `script1_ingest_index.py`**.

2.  **Run the Query Script:**
    *   Make sure your virtual environment is activated.
    *   Run the script:
    ```bash
    python script2_query_assistant.py
    ```
    *   The script will load the index. Once ready, you'll see the prompt:
    ```
    --- GitHub Repo Assistant Ready ---
    Ask questions about the content indexed from ./index_store.
    Type 'quit' or 'exit' to stop.

    Your Question:
    ```
    *   Type your questions about the repository and press Enter.
    *   The AI will provide answers based on the indexed content.
    *   Type `quit` or `exit` to end the session.

## 🤔 How It Works

1.  **Ingestion (Script 1):** `gitingest` fetches code and text from the target GitHub repository.
2.  **Embedding (Script 1):** Text chunks are converted into numerical vectors using the `BAAI/bge-small-en-v1.5` model.
3.  **Indexing (Script 1):** LlamaIndex stores these vectors efficiently in a `VectorStoreIndex`.
4.  **Persistence (Script 1):** The index is saved locally to the `PERSIST_DIR`.
5.  **Loading (Script 2):** The saved index is loaded from disk for querying.
6.  **Querying (Script 2):** Your question is embedded, and LlamaIndex finds the most relevant context chunks from the index using vector similarity search.
7.  **Response Generation (Script 2):** The retrieved context and your question are sent to the Google Gemini LLM via a custom prompt to generate a coherent answer.

## 🔧 Configuration Details

Key configuration variables are located at the top of each script:

*   `GOOGLE_API_KEY`: Your API key for Google AI Studio (Gemini). **Required in both scripts.**
*   `REPO_URL`: The target GitHub repository URL. **Required in Script 1.**
*   `PERSIST_DIR`: The directory to save/load the index. **Must match between scripts.**
*   `EMBEDDING_MODEL_NAME`: The Hugging Face model for embeddings. **Must match between scripts.**
*   `LLM_MODEL_NAME`: The Google Gemini model identifier. **Must match between scripts.**

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements or bug fixes.

## 📜 License

*(Optional: Choose and add a license. MIT is common for open source.)*

Example: This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
