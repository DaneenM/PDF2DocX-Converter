import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD  # Import tkinterdnd2 for drag & drop
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import os
import sys  # Needed for proper app exit handling
import subprocess  # Needed to open LibreOffice automatically

def select_pdf():
    """Let the user select a PDF file via file dialog."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        update_selected_file(file_path)

def update_selected_file(file_path):
    """Update the entry field and enable the convert button."""
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, file_path)
    convert_button.config(state=tk.NORMAL)  # Enable Convert button

def convert_pdf_to_word():
    """Convert the selected PDF file to a Word document and open it in LibreOffice."""
    pdf_file = pdf_entry.get()

    if not pdf_file:
        messagebox.showerror("Error", "Please select or drop a PDF file.")
        return

    # Ensure output folder exists
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Generate DOCX filename based on PDF name
    pdf_name = os.path.basename(pdf_file).replace(".pdf", ".docx")
    docx_file = os.path.join(output_folder, pdf_name)

    try:
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        
        messagebox.showinfo("Success", f"Conversion complete!\nSaved in: {docx_file}")

        # Automatically open the DOCX file in LibreOffice
        subprocess.run(["open", "-a", "LibreOffice", docx_file])  

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert file.\nError: {str(e)}")

def on_drop(event):
    """Handle file drop and update the UI."""
    dropped_file = event.data.strip()  # Get the dropped file path
    if os.path.isfile(dropped_file) and dropped_file.lower().endswith(".pdf"):
        update_selected_file(dropped_file)
    else:
        messagebox.showerror("Error", "Please drop a valid PDF file.")

def on_closing():
    """Handle the close event properly so the app exits without freezing."""
    if messagebox.askokcancel("Quit", "Are you sure you want to close?"):
        root.destroy()  # Properly destroy the window
        sys.exit(0)  # Ensure complete exit

# Create the GUI window using TkinterDnD for Drag & Drop support
root = TkinterDnD.Tk()  # Use TkinterDnD for native drag & drop
root.title("PDF to Word Converter")
root.geometry("400x250")
root.resizable(False, False)

# Handle Close Button (X)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Enable Drag & Drop with tkinterdnd2
pdf_entry = tk.Entry(root, width=40)
pdf_entry.pack(pady=5)
pdf_entry.drop_target_register(DND_FILES)
pdf_entry.dnd_bind("<<Drop>>", on_drop)

# UI Elements
tk.Label(root, text="Drag & Drop a PDF or Click Browse").pack(pady=5)
tk.Button(root, text="Browse", command=select_pdf).pack(pady=5)

# Convert Button (Initially disabled)
convert_button = tk.Button(root, text="Convert to Word", command=convert_pdf_to_word, bg="blue", fg="white", state=tk.DISABLED)
convert_button.pack(pady=15)

# Run the GUI
root.mainloop()
