import sqlite3
from datetime import datetime

DB_NAME = "orders.db"

def validate_order(order):
    """
    Phase 1: Input Validation
    Validates order data before insertion
    """
    required_fields = ["user", "item", "quantity", "price"]
    
    # Check for missing fields
    for field in required_fields:
        if field not in order:
            return False, f"Missing required field: {field}"
    
    # Validate quantity (must be positive)
    if not isinstance(order["quantity"], int) or order["quantity"] <= 0:
        return False, "Quantity must be a positive integer"
    
    # Validate price (must be positive)
    if not isinstance(order["price"], (int, float)) or order["price"] <= 0:
        return False, "Price must be a positive number"
    
    # Validate user
    if not isinstance(order["user"], str) or not order["user"].strip():
        return False, "User must be a non-empty string"
    
    # Validate item
    if not isinstance(order["item"], str) or not order["item"].strip():
        return False, "Item must be a non-empty string"
    
    return True, "Valid"


def check_inventory(item, quantity):
    """
    Phase 2: Prevent Overselling
    Checks if sufficient stock is available
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT stock FROM inventory WHERE item = ?",
        (item,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return False, f"Item '{item}' not found in inventory"
    
    stock = result[0]
    if stock < quantity:
        return False, f"Insufficient stock. Available: {stock}, Requested: {quantity}"
    
    return True, "Stock available"


def decrease_inventory(item, quantity):
    """
    Phase 2: Auto-Decrease Stock
    Decreases inventory after successful order
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE inventory 
        SET stock = stock - ?, updated_at = CURRENT_TIMESTAMP
        WHERE item = ?
        """,
        (quantity, item)
    )
    
    conn.commit()
    conn.close()


def insert_order(order, order_id=None):
    """
    Phase 1-2: Insert Order with validation and inventory management
    """
    # Validate order
    is_valid, message = validate_order(order)
    if not is_valid:
        print(f"❌ Validation Error: {message}")
        return False, message
    
    # Check inventory
    can_fulfill, inv_message = check_inventory(order["item"], order["quantity"])
    if not can_fulfill:
        print(f"❌ Inventory Error: {inv_message}")
        return False, inv_message
    
    # Generate order_id if not provided
    if order_id is None:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        conn.close()
        order_id = f"ORD{str(count + 1).zfill(6)}"
    
    # Get timestamp
    timestamp = order.get("timestamp", datetime.now().isoformat())
    status = order.get("status", "PENDING")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO orders
            (order_id, user, item, quantity, price, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order_id,
                order["user"],
                order["item"],
                order["quantity"],
                order["price"],
                status,
                timestamp
            )
        )
        
        conn.commit()
        conn.close()
        
        # Decrease inventory after successful order
        decrease_inventory(order["item"], order["quantity"])
        
        print(f"✅ Order {order_id} inserted successfully")
        return True, order_id
        
    except sqlite3.IntegrityError as e:
        print(f"❌ Database Error: {str(e)}")
        return False, str(e)
