import requests

headers = {
    'Authorization': 'Bearer 43d6cd7d8b3c44461ded9beea7e06bb318907fc2'
}

endpoint = "http://localhost:8000/api/products/"

# http://localhost:8000/admin/
# session -> post data
# selenium

data = {
    "title": "This field is done by singler function view",
    "price": 32.99
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())
