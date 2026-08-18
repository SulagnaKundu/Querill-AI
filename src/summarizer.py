from src.ai_engine import resilient_ai_call

def generate_instant_summary(extracted_text):
    prompt = f"Provide a comprehensive executive overview and primary takeaway of this text:\n\n{extracted_text[:5000]}"
    return resilient_ai_call(prompt, "You are an expert executive editor. Provide a clear, structured summary.")