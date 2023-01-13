import requests

product_id = input("What is the Product ID you want to update \n")

try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'{product_id} not a valid id')

if product_id:
    endpoint = f"http://localhost:8000/api/products/{product_id}/update/"

    data = {
        "title": "This field updated by singular class view",
        "price": 49.99
    }

    get_response = requests.put(endpoint, json=data)

    print(get_response.json())
