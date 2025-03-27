# 🧠 Local LLM Document QA Tool

A local AI-powered document Q&A interface that allows you to:

- Upload a file (PDF or TXT)
- Ask a question about its contents
- Get an answer from **Meta’s LLaMA 3.2 8B model**, running via **Ollama** on your machine
- All within a simple local web interface — **no internet or external API calls needed**

---

## 🧱 Stack & Flow

- **Frontend**: Plain HTML + JS (file upload + question form)
- **Backend**: Python Flask API running at `localhost:5000`
- **LLM**: llama 3.2 (8B) served locally via **Ollama** (`localhost:11434`)
- **Text Extraction**:
  - `.txt` files are read directly
  - `.pdf` files are parsed using `PyPDF2`
- **Prompt Construction**:
  ```text
  Use the following document to answer the question:

  [extracted file text]

  Question: [user question]
- Sends the prompt to the Ollama API ```(/api/generate)``` with ```stream=False``` (or handles token-wise output if ```stream=True```)

- Returns the response as JSON to the frontend

---

## 🔒 Local Only
- All inference is done offline — nothing leaves the machine

- You could easily swap out LLaMA for another Ollama-supported model (e.g. Mistral, Code LLaMA, etc.)


---

- Run ollama 
- Run app.py
- Open index.html file
