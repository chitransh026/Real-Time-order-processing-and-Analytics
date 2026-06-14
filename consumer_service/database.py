import sqlite3

DB_NAME = "orders.db"

def insert_order(order):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders
        (user,item,quantity,price)
        VALUES (?,?,?,?)
        """,
        (
            order["user"],
            order["item"],
            order["quantity"],
            order["price"]
        )
    )

    conn.commit()

    conn.close()