from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Add this
import requests
import os
import PyPDF2
import json

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS so frontend JS can connect

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_text(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        return "Unsupported file type."

@app.route('/ask', methods=['POST'])
def ask_about_file():
    file = request.files.get('file')
    prompt = request.form.get('prompt')

    if not file or not prompt:
        return jsonify({'error': 'File and prompt are required'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    file_text = extract_text(filepath)
    full_prompt = f"""
        You are an assistant. Use the following document to answer the question. Only use what is in the document.

        DOCUMENT:
        \"\"\"
        {file_text}
        \"\"\"

        QUESTION:
        {prompt}

        If the answer is not in the document, say so.
        """

    print("\n[DEBUG] Prompt being sent to Ollama:")
    print(full_prompt)
    print("----")

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.2",
            "prompt": full_prompt,
            "stream": False
        })

        print("[DEBUG] Raw response from Ollama:")
        print(response.text)

        reply = response.json().get("response", "")
        return jsonify({"response": reply})
    except Exception as e:
        print("[ERROR] Something went wrong when contacting Ollama:", e)
        return jsonify({"error": "Ollama request failed"}), 500

if __name__ == '__main__':
    app.run(port=5000)
