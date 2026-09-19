import subprocess

new_hash = "c2NyeXB0OjMyNzY4Ojg6MSRWTUxqZGU1enU3bnZpdFFuJGM1NDNkZmYzOWI1YTFmNmViNGJhNGM2MWRhNmU3NDI0YjVjZWNkODk2NDc0NGNlMTVlNzE1OTFkNmYzNWZiNDI4YTFjOWI5NTQ4MDllODk4YTM2YjdlMTIwNWFiZDgxMTc5YzQ5YWFkODU4MThkYWI5ZTc2YWRlNjBhZmZhNTBl"

sql = f"UPDATE accounts SET password = '{new_hash}', updated_at = NOW() WHERE email = '1241515924@qq.com'"

result = subprocess.run(
    ["docker", "exec", "-i", "docker-db_postgres-1", "psql", "-U", "postgres", "-d", "dify", "-c", sql],
    capture_output=True, text=True, timeout=10
)
print(result.stdout)
if result.stderr:
    print("ERR:", result.stderr[:200])

# Clear rate limit
result2 = subprocess.run(
    ["docker", "exec", "docker-redis-1", "redis-cli", "DEL", "login_error_rate_limit:1241515924@qq.com"],
    capture_output=True, text=True, timeout=5
)
print("Rate limit:", result2.stdout.strip())
