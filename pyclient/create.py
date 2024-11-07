import requests

endpoint = "http://localhost:8000/api/custom_admin/users/"

data = {
    "firstname": "panda",
    "lastname": "hyena",
    "gender": "Male",
    "email": "babaitu@gmail.com",
    "mobile": "9126751245",
    "address": "nepa",
    "role": "Sales Rep",
    "branch": 4,
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())