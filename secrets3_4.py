import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

s = requests.Session()
s.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
s.verify = False
s.headers.update({
    "Cookie": "eyJ1c2VybmFtZSI6InVzZXIyIn0.ZFC2aQ.BsZAct3LquXvcVCTmahoB9iTOBg"
})

while True: 
    r = s.post("https://secrets.quoccabank.com/update", json={"secret": f"{input()}"})