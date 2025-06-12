# extractors/__init__.py
from .pdf_extractors import PDF_EXTRACTORS
from .docx_extractors import DOCX_EXTRACTORS

def get_available_extractors(file_type):
    """Get dictionary of available extractors for the given file type."""
    if file_type == 'pdf':
        return PDF_EXTRACTORS
    elif file_type == 'docx':
        return DOCX_EXTRACTORS
    return {}