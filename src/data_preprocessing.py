# src/data_preprocessing.py
from confluent_kafka import Consumer, KafkaError
import json
import pandas as pd
import os

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'data-preprocessing-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['network-data'])

data_list = []

def save_data_to_csv(data_list, file_path):
    df = pd.DataFrame(data_list)
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        data = json.loads(msg.value().decode('utf-8'))
        data_list.append(data)

        if len(data_list) >= 100:  # Save every 100 messages
            save_data_to_csv(data_list, 'data/processed/network_data.csv')
            data_list = []

except KeyboardInterrupt:
    pass
finally:
    if data_list:
        save_data_to_csv(data_list, 'data/processed/network_data.csv')
    consumer.close()
