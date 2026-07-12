import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from google import genai
api_key = os.getenv("GEMINI_API_KEY_1") or os.getenv("GEMINI_API_KEY")
from google.genai import types
client = genai.Client(api_key=api_key)
result = client.models.embed_content(
    model="models/gemini-embedding-2",
    contents="Hello world",
    config=types.EmbedContentConfig(output_dimensionality=768)
)
print(f"Dimension: {len(result.embeddings[0].values)}")
