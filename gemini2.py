import os
import requests
import mimetypes
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    images_to_process = [
        "https://www.allaboutbirds.org/guide/assets/photo/301281071-480px.jpg",
    ]

    contents = []

    for img_path in images_to_process:
        if img_path.startswith(('http://', 'https://')):
            response = requests.get(img_path)
            image_bytes = response.content
            mime_type = response.headers.get('Content-Type', 'image/jpeg')
        else:
            with open(img_path, 'rb') as f:
                image_bytes = f.read()
            mime_type, _ = mimetypes.guess_type(img_path)
            if not mime_type:
                mime_type = 'image/jpeg'

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    contents.append("Make up a story based on the image contents.")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents,
    )

    print(response.text)

if __name__ == "__main__":
    main()