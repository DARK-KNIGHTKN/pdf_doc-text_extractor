# extractors/docx_extractors.py
import time
import io

def extract_with_docx2txt(file_path):
    """Extract text from DOCX using docx2txt."""
    import docx2txt
    
    start_time = time.time()
    
    try:
        text = docx2txt.process(file_path)
                
        end_time = time.time()
        
        stats = {
            'library': 'docx2txt',
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
            'library': 'docx2txt',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

def extract_with_python_docx(file_path):
    """Extract text from DOCX using python-docx."""
    import docx
    
    start_time = time.time()
    
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
        end_time = time.time()
        
        stats = {
            'library': 'python_docx',
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
            'library': 'python_docx',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

# def extract_with_textract(file_path):
#     """Extract text from DOCX using textract."""
#     import textract
    
#     start_time = time.time()
    
#     try:
#         text = textract.process(file_path).decode('utf-8')
                
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
    
    except Exception as e:
        end_time = time.time()
        return "", {
            'library': 'textract',
            'processing_time': end_time - start_time,
            'char_count': 0,
            'word_count': 0,
            'line_count': 0,
            'success': False,
            'error': str(e)
        }

# Dictionary mapping library names to their extraction functions
DOCX_EXTRACTORS = {
    'docx2txt': extract_with_docx2txt,
    'python_docx': extract_with_python_docx,
    #'textract': extract_with_textract
}