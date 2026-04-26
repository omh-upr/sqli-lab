import sqlite3
import os
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "challenge.db")

st.title("Inventory Search")
st.caption("SQL Injection Laboratory — this app is intentionally vulnerable.")

user_input = st.text_input("Search by category", placeholder="e.g. Electronics")
run = st.button("Search")

if run and user_input:
    query = f"SELECT id, name, category FROM products WHERE category like '{user_input}'"

    st.markdown("**Query executed:**")
    st.code(query, language="sql")

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        col_names = [d[0] for d in cur.description] if cur.description else []
        conn.close()

        if rows:
            st.markdown(f"**Results — {len(rows)} row(s):**")
            st.dataframe(
                [dict(zip(col_names, row)) for row in rows],
                hide_index=True,
            )

            header = " | ".join(col_names)
            separator = "-+-".join("-" * len(c) for c in col_names)
            body = "\n".join(" | ".join(str(v) for v in row) for row in rows)
            st.markdown("**Copy-friendly output:**")
            st.code(f"{header}\n{separator}\n{body}", language="text")
        else:
            st.info("No rows returned.")

    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
