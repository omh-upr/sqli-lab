This specification documents the architecture, data model, and security flaws for the SQL Injection (SQLi) laboratory, as implemented. It is deployed on **Streamlit Community Cloud** using a private GitHub repository.

---

## 1. Project Architecture

The project is a single-page Streamlit application connected to a committed SQLite database file.

* **Platform:** Streamlit Community Cloud
* **Database:** SQLite (`data/challenge.db`)
* **Primary Vulnerability:** Unparameterized f-string query in the `WHERE` clause of the search function
* **Secondary Goal:** Data exfiltration (leaking password hashes) and schema enumeration via UNION attacks

### Repository Structure

```
sqli-lab/
├── app.py              # Streamlit entry point
├── requirements.txt    # streamlit (sqlite3 is stdlib)
├── .gitignore
├── data/
│   └── challenge.db    # committed — restored on Streamlit Cloud reboot
├── src/
│   └── create_db.py    # run locally to regenerate challenge.db
└── docs/
    ├── spec01.md
    └── deployment01.md
```

---

## 2. Data Model (Schema)

### Table: `products` (The Search Target)

Students interact with this table through the search UI. `stock_count` and `price` are hidden from the UI but discoverable via injection.

| Column | Type | Content |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key |
| `name` | TEXT | Product Name |
| `category` | TEXT | Product Category (`Electronics`, `Clothing`, `Food`) |
| `stock_count` | INTEGER | Hidden column (not shown in UI) |
| `price` | REAL | Hidden column (not shown in UI) |

Seed data: 10 rows — 4 Electronics, 3 Clothing, 3 Food.

### Table: `users` (The Hack Target)

Students must discover this table and extract its contents.

| Column | Type | Content |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key |
| `username` | TEXT | See seed data below |
| `password_hash` | TEXT | SHA-256 hash of the password |
| `is_admin` | INTEGER | `1` = admin, `0` = regular user |

Seed data:

| username | plaintext | SHA-256 hash | is_admin |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9` | 1 |
| `professor` | `prof2024` | `be0594bf37209ed534c04d1843a81e2ebb48d62463d7cac2a2e5c1d5fd9bd091` | 1 |
| `student` | `pass123` | `9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c` | 0 |

> CrackStation recognizes all three hashes. Students should be hinted that passwords are common words or simple patterns.

---

## 3. Application Logic & UI

The Streamlit UI presents a minimal "Inventory Search" interface with no styling or sidebar.

1. **Search Input:** `st.text_input` — students enter a category string
2. **Search Button:** triggers query execution
3. **The Vulnerable Query:**
   ```python
   query = f"SELECT id, name, category FROM products WHERE category LIKE '{user_input}'"
   ```
4. **Query Display:** the raw SQL is shown in a `st.code` block (with built-in copy button) before execution — helps students see what their injection produces
5. **Results Table:** `st.dataframe` with proper column names from `cursor.description`, index hidden
6. **Copy-friendly Output:** results are also rendered as pipe-delimited text in a second `st.code` block for easy note-taking
7. **Error Feedback:** `sqlite3.Error` exceptions are displayed via `st.error()` — intentional, helps students debug injection syntax

---

## 4. Laboratory Challenges for Students

### Challenge A: The "OR" Bypass (Discovery)
* **Goal:** Return all products regardless of category
* **Payload:** `' OR 1=1 --`
* **Resulting query:** `... WHERE category LIKE '' OR 1=1 --'`
* **Expected output:** all 10 rows from `products`

### Challenge B: Schema Enumeration (UNION Attack)
* **Goal:** Discover that a `users` table exists and inspect its schema
* **Payload:** `' UNION SELECT 1, name, sql FROM sqlite_master --`
* **Learning point:** SQLite stores schema in `sqlite_master`; column count and types must match the original SELECT (int, text, text)

### Challenge C: Data Exfiltration (The Flag)
* **Goal:** Extract all usernames and password hashes
* **Payload:** `' UNION SELECT id, username, password_hash FROM users --`
* **Learning point:** column count alignment (3 columns: int, text, text); leaking data from a table not referenced in the original query

### Challenge D: Cracking the Hash
* **Goal:** Recover the plaintext `admin` password from its SHA-256 hash
* **Tool:** [CrackStation](https://crackstation.net)
* **Expected result:** `admin123`

---

## 5. Deployment

Local preparation is complete. For full deployment steps see **[deployment01.md](deployment01.md)**.

Summary:
1. Push repo (including `data/challenge.db`) to a **private** GitHub repository
2. Connect repo to Streamlit Community Cloud — set main file to `app.py`
3. Share the public app URL with students (no GitHub access required)
4. **Reset strategy:** reboot the app from the Streamlit dashboard to restore `challenge.db` from the committed version

---

## 6. Regenerating the Database

If the seed data needs to change, edit `src/create_db.py` and run:

```bash
python src/create_db.py
```

Then commit and push `data/challenge.db`. Streamlit Cloud will redeploy automatically.
