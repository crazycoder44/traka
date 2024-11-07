import requests

endpoint = "http://localhost:8000/api/custom_admin/users/"



get_response = requests.get(endpoint)

print(get_response.json())