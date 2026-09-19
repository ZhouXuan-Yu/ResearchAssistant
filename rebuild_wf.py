import yaml, json, psycopg2, uuid
from datetime import datetime

with open('/tmp/original.yml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
workflow = data['workflow']

graph = workflow['graph']
features = workflow['features']

# Update Code node
for node in graph['nodes']:
    if node['data'].get('type') == 'code':
        node['data']['code'] = '''import json

def main(arg1: str):
    """Parse extractions API response"""
    try:
        if isinstance(arg1, bytes):
            arg1 = arg1.decode("utf-8")
        data = json.loads(arg1) if isinstance(arg1, str) else arg1
    except Exception:
        return {"result": json.dumps({"error": "parse failed", "candidates": []}, ensure_ascii=False)}
    items = data.get("items", [])
    if not items:
        return {"result": json.dumps({"total": 0, "candidates": []}, ensure_ascii=False)}
    candidates = []
    for item in items:
        d = item.get("data", {})
        raw = item.get("raw_text", "")
        candidates.append({
            "name": d.get("name", ""),
            "phone": d.get("phone", ""),
            "email": d.get("email", ""),
            "education": d.get("education", {}),
            "experience": d.get("experience", {}),
            "skills": d.get("skills", []),
            "raw_text": raw[:3000]
        })
    return {"result": json.dumps({"total": len(candidates), "candidates": candidates}, ensure_ascii=False)}'''

    # Update HTTP URL
    if node['data'].get('type') == 'http-request':
        node['data']['url'] = 'http://host.docker.internal:8899/api/v1/extractions?per_page=50'

    # Update LLM prompt
    if node['data'].get('type') == 'llm':
        for tpl in node['data'].get('prompt_template', []):
            if tpl.get('role') == 'system':
                tpl['text'] = '你是一个HR简历筛选助手。默认输出核心简报。\n\n## 核心简报（默认）\n| # | 候选人 | 匹配方向 | 核心技能 | 亮点 | 风险 | 评分 | 建议 |\n|---|--------|---------|---------|------|------|------|------|\n\n按评分从高到低排列。7分以上建议面试。\n\n## 其他模式\n- 对比："对比A和B"\n- 岗位匹配："谁适合XX岗位"\n\n简洁专业，老板10秒看完。'

graph_json = json.dumps(graph, ensure_ascii=False)
features_json = json.dumps(features, ensure_ascii=False)

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
now = datetime.utcnow().isoformat()
draft_id = str(uuid.uuid4())
pub_id = str(uuid.uuid4())
pub_ver = now

cur.execute(
    "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    (draft_id, '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', '22b49776-b615-4a49-bd26-bd5ca8454d5e', 'workflow', 'draft', graph_json, features_json, '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', now, '{}', '{}')
)
cur.execute(
    "INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, updated_at, environment_variables, conversation_variables) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    (pub_id, '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', '22b49776-b615-4a49-bd26-bd5ca8454d5e', 'workflow', pub_ver, graph_json, features_json, '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', now, '{}', '{}')
)
conn.commit()
print("DONE. Draft:", draft_id, "Published:", pub_id)
conn.close()
