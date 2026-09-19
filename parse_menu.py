"""
从保存的home_full.html中精确提取菜单树 + 直接爬取
"""
import re, json, os, time
from playwright.sync_api import sync_playwright

# ============================================================
# 1. 从HTML中精确解析菜单
# ============================================================
def parse_menu_from_html(html):
    """从完整HTML中解析菜单层级"""
    results = []
    
    # 提取所有带有OpenChildPage的onclick
    pattern = re.compile(r"OpenChildPage\('([^']+)'[^)]*\)")
    
    # 找所有带onclick的元素，确定它们的类型和层级
    # 使用位置关系来确定层级
    
    elements = []
    
    # 一级模块
    for m in re.finditer(r'<span[^>]*onclick="[^"]*OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*>\s*([^<]+?)\s*</span>', html):
        elements.append({"type": "module", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    # 二级分类 (h4中的a)
    for m in re.finditer(r'<h4[^>]*>\s*<a[^>]*onclick="[^"]*OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*>\s*([^<]+?)\s*</a>', html):
        elements.append({"type": "category", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    # 三级页面
    for m in re.finditer(r'<a[^>]*onclick="OpenChildPage\(\'([^\']+)\'[^)]*\)[^"]*"[^>]*class="[^"]*frame-content-sidebarsublist-index[^"]*"[^>]*>\s*([^<]+?)\s*</a>', html):
        elements.append({"type": "page", "pos": m.start(), "url": m.group(1), "name": m.group(2).strip()})
    
    elements.sort(key=lambda x: x["pos"])
    
    current_module = {"name": "", "url": ""}
    current_category = {"name": "", "url": ""}
    
    for el in elements:
        if el["type"] == "module":
            current_module = {"name": el["name"], "url": el["url"]}
            current_category = {"name": "", "url": ""}
        elif el["type"] == "category":
            current_category = {"name": el["name"], "url": el["url"]}
        elif el["type"] == "page":
            results.append({
                "module": current_module["name"],
                "category": current_category["name"] or el["name"],
                "page": el["name"],
                "url": el["url"]
            })
    
    return results

# ============================================================
# 2. 主爬虫
# ============================================================
def main():
    with open(r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\home_full.html", 'r', encoding='utf-8') as f:
        html = f.read()
    
    pages = parse_menu_from_html(html)
    print(f"解析到 {len(pages)} 个页面")
    
    # 检查URL完整性
    bad_urls = [p for p in pages if not p['url'].startswith(('http', 'Sale', 'Stock', 'Purchase', 'common', 'sale', 'stock', 'purchase', 'report', '/', 'workflow'))]
    print(f"可能异常的URL: {len(bad_urls)}")
    for p in bad_urls[:10]:
        print(f"  {p['module']} > {p['category']} > {p['page']}: [{p['url']}]")
    
    # 保存完整菜单
    out = r"D:\WorkProject\汽配云\数据库"
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "menu_tree.json"), 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    # 按模块统计
    modules = {}
    for p in pages:
        m = p.get("module", "?")
        modules.setdefault(m, []).append(p)
    
    print(f"\n模块统计:")
    for mod, items in modules.items():
        cats = {}
        for item in items:
            cats[item.get("category","?")] = cats.get(item.get("category","?"), 0) + 1
        print(f"  [{mod}] ({len(items)}页)")
        for c, cnt in cats.items():
            print(f"    - {c}: {cnt}页")
    
    return pages

if __name__ == "__main__":
    pages = main()
    print(f"\n总计: {len(pages)} 页")
