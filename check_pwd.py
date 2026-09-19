import sys
sys.path.insert(0, '/app/api')
from werkzeug.security import check_password_hash
import base64
import psycopg2

conn = psycopg2.connect(host='docker-db_postgres-1', database='dify', user='postgres', password='difyai123456')
cur = conn.cursor()
cur.execute("SELECT password FROM accounts WHERE email = '1241515924@qq.com'")
row = cur.fetchone()
stored_b64 = row[0]
stored_hash = base64.b64decode(stored_b64).decode()

print(f"Stored hash: {stored_hash[:60]}...")

for pwd in ['123456', '15939702654tjl!', 'admin', '12345678']:
    ok = check_password_hash(stored_hash, pwd)
    print(f"  {pwd}: {ok}")

cur.close()
conn.close()
