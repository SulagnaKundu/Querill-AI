import pypdf

def extract_pdf_text(file_obj):
    reader = pypdf.PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text