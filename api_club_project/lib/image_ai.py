from google import genai
from google.genai import types
import os, re


MODEL = "gemini-3-flash-preview"
MODEL = "gemini-3.1-flash-lite-preview"
MODEL = "gemini-2.5-flash-lite"

def data_url_to_google_types(data_url):
    _, media_type, encode_base, content = re.split("data:|;|,", data_url)
    return types.Part.from_bytes(
        mime_type=media_type,
        data=content,
    )
    
def image_summary(client, image_data_url):
    results = {}
    
    try:
        prompt = f"""
            Please use a paragraph not exceeding 30 words to explain the given image.
        """
        
        response = client.models.generate_content(
            model = MODEL,
            contents=[
                prompt,
                data_url_to_google_types(image_data_url)
            ]
        )
            
        results["description"] = response.text
    except Exception as e:
        results["description"] = f"Exception occured: {e}"
        
    return results

def make_story(client, image_url_with_desc):
    try:
        contents = [
            """
            Based on the input images, and their descriptions, please make up a story.
            Control the output within 100 words.
            """
        ]
        i = 0
        for it in image_url_with_desc:
            i += 1
            contents.append(data_url_to_google_types(it["data_url"]))
            contents.append(f"The {i}-th image's description: " + it["description"])
        
        response = client.models.generate_content(
            model = MODEL,
            contents=contents,
        )
        
        return {
            "story": response.text
        }
    except Exception as e:
        return {
            "story": f"Exception occured: {e}"
        }