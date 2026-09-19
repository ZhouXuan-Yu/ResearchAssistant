import subprocess, base64
from werkzeug.security import generate_password_hash

# 生成新密码哈希
new_password = '15939702654Tjl!'
raw_hash = generate_password_hash(new_password)
stored = base64.b64encode(raw_hash.encode()).decode()

# 写入文件
with open('/tmp/new_hash.txt', 'w') as f:
    f.write(stored)
print("Hash generated and saved")
