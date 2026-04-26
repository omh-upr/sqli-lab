import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "challenge.db")


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS users;

        CREATE TABLE products (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            stock_count INTEGER NOT NULL,
            price       REAL NOT NULL
        );

        CREATE TABLE users (
            id            INTEGER PRIMARY KEY,
            username      TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin      INTEGER NOT NULL DEFAULT 0
        );
    """)

    products = [
        ("Laptop Pro 15",       "Electronics", 12,  1299.99),
        ("Wireless Mouse",      "Electronics", 85,    29.99),
        ("USB-C Hub",           "Electronics", 43,    49.99),
        ("Mechanical Keyboard", "Electronics",  7,   119.99),
        ("Cotton T-Shirt",      "Clothing",    200,   19.99),
        ("Denim Jacket",        "Clothing",     34,   89.99),
        ("Running Shoes",       "Clothing",     56,   74.99),
        ("Organic Coffee 1kg",  "Food",        150,   18.99),
        ("Dark Chocolate Bar",  "Food",        300,    3.49),
        ("Olive Oil 500ml",     "Food",         75,   12.99),
    ]
    cur.executemany(
        "INSERT INTO products (name, category, stock_count, price) VALUES (?, ?, ?, ?)",
        products,
    )

    users = [
        ("admin",     sha256("admin123"), 1),
        ("professor", sha256("prof2024"), 1),
        ("student",   sha256("pass123"),  0),
    ]
    cur.executemany(
        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
        users,
    )

    conn.commit()
    conn.close()
    print(f"Database created at {os.path.abspath(DB_PATH)}")
    print(f"  admin    password_hash: {sha256('admin123')}")
    print(f"  professor password_hash: {sha256('prof2024')}")
    print(f"  student  password_hash: {sha256('pass123')}")


if __name__ == "__main__":
    main()
