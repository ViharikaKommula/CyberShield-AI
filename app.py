# app.py

from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__, template_folder='web/templates')

def preprocess_data(data):
    try:
        data['length'] = int(data['length'])
        data['packet_count'] = int(data['packet_count'])
        data['total_length'] = data['length'] * data['packet_count']
        return data
    except ValueError as e:
        print(f"Error in preprocessing data: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Preprocess the data
    processed_data = preprocess_data(data)

    if processed_data is None:
        return jsonify({'error': 'Error in preprocessing data'}), 400

    # Perform prediction or other processing with processed_data
    # Example: prediction = model.predict(processed_data)

    return jsonify({'total_length': processed_data['total_length']})

if __name__ == '__main__':
    app.run(debug=True)
