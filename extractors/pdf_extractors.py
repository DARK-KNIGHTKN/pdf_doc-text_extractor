# extractors/pdf_extractors.py
import time
import io

def extract_with_pypdf2(file_path):
    """Extract text from PDF using PyPDF2."""
    from PyPDF2 import PdfReader
    
    start_time = time.time()
    
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
                
        end_time = time.time()
        
        stats = {
            'library': 'PyPDF2',
            'processing_time': end_time - start_time,
            'char_count': len(text),
            'word_count': len(text.split()),
            'line_count': len(text.splitlines()),
            'success': True,
            'error': None
        }
        
        return text, stats
    
    except Exception as e:
        end_time = time.time()
        return "", {
            'library': 'PyPDF2',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

def extract_with_pdfplumber(file_path):
    """Extract text from PDF using pdfplumber."""
    import pdfplumber
    
    start_time = time.time()
    
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
                
        end_time = time.time()
        
        stats = {
            'library': 'pdfplumber',
            'processing_time': end_time - start_time,
            'char_count': len(text),
            'word_count': len(text.split()),
            'line_count': len(text.splitlines()),
            'success': True,
            'error': None
        }
        
        return text, stats
    
    except Exception as e:
        end_time = time.time()
        return "", {
            'library': 'pdfplumber',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

def extract_with_pdfminer(file_path):
    """Extract text from PDF using pdfminer.six."""
    from pdfminer.high_level import extract_text as pdfminer_extract
    
    start_time = time.time()
    
    try:
        text = pdfminer_extract(file_path)
                
        end_time = time.time()
        
        stats = {
            'library': 'pdfminer',
            'processing_time': end_time - start_time,
            'char_count': len(text),
            'word_count': len(text.split()),
            'line_count': len(text.splitlines()),
            'success': True,
            'error': None
        }
        
        return text, stats
    
    except Exception as e:
        end_time = time.time()
        return "", {
            'library': 'pdfminer',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

# def extract_with_textract(file_path):
#     """Extract text from PDF using textract."""
#     import textract
    
#     start_time = time.time()
    
#     try:
#         text = textract.process(file_path, method='pdfminer').decode('utf-8')
                
#         end_time = time.time()
        
#         stats = {
#             'library': 'textract',
#             'processing_time': end_time - start_time,
#             'char_count': len(text),
#             'word_count': len(text.split()),
#             'line_count': len(text.splitlines()),
#             'success': True,
#             'error': None
#         }
        
#         return text, stats
    
#     except Exception as e:
#         end_time = time.time()
#         return "", {
#             'library': 'textract',
#             'processing_time': end_time - start_time,
#             'char_count': 0,
#             'word_count': 0,
#             'line_count': 0,
#             'success': False,
#             'error': str(e)
#         }

# Dictionary mapping library names to their extraction functions
PDF_EXTRACTORS = {
    'PyPDF2': extract_with_pypdf2,
    'pdfplumber': extract_with_pdfplumber,
    'pdfminer': extract_with_pdfminer,
    #'textract': extract_with_textract
}