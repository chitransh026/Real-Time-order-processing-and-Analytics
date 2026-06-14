from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders",

    bootstrap_servers="localhost:9392",

    auto_offset_reset="earliest",

    value_deserializer=lambda m:
    json.loads(
        m.decode("utf-8")
    )
)

print("Listening for Orders...\n")

for message in consumer:

    print("=" * 40)

    print(message.value)

    print("=" * 40)

    