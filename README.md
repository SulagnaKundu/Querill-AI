# ⚡ Querill AI — Intelligent Document Analytics & RAG Engine

Querill AI is an end-to-end Retrieval-Augmented Generation (RAG) platform designed to ingest complex PDF documents, extract high-yield insights, and support context-aware semantic search. Built with FastAPI, LangChain, Chromadb, and multi-provider AI fallback infrastructure.

---

## ✨ Key Features

* **📄 Document Ingestion & Parsing**: Extracts, cleans, and analyzes text from multi-page PDFs using `PyPDF`.
* **🧠 Dynamic RAG Engine**: Generates vector embeddings with `sentence-transformers` and performs fast vector search using `ChromaDB`.
* **📊 Visual Mind Map Engine**: Converts unstructured document flows into structured JSON visual flowcharts.
* **🎴 Automated Study Kit**: Automatically generates interactive flashcards and practice Q&A pairs for active recall.
* **🔄 Resilient AI Provider Fallback**: Automatic key-rotation and dynamic provider switching across Google Gemini and Groq API chains to prevent rate limits and downtime.
* **🎨 Modern Responsive UI**: Single-page application built with HTMX and Tailwind CSS featuring asynchronous tabbed navigation and live loading spinners.

---

## 🛠️ Tech Stack

* **Backend Framework**: FastAPI (Python 3.10+)
* **RAG & Vector Database**: LangChain, ChromaDB, HuggingFace Sentence Transformers
* **AI Providers**: Google GenAI (`gemini-2.0-flash`), Groq (`llama-3.1-8b-instant`)
* **Frontend**: HTMX, Tailwind CSS, Jinja2 Templates, Markdown2
* **Web Server**: Uvicorn

---

## 🚀 Quickstart (Local Development)

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/SulagnaKundu/Querill-AI.git
cd Querill-AI

 3. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

4. Install Dependencies
```bash
pip install -r requirements.txt

5. Configure Environment Variables
Create a .env file in the root directory:
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEYS=key_1,key_2,key_3,key_4,key_5

6. Run the Application
```bash
uvicorn app:app --reload


🏗️ Architecture & RAG Pipeline
PDF Ingestion: Text chunks extracted and processed with pypdf.

Embedding Creation: Text chunks converted to dense vectors via sentence-transformers/all-MiniLM-L6-v2.

Similarity Search: Queries hit ChromaDB vector store using k=3 cosine distance matching with expanded context queries.

Context Ingestion: Matching chunks synthesized by resilient_ai_call to produce grounded structured answers.



