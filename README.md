# 📄 PDF to Word Converter

A simple, modern, and easy-to-use tool to convert PDFs to Word documents.

## 🛠️ Installation

Make sure you have Python **3.8+** installed.

### 🔹 Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pdf-to-word.git
cd pdf-to-word
```

### 🔹 Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Step 3: Run the Application
```bash
python app.py  # Or whatever your main file is named
```

---

## 🔧 Dependencies

This app requires:

- `tkinter` (Pre-installed with Python)
- `tkinterdnd2` (For drag & drop functionality)
- `pdf2docx` (For converting PDFs to Word)

If `tkinterdnd2` doesn't install properly, try:
```bash
pip install git+https://github.com/pmgbergen/tkinterdnd2.git
```

---

## 🖥️ Compatible With:
✅ Windows  
✅ macOS  
✅ Linux (May require `python3-tk` installation)
```

---

### **📦 Add a `requirements.txt` File**
Create a file called `requirements.txt` in your project and add:
```
pdf2docx
tkinterdnd2 @ git+https://github.com/pmgbergen/tkinterdnd2.git
```
Now, anyone can install dependencies with:
```bash
pip install -r requirements.txt
```
