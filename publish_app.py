"""为 简历-招聘 app 创建 workflow draft + 发布 + API token"""
import psycopg2, json, uuid
from datetime import datetime, timezone

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

app_id = '2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc'
tenant_id = '50c15e0b-2bb9-4db6-9e7d-e61e75190c72'
now = datetime.now(timezone.utc).isoformat()

# 获取 chat draft 的 graph 和 features
cur.execute("SELECT graph, features FROM workflows WHERE app_id=%s AND version='draft' AND type='chat'", (app_id,))
row = cur.fetchone()
graph = row[0]
features = row[1] if row[1] else '{}'

print(f"Graph length: {len(graph)} bytes")

# 1. 创建 workflow type draft
wid_wf = str(uuid.uuid4())
cur.execute(
    "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    (wid_wf, tenant_id, app_id, 'workflow', 'draft', graph, features, tenant_id, now, '{}', '{}')
)
print(f"Workflow draft: {wid_wf[:8]}...")

# 2. 创建 published chat (用时间戳做version)
pub_ver = now
wid_pub = str(uuid.uuid4())
cur.execute(
    "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    (wid_pub, tenant_id, app_id, 'chat', pub_ver, graph, features, tenant_id, now, '{}', '{}')
)
print(f"Published chat: {wid_pub[:8]}... version={pub_ver}")

# 3. 创建 API token
import secrets
token_str = 'app-' + secrets.token_urlsafe(24)
token_id = str(uuid.uuid4())
cur.execute(
    "INSERT INTO api_tokens (id, app_id, token, created_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
    (token_id, app_id, token_str, now)
)
print(f"API Token: {token_str}")

conn.commit()
conn.close()
print("\nDone! 现在可以测试了")
