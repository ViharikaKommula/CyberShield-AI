# src/feature_engineering.py
import pandas as pd
import os

def feature_engineering(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    df = pd.read_csv(input_file)
    
    required_columns = ['timestamp', 'length', 'protocol', 'packet_count', 'source_ip', 'destination_ip', 'target']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"Missing columns in the data: {', '.join(missing_columns)}")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    df['second'] = df['timestamp'].dt.second
    df['protocol_num'] = df['protocol'].apply(lambda x: 1 if x == 'TCP' else 2)
    
    df['total_length'] = df['length'] * df['packet_count']
    
    feature_columns = ['hour', 'minute', 'second', 'length', 'protocol_num', 'total_length', 'source_ip', 'destination_ip', 'target']
    df[feature_columns].to_csv(output_file, index=False)
    print(f"Feature engineering completed. Data saved to {output_file}")

if __name__ == "__main__":
    input_file = 'data/processed/network_data.csv'
    output_file = 'data/processed/network_features.csv'
    feature_engineering(input_file, output_file)
