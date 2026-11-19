## Get request :
#
from urllib import response

import requests
# response = requests.get("https://org.dev.invorush.com")
# print(response.status_code)
# print(response.text)


### Query parameter :

# response = requests.get("https://org.invorush.com", params = {"q": "python"})


### json response :
#
# response = requests.get("https://org.dev.invorush.com/api/auth/login-with-email-password")
# data = response.json()
# print(data)



####  post request :
#
# response = requests.post("https://org.dev.invorush.com/api/auth/login-with-email-password",
# json = {"name": "sudip", "age": "24"})


### Header handling :

header = {"Authoraization" : "Bearer token "}

response = requests.get("https://api.github.com/user", headers=header)



## Error  handling :


