import requests

# endpoint = "https://httpbin.org/status/200/"
# endpoint = "https://httpbin.org/anything"

endpoint = "http://localhost:8000/api/"

# API -> Application Programing Interface -> Emilate HTTP Get Request
get_response = requests.post(
    endpoint, params={"product_id": 123})  # HTTP request
# get_response = requests.get(endpoint, params={"abc": 123})

# print(get_response.text)  # print raw text response
# print(get_response.status_code)  # print raw text response

# REST APIs -> Web Api

# HTTP Request -> HTML
# REST API HTTP Request -> JSON

# JSON -> JavaScript Object Nototion ~ Python Dict

print(get_response.json())  # print json response
