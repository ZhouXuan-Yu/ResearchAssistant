"""从 fixed_workflow.yml 恢复工作流到数据库"""
import json, yaml, psycopg2, uuid
from datetime import datetime, timezone

with open('/tmp/fixed_workflow.yml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

graph = data['workflow']['graph']
features = data['workflow']['features']

graph_json = json.dumps(graph, ensure_ascii=False)
features_json = json.dumps(features, ensure_ascii=False)

print(f"Graph: {len(graph_json)} bytes, {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'
tenant_id = '50c15e0b-2bb9-4db6-9e7d-e61e75190c72'
now = datetime.now(timezone.utc).isoformat()

# 删除所有旧记录
cur.execute("DELETE FROM workflows WHERE app_id=%s", (app_id,))
print(f"Deleted {cur.rowcount} old records")

# 插入4条新记录
records = [
    ('workflow', 'draft'),
    ('chat', 'draft'),
    ('workflow', now),
    ('chat', now),
]
for typ, ver in records:
    wid = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (wid, tenant_id, app_id, typ, ver, graph_json, features_json, tenant_id, now, '{}', '{}')
    )
    print(f"  {typ}/{ver}: {wid[:8]}...")

# 更新apps表的workflow_id指向已发布的chat版本
cur.execute("SELECT id FROM workflows WHERE app_id=%s AND type='chat' AND version=%s", (app_id, now))
pub_id = cur.fetchone()[0]
cur.execute("UPDATE apps SET workflow_id=%s, updated_at=NOW() WHERE id=%s", (pub_id, app_id))
print(f"App workflow_id → {pub_id[:8]}...")

conn.commit()
conn.close()
print("\nDone! 刷新浏览器即可。")
