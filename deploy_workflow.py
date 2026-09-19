"""
将 HR.yml 工作流部署到 Dify 数据库，替换当前 draft
"""
import yaml, json, psycopg2, uuid
from datetime import datetime, timezone

# 读取工作流定义
with open('/tmp/HR_deploy.yml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

workflow = data['workflow']
graph = workflow['graph']
features = workflow['features']

# 验证和修正
http_count = 0
for node in graph['nodes']:
    t = node['data'].get('type', '')
    if t == 'http-request':
        http_count += 1
        url = node['data'].get('url', '')
        print(f"[HTTP节点] 当前URL: {url}")
        # 确保使用正确的端点
        if '/api/v1/emails' in url:
            node['data']['url'] = 'http://host.docker.internal:8899/api/v1/extractions?per_page=50'
            print(f"  -> 修正为: {node['data']['url']}")
        elif '/api/v1/extractions' in url:
            print(f"  -> URL已正确 ✓")
        elif '/api/v1/crawl' in url:
            print(f"  -> crawl端点，保持不变 ✓")
    elif t == 'llm':
        model_name = node['data'].get('model', {}).get('name', '')
        print(f"[LLM节点] 模型: {model_name}")

graph_json = json.dumps(graph, ensure_ascii=False)
features_json = json.dumps(features, ensure_ascii=False)

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

now = datetime.now(timezone.utc).isoformat()
tenant_id = '50c15e0b-2bb9-4db6-9e7d-e61e75190c72'
app_id = '22b49776-b615-4a49-bd26-bd5ca8454d5e'

# 删除旧的draft
cur.execute("DELETE FROM workflows WHERE app_id=%s AND version='draft'", (app_id,))
print(f"[DB] 清理旧draft: {cur.rowcount} 条")

# 插入新的 workflow draft + chat draft
for (typ,) in [('workflow',), ('chat',)]:
    wid = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (wid, tenant_id, app_id, typ, 'draft', graph_json, features_json, tenant_id, now, '{}', '{}')
    )
    print(f"[DB] 插入 {typ} draft: {wid[:8]}...")

conn.commit()
conn.close()
print("\n[DONE] 工作流已部署到数据库")
print("请在 Dify 中点击「发布更新」以发布新版本")
