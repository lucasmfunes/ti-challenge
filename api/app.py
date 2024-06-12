from flask import Flask, jsonify, request
from flask_cors import CORS
from core.database import query_db

app = Flask(__name__)
CORS(app)

@app.route('/api/process_header', methods=['GET'])
def get_process_header():
    data = query_db("SELECT * FROM process_header")
    return jsonify(data)

@app.route('/api/etl_data', methods=['GET'])
def get_etl_data():
    data = query_db("SELECT * FROM etl_data")
    return jsonify(data)

@app.route('/api/register_data', methods=['GET'])
def get_register_data():
    process_id = request.args.get('process_id')
    if process_id:
        data = query_db("SELECT * FROM register_data WHERE process_id = ?", [process_id])
    else:
        data = query_db("SELECT * FROM register_data")
    return jsonify(data)

@app.route('/api/gender_data', methods=['GET'])
def get_gender_data():
    process_id = request.args.get('process_id')
    if process_id:
        data = query_db("SELECT * FROM gender_data WHERE process_id = ?", [process_id])
    else:
        data = query_db("SELECT * FROM gender_data")
    return jsonify(data)

@app.route('/api/age_data', methods=['GET'])
def get_age_data():
    process_id = request.args.get('process_id')
    if process_id:
        data = query_db("SELECT * FROM age_data WHERE process_id = ?", [process_id])
    else:
        data = query_db("SELECT * FROM age_data")
    return jsonify(data)

@app.route('/api/city_data', methods=['GET'])
def get_city_data():
    process_id = request.args.get('process_id')
    if process_id:
        data = query_db("SELECT * FROM city_data WHERE process_id = ?", [process_id])
    else:
        data = query_db("SELECT * FROM city_data")
    return jsonify(data)

@app.route('/api/os_data', methods=['GET'])
def get_os_data():
    process_id = request.args.get('process_id')
    if process_id:
        data = query_db("SELECT * FROM os_data WHERE process_id = ?", [process_id])
    else:
        data = query_db("SELECT * FROM os_data")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
