import requests, base64

s = requests.Session()

# 获取 CSRF token
r = s.get('http://localhost/console/api/system-features')
csrf = s.cookies.get('csrf_token', '')
print(f'CSRF: {csrf[:20] if csrf else "none"}')

# Base64 编码密码
password_b64 = base64.b64encode('123456'.encode()).decode()

login_data = {
    'email': '1241515924@qq.com',
    'password': password_b64,
    'remember_me': True
}

r2 = s.post('http://localhost/console/api/login',
    json=login_data,
    headers={'X-CSRF-Token': csrf}
)
print(f'Login status: {r2.status_code}')
print(f'Response: {r2.text[:300]}')
