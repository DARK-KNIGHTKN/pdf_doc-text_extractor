📄 Document Text Extractor Tester 
Python Platform License Status

A Python application with a graphical interface for testing and comparing different text extraction libraries for PDF and DOCX files.

  _____                                       _     ______      _                  _             
 |  __ \                                     | |   |  ____|    | |                | |            
 | |  | | ___   ___ _   _ _ __ ___   ___ _ __ | |_  | |__  _  _| |_ _ __ __ _  ___| |_ ___  _ __ 
 | |  | |/ _ \ / __| | | | '_ ` _ \ / _ \ '_ \| __| |  __|| |/ / __| '__/ _` |/ __| __/ _ \| '__|
 | |__| | (_) | (__| |_| | | | | | |  __/ | | | |_  | |___| <| |_| | | (_| | (__| || (_) | |   
 |_____/ \___/ \___|\__,_|_| |_| |_|\___|_| |_|\__| |______\_/\___|_|  \__,_|\___|\__\___/|_|   
                                                                                                
📋 Table of Contents
✨ Features 
📚 Supported Libraries 
🛠️ Installation 
🚀 Usage 
📏 File Size Limitations 
📁 Directory Structure 
📊 Comparing Library Performance 
📦 Requirements 
❓ Troubleshooting 
✨ Features
📤 Upload and process both resume and job description files
📑 Support for PDF and DOCX file formats
🧪 Test multiple extraction libraries side-by-side
📊 Compare extraction statistics (character count, word count, processing time)
⚠️ View detailed error messages when extraction fails
💾 Save extracted text to files for further analysis
🖱️ User-friendly interface with step-by-step workflow
📚 Supported Libraries
File Type	Library	Description
📄 PDF	PyPDF2	Fast, pure-Python PDF library
📄 PDF	pdfplumber	Good for extracting tables and structured content
📄 PDF	pdfminer.six	Detailed text extraction with layout analysis
📝 DOCX	docx2txt	Simple and fast DOCX conversion
📝 DOCX	python-docx	Full-featured DOCX parsing library
💡 Tip: Different libraries excel at different types of documents. Try multiple libraries for best results!

🛠️ Installation
Prerequisites
Python 3.7 or higher
<details> <summary>📋 Detailed Installation Steps</summary>
Clone this repository or download the source code

git clone <repository-url>
cd pdf_docx_extractor_test
Create a virtual environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

pip install -r requirements.txt
</details>
🚀 Usage
Run the application
python app.py
<details> <summary>🔍 Step-by-step Workflow</summary>
File Selection Screen:

Click "Browse..." to upload a resume file (PDF or DOCX)
Click "Browse..." to upload a job description file (PDF or DOCX)
Click "Next" to continue
Library Selection Screen:

Select which libraries to use for extracting text
Different options will appear based on your file types
Click "Process Files" to start extraction
Results Screen:

View statistics for each extraction (character count, word count, time)
Select a row to see detailed error information (if applicable)
Find extracted text files in the output directory
Click "Clear & Start Over" to process new files
</details>
⚠️ Note: Some libraries may take longer to process complex documents with many pages or images.

📏 File Size Limitations
The application limits each file to a maximum of 2MB to ensure good performance.

📌 Note: This limit can be adjusted in the code if needed for larger files.

📁 Directory Structure
pdf_docx_extractor_test/
├── app.py                 # Main application file
├── extractors/            # Text extraction modules
│   ├── __init__.py
│   ├── pdf_extractors.py  # PDF extraction functions
│   └── docx_extractors.py # DOCX extraction functions
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── file_utils.py      # File handling utilities
├── output/                # Output directory
│   ├── [filename1]/       # Folder for each processed file
│   │   ├── filename1_PyPDF2.txt
│   │   ├── filename1_pdfplumber.txt
│   │   └── ...
│   └── [filename2]/
│       ├── filename2_PyPDF2.txt
│       └── ...
└── requirements.txt       # Dependencies
📊 Comparing Library Performance
When evaluating which library works best, consider:

<details> <summary>📈 Performance Metrics</summary>
Character Count: Higher counts may indicate better extraction
Processing Time: Faster is better, especially for large documents
Quality of Extraction: Check the output files to see which library:
Better preserves formatting
Correctly handles tables and special characters
Properly processes complex layouts
</details>
💡 Tip: For resumes with complex formatting, pdfplumber often provides better results than PyPDF2.

📦 Requirements
<details> <summary>View Dependencies</summary>
PyPDF2>=3.0.0
pdfplumber>=0.7.0
pdfminer.six>=20221105
python-docx>=0.8.11
docx2txt>=0.8
</details>
❓ Troubleshooting
<details> <summary>Common Issues and Solutions</summary>
"CropBox missing from /Page" warnings: These are normal PyPDF2 messages and can be safely ignored
Import errors: Ensure all packages are correctly installed in your virtual environment
Empty extraction results: Some PDF protection methods can prevent text extraction
Slow processing: Large or complex documents may take longer to process
</details>
⚠️ Warning: Some highly-formatted or scanned documents may not extract well with any library.

This tool was created to test and compare text extraction capabilities for resume and job description processing.