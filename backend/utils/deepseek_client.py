# backend/utils/deepseek_client.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def analyze_data(self, content, analysis_type="general"):
        """
        Send data to DeepSeek API for analysis
        """
        endpoint = f"{self.base_url}/analyze"

        payload = {
            "content": content,
            "analysis_type": analysis_type,
            "options": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API error: {str(e)}")

    async def generate_visualization(self, data, viz_type="auto"):
        """
        Generate visualization recommendations based on data
        """
        endpoint = f"{self.base_url}/visualize"

        payload = {
            "data": data,
            "visualization_type": viz_type
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API error: {str(e)}")