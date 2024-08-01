# src/model_training.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess_data(df):
    # Encode categorical features like IP addresses
    label_encoder = LabelEncoder()
    df['source_ip'] = label_encoder.fit_transform(df['source_ip'])
    df['destination_ip'] = label_encoder.fit_transform(df['destination_ip'])
    
    # Select features and target variable
    feature_columns = ['hour', 'minute', 'second', 'length', 'protocol_num', 'total_length', 'source_ip', 'destination_ip']
    X = df[feature_columns]
    y = df['target']
    
    return X, y

def train_model(input_file, model_file):
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    df = pd.read_csv(input_file)
    
    if 'target' not in df.columns:
        print("Target column 'target' not found in the data.")
        return
    
    # Handle missing values
    df.dropna(subset=['target'], inplace=True)
    
    X, y = preprocess_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, model_file)
    print(f"Model training completed. Model saved to {model_file}")

if __name__ == "__main__":
    input_file = 'data/processed/network_features.csv'
    model_file = 'models/network_model.pkl'
    train_model(input_file, model_file)
