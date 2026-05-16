# RAG Support Chatbot — Setup Guide (English)

The chatbot answers **only** questions about the Hospital Appointment System, using documentation in `docs/` and a local vector database.

## Architecture (simple)

```
User types in widget (base.html)
    → POST /chat  (app.py)
    → RagAssistant.answer()  (rag_chat.py)
    → Chroma retriever (vector_store/)
    → Ollama LLM (gemma3:4b)
    → JSON { answer, sources }
```

## Prerequisites

1. **Ollama** installed and running: https://ollama.com  
2. Models pulled once:

```powershell
ollama pull nomic-embed-text
ollama pull gemma3:4b
```

3. Python packages (see `requirements.txt`):

```powershell
cd C:\Users\Administrator\hospital-appointment
.\.venv\Scripts\pip install -r requirements.txt
```

## Step-by-step (first time)

### 1. Write or update knowledge base

Edit `docs/system_guide.md` (routes, booking rules, data model).  
You can add more `.md`, `.txt`, or `.pdf` files under `docs/`.

### 2. Build the vector index

```powershell
.\.venv\Scripts\python.exe rag_build.py
```

Expected output: `Indexed N chunks into ...\vector_store`

### 3. Start the web app

```powershell
.\.venv\Scripts\python.exe app.py init-db
.\.venv\Scripts\python.exe app.py run
```

Open http://127.0.0.1:5000 — click the **?** button (bottom-right).

### 4. Test sample questions

- "How do I book an appointment?"
- "How can I cancel?"
- "What is on the admin page?"
- "What database do you use?"

Off-topic questions should get:  
`I can only answer questions about Hospital Appointment System.`

## Files you own (chatbot)

| File | Role |
|------|------|
| `docs/system_guide.md` | Source text for RAG |
| `rag_build.py` | Index docs → Chroma |
| `rag_chat.py` | Retrieve + LLM prompt |
| `app.py` | `POST /chat`, session memory |
| `templates/base.html` | Chat widget UI + JavaScript |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Chat always says "contact support" | Ollama not running or models not pulled |
| `No documents found in ./docs` | Add files under `docs/` and run `rag_build.py` |
| Booking works but chat does not | Normal if `RagAssistant()` failed at startup — check Ollama |
| Wrong answers | Update `docs/system_guide.md`, re-run `rag_build.py` |

## Security note (demo)

- Chat history is stored **in server memory** (not in SQLite).
- No API keys in repo — everything runs locally via Ollama.
- Do not commit `.env` or passwords.
