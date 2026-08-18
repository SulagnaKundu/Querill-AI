import os
import shutil
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import markdown2

from src.pdf_processor import extract_pdf_text
from src.summarizer import generate_instant_summary
from src.ai_engine import generate_mindmap, generate_study_materials, answer_custom_question
from src.vector_store import build_vector_store

load_dotenv()

app = FastAPI(title="Querill AI")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

state = {"pdf_text": None, "vector_db": None, "study_kit": None}

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/process", response_class=HTMLResponse)
async def process_pdf(
    request: Request,
    file: UploadFile = File(...),
    flashcards: int = Form(5),
    questions: int = Form(5)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    file.file.seek(0)
    extracted_text = extract_pdf_text(file.file)
    state["pdf_text"] = extracted_text

    state["vector_db"] = build_vector_store(tmp_path)
    raw_summary = generate_instant_summary(extracted_text)
    
    # Converting raw markdown into clean HTML tags
    formatted_summary = markdown2.markdown(raw_summary)

    mindmap = generate_mindmap(extracted_text)
    study_kit = generate_study_materials(extracted_text, flashcards, questions)
    state["study_kit"] = study_kit

    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    word_count = len(extracted_text.split())

    return templates.TemplateResponse(
        request=request,
        name="partials/workspace.html",
        context={
            "summary": formatted_summary,
            "mindmap": mindmap,
            "study_kit": study_kit,
            "word_count": word_count
        }
    )

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, query: str = Form(...)):
    if not state["vector_db"]:
        return "<div class='p-4 text-red-400 bg-red-950/30 border border-red-800/50 rounded-xl text-sm'>Please upload a document first.</div>"

    raw_answer = answer_custom_question(query, state["vector_db"])
    formatted_answer = markdown2.markdown(raw_answer)

    return f"""
    <div class="p-6 bg-slate-900 border border-slate-800 rounded-2xl text-slate-200 mt-4 leading-relaxed space-y-3 shadow-lg transition-all animate-fadeIn">
        <div class="flex items-center gap-2 text-sky-400 font-bold text-sm tracking-wide border-b border-slate-800 pb-2">
            <span>💡</span> <span>Reasoning Engine Answer:</span>
        </div>
        <div class="prose prose-invert max-w-none text-sm text-slate-300 leading-relaxed space-y-2">
            {formatted_answer}
        </div>
    </div>
    """