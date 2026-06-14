import sqlite3
from datetime import datetime, timedelta

DBname = 'orders.db'

# ============ PHASE 1 ANALYTICS ============

def get_total_orders():
    """Total number of orders"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status != 'FAILED'")
    result = cursor.fetchone()[0]
    conn.close()
    
    return result


def get_total_revenue():
    """Total revenue from all completed orders"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COALESCE(SUM(price * quantity), 0)
        FROM orders
        WHERE status IN ('COMPLETED', 'PENDING')
    """)
    
    result = cursor.fetchone()[0]
    conn.close()
    
    return round(result, 2)


def get_average_order_value():
    """Average order value"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COALESCE(
            AVG(price * quantity),
            0
        )
        FROM orders
        WHERE status != 'FAILED'
    """)
    
    result = cursor.fetchone()[0]
    conn.close()
    
    return round(result, 2)


def get_top_product():
    """Most ordered product"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            item,
            SUM(quantity) as total_quantity,
            SUM(price * quantity) as total_revenue
        FROM orders
        WHERE status != 'FAILED'
        GROUP BY item
        ORDER BY total_quantity DESC
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    conn.close()
    
    return result


# ============ PHASE 2: INVENTORY ANALYTICS ============

def get_remaining_stock():
    """Phase 2: Remaining stock for all products"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT item, stock
        FROM inventory
        ORDER BY item
    """)
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_low_stock_products(threshold=10):
    """Phase 2: Products with stock below threshold"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT item, stock
        FROM inventory
        WHERE stock < ?
        ORDER BY stock ASC
    """, (threshold,))
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_revenue_by_product():
    """Phase 3: Revenue breakdown by product"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            item,
            SUM(price * quantity) as total_revenue,
            SUM(quantity) as total_units
        FROM orders
        WHERE status IN ('COMPLETED', 'PENDING')
        GROUP BY item
        ORDER BY total_revenue DESC
    """)
    
    result = cursor.fetchall()
    conn.close()
    
    return result


# ============ PHASE 3: ADVANCED ANALYTICS ============

def get_recent_orders(limit=10):
    """Phase 3: Show recent orders"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            order_id,
            user,
            item,
            quantity,
            price,
            status,
            timestamp
        FROM orders
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_orders_per_hour():
    """Phase 3: Orders grouped by hour (requires timestamp)"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
            COUNT(*) as order_count,
            SUM(price * quantity) as revenue_in_hour
        FROM orders
        WHERE status != 'FAILED'
        GROUP BY strftime('%Y-%m-%d %H:00:00', timestamp)
        ORDER BY hour DESC
    """)
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_orders_by_date():
    """Orders grouped by date for trend analytics"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            DATE(timestamp) as date,
            COUNT(*) as order_count,
            SUM(price * quantity) as daily_revenue
        FROM orders
        WHERE status != 'FAILED'
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    """)
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def get_order_status_summary():
    """Summary of orders by status"""
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            status,
            COUNT(*) as count,
            ROUND(SUM(price * quantity), 2) as revenue
        FROM orders
        GROUP BY status
    """)
    
    result = cursor.fetchall()
    conn.close()
    
    return result


def print_analytics_dashboard():
    """Print comprehensive analytics dashboard"""
    print("\n" + "="*60)
    print("📊 REAL-TIME ORDER ANALYTICS DASHBOARD")
    print("="*60)
    
    # Phase 1 Metrics
    print("\n📈 PHASE 1: CORE METRICS")
    print("-" * 60)
    print(f"Total Orders: {get_total_orders()}")
    print(f"Total Revenue: ₹{get_total_revenue():,.2f}")
    print(f"Average Order Value: ₹{get_average_order_value():,.2f}")
    top_product = get_top_product()
    if top_product:
        print(f"Top Product: {top_product[0]} ({top_product[1]} units, ₹{top_product[2]:,.2f})")
    
    # Phase 2 Inventory Metrics
    print("\n📦 PHASE 2: INVENTORY MANAGEMENT")
    print("-" * 60)
    print("Remaining Stock:")
    for item, stock in get_remaining_stock():
        status = "✓" if stock >= 10 else "⚠️ LOW"
        print(f"  {item}: {stock} {status}")
    
    low_stock = get_low_stock_products()
    if low_stock:
        print("\n⚠️  Low Stock Alerts (< 10 units):")
        for item, stock in low_stock:
            print(f"  {item}: {stock}")
    
    # Phase 3 Advanced Analytics
    print("\n💹 PHASE 3: ADVANCED ANALYTICS")
    print("-" * 60)
    
    print("\nRevenue by Product:")
    for item, revenue, units in get_revenue_by_product():
        print(f"  {item}: ₹{revenue:,.2f} ({units} units)")
    
    print("\nOrders per Hour:")
    for hour, count, revenue in get_orders_per_hour()[:5]:
        print(f"  {hour}: {count} orders, ₹{revenue:,.2f}")
    
    print("\nOrder Status Summary:")
    for status, count, revenue in get_order_status_summary():
        print(f"  {status}: {count} orders, ₹{revenue:,.2f}")
    
    print("\nRecent Orders (Last 10):")
    for order_id, user, item, qty, price, status, timestamp in get_recent_orders(10):
        print(f"  {order_id} | {user} | {item} x{qty} @ ₹{price} | {status} | {timestamp}")
    
    print("\n" + "="*60 + "\n")
