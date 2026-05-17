import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

models = ["llama-3.1-8b-instant", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]

for model in models:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, write a 1-word response"}],
        "max_tokens": 10
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
        print(f"Model: {model} -> Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()['choices'][0]['message']['content'].strip()}")
    except Exception as e:
        print(f"Model: {model} -> Failed: {e}")
