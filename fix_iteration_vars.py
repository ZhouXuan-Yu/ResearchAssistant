"""
修复遍历候选人迭代内部节点的变量引用问题：
将 #1782704623626.raw_jd_text# 和 #1782786694136.full_jd_text# 
改为在迭代节点上声明 inputs，内部通过迭代节点 ID 引用
"""
import psycopg2, json, copy

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'
ITER_ID = '1782725226412'  # 遍历候选人

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s AND type='chat' AND version='draft'", (app_id,))
row = cur.fetchone()
wid, typ, ver, graph_str = row
graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str

iteration_node = None
for node in graph['nodes']:
    if node['id'] == ITER_ID and node['data'].get('type') == 'iteration':
        iteration_node = node
        break

if not iteration_node:
    print("ERROR: iteration node not found")
    conn.close()
    exit()

# 添加外部变量声明到迭代节点的 data 里
# Dify 迭代节点使用 variable_selector 来声明外部输入
iteration_node['data']['variable_selector'] = [
    ["1782786694136", "full_jd_text"],
    ["1782704623626", "raw_jd_text"]
]
print("Added variable_selector to iteration node")

# 修改迭代内部节点，将外部变量引用改为通过迭代节点
for node in graph['nodes']:
    parent = node.get('parentId', '')
    if parent == ITER_ID:
        title = node['data'].get('title', '')
        
        # 修改 LLM 节点的 prompt_template
        if node['data'].get('type') == 'llm':
            for tpl in node['data'].get('prompt_template', []):
                text = tpl.get('text', '')
                if '#1782704623626.raw_jd_text#' in text or '#1782786694136.full_jd_text#' in text:
                    # 改为通过迭代节点引用: #迭代ID.变量名#
                    text = text.replace('#1782704623626.raw_jd_text#', f'#{ITER_ID}.raw_jd_text#')
                    text = text.replace('#1782786694136.full_jd_text#', f'#{ITER_ID}.full_jd_text#')
                    tpl['text'] = text
                    print(f"  [{title}] Updated variable references")
        
        # 修改 HTTP 节点 (写回人才库) - 如果有引用外部变量
        elif node['data'].get('type') == 'http-request':
            body = node['data'].get('body', {})
            for item in body.get('data', []):
                val = item.get('value', '')
                if '#1782704623626.raw_jd_text#' in val or '#1782786694136.full_jd_text#' in val:
                    val = val.replace('#1782704623626.raw_jd_text#', f'#{ITER_ID}.raw_jd_text#')
                    val = val.replace('#1782786694136.full_jd_text#', f'#{ITER_ID}.full_jd_text#')
                    item['value'] = val
                    print(f"  [{title}] Updated body variable references")

# 也修改其他包含这些引用的节点（汇总报告等）
for node in graph['nodes']:
    if node['data'].get('type') == 'code':
        code = node['data'].get('code', '')
        # Code 节点的 variables 中可能有引用
        for var in node['data'].get('variables', []):
            sel = var.get('value_selector', [])
            # 不需要修改 Code 节点，它通过 variables 配置引用

# 写入数据库
new_graph = json.dumps(graph, ensure_ascii=False)
cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))

# 同时同步到其他3条记录
for rec_id, rec_typ, rec_ver in [
    ('bec8e8e5-5bf4-499f-8644-b294213e4945', 'workflow', 'draft'),
    ('53bd7d42-593a-4cd8-95e0-265b674b1492', 'chat', '2026-06-30 09:51:46.356316'),
    ('1902e292-ea91-4d25-8219-232ee4df7e64', 'workflow', '2026-06-30 09:51:46.356316'),
]:
    cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, rec_id))

conn.commit()
conn.close()
print("\nDone! All 4 workflow records updated.")
print("Changes: iteration now declares external inputs,")
print("child nodes reference via #1782725226412.变量名#")
