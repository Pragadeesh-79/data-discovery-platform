from pdfminer.high_level import extract_text

def parse_pdf(file_path: str) -> str:
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""
