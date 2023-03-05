# COMP6443 W2 Challenges Write-ups

## Blog 1
- **Flag:** <span style="color:red"><b>CCOMP6443{ivefinallyfoundsomeone}</b></span><br>
- Details/Explanation:
  - View source page of `blog.quoccabank.com`.

## Blog 2
- **Flag:** <span style="color:red"><b>COMP6443{hiddenpostflag}</b></span><br>
- Details/Explanation:
  - By examining blog posts, *Scott* is posted by the admin.
  - Click **Admin** to redirect to `blog.quoccabank.com/?author=1`.
  - Since `document.location = blogquoccabank.com/? + document.cookie;`, check cookie for the webpage. 
  - There was no cookie, so set it to some values, e.g. `document.cookie = "name=admin";`.
  - Under `blog.quoccabank.com/?name=admin`, search for **admin**.

## Blog 4
- **Flag:** <span style="color:red"><b>COMP6443{strongpasswordsaregreat}</b></span><br>
- Details/Explanation:
  - Click the flag shown on `blog.quoccabank.com/?s=admin` (From Blog 2: search for admin), this will redirect to `blog.quoccabank.com/?page_id=2`.
  - Click *your dashboard*, this will redirect to a login page. 
  - Login as **username:admin** and **password:admin**.
  - View **dashboard**.

## Blog 3
- **Flag:** <span style="color:red"><b>COMP6443{restructuringisonthecards}</b></span><br>
- Details/Explanation:
  - Since there's a search feature under `blog.quoccabank.com/?name=admin`, try searching for **COMP6443**. 
  - The flag is in the draft. 

## Blog 5
- **Flag:** <span style="color:red"><b>COMP6443{Ifoundsarah}</b></span><br>
- Details/Explanation:
  - Login as **username:sarah** and **password:quocca**. 

## Sales
- **Flag:** <span style="color:red"><b>COMP6443{WhY_Ev3n_H4vE_A_l0g1n}</b></span><br>
- Details/Explanation:
  - Check the cookie of the website (`document.cookie="metadata=YWRtaW49MQ%3D%3D"`).
  - The hex value for **3D** is `=`. Therefore, the cookie is `YWRtaW49MQ==`, which looks like a **Base64** pattern. 
  - Decode it with Base64 gives **admin=0**. 
  - Encode **admin=1** with Base64, then overwrite the initial cookie with the encoded string. 
  - Refresh the webpage redirects to the admin account. 

## Files 2
- **Flag:** <span style="color:red"><b>COMP6443{St@ff_OnLY_Bey0nd_7hiS_P01n7_z5346077_WZMW+THBCeV5VjdcOlln}</b></span><br>
- Details/Explanation:
  - Register with random username and password. 
  - Create a new file and inspect the webpage. 
  - Check the **javascript files** which doesn't seem to appear on other webpages. 
  - In `app.d4309454.js` file, search for **staff** to get staff access from home.
  - To get access, go to `files.quoccabank.com/covid19/supersecret/lmao/grant_staff_access?username=adam`, but with the **registered username** instead of adam.
  - Back to the default page, there are three files which have been added to the account. 
  - The flag is in the *staff_super_secret_file*.

# Files 1
- **Flag:** <span style="color:red"><b>COMP6443{I_Luv_Id0R_z5346077_TD2lfzVFaJXYYHGHXvdI}</b></span><br>
- Details/Explanation:
  - Get the flag from the file, called *flag*.


## Files 3
- **Flag:** <span style="color:red"><b>COMP6443{L00k_@_me_I_am_Th3_ADm1n_N0w_v2_z5346077_z+jaODGxuhK1c82YY0//}</b></span><br>
- Details/Explanation:
  - Check the cookie of the webpage.
  - The session value has **Base64** pattern. Since there's a flask secret key in the **staff_flask_secret_key**, decode the session value with the secret key using `flask_session_cookie_manager`. 
  - The decoded string is `{'role': 'Staff', 'username': 'admin123'}`. Hence, changing the role and username to **admin** can get admin access. 
  - Encode `{"role": "Admin", "username":"admin"}` with the same secret key. 
  - Overwrite the initial cookie with the encoded string. 
  - Refresh the page and there's a new file added, called *nothing_to_see_here*. 

## Files 4
- **Flag:** <span style="color:red"><b>COMP6443{BrUt3_f0rCE_B35t_f0rCE_z5346077_W2/7Nnfofp+rYHib5Cg5}</b></span><br>
- Details/Explanation:
  - Go to `files.quoccabank.com/admin`. 
  - Since the access code is in 4 digits, brute force the access code, ranges from **0000-9999**, using `Burp Intruder`. 

## Blog 6
- **Flag:** <span style="color:red"><b>COMP6443{BrUt3_f0rCE_B35t_f0rCE_z5346077_W2/7Nnfofp+rYHib5Cg5}</b></span><br>
- Details/Explanation:
  - Try to search for other users by changing the author value (e.g. `blog.quoccabank.com/?author=2`). 
  - Inspect the HTTP history in Burp Proxy. Note that the title includes the username of the user. 
  - Try a few times with different authors. `author=5` corresponds to the **administrator**. 
  - Brute force the password using *2020-200_most_used_passwords.txt* by *SecLists*. 
  - After getting the correct password, login to get adminstrator access. The administrator can view all information, including posts, pages, comments and users. 
  - Check the **user** section to get the flag.


