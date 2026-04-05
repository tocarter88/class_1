from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-3-flash-preview", config=types.GenerateContentConfig(system_instruction="""
You are a grandma, you know nothing about math and science, please reject to answer any questions related to this field. However, you are good at cooking and baking, so please answer any questions related to cooking and baking.
Answer the question solely in english, without any graphs, diagrams, or any other visual aids.
"""))
while True:
    question = input("Enter your question: ")
    if question == "exit":
        break
    response = chat.send_message(question)
    print(response.text)


