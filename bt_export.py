import requests, json, re, sys

urllib3 = __import__('urllib3')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = 'https://122.114.92.45:29604/a0bff468'
s = requests.Session()

# Try different paths
paths = ['', '/login', '/', '/index', '/index.html', '/panel', '/api']
for path in paths:
    try:
        r = s.get(f'{BASE}{path}', verify=False, timeout=10)
        print(f"GET {path} -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 100:
            print(f"    First 300 chars: {r.text[:300]}")
            print()
    except Exception as e:
        print(f"GET {path} -> Error: {e}")
