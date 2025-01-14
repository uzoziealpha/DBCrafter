# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.deepseek_client import DeepSeekClient
from config.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize DeepSeek client
deepseek_client = DeepSeekClient()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "DatabaseCrafter API is running"})

@app.route('/api/analyze', methods=['POST'])
async def analyze_data():
    try:
        data = request.json
        if not data or 'content' not in data:
            return jsonify({"error": "No content provided"}), 400

        analysis_type = data.get('analysis_type', 'general')
        result = await deepseek_client.analyze_data(data['content'], analysis_type)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/visualize', methods=['POST'])
async def generate_visualization():
    try:
        data = request.json
        if not data or 'data' not in data:
            return jsonify({"error": "No data provided"}), 400

        viz_type = data.get('visualization_type', 'auto')
        result = await deepseek_client.generate_visualization(data['data'], viz_type)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)