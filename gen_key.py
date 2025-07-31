from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("🔐 아래 값을 복사해서 .env에 넣으세요:")
print(f"ENCRYPTION_KEY={key.decode()}")