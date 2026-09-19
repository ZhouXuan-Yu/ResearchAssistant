"""直接在 Dify API 容器内运行：重置密码 + 创建登录会话"""
import sys
sys.path.insert(0, '/app/api')

# 导入 Dify 内部模块
from werkzeug.security import generate_password_hash
import base64

# 1. 生成简单密码的哈希
new_pwd = '123456'
raw_hash = generate_password_hash(new_pwd)
encoded = base64.b64encode(raw_hash.encode()).decode()
print(f"New hash for '123456': {encoded[:50]}...")

# 2. 更新数据库
import psycopg2
conn = psycopg2.connect(
    host='docker-db_postgres-1',
    database='dify',
    user='postgres',
    password='difyai123456'
)
cur = conn.cursor()
cur.execute("UPDATE accounts SET password = %s, name = 'admin', updated_at = NOW() WHERE email = '1241515924@qq.com'", (encoded,))
conn.commit()
print(f"Updated: {cur.rowcount} row(s)")

# 验证
cur.execute("SELECT email, name, password FROM accounts WHERE email = '1241515924@qq.com'")
row = cur.fetchone()
print(f"Account: {row[0]}, name={row[1]}, hash={row[2][:40]}...")

cur.close()
conn.close()
print("DONE")
