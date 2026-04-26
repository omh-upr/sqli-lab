# SQL Injection Laboratory

A deliberately vulnerable Streamlit app for teaching SQL injection techniques. Students interact with an inventory search interface and progressively exploit it through OR bypasses, UNION-based schema enumeration, and data exfiltration.

## Quick Start (Local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install streamlit
python src/create_db.py
streamlit run app.py
```

## Repository Structure

```
├── app.py              # Streamlit app (vulnerable search interface)
├── requirements.txt    # streamlit
├── data/
│   └── challenge.db    # SQLite database — committed, do not gitignore
└── src/
    └── create_db.py    # Regenerates challenge.db from scratch
```

## Regenerating the Database

If seed data changes, re-run the script and commit the result:

```bash
python src/create_db.py
git add data/challenge.db && git commit -m "Regenerate database"
git push
```

## Documentation

- [docs/spec01.md](docs/spec01.md) — full specification: schema, challenges, and payloads
- [docs/deployment01.md](docs/deployment01.md) — step-by-step Streamlit Cloud deployment guide
