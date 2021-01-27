'''import hashlib

password = str(input())
h = hashlib.md5(password.encode())
p = h.hexdigest()
# Пароль, сохраненный в базе '5f4dcc3b5aa765d61d8327deb882cf99'
h2 = hashlib.md5(b"password")   # Пароль, введенный пользователем
if p == h2.hexdigest():
    print("Пароль правильный")'''

import base64
from cryptography.fernet import Fernet

# Шифруем

#get key
s = 'resu94'
s = s + ('y'*(32 - len(s)))
b = s.encode("UTF-8")
cipher_key = base64.b64encode(b)
cipher = Fernet(cipher_key)
text = b'1234'
encrypted_text = cipher.encrypt(text)
print(encrypted_text)
print("\n")



# Дешифруем
decrypted_text = cipher.decrypt(encrypted_text)
print(decrypted_text)

#cipher_key = b'cmVzdTk0eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXk='

#gAAAAABfSiIt5MtzjLSapViWD0DBetWG-yZORXkN8C6uXNeq-lWs6JrtJCGr1TEvur_RrJRgPdcSWwJl4ihICdsQu8Y69tn58Q==
#hashedpass = gAAAAABfSRzRMabNiXJnldtejmJZLyRLepDHqzIIgPOEtKtObmK4J6OlAa4QSa5-V2yU1rZ4XWGf28b3lp7mzCojOScIK5noNQ
#bhashedpass = b'gAAAAABfSRzRMabNiXJnldtejmJZLyRLepDHqzIIgPOEtKtObmK4J6OlAa4QSa5-V2yU1rZ4XWGf28b3lp7mzCojOScIK5noNQ'
#через регистрацию
#cipher_key = b'cmVzdTk0eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXk='
#encrypted_text = b'gAAAAABfSiO42vX95VBiTAP7_D5gPbetBq3qs52qd7kEghUdTc-tfcRUEWF8FmCCle-j8wnq4LEZKqddpmXO7G_Nmz-yf8jmIg=='

