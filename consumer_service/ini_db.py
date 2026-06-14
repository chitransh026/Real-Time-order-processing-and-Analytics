import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database initialized")

