# GitHub Project — Status field options (English)

Use this list on: **Project → Settings → Fields → Status → Add option**

Add options **in this order** (left → right on the board).

---

## Phase A — Software engineering (core app)

| Order | Status name | What it means |
|------:|-------------|----------------|
| 1 | `01 — Idea & scope` | Defined goal: hospital appointment booking demo (Flask + SQLite) |
| 2 | `02 — Repo & gitignore` | GitHub repo, `.gitignore`, first commit |
| 3 | `03 — Python venv` | Virtual environment + `pip install -r requirements.txt` |
| 4 | `04 — Flask app factory` | `create_app()`, config, SQLite in `instance/` |
| 5 | `05 — Database models` | `Doctor`, `Slot`, `Appointment`, relationships, constraints |
| 6 | `06 — init-db & demo data` | CLI `init-db`, 3 doctors, slots for 5 days |
| 7 | `07 — Route: index` | `GET /` — filter by `?day=`, slots grouped by doctor |
| 8 | `08 — Route: book` | `GET/POST /slots/<id>/book` — form, validation, no double booking |
| 9 | `09 — Route: cancel` | `GET /cancel/<token>` — free the slot again |
| 10 | `10 — Route: admin` | `GET /admin/appointments` — all bookings (joins) |
| 11 | `11 — Jinja2 templates` | `base`, `index`, `book`, `success`, `admin` |
| 12 | `12 — CSS & UI` | `static/styles.css`, doctor cards, day buttons |
| 13 | `13 — Team documentation` | `README`, `START`, `BACKEND-DEVELOPER` |
| 14 | `14 — Manual test` | Book → confirm → admin → cancel → slot free |

## Phase B — RAG support chatbot (step by step)

| Order | Status name | What it means |
|------:|-------------|----------------|
| 15 | `15 — Chat: system guide` | Wrote `docs/system_guide.md` (routes, rules, models) |
| 16 | `16 — Chat: RAG dependencies` | Installed langchain, chroma, ollama packages |
| 17 | `17 — Chat: Ollama models` | `ollama pull nomic-embed-text` + `ollama pull gemma3:4b` |
| 18 | `18 — Chat: rag_build.py` | Load docs, split text, build Chroma in `vector_store/` |
| 19 | `19 — Chat: index vectors` | Ran `python rag_build.py` — chunks indexed |
| 20 | `20 — Chat: rag_chat.py` | `RagAssistant` — retrieve k=4, prompt, scope guard |
| 21 | `21 — Chat: POST /chat` | JSON API, session history (last 12 messages) |
| 22 | `22 — Chat: assistant init` | `RagAssistant()` in `create_app()`, graceful fallback |
| 23 | `23 — Chat: widget UI` | Floating `?` button + Support Chat panel in `base.html` |
| 24 | `24 — Chat: frontend fetch` | `fetch("/chat")`, `session_id` in `localStorage` |
| 25 | `25 — Chat: test Q&A` | Ask about booking, cancel, admin — only system topics |

## Phase C — Done

| Order | Status name | What it means |
|------:|-------------|----------------|
| 26 | `26 — Presentation ready` | Demo script rehearsed, dates refreshed with `init-db` |
| 27 | `Done` | Shipped / presented |

---

## Short list (if GitHub limits options)

```
Backlog
Planning
Backend core
Frontend & templates
Database & init-db
Testing (booking flow)
Chat — docs & vector index
Chat — RAG backend
Chat — widget UI
Integration test
Presentation ready
Done
```

---

## How to add on GitHub (you do this in the browser)

1. Open your project **Settings** → **Fields** → **Status**.
2. Click **Add option** for each row in the tables above.
3. Click **Save**.
4. On the board view, set **Group by: Status**.

This file lives in the repo so teammates can copy the same labels.
