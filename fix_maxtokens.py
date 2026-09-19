"""修复 LLM 节点 max_tokens"""
import psycopg2, json

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = 'f229fc82-992d-4de1-8d75-4ed76c0e9730'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for wid, typ, ver, graph_str in cur.fetchall():
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    modified = False
    
    for node in graph['nodes']:
        if node['data'].get('type') == 'llm':
            title = node['data'].get('title', '')
            params = node['data'].get('model', {}).get('completion_params', {})
            mt = params.get('max_tokens', 0)
            if title in ('匹配打分', '画像标签') and mt < 4096:
                node['data']['model']['completion_params']['max_tokens'] = 4096
                modified = True
                print(f"  [{title}] max_tokens: {mt} → 4096")
    
    if modified:
        new_graph = json.dumps(graph, ensure_ascii=False)
        cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))
        print(f"Updated {wid[:8]}")

conn.commit()
conn.close()
print("Done")
