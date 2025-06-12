# utils/file_utils.py
import os
import shutil
from pathlib import Path

def create_output_directories():
    """Create the base output directory if it doesn't exist."""
    # Just create the base output directory
    os.makedirs("output", exist_ok=True)
    return True

def save_extracted_text(text, file_type, library_name, original_filename):
    """
    Save extracted text using the file-based directory structure.
    
    Args:
        text: The extracted text content
        file_type: 'resume' or 'jd'
        library_name: Name of the extraction library used
        original_filename: Original filename without extension
        
    Returns:
        Path to the saved file
    """
    # Create directory for this file if it doesn't exist
    file_dir = f"output/{original_filename}"
    os.makedirs(file_dir, exist_ok=True)
    
    # Create output path with library name as suffix
    output_file = f"{file_dir}/{original_filename}_{library_name}.txt"
    
    # Write text to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return output_file

def get_file_stats(file_path):
    """Get basic file statistics."""
    file_size = os.path.getsize(file_path)
    return {
        'file_size': file_size,
        'file_size_kb': file_size / 1024
    }

def is_valid_file_type(file_path):
    """Check if file is PDF or DOCX."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.pdf', '.docx']

def get_file_type(file_path):
    """Determine if file is PDF or DOCX."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return 'pdf'
    elif ext == '.docx':
        return 'docx'
    return None

def is_file_size_valid(file_path, max_size_mb=2):
    """Check if file size is under the limit."""
    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes <= (max_size_mb * 1024 * 1024)

def get_base_filename(file_path):
    """Get filename without extension."""
    return Path(file_path).stem