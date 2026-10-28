from src.vector_store import build_vector_store

def evaluate_retrieval(pdf_path, test_cases):
    vector_db = build_vector_store(pdf_path)
    correct_hits = 0
    
    for question, expected_keyword in test_cases:
        docs = vector_db.similarity_search(question, k=3)
        combined_text = " ".join([doc.page_content.lower() for doc in docs])
        
        if expected_keyword.lower() in combined_text:
            correct_hits += 1
            print(f"✅ PASS: '{question}' found keyword '{expected_keyword}'")
        else:
            print(f"❌ FAIL: '{question}' missed keyword '{expected_keyword}'")
            
    precision = (correct_hits / len(test_cases)) * 100
    print(f"\nFinal Retrieval Precision: {precision}%")

if __name__ == "__main__":
    # Replace with an actual PDF in your folder and keywords inside it
    sample_pdf = "the_last_leaf_o_henry.pdf" 
    tests = [
        ("Who painted the last leaf?", "behrman"),
        ("who was sick?", "johnsy"),
        ("what was johnsy suffering from?", "pneumonia"),
        ("what was the last leaf?", "behrman"),
        ("What did Johnsy believe would happen when the last leaf fell?", "die"),
        ("Who painted the fake leaf on the wall during the storm?","behrman"),
        ("What did the doctor say Johnsy needed in order to recover?", "will (or will to live)"),
        ("What did Behrman consider to be his masterpiece?","masterpiece (referring to the painted leaf)")
    ]
    evaluate_retrieval(sample_pdf, tests)