import sqlite3

DBname='orders.db'

def get_total_orders():
    conn=sqlite3.connect(DBname)

    cursor=conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    result=cursor.fetchone()[0]

    conn.close()

    return result

def get_total_revenue():
    conn=sqlite3.connect(DBname)
    cursor=conn.cursor()

    cursor.execute("""
   SELECT COALESCE(SUM(price * quantity),
   0
   )
   FROM orders
    """)

    result=cursor.fetchone()[0]

    conn.close()

def get_average_order_value():

    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(
            AVG(price * quantity),
            0
        )
        FROM orders
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return round(result, 2)

def get_top_product():

    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            item,
            SUM(quantity) as total_quantity

        FROM orders

        GROUP BY item

        ORDER BY total_quantity DESC

        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    return result
    
