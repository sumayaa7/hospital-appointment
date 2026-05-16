# How to run 4everCare (fresh dates every time)

Do these steps **on presentation day** (or whenever you need up-to-date slot dates).

---

## Step 1. Open PowerShell

- Press `Win + X` → **Windows PowerShell** or **Terminal**, or  
- Search for `PowerShell` in the Start menu.

---

## Step 2. Go to the project folder

```powershell
cd C:\Users\Administrator\hospital-appointment
```

---

## Step 3. Refresh the database (today + next 5 days)

```powershell
.\.venv\Scripts\python.exe app.py init-db
```

Expected: `Initialized database with demo data.`

**If you see "running scripts is disabled"** — use the full path above (no `Activate.ps1`), or see **Plan B** below.

**If you see "No module named 'dotenv'"** — you used system `py` instead of `.venv`. Always use:

`.\.venv\Scripts\python.exe app.py ...`

---

## Step 4. (Optional) Rebuild chatbot index after editing docs

Only if you changed files in `docs/`:

```powershell
.\.venv\Scripts\python.exe rag_build.py
```

Make sure **Ollama** is running and models are installed (see [CHATBOT_SETUP.md](CHATBOT_SETUP.md)).

---

## Step 5. Start the server

```powershell
.\.venv\Scripts\python.exe app.py run
```

Expected:

```
* Running on http://127.0.0.1:5000
```

**Keep this window open** while you demo.

---

## Step 6. Open the site

Browser address: **http://127.0.0.1:5000/**

You should see day buttons (e.g. Mar 16, Mar 17, …) with current dates.

Click **?** (bottom-right) to test the support chat.

---

## Every time — short checklist

1. `cd C:\Users\Administrator\hospital-appointment`
2. `.\.venv\Scripts\python.exe app.py init-db`
3. `.\.venv\Scripts\python.exe app.py run`
4. Browser → http://127.0.0.1:5000/

Stop server: **Ctrl+C** in PowerShell.

---

## Plan B — PowerShell script policy

If activation is blocked, run **once** as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Answer `Y`. Or keep using:

`.\.venv\Scripts\python.exe app.py init-db`  
`.\.venv\Scripts\python.exe app.py run`

(no activation needed)
