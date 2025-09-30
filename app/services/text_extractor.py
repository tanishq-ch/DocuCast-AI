import fitz  # PyMuPDF

def extract_text_from_file(filepath):
    """
    Extracts raw text from a given file (PDF or TXT).

    Args:
        filepath (str): The full path to the file.

    Returns:
        str: The extracted text content, or an empty string if extraction fails.
    """
    try:
        if filepath.lower().endswith('.pdf'):
            with fitz.open(filepath) as doc:
                text = "".join(page.get_text() for page in doc)
            return text
        elif filepath.lower().endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            return text
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""