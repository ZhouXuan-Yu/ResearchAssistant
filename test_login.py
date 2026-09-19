"""最小登录测试"""
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
    )
    ctx = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: ()=>false})")
    
    page = ctx.new_page()
    page.goto("https://login.qpyun.cn/logins/login", wait_until="networkidle")
    time.sleep(2)
    
    # 切换密码登录
    page.evaluate("document.getElementById('loginMobile')?.click()")
    time.sleep(1)
    
    # 填写
    page.fill('input[placeholder="请输入账号"]', "18609188315")
    page.fill('input[placeholder="请输入密码"]', "18609188315A")
    
    # 点击登录
    print("点击登录...")
    page.click('#btnLoginCommon')
    
    # 打印URL变化
    for i in range(60):
        time.sleep(1)
        url = page.url
        print(f"[{i+1}s] {url[:100]}")
        if "Main.aspx" in url:
            print("成功！")
            break
        if "Reception.aspx" in url and i > 10 and i % 5 == 0:
            # 检查是否有跳转
            print("  检查页面...")
            page.evaluate("console.log('page title: ' + document.title)")
    
    print(f"最终URL: {page.url}")
    input("按回车关闭...")
    browser.close()
