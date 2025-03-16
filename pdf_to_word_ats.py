import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox, scrolledtext, Menu
from pdf2docx import Converter
from docx import Document
import os
import re
import subprocess

def select_pdf():
    """Let the user select a PDF file via file dialog."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        update_selected_file(file_path)

def update_selected_file(file_path):
    """Update the entry field and enable the convert button."""
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, file_path)
    convert_button.config(state=tk.NORMAL, bg="blue", fg="white")
    check_ats_button_state()

def convert_pdf_to_word():
    """Convert the selected PDF file to a Word document."""
    pdf_file = pdf_entry.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select or drop a PDF file.")
        return

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    pdf_name = os.path.basename(pdf_file).replace(".pdf", ".docx")
    docx_file = os.path.join(output_folder, pdf_name)

    try:
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        
        messagebox.showinfo("Success", f"Conversion complete!\nSaved in: {docx_file}")
        subprocess.run(["open", "-a", "LibreOffice", docx_file])

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert file.\nError: {str(e)}")

def extract_text_from_docx(docx_path):
    """Extract text from a Word document (.docx)."""
    if not os.path.exists(docx_path):
        messagebox.showerror("Error", "No converted resume found.")
        return ""

    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def compare_keywords(resume_text, job_description):
    """Check for missing and present keywords in a resume."""
    job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))

    missing_keywords = job_words - resume_words
    matched_keywords = job_words & resume_words

    return missing_keywords, matched_keywords

def check_ats():
    """Check ATS compatibility and give a pass/fail score."""
    pdf_file = pdf_entry.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    docx_file = os.path.join(os.getcwd(), "output", os.path.basename(pdf_file).replace(".pdf", ".docx"))
    job_description = job_desc_text.get("1.0", tk.END).strip()

    if not os.path.exists(docx_file):
        messagebox.showerror("Error", "No converted resume found.")
        return

    resume_text = extract_text_from_docx(docx_file)
    missing, matched = compare_keywords(resume_text, job_description)

    # Basic ATS Scoring System
    keyword_match_score = (len(matched) / (len(matched) + len(missing))) * 100 if (len(matched) + len(missing)) > 0 else 0
    resume_length = len(resume_text.split())

    # ATS-Friendly Formatting Check
    formatting_issues = 0
    if resume_length < 200:
        formatting_issues += 1  
    if "image" in resume_text.lower() or "table" in resume_text.lower():
        formatting_issues += 0.5  

    # Final Score Calculation
    final_score = keyword_match_score - (formatting_issues * 10)  
    final_score = max(0, min(100, final_score))

    # Pass/Fail Criteria
    if final_score >= 75:
        ats_result = "✅ Pass (Your resume is ATS-friendly)"
    elif final_score >= 50:
        ats_result = "⚠️ Warning (May pass, but needs improvements)"
    else:
        ats_result = "❌ Fail (Your resume may not pass an ATS filter)"

    result_message = (
        f"🔹 **ATS Score:** {final_score:.2f}%\n"
        f"✅ **Matched Keywords:** {len(matched)}\n"
        f"❌ **Missing Keywords:** {', '.join(missing) if missing else 'None'}\n"
        f"📄 **Resume Length:** {resume_length} words\n"
        f"{ats_result}"
    )

    messagebox.showinfo("ATS Check Results", result_message)

def check_ats_button_state():
    """Enable ATS check button only when both fields are filled."""
    if pdf_entry.get().strip() and job_desc_text.get("1.0", tk.END).strip():
        ats_button.config(state=tk.NORMAL, bg="green", fg="white")
    else:
        ats_button.config(state=tk.DISABLED, bg="lightgray", fg="black")

def clear_text():
    """Clear the job description text box."""
    job_desc_text.delete("1.0", tk.END)
    check_ats_button_state()

def on_drop(event):
    """Handle file drop and update the UI."""
    dropped_file = event.data.strip()  
    if os.path.isfile(dropped_file) and dropped_file.lower().endswith(".pdf"):
        update_selected_file(dropped_file)
    else:
        messagebox.showerror("Error", "Please drop a valid PDF file.")

def on_closing():
    """Handle the close event properly so the app exits without freezing."""
    if messagebox.askokcancel("Quit", "Are you sure you want to close?"):
        root.destroy()

def create_context_menu(widget):
    """Create right-click context menu for copy, cut, and paste."""
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))

    def show_menu(event):
        """Show context menu on right-click."""
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-2>" if os.name == "posix" else "<Button-3>", show_menu)  

# Create GUI
root = TkinterDnD.Tk()  
root.title("PDF to Word + ATS Checker")
root.geometry("600x600")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Enable Drag & Drop
pdf_entry = tk.Entry(root, width=50)
pdf_entry.pack(pady=5)
pdf_entry.drop_target_register(DND_FILES)
pdf_entry.dnd_bind("<<Drop>>", on_drop)

# UI Elements
tk.Label(root, text="Drag & Drop a PDF or Click Browse").pack(pady=5)
tk.Button(root, text="📂 Browse", command=select_pdf, font=("Arial", 10, "bold"), bg="lightgray").pack(pady=5)

# Convert Button
convert_button = tk.Button(root, text="🔄 Convert to Word", command=convert_pdf_to_word, bg="gray", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
convert_button.pack(pady=10)

# Job Description Input
tk.Label(root, text="Paste Job Description Below:").pack(pady=5)
frame = tk.Frame(root)
frame.pack()

job_desc_text = scrolledtext.ScrolledText(frame, height=6, width=60, wrap=tk.WORD)
job_desc_text.pack(side=tk.LEFT, padx=5, pady=5)
job_desc_text.bind("<KeyRelease>", lambda event: check_ats_button_state())

# Add clear button next to the text box
clear_button = tk.Button(frame, text="🗑 Clear Text", command=clear_text, font=("Arial", 10, "bold"), bg="red", fg="white")
clear_button.pack(side=tk.RIGHT, padx=5)

# Add right-click menu to the job description box
create_context_menu(job_desc_text)

# Improved ATS Check Button
ats_button = tk.Button(root, text="🔍 Check ATS Compatibility", command=check_ats, font=("Arial", 11, "bold"), bg="lightgray", fg="black", padx=10, pady=5, state=tk.DISABLED)
ats_button.pack(pady=15)

# Run GUI
root.mainloop()
