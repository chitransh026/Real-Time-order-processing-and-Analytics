from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9392",
    value_serializer=lambda v:
    json.dumps(v).encode("utf-8")
)

def send_order(order):

    producer.send(
        "orders",
        value=order
    )

    producer.flush()

    print("Order Published")