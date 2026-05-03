import json, os
from dotenv import load_dotenv
from google import genai
load_dotenv()

from flask import Flask, render_template, request

from lib.image_ai import image_summary, make_story

app = Flask(__name__)


# GET / - Home Page
# Renders the front-end interface for the application
# Input: None
# Output: HTML page (index.html)
@app.route('/')
def index():
    return render_template("index.html")

# POST /summary_image - Generate Image Summary
# Analyzes an image and generates a text summary of its content
# Input: JSON object with format {"url": "image_url_string"}
# Example Input: {"url": "https://example.com/image.jpg"}
# Output: JSON object with format {"description": "<image_description>"}
# Example Output: {"description": "A sunset over a calm ocean with golden clouds reflecting on the water"}
@app.route('/summary_image', methods=['POST'])
def summary_image():
    print("Process Image Summary")
    
    images= json.loads(request.data)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    value = json.dumps(image_summary(client, images["url"]))
    print(value)
    return value

# POST /generate_story - Generate Story from Images
# Creates a cohesive story based on a sequence of images and their descriptions
# Input: JSON array of objects with format [{"data_url": "base64_image_data", "description": "image_description"}, ...]
# Example Input: [{"data_url": "data:image/jpeg;base64,/9j/4AAQSkZJRg...", "description": "A girl walks into the forest"}, {"data_url": "data:image/jpeg;base64,/9j/4AAQSkZJRg...", "description": "She discovers a magical cabin"}]
# Output: JSON object with format {"story": "<generated_story>"}
# Example Output: {"story": "Once upon a time, a curious girl decided to explore the mysterious forest. As she walked deeper into the woods, the sunlight filtered through the tall trees. Suddenly, she came upon a charming cabin hidden among the trees..."}
@app.route('/generate_story', methods=['POST'])
def generate_story():
    print("Generate Story")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    image_url_with_desc_list = json.loads(request.data)
    value = json.dumps(make_story(client, image_url_with_desc_list))
    print(value)
    return value



if __name__ == '__main__':
    app.run(debug=True)