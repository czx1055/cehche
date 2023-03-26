
import requests

params = {"prompt":"你好","options":{}}
url = "http://chat.dl-100.cn/api/chat-process"
        
        
response = requests.post(url,json=params)

print(response.text)