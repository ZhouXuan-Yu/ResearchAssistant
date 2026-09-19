import requests
import json

cookies = {}
with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\qpyun_cookies.txt','r') as f:
    for item in f.read().split(';'):
        if '=' in item:
            k,v = item.strip().split('=',1)
            cookies[k.strip()]=v.strip()

s = requests.Session()
s.cookies.update(cookies)
s.headers.update({'User-Agent': 'Mozilla/5.0'})
r = s.get('https://erp.qpyun.cn/home.aspx', timeout=10)
html = r.text

print(f"HTML length: {len(r.text)}")
print(f"URL: {r.url}")

# Save for inspection
with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\home_static.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Check for key JS elements
keywords = ['BtnLoadMenu', 'SelectMenuInFo', 'OpenChildPage', 'frame-content-sidebarlist', 'nav', 'loadMenu', 'getMenu', 'data-menu', 'menudata']
for kw in keywords:
    count = html.count(kw)
    print(f"  '{kw}': {count} occurrences")

# Check for script tags that might load menu
import re
scripts = re.findall(r'<script[^>]*src="([^"]+)"[^>]*>', html)
print(f"\nExternal scripts ({len(scripts)}):")
for s in scripts[:15]:
    print(f"  {s}")
