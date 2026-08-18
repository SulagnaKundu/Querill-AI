import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

def resilient_ai_call(prompt: str, system_prompt: str = "") -> str:
    errors = []
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # Extract Groq keys (supports comma-separated list GROQ_API_KEYS or single GROQ_API_KEY)
    groq_keys_str = os.getenv("GROQ_API_KEYS") or os.getenv("GROQ_API_KEY") or ""
    groq_keys = [k.strip() for k in groq_keys_str.split(",") if k.strip()]

    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

    # 1. Try Gemini Provider First
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            
            # Fetch active models dynamically from Google API
            gemini_candidates = []
            try:
                available = [m.name for m in client.models.list()]
                gemini_candidates = [m.replace("models/", "") for m in available if "flash" in m or "pro" in m]
            except Exception:
                pass

            # Ensure default active models are included in the fallback chain
            defaults = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.0-pro-exp-02-05"]
            for d in defaults:
                if d not in gemini_candidates:
                    gemini_candidates.append(d)

            for model_name in gemini_candidates:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=full_prompt,
                    )
                    if response.text:
                        return response.text
                except Exception as ex:
                    errors.append(f"[gemini:{model_name}] -> {ex}")
        except Exception as ex:
            errors.append(f"[gemini_init] -> {ex}")

    # 2. Try Groq Provider Keys
    if groq_keys:
        try:
            from groq import Groq
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            for idx, key in enumerate(groq_keys):
                try:
                    client = Groq(api_key=key)
                    
                    # Fetch active models dynamically from Groq API
                    groq_candidates = []
                    try:
                        available_groq = [m.id for m in client.models.list().data]
                        groq_candidates = [m for m in available_groq if "llama" in m or "mixtral" in m]
                    except Exception:
                        pass

                    defaults_groq = ["llama-3.1-8b-instant", "llama3-70b-8192", "mixtral-8x7b-32768"]
                    for d in defaults_groq:
                        if d not in groq_candidates:
                            groq_candidates.append(d)

                    for model_name in groq_candidates:
                        try:
                            response = client.chat.completions.create(
                                model=model_name,
                                messages=messages,
                                temperature=0.3,
                            )
                            if response.choices and response.choices[0].message.content:
                                return response.choices[0].message.content
                        except Exception as ex:
                            errors.append(f"[groq_key_{idx+1}:{model_name}] -> {ex}")
                except Exception as ex:
                    errors.append(f"[groq_key_{idx+1}_init] -> {ex}")
        except Exception as ex:
            errors.append(f"[groq_import] -> {ex}")

    raise Exception(f"All AI providers and keys failed. Details: {errors}")


def generate_mindmap(extracted_text: str) -> dict:
    prompt = f"Analyze this text and output a JSON object with 'topic' and a list of 'branches' (with 'step' and 'details'):\n\n{extracted_text[:4000]}"
    res = resilient_ai_call(prompt, "You are a JSON visual graph builder. Respond ONLY in valid JSON.")
    try:
        clean_res = res.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_res)
    except Exception:
        return {"topic": "Document Overview", "branches": [{"step": "Key Details", "details": res[:300]}]}


def generate_study_materials(extracted_text: str, num_cards: int = 5, num_qs: int = 5) -> dict:
    prompt = f"Generate {num_cards} flashcards ('front', 'back') and {num_qs} QA pairs ('question', 'answer') in JSON format:\n\n{extracted_text[:4000]}"
    res = resilient_ai_call(prompt, "You are an educational designer. Respond ONLY in valid JSON.")
    try:
        clean_res = res.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_res)
    except Exception:
        return {"flashcards": [], "qa_pairs": []}


def answer_custom_question(query: str, vector_db) -> str:
    if not vector_db:
        return "Vector database is not initialized. Please upload a document first."

    docs_direct = vector_db.similarity_search(query, k=3)
    docs_expanded = vector_db.similarity_search(f"key context regarding {query}", k=3)

    seen = set()
    combined_chunks = []
    for doc in docs_direct + docs_expanded:
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        if content not in seen:
            seen.add(content)
            combined_chunks.append(content)

    context = "\n\n---\n\n".join(combined_chunks)

    system_prompt = (
        "You are an expert document analyst. Answer questions based strictly on the provided context.\n"
        "Structure your response clearly:\n"
        "• Direct Answer: Concise summary\n"
        "• Key Evidence: Exact context facts\n"
        "• Analytical Insights: Key takeaways"
    )
    prompt = f"Context:\n{context}\n\nQuestion: {query}"

    return resilient_ai_call(prompt, system_prompt)