import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()

# Create orders table with order_id, timestamp, and status
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE NOT NULL,
    user TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    status TEXT DEFAULT 'PENDING',
    timestamp DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create inventory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT UNIQUE NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Initialize inventory with sample data
cursor.execute("SELECT COUNT(*) FROM inventory")
if cursor.fetchone()[0] == 0:
    inventory_items = [
        ("Drone", 50),
        ("Camera", 30),
        ("Battery", 100)
    ]
    cursor.executemany(
        "INSERT INTO inventory (item, stock) VALUES (?, ?)",
        inventory_items
    )
    conn.commit()

conn.close()

print("Database initialized with orders and inventory tables")
