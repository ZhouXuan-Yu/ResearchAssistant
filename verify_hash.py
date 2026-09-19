import base64
from werkzeug.security import check_password_hash

stored_b64 = "c2NyeXB0OjMyNzY4Ojg6MSRWTUxqZGU1enU3bnZpdFFuJGM1NDNkZmYzOWI1YTFmNmViNGJhNGM2MWRhNmU3NDI0YjVjZWNkODk2NDc0NGNlMTVlNzE1OTFkNmYzNWZiNDI4YTFjOWI5NTQ4MDllODk4YTM2YjdlMTIwNWFiZDgxMTc5YzQ5YWFkODU4MThkYWI5ZTc2YWRlNjBhZmZhNTBl"
stored_hash = base64.b64decode(stored_b64).decode()

result = check_password_hash(stored_hash, '15939702654tjl!')
print("Password match:", result)
