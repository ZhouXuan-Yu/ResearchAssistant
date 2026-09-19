"""修复 匹配打分 节点: 添加候选人姓名到user prompt"""
import psycopg2, json

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = 'f229fc82-992d-4de1-8d75-4ed76c0e9730'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for wid, typ, ver, graph_str in cur.fetchall():
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    modified = False
    
    for node in graph['nodes']:
        if node['data'].get('type') == 'llm' and node['data'].get('title') == '匹配打分':
            for tpl in node['data'].get('prompt_template', []):
                if tpl.get('role') == 'user':
                    old = tpl['text']
                    # 在用户提示中加入候选人姓名
                    if '候选人全维度' in old and 'item.name' not in old:
                        tpl['text'] = '【候选人姓名】{{#1782725226412.item.name#}}\n' + old
                        modified = True
                        print(f"  [匹配打分] Added candidate name to user prompt")
    
    if modified:
        new_graph = json.dumps(graph, ensure_ascii=False)
        cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))
        print(f"  Updated {wid[:8]}")

conn.commit()
conn.close()
print("Done")
