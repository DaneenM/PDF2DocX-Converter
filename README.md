### **📌 Updated README Without Drag & Drop**
Since **drag-and-drop doesn’t work**, I’ve removed it and updated the instructions accordingly.

---

### **📂 README.md for PDF2DocX Converter**
```markdown
# 📄 PDF2DocX Converter

PDF2DocX Converter is a simple desktop application that allows users to **convert PDF files to Word (.docx) format** quickly. The converted file is automatically opened in **LibreOffice** for easy editing.

## 🚀 Features

✔ **Simple PDF to DOCX Conversion** – No complex settings, just select and convert  
✔ **Automatic DOCX Saving** – Saves converted files in the `output/` folder  
✔ **Opens in LibreOffice** – No need for Microsoft Word  
✔ **Works on macOS** – Fully optimized for Mac users  
✔ **Fast & Lightweight** – Minimal UI, no unnecessary features  

## 📂 Installation

### 1️⃣ **Install Dependencies**
Make sure you have **Python 3** installed. Then, install the required libraries:

```bash
python3 -m pip install pdf2docx tkinter
```

### 2️⃣ **Install LibreOffice (if not installed)**
LibreOffice is needed to open DOCX files. Install it via Homebrew:

```bash
brew install --cask libreoffice
```

## ▶️ Usage

### **Run the App**
```bash
python3 pdf_to_word_gui.py
```

### **Convert a PDF**
1. Click **"Browse"** and select a **PDF file**  
2. Click **"Convert to Word"**  
3. The converted DOCX file will be saved in the `output/` folder  
4. **LibreOffice automatically opens the DOCX file** for editing  

## 🔄 Troubleshooting

### **Can't Find the Converted DOCX?**
Run this command to locate the most recent `.docx` files:
```bash
find ~/ -name "*.docx" -type f -print | sort -r | head -10
```

### **LibreOffice Asks About File Format?**
Set LibreOffice to **always save in DOCX format**:
1. Open **LibreOffice**
2. Go to **Preferences > Load/Save > General**
3. Set **Default File Format** to **Microsoft Word 2007-365 (.docx)**
4. **Uncheck** "Ask when not saving in ODF or default format"

## 📜 License
This project is open-source and free to use.

---

### **🔥 Now You Can Easily Convert & Edit PDFs as Word Docs on Mac! 🚀**
```

---

### **📌 What’s Changed?**
✔ **Removed all drag-and-drop references**  
✔ **Updated instructions to only use the "Browse" button**  
✔ **Ensured clarity in troubleshooting steps**  

---

### **🔥 Now the README Matches the Working Features! 🚀**
Let me know if you need any final updates! 😊
