import json
import requests

url = "https://pokeapi.co/api/v2/pokemon/ditto"
response = requests.get(url)
data = response.content
print(data)