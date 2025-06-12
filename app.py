# app.py
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import time
import traceback

from extractors import get_available_extractors
from utils.file_utils import (
    create_output_directories,
    save_extracted_text,
    get_file_stats,
    is_valid_file_type,
    get_file_type,
    is_file_size_valid,
    get_base_filename
)

class DocumentExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Text Extractor Tester")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Create output directories
        create_output_directories()
        
        # Initialize file paths
        self.resume_path = None
        self.jd_path = None
        
        # Initialize file types
        self.resume_type = None
        self.jd_type = None
        
        # Selected extractors
        self.selected_resume_extractors = {}
        self.selected_jd_extractors = {}
        
        # Results
        self.results = []
        
        # Build UI
        self.build_ui()
        
    def build_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection section
        self.create_file_selection_section()
        
        # Library selection section (initially hidden)
        self.create_library_selection_section()
        
        # Results section (initially hidden)
        self.create_results_section()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_file_selection_section(self):
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Resume file selection
        resume_frame = ttk.Frame(file_frame)
        resume_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(resume_frame, text="Resume File:").pack(side=tk.LEFT, padx=5)
        self.resume_path_var = tk.StringVar()
        ttk.Entry(resume_frame, textvariable=self.resume_path_var, width=50, state="readonly").pack(side=tk.LEFT, padx=5)
        ttk.Button(resume_frame, text="Browse...", command=self.browse_resume).pack(side=tk.LEFT, padx=5)
        
        # JD file selection
        jd_frame = ttk.Frame(file_frame)
        jd_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(jd_frame, text="Job Description File:").pack(side=tk.LEFT, padx=5)
        self.jd_path_var = tk.StringVar()
        ttk.Entry(jd_frame, textvariable=self.jd_path_var, width=50, state="readonly").pack(side=tk.LEFT, padx=5)
        ttk.Button(jd_frame, text="Browse...", command=self.browse_jd).pack(side=tk.LEFT, padx=5)
        
        # File size note
        ttk.Label(file_frame, text="Note: Maximum file size is 2MB", foreground="gray").pack(anchor=tk.W, padx=5, pady=5)
        
        # Next button
        next_button = ttk.Button(file_frame, text="Next", command=self.validate_files_and_proceed)
        next_button.pack(anchor=tk.E, padx=5, pady=5)
        
    def create_library_selection_section(self):
        self.library_frame = ttk.LabelFrame(self.main_frame, text="Library Selection", padding="10")
        # Don't pack yet - will be shown after file validation
        
        # Resume extractors section
        self.resume_extractors_frame = ttk.LabelFrame(self.library_frame, text="Resume Extractors", padding="5")
        self.resume_extractors_frame.pack(fill=tk.X, pady=5)
        
        # JD extractors section
        self.jd_extractors_frame = ttk.LabelFrame(self.library_frame, text="Job Description Extractors", padding="5")
        self.jd_extractors_frame.pack(fill=tk.X, pady=5)
        
        # Process button
        process_frame = ttk.Frame(self.library_frame)
        process_frame.pack(fill=tk.X, pady=10)
        
        self.process_button = ttk.Button(process_frame, text="Process Files", command=self.process_files)
        self.process_button.pack(side=tk.RIGHT, padx=5)
        
        self.back_button = ttk.Button(process_frame, text="Back", command=self.go_back_to_file_selection)
        self.back_button.pack(side=tk.RIGHT, padx=5)
        
    def create_results_section(self):
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        # Don't pack yet - will be shown after processing
        
        # Create a treeview for results
        columns = ("Document", "Library", "Status", "Characters", "Words", "Lines", "Time (s)")
        self.results_tree = ttk.Treeview(self.results_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == "Document" or col == "Library":
                self.results_tree.column(col, width=120, anchor=tk.W)
            elif col == "Status":
                self.results_tree.column(col, width=60, anchor=tk.CENTER)
            else:
                self.results_tree.column(col, width=80, anchor=tk.CENTER)
                
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add scrollbars
        tree_scroll_y = ttk.Scrollbar(self.results_tree, orient="vertical", command=self.results_tree.yview)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=tree_scroll_y.set)
        
        # Buttons
        buttons_frame = ttk.Frame(self.results_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        self.clear_button = ttk.Button(buttons_frame, text="Clear & Start Over", command=self.reset_app)
        self.clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Error details section (hidden by default)
        self.error_frame = ttk.LabelFrame(self.results_frame, text="Error Details", padding="5")
        # Don't pack yet - will be shown when an error row is selected
        
        self.error_text = tk.Text(self.error_frame, height=5, width=50, wrap=tk.WORD)
        self.error_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind selection event to show error details
        self.results_tree.bind("<<TreeviewSelect>>", self.show_error_details)
    
    def browse_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume File",
            filetypes=(("PDF files", "*.pdf"), ("DOCX files", "*.docx"), ("All files", "*.*"))
        )
        if file_path:
            self.resume_path = file_path
            self.resume_path_var.set(file_path)
            
    def browse_jd(self):
        file_path = filedialog.askopenfilename(
            title="Select Job Description File",
            filetypes=(("PDF files", "*.pdf"), ("DOCX files", "*.docx"), ("All files", "*.*"))
        )
        if file_path:
            self.jd_path = file_path
            self.jd_path_var.set(file_path)
    
    def validate_files_and_proceed(self):
        # Check if files are selected
        if not self.resume_path or not self.jd_path:
            messagebox.showerror("Error", "Please select both resume and job description files.")
            return
        
        # Validate file types
        if not is_valid_file_type(self.resume_path):
            messagebox.showerror("Error", f"Resume file must be PDF or DOCX format.")
            return
            
        if not is_valid_file_type(self.jd_path):
            messagebox.showerror("Error", f"Job description file must be PDF or DOCX format.")
            return
        
        # Validate file sizes
        if not is_file_size_valid(self.resume_path, 2):
            messagebox.showerror("Error", f"Resume file exceeds maximum size of 2MB.")
            return
            
        if not is_file_size_valid(self.jd_path, 2):
            messagebox.showerror("Error", f"Job description file exceeds maximum size of 2MB.")
            return
        
        # Get file types
        self.resume_type = get_file_type(self.resume_path)
        self.jd_type = get_file_type(self.jd_path)
        
        # Hide file selection and show library selection
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
            
        self.library_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Populate library selection checkboxes
        self.populate_library_selections()
        
    def populate_library_selections(self):
        # Clear existing widgets
        for widget in self.resume_extractors_frame.winfo_children():
            widget.destroy()
        
        for widget in self.jd_extractors_frame.winfo_children():
            widget.destroy()
            
        # Dictionary to store checkbox variables
        self.resume_extractor_vars = {}
        self.jd_extractor_vars = {}
        
        # Populate resume extractors
        resume_extractors = get_available_extractors(self.resume_type)
        
        if resume_extractors:
            ttk.Label(self.resume_extractors_frame, text=f"Select libraries for {self.resume_type.upper()} processing:").pack(anchor=tk.W, padx=5, pady=5)
            
            for name in resume_extractors:
                var = tk.BooleanVar(value=True)  # Default checked
                self.resume_extractor_vars[name] = var
                cb = ttk.Checkbutton(self.resume_extractors_frame, text=name, variable=var)
                cb.pack(anchor=tk.W, padx=20, pady=2)
        else:
            ttk.Label(self.resume_extractors_frame, text=f"No extractors available for {self.resume_type.upper()} files.").pack(anchor=tk.W, padx=5, pady=5)
        
        # Populate JD extractors
        jd_extractors = get_available_extractors(self.jd_type)
        
        if jd_extractors:
            ttk.Label(self.jd_extractors_frame, text=f"Select libraries for {self.jd_type.upper()} processing:").pack(anchor=tk.W, padx=5, pady=5)
            
            for name in jd_extractors:
                var = tk.BooleanVar(value=True)  # Default checked
                self.jd_extractor_vars[name] = var
                cb = ttk.Checkbutton(self.jd_extractors_frame, text=name, variable=var)
                cb.pack(anchor=tk.W, padx=20, pady=2)
        else:
            ttk.Label(self.jd_extractors_frame, text=f"No extractors available for {self.jd_type.upper()} files.").pack(anchor=tk.W, padx=5, pady=5)
    
    def go_back_to_file_selection(self):
        # Hide library selection
        self.library_frame.pack_forget()
        
        # Show file selection
        self.create_file_selection_section()
        
    def process_files(self):
        # Get selected extractors
        resume_extractors = {}
        jd_extractors = {}
        
        # Get resume extractors
        for name, var in self.resume_extractor_vars.items():
            if var.get():
                extractors = get_available_extractors(self.resume_type)
                resume_extractors[name] = extractors[name]
        
        # Get JD extractors
        for name, var in self.jd_extractor_vars.items():
            if var.get():
                extractors = get_available_extractors(self.jd_type)
                jd_extractors[name] = extractors[name]
        
        # Check if at least one extractor is selected for each
        if not resume_extractors:
            messagebox.showerror("Error", "Please select at least one library for resume processing.")
            return
            
        if not jd_extractors:
            messagebox.showerror("Error", "Please select at least one library for job description processing.")
            return
            
        # Hide library selection
        self.library_frame.pack_forget()
        
        # Show results frame
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.results = []
        
        # Process files in a separate thread
        self.status_var.set("Processing files...")
        self.process_button.config(state=tk.DISABLED)
        self.back_button.config(state=tk.DISABLED)
        
        threading.Thread(target=self._process_files_thread, args=(resume_extractors, jd_extractors)).start()
    
    def _process_files_thread(self, resume_extractors, jd_extractors):
        try:
            # Process resume
            resume_filename = get_base_filename(self.resume_path)
            for name, extractor_func in resume_extractors.items():
                try:
                    self.root.after(0, lambda: self.status_var.set(f"Processing resume with {name}..."))
                    
                    # Extract text
                    text, stats = extractor_func(self.resume_path)
                    
                    # Save to file
                    output_file = save_extracted_text(text, "resume", name, resume_filename)
                    
                    # Store result
                    result = {
                        "document": "Resume",
                        "library": name,
                        "status": "Success" if stats["success"] else "Failed",
                        "char_count": stats["char_count"],
                        "word_count": stats["word_count"],
                        "line_count": stats["line_count"],
                        "time": f"{stats['processing_time']:.3f}",
                        "error": stats["error"],
                        "output_file": output_file
                    }
                    self.results.append(result)
                    
                    # Update UI
                    self.root.after(0, lambda r=result: self.add_result_to_tree(r))
                    
                except Exception as e:
                    # Handle unexpected errors
                    error_msg = f"Error processing resume with {name}: {str(e)}"
                    result = {
                        "document": "Resume",
                        "library": name,
                        "status": "Error",
                        "char_count": 0,
                        "word_count": 0,
                        "line_count": 0,
                        "time": "N/A",
                        "error": error_msg,
                        "output_file": None
                    }
                    self.results.append(result)
                    
                    # Update UI
                    self.root.after(0, lambda r=result: self.add_result_to_tree(r))
            
            # Process job description
            jd_filename = get_base_filename(self.jd_path)
            for name, extractor_func in jd_extractors.items():
                try:
                    self.root.after(0, lambda: self.status_var.set(f"Processing job description with {name}..."))
                    
                    # Extract text
                    text, stats = extractor_func(self.jd_path)
                    
                    # Save to file
                    output_file = save_extracted_text(text, "jd", name, jd_filename)
                    
                    # Store result
                    result = {
                        "document": "Job Description",
                        "library": name,
                        "status": "Success" if stats["success"] else "Failed",
                        "char_count": stats["char_count"],
                        "word_count": stats["word_count"],
                        "line_count": stats["line_count"],
                        "time": f"{stats['processing_time']:.3f}",
                        "error": stats["error"],
                        "output_file": output_file
                    }
                    self.results.append(result)
                    
                    # Update UI
                    self.root.after(0, lambda r=result: self.add_result_to_tree(r))
                    
                except Exception as e:
                    # Handle unexpected errors
                    error_msg = f"Error processing job description with {name}: {str(e)}"
                    result = {
                        "document": "Job Description",
                        "library": name,
                        "status": "Error",
                        "char_count": 0,
                        "word_count": 0,
                        "line_count": 0,
                        "time": "N/A",
                        "error": error_msg,
                        "output_file": None
                    }
                    self.results.append(result)
                    
                    # Update UI
                    self.root.after(0, lambda r=result: self.add_result_to_tree(r))
            
            # Processing complete
            self.root.after(0, lambda: self.status_var.set("Processing complete"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}"))
            
        finally:
            self.root.after(0, lambda: self.process_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.back_button.config(state=tk.NORMAL))
    
    def add_result_to_tree(self, result):
        # Add result to the treeview
        values = (
            result["document"],
            result["library"],
            result["status"],
            result["char_count"],
            result["word_count"],
            result["line_count"],
            result["time"]
        )
        
        item_id = self.results_tree.insert('', 'end', values=values)
        
        # Set tag for error items
        if result["status"] != "Success":
            self.results_tree.item(item_id, tags=('error',))
            
        # Configure tag
        self.results_tree.tag_configure('error', background='#ffcccc')
    
    def show_error_details(self, event):
        # Get selected item
        selected = self.results_tree.focus()
        if not selected:
            return
            
        # Get values
        values = self.results_tree.item(selected, 'values')
        if not values:
            return
            
        # Find corresponding result
        result = None
        for r in self.results:
            if (r["document"] == values[0] and 
                r["library"] == values[1] and 
                r["status"] == values[2]):
                result = r
                break
                
        if not result or not result["error"]:
            # Hide error frame if no error
            self.error_frame.pack_forget()
            return
            
        # Show error details
        self.error_text.delete(1.0, tk.END)
        self.error_text.insert(tk.END, result["error"])
        self.error_frame.pack(fill=tk.X, pady=10)
    
    def reset_app(self):
        # Clear file paths
        self.resume_path = None
        self.jd_path = None
        self.resume_path_var.set("")
        self.jd_path_var.set("")
        
        # Clear file types
        self.resume_type = None
        self.jd_type = None
        
        # Clear results
        self.results = []
        
        # Reset UI
        self.results_frame.pack_forget()
        self.library_frame.pack_forget()
        self.error_frame.pack_forget()
        
        # Show file selection again
        self.create_file_selection_section()
        
        # Reset status
        self.status_var.set("Ready")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentExtractorApp(root)
    root.mainloop()