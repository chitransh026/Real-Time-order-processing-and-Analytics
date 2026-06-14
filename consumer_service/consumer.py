from kafka import KafkaConsumer
import json
from database import insert_order
from analytics import print_analytics_dashboard
from datetime import datetime

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9392",
    auto_offset_reset="earliest",
    group_id="order-consumer-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("="*60)
print("🚀 KAFKA CONSUMER - Real-Time Order Processing")
print("="*60)
print("Listening for Orders...\n")

order_count = 0

for message in consumer:
    order = message.value
    
    # Add timestamp if not provided
    if "timestamp" not in order:
        order["timestamp"] = datetime.now().isoformat()
    
    # Set default status if not provided
    if "status" not in order:
        order["status"] = "PENDING"
    
    # Process order with validation and inventory check
    success, result = insert_order(order)
    
    print("=" * 60)
    if success:
        order_count += 1
        print(f"✅ ORDER #{order_count} PROCESSED")
        print(f"Order ID: {result}")
        print(f"User: {order.get('user')}")
        print(f"Item: {order.get('item')}")
        print(f"Quantity: {order.get('quantity')}")
        print(f"Price: ₹{order.get('price')}")
        print(f"Timestamp: {order.get('timestamp')}")
        print(f"Status: {order.get('status')}")
        
        # Show analytics every 5 orders
        if order_count % 5 == 0:
            print("\n")
            print_analytics_dashboard()
    else:
        print(f"❌ ORDER REJECTED")
        print(f"Reason: {result}")
        print(f"Order Data: {json.dumps(order, indent=2)}")
    
    print("=" * 60)
