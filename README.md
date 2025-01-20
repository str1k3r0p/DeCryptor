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
If you are facing errors while installing the required dependencies, you can convert this tool to an exe file using ## **PyInstaller**
Install _pyinstaller_ in your system using the following command.
```bash
pip install pyinstaller
```
Now run
```bash
pyinstaller --onefile --windowed path/to/file/Decrytor.py
```
Make sure you give the correct path for the file "Decrytor.py"
The script will process each browser and output the decrypted passwords to `decrypted_password.csv`.

### CSV Output Format
| Index | Browser | URL         | Username | Password | User |
|-------|---------|------------ |----------|----------|------|
| 0     | chrome  | example.com | user1    | pass1    | MachineUser |
| 1     | firefox | example.org | user2    | pass2    | MachineUser |

## Security Warning
This tool accesses sensitive data and decrypts saved passwords. Use it responsibly and only on systems where you have appropriate permissions. Unauthorized access to personal data may be illegal.

## License
This project is open-source and distributed under the MIT License. Please refer to the LICENSE file for full terms and conditions.

## Disclaimer
The authors are not responsible for any misuse of this tool. It is intended for educational and ethical purposes only.

