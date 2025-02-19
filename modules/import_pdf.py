import PyPDF2

def extract_text(pdf_path):
    """
    Extracts text from a PDF file.
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text from the PDF file.
    """
    text = ""
    
    print(f"Extracting text from PDF file: {pdf_path}")
    try:
        # Open the PDF file in binary mode
        with open(pdf_path, "rb") as file:
            # Create a PdfReader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Iterate through all the pages and extract text
            for page_number, page in enumerate(pdf_reader.pages, start=1):
                page_text = page.extract_text()
                text += page_text
        return text
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
