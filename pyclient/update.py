import requests

endpoint = "http://localhost:8000/api/custom_admin/branches/4/update/"

data = {
    "branchname": "lasu",
    "address": "7, Eniyanlonbinu Street, Mafoluku, Oshodi"
}

get_response = requests.patch(endpoint, json=data)

print(get_response.json())

