"""
汽配云ERP完整爬虫 - Playwright已登录会话
直接使用work-frame提取菜单并导航爬取
"""

import os, re, json, time
from datetime import datetime
from playwright.sync_api import sync_playwright
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

CONFIG = {
    "output_root": r"D:\WorkProject\汽配云\数据库",
    "base_url": "https://erp.qpyun.cn/",
    "page_interval": 4,
    "timeout": 25,
    "save_html": True,
    "save_xlsx": True,
    "follow_pagination": True,
    "max_pages_per_item": 5,
    "progress_file": "crawl_progress.json",
}

HEADER_STYLE = {
    "font": Font(bold=True, size=11, color="FFFFFF"),
    "fill": PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid"),
    "alignment": Alignment(horizontal="center", vertical="center", wrap_text=True),
    "border": Border(left=Side("thin"), right=Side("thin"), top=Side("thin"), bottom=Side("thin")),
}

def sanitize(n):
    return re.sub(r'[<>:\"/\\|?*]', '_', n.strip())[:80]


def load_progress():
    p = os.path.join(CONFIG["output_root"], CONFIG["progress_file"])
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"done": [], "stats": {"done": 0, "fail": 0}}


def save_progress(prog):
    p = os.path.join(CONFIG["output_root"], CONFIG["progress_file"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)


def extract_menu_from_frame(frame):
    """从work-frame提取完整菜单树（精确版）"""
    html = frame.content()
    
    elements = []
    
    # 一级模块：span中的onclick有"return false;OpenChildPage(...)"
    for m in re.finditer(
        r'<span[^>]*onclick="return false;OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*>\s*([^<]+?)\s*(?:<a[^>]*>.*?</a>)?\s*<span[^>]*></span>\s*</span>',
        html
    ):
        elements.append({"type": "module", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    # 简化版：只匹配span文本，不过滤内部的a标签
    for m in re.finditer(
        r'<span[^>]*onclick="return false;OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*>(.*?)</span>',
        html
    ):
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and text not in [e["name"] for e in elements if e["type"] == "module"]:
            elements.append({"type": "module", "pos": m.start(), "url": m.group(1), "name": text})
    
    # 二级分类 h4 > a
    for m in re.finditer(
        r'<h4[^>]*>\s*<a[^>]*onclick="[^"]*OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*>\s*([^<]+?)\s*</a>',
        html
    ):
        elements.append({"type": "category", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    # 三级页面 a.frame-content-sidebarsublist-index
    for m in re.finditer(
        r'<a[^>]*onclick="OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*class="[^"]*frame-content-sidebarsublist-index[^"]*"[^>]*>\s*([^<]+?)\s*</a>',
        html
    ):
        elements.append({"type": "page", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    elements.sort(key=lambda x: x["pos"])
    
    # 建立层级
    results = []
    cur_mod = {"name": "", "url": ""}
    cur_cat = {"name": "", "url": ""}
    
    for el in elements:
        if el["type"] == "module":
            cur_mod = {"name": el["name"], "url": el["url"]}
            cur_cat = {"name": "", "url": ""}
        elif el["type"] == "category":
            cur_cat = {"name": el["name"], "url": el["url"]}
        elif el["type"] == "page":
            results.append({
                "module": cur_mod["name"],
                "category": cur_cat["name"] or el["name"],
                "page": el["name"],
                "url": el["url"]
            })
    
    # 也把自身有URL的h4作为叶子添加（如果没被上面的page覆盖）
    url_set = {r["url"] for r in results}
    cur_mod2 = {"name": "", "url": ""}
    for el in elements:
        if el["type"] == "module":
            cur_mod2 = {"name": el["name"], "url": el["url"]}
        elif el["type"] == "category" and el["url"] and el["url"] not in url_set:
            results.append({
                "module": cur_mod2["name"],
                "category": el["name"],
                "page": el["name"],
                "url": el["url"]
            })
            url_set.add(el["url"])
    
    return results


def extract_tables_from_html(html):
    """从HTML提取表格"""
    tables = []
    for m in re.finditer(r'<table[^>]*>(.*?)</table>', html, re.DOTALL):
        rows = []
        for trm in re.finditer(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.DOTALL):
            cells = []
            for tdm in re.finditer(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', trm.group(1), re.DOTALL):
                t = re.sub(r'<[^>]+>', '', tdm.group(1)).strip()
                t = re.sub(r'&nbsp;', ' ', t)
                t = re.sub(r'\s+', ' ', t)
                cells.append(t)
            if cells:
                rows.append(cells)
        if len(rows) > 1:
            tables.append({"rows": rows})
    return tables


def save_xlsx(tables, path):
    if not tables:
        return
    wb = Workbook()
    wb.remove(wb.active)
    for ti, t in enumerate(tables):
        ws = wb.create_sheet(title=f"Table{ti+1}"[:31])
        rows = t["rows"]
        if not rows:
            continue
        for ci, v in enumerate(rows[0], 1):
            c = ws.cell(1, ci, v)
            for k, val in HEADER_STYLE.items():
                setattr(c, k, val)
        for ri, row in enumerate(rows[1:], 2):
            for ci, v in enumerate(row, 1):
                c = ws.cell(ri, ci, v)
                c.alignment = Alignment(vertical="top", wrap_text=True)
                c.border = HEADER_STYLE["border"]
        for ci in range(1, len(rows[0]) + 1):
            mx = max((len(str(r[ci-1]) if ci <= len(r) else "")) for r in rows)
            ws.column_dimensions[ws.cell(1, ci).column_letter].width = min(mx * 2 + 4, 60)
    wb.save(path)


def get_pagination(html):
    pm = re.search(r'第\s*(\d+)\s*/\s*(\d+)\s*页', html)
    if pm:
        return {"has": True, "cur": int(pm.group(1)), "total": int(pm.group(2))}
    return {"has": False, "cur": 1, "total": 1}


def crawl_page(page, item, progress):
    """爬取单个页面"""
    url = item["url"]
    if not url.startswith("http"):
        url = CONFIG["base_url"] + url.lstrip("/")
    
    try:
        resp = page.request.get(url)
        if not resp.ok:
            print(f"  [!] HTTP {resp.status}")
            progress["stats"]["fail"] += 1
            save_progress(progress)
            return False
        html = resp.text()
    except Exception as e:
        print(f"  [!] {e}")
        progress["stats"]["fail"] += 1
        save_progress(progress)
        return False
    
    mod = sanitize(item.get("module", "?"))
    cat = sanitize(item.get("category", "?"))
    pg = sanitize(item.get("page", "?"))
    folder = os.path.join(CONFIG["output_root"], mod, cat, pg)
    os.makedirs(folder, exist_ok=True)
    
    extra = ""
    
    # 保存HTML
    if CONFIG["save_html"]:
        with open(os.path.join(folder, f"{pg}.html"), 'w', encoding='utf-8') as f:
            f.write(html)
    
    # 提取表格并保存XLSX
    if CONFIG["save_xlsx"]:
        tables = extract_tables_from_html(html)
        if tables:
            save_xlsx(tables, os.path.join(folder, f"{pg}.xlsx"))
            extra += f" [T:{len(tables)}]"
    
    # 分页
    if CONFIG["follow_pagination"]:
        pgi = get_pagination(html)
        if pgi["has"] and pgi["total"] > 1:
            tp = min(pgi["total"], CONFIG["max_pages_per_item"])
            extra += f" [P:1/{tp}]"
            for pn in range(2, tp + 1):
                # 构造分页URL
                pu = re.sub(r'([?&]page(?:no|index)?=)\d+', rf'\g<1>{pn}', url, flags=re.I)
                if pu == url:
                    pu = re.sub(r'([?&]p=)\d+', rf'\g<1>{pn}', url, flags=re.I)
                if pu != url:
                    try:
                        time.sleep(2)
                        r2 = page.request.get(pu)
                        if r2.ok:
                            h2 = r2.text()
                            if CONFIG["save_html"]:
                                with open(os.path.join(folder, f"{pg}_p{pn}.html"), 'w', encoding='utf-8') as f:
                                    f.write(h2)
                            if CONFIG["save_xlsx"]:
                                t2 = extract_tables_from_html(h2)
                                if t2:
                                    save_xlsx(t2, os.path.join(folder, f"{pg}_p{pn}.xlsx"))
                            extra += f" {pn}"
                    except:
                        break
    
    key = f"{item.get('module','')}\\{item.get('category','')}\\{item.get('page','')}"
    if key not in progress["done"]:
        progress["done"].append(key)
    progress["stats"]["done"] += 1
    save_progress(progress)
    
    print(extra, end="")
    return True


def main():
    print("=" * 60)
    print("  汽配云ERP爬虫 v6 (Playwright API请求)")
    print(f"  {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 60)
    
    os.makedirs(CONFIG["output_root"], exist_ok=True)
    progress = load_progress()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>false})")
        page = ctx.new_page()
        
        # 登录
        print("[1] 登录...")
        page.goto("https://login.qpyun.cn/logins/login", wait_until="networkidle")
        time.sleep(2)
        page.evaluate("document.getElementById('loginMobile')?.click()")
        time.sleep(1)
        page.fill('input[placeholder="请输入账号"]', "18609188315")
        page.fill('input[placeholder="请输入密码"]', "18609188315A")
        page.click('#btnLoginCommon')
        
        # 等待跳转
        for i in range(90):
            time.sleep(1)
            if "Reception.aspx" in page.url or "Main.aspx" in page.url:
                break
        time.sleep(5)
        
        # 如果没自动跳转，手动导航
        if "Main.aspx" not in page.url:
            page.goto("https://erp.qpyun.cn/AiWorkspace/Main.aspx?url=home.aspx", wait_until="networkidle")
            time.sleep(8)
        
        print(f"[2] 当前URL: {page.url[:80]}")
        
        # 提取菜单
        frame = page.frame(name="work-frame")
        if not frame:
            print("[!] 无work-frame")
            browser.close()
            return
        
        frame.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(3)
        
        menu = extract_menu_from_frame(frame)
        print(f"[3] 菜单: {len(menu)} 页")
        
        # 显示菜单结构
        mods = {}
        for item in menu:
            m = item.get("module", "?")
            mods.setdefault(m, []).append(item)
        for m, items in mods.items():
            cats = {}
            for it in items:
                cats[it.get("category", "?")] = cats.get(it.get("category", "?"), 0) + 1
            print(f"  [{m}] ({len(items)}页)")
            for c, n in cats.items():
                print(f"    - {c}: {n}页")
        
        # 保存菜单
        with open(os.path.join(CONFIG["output_root"], "menu_tree.json"), 'w', encoding='utf-8') as f:
            json.dump(menu, f, ensure_ascii=False, indent=2)
        
        # 开始爬取
        print(f"\n[4] 开始爬取 ({CONFIG['page_interval']}秒间隔)")
        total = len(menu)
        done_before = len(progress.get("done", []))
        progress["stats"]["total"] = total
        
        for i, item in enumerate(menu):
            key = f"{item.get('module','')}\\{item.get('category','')}\\{item.get('page','')}"
            if key in progress.get("done", []):
                continue
            
            ms = item.get('module', '?')[:8]
            cs = item.get('category', '?')[:8]
            ps = item.get('page', '?')[:25]
            
            print(f"[{i+1:>3}/{total}] {ms} > {cs} > {ps}", end="", flush=True)
            
            if crawl_page(page, item, progress):
                print(" [OK]")
            else:
                print(" [FAIL]")
            
            time.sleep(CONFIG["page_interval"])
        
        print(f"\n{'='*60}")
        print(f"[完成] 成功:{progress['stats']['done']} 失败:{progress['stats']['fail']}")
        print(f"  总计:{len(progress['done'])}/{total}")
        print(f"  输出:{CONFIG['output_root']}")
        print(f"{'='*60}")
        
        browser.close()


if __name__ == "__main__":
    main()
