import json, uuid, subprocess, yaml

with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'r', encoding='utf-8') as f:
    dsl = yaml.safe_load(f)

app_id = str(uuid.uuid4())
wf_id = str(uuid.uuid4())
tenant_id = '50c15e0b-2bb9-4db6-9e7d-e61e75190c72'
account_id = 'cab519a5-f98d-46b7-ac77-17021c576797'

graph = json.dumps(dsl['workflow']['graph'], ensure_ascii=False)
features = json.dumps(dsl['workflow'].get('features', {}), ensure_ascii=False)
env_vars = json.dumps(dsl['workflow'].get('environment_variables', []), ensure_ascii=False)

def esc(s):
    return s.replace("'", "''")

app_name = esc(dsl['app']['name'])
app_desc = esc(dsl['app'].get('description', ''))

sql = f"""INSERT INTO apps (id, tenant_id, name, mode, icon, icon_background, description, enable_site, enable_api, max_active_requests, created_by, maintainer, updated_by)
VALUES ('{app_id}', '{tenant_id}', '{app_name}', 'workflow', '📄', '#FFD93D', '{app_desc}', true, true, 0, '{account_id}', '{account_id}', '{account_id}');

INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, environment_variables, conversation_variables, created_by, updated_by, marked_name, marked_comment, rag_pipeline_variables, created_at, updated_at)
VALUES ('{wf_id}', '{tenant_id}', '{app_id}', 'workflow', 'draft', '{esc(graph)}', '{esc(features)}', '{esc(env_vars)}', '{{}}', '{account_id}', '{account_id}', '', '', '{{}}', NOW(), NOW());
"""

r = subprocess.run(['docker', 'exec', '-i', 'docker-db_postgres-1', 'psql', '-U', 'postgres', '-d', 'dify'], 
                   input=sql, capture_output=True, text=True, timeout=10)
print(r.stdout)
if r.stderr:
    print('ERR:', r.stderr[:300])
print(f'\nApp ID: {app_id}')
print(f'URL: http://localhost/app/{app_id}/workflow')
