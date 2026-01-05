import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No API Key found.")
    exit()

client = genai.Client(api_key=api_key)

print("--- Available Free Models for your Key ---")
try:
    # Just list them and print the name
    for model in client.models.list():
        # The new SDK returns names like "models/gemini-1.5-flash"
        print(f"✅ {model.name}")
except Exception as e:
    print(f"Error: {e}")