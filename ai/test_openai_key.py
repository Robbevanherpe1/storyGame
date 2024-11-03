import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, this is a test!"}]
    )
    print("Response from OpenAI:", response['choices'][0]['message']['content'])
except Exception as e:
    print("Error:", e)
