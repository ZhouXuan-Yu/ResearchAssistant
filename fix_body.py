"""修复 拉取邮件 和 获取候选人 节点的 body 配置"""
import psycopg2, json

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'

# 获取所有workflow
cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for row in cur.fetchall():
    wid, typ, ver, graph_str = row
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    
    modified = False
    for node in graph.get('nodes', []):
        if node['data'].get('type') == 'http-request':
            title = node['data'].get('title', '')
            body = node['data'].get('body', {})
            body_type = body.get('type', '')
            body_data = body.get('data', [])
            
            # 如果是 json 类型且 data 为空，改为 none
            if body_type == 'json' and len(body_data) == 0:
                node['data']['body'] = {'type': 'none', 'data': []}
                modified = True
                print(f"  [{title}] body: json+empty → none")
            
            url = node['data'].get('url', '')
            if 'host.docker.internal' in url:
                node['data']['url'] = url.replace('host.docker.internal:8899', 'email-gateway:8899')
                modified = True
                print(f"  [{title}] URL fixed → {node['data']['url']}")
    
    if modified:
        new_graph = json.dumps(graph, ensure_ascii=False)
        cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))
        print(f"Updated {wid[:8]} ({typ}/{ver})")

conn.commit()
conn.close()
print("\nDone!")
