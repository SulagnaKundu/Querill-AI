
---
title: Querill AI
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---
# ⚡ Querill AI

Querill AI is a high-performance Retrieval-Augmented Generation (RAG) engine designed for fast, grounded, and resilient context processing from complex PDF documents.

---

## 🚀 Quickstart (Local Development)

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your machine.

### 2. Clone the Repository
```bash
git clone [https://github.com/SulagnaKundu/Querill-AI.git](https://github.com/SulagnaKundu/Querill-AI.git)
cd Querill-AI

```

### 3. Set Up Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEYS=key_1,key_2,key_3,key_4,key_5

```

### 6. Run the Application

```bash
uvicorn app:app --reload

```

Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 🏗️ Architecture & RAG Pipeline

1. **PDF Ingestion**: Text chunks extracted and processed with `pypdf`.
2. **Embedding Creation**: Text chunks converted to dense vectors via `sentence-transformers/all-MiniLM-L6-v2`.
3. **Similarity Search**: Queries hit ChromaDB vector store using `k=3` cosine distance matching with expanded context queries.
4. **Context Ingestion**: Matching chunks synthesized by `resilient_ai_call` to produce grounded structured answers.

