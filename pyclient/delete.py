import requests

endpoint = "http://localhost:8000/api/products/10/delete/"


get_response = requests.delete(endpoint)

print(get_response)