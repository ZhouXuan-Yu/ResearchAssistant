"""导出修复后的工作流为 YAML"""
import json, yaml, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
cur.execute("SELECT graph, features FROM workflows WHERE app_id=%s AND type='chat' AND version='draft'",
            ('2b6abe8a-ec4e-4ecc-9074-ef280b3cbacc',))
graph, features = cur.fetchone()

if isinstance(graph, str):
    graph = json.loads(graph)
if isinstance(features, str):
    features = json.loads(features)

output = {
    'app': {
        'description': 'HR简历筛选助手 - 自动拉取邮件、解析简历、AI评估打分',
        'icon': '🤖',
        'icon_background': '#FFEAD5',
        'mode': 'advanced-chat',
        'name': '简历-招聘'
    },
    'workflow': {
        'graph': graph,
        'features': features
    }
}

with open('/tmp/fixed_workflow.yml', 'w', encoding='utf-8') as f:
    yaml.dump(output, f, allow_unicode=True, default_flow_style=False)

print(f"Exported: {len(json.dumps(graph))} bytes graph")
conn.close()
