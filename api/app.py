from flask import Flask, jsonify
from core.database import query_db

app = Flask(__name__)

@app.route('/api/process_header', methods=['GET'])
def get_process_header():
    data = query_db("SELECT * FROM process_header")
    return jsonify(data)

@app.route('/api/etl_data', methods=['GET'])
def get_etl_data():
    data = query_db("SELECT * FROM etl_data")
    return jsonify(data)

@app.route('/api/summary_data', methods=['GET'])
def get_summary_data():
    data = query_db("SELECT * FROM summary_data")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
