from cryptography.fernet import Fernet
import os

# 암호화 키 파일
KEY_FILE = "encryption_key.key"

# 키가 없다면 생성
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

# 키 로딩
with open(KEY_FILE, "rb") as f:
    key = f.read()

fernet = Fernet(key)

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
