import base64
from werkzeug.security import check_password_hash, generate_password_hash

new = generate_password_hash('15939702654tjl!')
print("New hash:", new[:50])

ok = check_password_hash(new, '15939702654tjl!')
print("Self-check:", ok)

b64 = base64.b64encode(new.encode()).decode()
decoded = base64.b64decode(b64).decode()
print("Roundtrip:", decoded[:50])
ok2 = check_password_hash(decoded, '15939702654tjl!')
print("Roundtrip-check:", ok2)
