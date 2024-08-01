# src/data_collection.py
from confluent_kafka import Producer
import json
import time
import random

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Simulate data collection
def collect_data():
    return {
        'timestamp': time.time(),
        'length': random.randint(50, 150),
        'source_ip': f"192.168.1.{random.randint(1, 255)}",
        'destination_ip': f"192.168.1.{random.randint(1, 255)}",
        'protocol': random.choice(['TCP', 'UDP']),
        'packet_count': random.randint(1, 100),
        'target': random.choice([0, 1])  # Simulated target variable
    }

try:
    while True:
        data = collect_data()
        producer.produce('network-data', value=json.dumps(data), callback=delivery_report)
        producer.flush()
        time.sleep(1)  # Reduce sleep time to collect data faster
except KeyboardInterrupt:
    pass
finally:
    producer.flush()
