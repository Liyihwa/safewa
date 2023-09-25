import logwa
import time
import requests

headers={
    'Host':'1.1.1.1'
}

print(requests.get("http://10.16.19.146/heros",headers=headers).text)