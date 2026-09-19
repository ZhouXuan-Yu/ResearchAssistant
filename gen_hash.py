import hashlib, binascii, base64, secrets

def hash_password(password_str, salt_byte):
    dk = hashlib.pbkdf2_hmac('sha256', password_str.encode('utf-8'), salt_byte, 10000)
    return binascii.hexlify(dk)

password = '123456'
salt = secrets.token_bytes(16)

hashed = hash_password(password, salt)
hashed_b64 = base64.b64encode(hashed).decode()
salt_b64 = base64.b64encode(salt).decode()

print(f"Password hash: {hashed_b64}")
print(f"Salt: {salt_b64}")
