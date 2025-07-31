from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path(__file__).resolve().parent.parent/"encryption_key.key"

if not KEY_FILE.exists():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

fernet = Fernet(key)

def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    try:
        return fernet.decrypt(value.encode()).decode()
    except Exception as e:
        print(f"[ERROR] 복호화 실패 : {e}")
        return""
