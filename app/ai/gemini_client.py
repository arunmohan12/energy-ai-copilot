import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")
if not api_key:
    raise ValueError("API key is required")

client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model=gemini_model,
input="Say hello in one sentence."
)

print(interaction.output_text)
