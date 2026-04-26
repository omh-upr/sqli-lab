# Deployment Guide — Streamlit Community Cloud

## Prerequisites
- A GitHub account
- A Streamlit Community Cloud account (free) at [share.streamlit.io](https://share.streamlit.io)

---

## Phase 1: Prepare the Repository

### 1. Create a Private GitHub Repository
1. Go to GitHub → **New repository**
2. Name it (e.g. `sqli-lab`)
3. Set visibility to **Private**
4. Do **not** initialize with a README (the repo already has content)
5. Click **Create repository**

### 2. Push the Project
From the project root on your machine:

```bash
git remote add origin https://github.com/<your-username>/sqli-lab.git
git add app.py requirements.txt .gitignore data/challenge.db src/create_db.py docs/
git commit -m "Initial commit: SQLi lab"
git push -u origin main
```

Verify on GitHub that `data/challenge.db` is present — Streamlit Cloud will serve it directly and it is what gets restored on reboot.

---

## Phase 2: Deploy on Streamlit Community Cloud

### 3. Connect Your Account
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**

### 4. Configure the App
Fill in the deployment form:

| Field | Value |
|---|---|
| **Repository** | `<your-username>/sqli-lab` |
| **Branch** | `main` |
| **Main file path** | `app.py` |
| **App URL** | choose a slug, e.g. `sqli-lab` |

Leave **Python version** at the default (3.11+).

### 5. Deploy
Click **Deploy**. Streamlit Cloud will:
1. Clone your private repo
2. Install dependencies from `requirements.txt` (`streamlit`)
3. Start `app.py`

First boot typically takes 2–3 minutes. Subsequent cold starts are faster.

---

## Phase 3: Grant Students Access

Since the repo is private, the **app itself is public by default** on Streamlit Cloud — students only need the app URL, not access to the repo. Share the URL (e.g. `https://sqli-lab.streamlit.app`) with your class.

If you want to restrict access to specific people, go to **App settings → Sharing** and add email addresses.

---

## Phase 4: Running, Stopping, and Modifying the App

### Running the App
The app starts automatically after deployment and restarts on its own if it crashes. If it was manually stopped or went to sleep:

1. Go to [share.streamlit.io](https://share.streamlit.io) → your app
2. Click the **⋮ menu** → **Reboot app**

> Streamlit Cloud puts apps to sleep after ~7 days of inactivity. The next visitor will wake it up automatically (cold start takes ~30 seconds).

### Stopping the App
To take the app offline temporarily:

1. Go to [share.streamlit.io](https://share.streamlit.io) → your app
2. Click the **⋮ menu** → **Pause app**

Students will see a "This app has been paused" page. Resume it the same way via **⋮ → Resume app** when ready.

To permanently remove the app, click **⋮ → Delete app**. This only removes the deployment — your GitHub repo is unaffected.

### Modifying the App
Streamlit Cloud watches the connected branch and **redeploys automatically on every push**.

**Workflow for any change:**

```bash
# 1. Edit files locally (app.py, etc.)

# 2. If you changed the database schema or seed data, regenerate it
python src/create_db.py

# 3. Stage, commit, and push
git add app.py                     # or whichever files changed
git add data/challenge.db          # include if regenerated
git commit -m "describe the change"
git push
```

Streamlit Cloud picks up the push within seconds and redeploys. Downtime during redeploy is typically under 30 seconds.

> **Important:** changes to `data/challenge.db` must be committed and pushed — the cloud instance has no other way to receive database updates.

---

## Phase 5: Resetting the Database

If a student uses a destructive payload (`DELETE`, `DROP`, `UPDATE`) and corrupts the database for others:

1. Go to [share.streamlit.io](https://share.streamlit.io) → your app
2. Click the **⋮ menu** → **Reboot app**

Rebooting re-clones the repo and restores `data/challenge.db` to the committed version. No manual intervention needed.

> If you want a clean state after each session, simply reboot before each class.

---

## File Checklist Before Pushing

```
sqli-lab/
├── app.py              ✅ Streamlit entry point
├── requirements.txt    ✅ contains: streamlit
├── .gitignore          ✅ excludes .venv/, __pycache__/
├── data/
│   └── challenge.db    ✅ committed (NOT in .gitignore)
└── src/
    └── create_db.py    ✅ (for local re-generation only)
```
