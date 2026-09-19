"""回滚迭代变量修改"""
import psycopg2, json

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'

ITER_ID = '1782725226412'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for row in cur.fetchall():
    wid, typ, ver, graph_str = row
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    
    modified = False
    
    # 修复迭代节点：删除 variable_selector
    for node in graph['nodes']:
        if node['id'] == ITER_ID and 'variable_selector' in node.get('data', {}):
            del node['data']['variable_selector']
            modified = True
            print(f"[{wid[:8]}] Removed variable_selector from iteration")
        
        # 修复子节点：回滚变量引用
        parent = node.get('parentId', '')
        if parent == ITER_ID and node['data'].get('type') == 'llm':
            for tpl in node['data'].get('prompt_template', []):
                text = tpl.get('text', '')
                changed = False
                if f'#{ITER_ID}.raw_jd_text#' in text:
                    text = text.replace(f'#{ITER_ID}.raw_jd_text#', '#1782704623626.raw_jd_text#')
                    changed = True
                if f'#{ITER_ID}.full_jd_text#' in text:
                    text = text.replace(f'#{ITER_ID}.full_jd_text#', '#1782786694136.full_jd_text#')
                    changed = True
                if changed:
                    tpl['text'] = text
                    modified = True
                    print(f"  [{node['data']['title']}] Reverted variable refs")
    
    if modified:
        new_graph = json.dumps(graph, ensure_ascii=False)
        cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))

conn.commit()
conn.close()
print("Done - reverted")
