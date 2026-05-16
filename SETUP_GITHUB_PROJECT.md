# Set up your GitHub Project board (one-time)

## Already done for you

- **26 tasks** were created as Issues in the repo (label: `project-roadmap`)
- See: https://github.com/sumayaa7/hospital-appointment/issues?q=label%3Aproject-roadmap

## Finish the Project board (2 minutes)

Your saved GitHub token can push code but **cannot edit Projects**. You need a token with **project** scope once.

### Step 1 — Create token

1. Open: https://github.com/settings/tokens  
2. **Generate new token (classic)**  
3. Note: `Hospital Project Setup`  
4. Expiration: 7 days (or your choice)  
5. Check scopes: **repo** and **project**  
6. **Generate token** → copy it (starts with `ghp_`)

### Step 2 — Run the setup script

Double-click:

```
RUN-SETUP-PROJECT.bat
```

Paste the token → Enter.

The script will:

- Add all 27 **Status** options (English)  
- Add all 26 issues to your Project  
- Set Status to **Done** (or **Presentation ready** for step 26)

### Step 3 — Open the board

https://github.com/users/sumayaa7/projects/1

In **View** settings → **Group by** → **Status** (optional, for Kanban columns).

---

## Manual alternative (no script)

1. Open: https://github.com/sumayaa7/hospital-appointment/issues?q=label%3Aproject-roadmap  
2. Select all issues (checkbox at top)  
3. Right sidebar → **Projects** → choose **Hospital Appointment and RAG Chat**  
4. Add Status options manually from `PROJECT_STATUS.md`
