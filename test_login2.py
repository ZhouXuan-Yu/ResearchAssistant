"""
最快测试：登录+菜单提取
"""
import time, json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
    ctx = browser.new_context(viewport={"width":1920,"height":1080})
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>false})")
    
    page = ctx.new_page()
    page.goto("https://login.qpyun.cn/logins/login", wait_until="networkidle")
    time.sleep(2)
    
    # 切换密码登录
    page.evaluate("document.getElementById('loginMobile')?.click()")
    time.sleep(1)
    
    # 截图看状态
    page.screenshot(path=r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\debug1_after_switch.png")
    
    # 用type模拟键盘输入
    acct = page.locator('input[placeholder="请输入账号"]')
    acct.click()
    time.sleep(0.2)
    acct.fill("18609188315")
    time.sleep(0.2)
    
    pwd = page.locator('input[placeholder="请输入密码"]')
    pwd.click()
    time.sleep(0.2)
    pwd.fill("18609188315A")
    
    page.screenshot(path=r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\debug2_after_fill.png")
    
    # 检查按钮
    btn = page.locator('#btnLoginCommon')
    print(f"按钮可见: {btn.is_visible()}")
    print(f"按钮文本: {btn.inner_text()}")
    print(f"URL: {page.url}")
    
    # 直接用evaluate触发登录
    print("尝试JS提交...")
    page.evaluate("""
        if (typeof ValidateForm === 'function') {
            ValidateForm();
        } else if (document.getElementById('btnLoginCommon')) {
            document.getElementById('btnLoginCommon').click();
        }
    """)
    
    # 等待跳转
    for i in range(60):
        time.sleep(1)
        url = page.url
        if i % 10 == 0:
            print(f"[{i}s] {url[:80]}")
        if "Main.aspx" in url or "Reception.aspx" in url:
            print(f"[+] 跳转成功! 用时{i}s")
            break
    
    print(f"最终URL: {page.url}")
    page.screenshot(path=r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\debug3_final.png")
    
    if "Main.aspx" in page.url:
        time.sleep(5)
        frame = page.frame(name="work-frame")
        if frame:
            html = frame.content()
            with open(r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\home_full.html",'w',encoding='utf-8') as f:
                f.write(html)
            print(f"HTML: {len(html)} 字节")
            
            urls = frame.evaluate("""()=>{
                const links=document.querySelectorAll('[onclick*="OpenChildPage"]');
                const r=[];
                links.forEach(l=>{
                    const oc=l.getAttribute('onclick');
                    const s=oc.indexOf("OpenChildPage('");
                    if(s>=0){
                        const ue=oc.indexOf("'",s+16);
                        if(ue>s)r.push({url:oc.substring(s+16,ue),text:l.innerText.trim().substring(0,30)});
                    }
                });
                return r;
            }""")
            with open(r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\menu_urls.json",'w',encoding='utf-8') as f:
                json.dump(urls,f,ensure_ascii=False,indent=2)
            print(f"URLs: {len(urls)}")
            for u in urls[:20]:
                print(f"  {u['text'][:20]} -> {u['url'][:60]}")
    
    browser.close()
