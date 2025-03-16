import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import os
import subprocess

class PDFtoWordApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("PDF to Word Converter")
        self.master.geometry("500x420")  # 🔥 Perfectly sized
        self.master.resizable(False, False)
        self.master.configure(bg="#F8F9FA")
        self.pack(pady=15)
        self.create_widgets()

    def create_widgets(self):
        # --- Fonts & Colors ---
        title_font = ("Arial", 18, "bold")
        button_font = ("Arial", 11, "bold")
        entry_font = ("Arial", 10)
        primary_color = "#007BFF"
        danger_color = "#DC3545"
        success_color = "#28A745"
        neutral_gray = "#E9ECEF"
        text_color = "#222"  # Dark text for better contrast

        # --- Main Frame (Sleek UI) ---
        frame = tk.Frame(self.master, bg="white", relief="flat", bd=0)
        frame.pack(padx=15, pady=10, ipadx=10, ipady=10, fill="both", expand=True)

        # --- Title Section ---
        title_label = tk.Label(frame, text="PDF to Word Converter", font=title_font, bg="white", fg=text_color)
        title_label.pack(pady=(5, 15))

        # --- File Selection Area ---
        file_frame = tk.Frame(frame, bg="white")
        file_frame.pack(pady=5)

        self.pdf_entry = tk.Entry(file_frame, width=40, font=entry_font, bd=1, relief="solid", bg="#fff", fg=text_color)
        self.pdf_entry.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)
        self.pdf_entry.drop_target_register(DND_FILES)
        self.pdf_entry.dnd_bind("<<Drop>>", self.on_drop)
        self.pdf_entry.bind("<KeyRelease>", self.check_button_state)

        browse_button = tk.Button(file_frame, text="Browse", command=self.select_pdf, font=button_font, 
                                  bg=primary_color, fg=text_color, bd=0, padx=12, pady=6, relief="flat")
        browse_button.pack(side=tk.LEFT, padx=5)
        browse_button.bind("<Enter>", lambda e: browse_button.config(bg="#0056b3"))
        browse_button.bind("<Leave>", lambda e: browse_button.config(bg=primary_color))

        clear_button = tk.Button(file_frame, text="Clear", command=self.clear_file, font=button_font, 
                                 bg=danger_color, fg=text_color, bd=0, padx=12, pady=6, relief="flat")
        clear_button.pack(side=tk.LEFT, padx=5)
        clear_button.bind("<Enter>", lambda e: clear_button.config(bg="#b52b3b"))
        clear_button.bind("<Leave>", lambda e: clear_button.config(bg=danger_color))

        # --- Drag & Drop Section ---
        self.drop_area = tk.Label(
            frame, text="Drag & Drop PDF Here", font=("Arial", 12, "bold"), bg=neutral_gray, fg=text_color,
            relief="flat", width=45, height=3, padx=10, pady=10
        )
        self.drop_area.pack(pady=15, ipadx=10, ipady=10, fill="x")
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        # --- Convert Button (🔥 Fixed Text Readability) ---
        self.convert_button = tk.Button(
            frame, text="Convert to Word", command=self.convert_pdf_to_word, font=button_font,
            bg=success_color, fg=text_color, state=tk.DISABLED, bd=0, padx=15, pady=12, relief="flat"
        )
        self.convert_button.pack(pady=20)
        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg="#218838") if self.convert_button["state"] == "normal" else None)
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg=success_color) if self.convert_button["state"] == "normal" else None)

        # --- Status Message ---
        self.status_label = tk.Label(frame, text="", font=("Arial", 10), bg="white", fg="green")
        self.status_label.pack(pady=5)

    def select_pdf(self):
        """Let the user select a PDF file via file dialog."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.update_selected_file(file_path)

    def clear_file(self):
        """Clear the selected PDF file."""
        self.pdf_entry.delete(0, tk.END)  # Clear input field
        self.convert_button.config(state=tk.DISABLED)  # Disable Convert button
        self.status_label.config(text="", fg="green")  # Reset status message

    def update_selected_file(self, file_path):
        """Update the entry field and enable convert button."""
        self.pdf_entry.delete(0, tk.END)
        self.pdf_entry.insert(0, file_path)
        self.convert_button.config(state=tk.NORMAL)  # Enable Convert button

    def convert_pdf_to_word(self):
        """Convert the selected PDF file to a Word document."""
        pdf_file = self.pdf_entry.get()
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
            self.status_label.config(text=f"✔ File saved: {docx_file}", fg="green")

            # Open the converted file
            if os.name == "nt":  # Windows
                os.startfile(docx_file)
            elif os.name == "posix":  # macOS & Linux
                subprocess.run(["open", docx_file])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert file.\nError: {str(e)}")
            self.status_label.config(text="Conversion failed!", fg="red")

    def on_drop(self, event):
        """Handle file drop."""
        dropped_file = event.data.strip().lstrip('{').rstrip('}')
        if os.path.isfile(dropped_file) and dropped_file.lower().endswith(".pdf"):
            self.update_selected_file(dropped_file)
        else:
            messagebox.showerror("Error", "Please drop a valid PDF file.")

    def check_button_state(self, event=None):
        """Enable the Convert button only if a PDF file is selected."""
        if self.pdf_entry.get().strip():
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)

# --- Run GUI ---
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFtoWordApp(master=root)
    app.mainloop()
