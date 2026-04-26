import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# dotenv -f /path/to/.env run python3 app.py
load_dotenv() # load from .env by default in the current directory
    
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello, World!", 200
#/add?num1=5&num2=9  —> expect to see {“sum”: 14}
@app.route('/add')
def add():
    try:
        num1 = int(request.args.get('num1'))
        num2 = int(request.args.get('num2'))

        return json.dumps('sum': sum), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

@app.route('/add_post', methods=['POST'])
def add_post():
    try:
        data = json.loads(request.data)
        num1 = data['num1']
        num2 = data['num2']
        sum = num1 + num2
        return json.dumps({'sum': int(num1)}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500


def data_url_to_google_types(data_url):
    _, media_type, encode_base, content = re.split("data:|;|,", data_url)
    return types.Part.from_bytes(
        mime_type=media_type,
        data=content,
    )               

def make_summary(image_url_obj):
    try:
        contents = (
            """
            Make a summary for the input image.
            Make the summary 
        )

@app.route('/generate_summary', methods=['POST'])
def generate_story():

        

if __name__ == '__main__':
    app.run(debug=True)