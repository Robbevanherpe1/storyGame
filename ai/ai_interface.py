import openai
import os
from dotenv import load_dotenv

# Load the .env file for environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_response(prompt):
    """Generate a response from the OpenAI API based on the provided prompt."""
    try:
        # Make the API call to OpenAI's chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Specify the model you want to use
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Control randomness in response
        )
        
        # Extract and return the assistant's message content
        return response['choices'][0]['message']['content']
    
    except openai.error.OpenAIError as e:
        # Catch and handle OpenAI-specific errors
        print(f"OpenAI API Error: {e}")
        return "Sorry, I couldn't generate a response at this time."
    except Exception as e:
        # Catch any other errors
        print(f"Unexpected Error: {e}")
        return "Sorry, I couldn't generate a response at this time."
