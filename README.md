# Hospital Appointment System (4everCare demo)

A small **working** web app for presentations: patients book doctor time slots (Flask + SQLite + optional RAG chatbot).

## Features

- View doctors and available slots (by day)
- Book a free slot (patient name + phone)
- Confirmation page with cancel link
- Admin page listing all appointments (no login in this demo)
- **Support chatbot** (RAG): answers questions about this system only

## Quick start (Windows / PowerShell)

From the `hospital-appointment` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py init-db
py app.py run
```

Open: http://127.0.0.1:5000

For **fresh dates on presentation day**, see [START.md](START.md).

## Commands

| Command | Description |
|---------|-------------|
| `py app.py init-db` | Creates `instance/app.db` and loads demo doctors + slots |
| `py app.py run` | Starts the development server |
| `py rag_build.py` | Builds vector index for the chatbot (requires Ollama) |

## Chatbot (optional)

See [CHATBOT_SETUP.md](CHATBOT_SETUP.md) for Ollama models and indexing steps.

## Project management (GitHub)

Status labels for your GitHub Project board: [PROJECT_STATUS.md](PROJECT_STATUS.md)

## Backend deep dive

For defense / presentation as Backend Developer: [BACKEND-DEVELOPER.md](BACKEND-DEVELOPER.md)

## 3–5 minute demo script

1. Home page: pick a day, show doctors and free slots  
2. Book a slot → confirmation page  
3. Open **All appointments** (admin)  
4. Cancel via link → slot is free again  
5. Open **?** chat → ask "How do I book?" or "How do I cancel?"

## Tech stack

- **Backend:** Flask, Flask-SQLAlchemy  
- **Database:** SQLite (`instance/app.db`)  
- **Frontend:** Jinja2 templates, CSS  
- **Chatbot:** LangChain + Chroma + Ollama (local)

## Repository structure

```
hospital-appointment/
├── app.py                 # Routes, models, booking logic, /chat API
├── rag_chat.py            # RAG assistant
├── rag_build.py           # Index docs/ into vector_store/
├── docs/system_guide.md   # Chatbot knowledge base
├── templates/             # HTML pages + chat widget
├── static/styles.css
├── PROJECT_STATUS.md      # GitHub Project Status options
├── CHATBOT_SETUP.md
├── START.md
└── BACKEND-DEVELOPER.md
```
