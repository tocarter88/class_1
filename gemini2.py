from dotenv import load_dotenv
from google import genai
import os
from google.genai import types
import requests

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = requests.get('https://www.allaboutbirds.org/guide/assets/photo/301281071-480px.jpg')
image_bytes = response.content


client = genai.Client()
response = client.models.generate_content(
model='gemini-2.5-flash-lite',
contents=[
    types.Part.from_bytes(
    data=image_bytes,
    mime_type='image/jpeg',
    ),
    'Caption this image.'
]
)

print(response.text)


