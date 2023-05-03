# Mid-Term

## q1
### Flag: COMP6443MIDTERM{d3v_S1T32_Ne3D_G0od_p4sSwOrdz}
1. Check robots.txt
2. Go to https://q1.midterm.quoccabank.com/dev
3. Brute force password for username=admin

## q2
1. Create account using username=admin and password=admin123
2. Log in and clink the 'flag' hyperlink.
3. Check cookie, which is user=admin
4. Since I'm not granted the rank 'senate', I attempted to overwrite or add cookie with 'user=senate', 'rank='senate' and  'role=senate'

## q3
1. Check cookie and the cookie is in base64
2. Decode it using flask session
3. Possible solutions: Encode it with a different alagorithm


