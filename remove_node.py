"""
删除"写回人才库"节点及其连线。
该节点引用了不存在的 candidate_id 变量且实际在线程中是独立的非关键路径。
"""
import psycopg2, json

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'
NODE_ID = '1782727096984'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for row in cur.fetchall():
    wid, typ, ver, graph_str = row
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    
    # 删除节点
    graph['nodes'] = [n for n in graph['nodes'] if n['id'] != NODE_ID]
    
    # 删除相关连线
    graph['edges'] = [e for e in graph['edges'] 
                      if e['source'] != NODE_ID and e['target'] != NODE_ID]
    
    new_graph = json.dumps(graph, ensure_ascii=False)
    cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))
    print(f"Updated {wid[:8]} ({typ}/{ver}) - removed 写回人才库")

conn.commit()
conn.close()
print("\nDone! Refreshing browser will show clean checklist.")
