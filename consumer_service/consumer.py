from kafka import KafkaConsumer
import json
from database import insert_order

consumer = KafkaConsumer(
    "orders",

    bootstrap_servers="localhost:9392",

    auto_offset_reset="earliest",
    group_id="order-consumer-group",
    value_deserializer=lambda m:
    json.loads(
        m.decode("utf-8")
    )
)

print("Listening for Orders...\n")

for message in consumer:
    order = message.value
    insert_order(order)

    print("=" * 40)

    print(message.value)

    print("=" * 40)

    