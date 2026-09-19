"""简化版：直接操作 DB + 绕过 Flask context"""
import sys, yaml, json, uuid, time
sys.path.insert(0, '/app/api')

from extensions.ext_database import db
from models.model import App, Account
from models.workflow import Workflow
from models.account import Tenant, TenantAccountJoin
from flask import Flask

# 创建最小 Flask app 以初始化 db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:difyai123456@docker-db_postgres-1:5432/dify'
db.init_app(app)

with app.app_context():
    # 获取数据
    tenant = db.session.query(Tenant).first()
    account = db.session.query(Account).filter(Account.email == '1241515924@qq.com').first()
    print(f"Tenant: {tenant.id}, Account: {account.id}")
    
    # 读取 YAML
    with open('/tmp/workflow.yml', 'r', encoding='utf-8') as f:
        yaml_content = f.read()
    dsl = yaml.safe_load(yaml_content)
    
    # 创建 app
    app_id = str(uuid.uuid4())
    new_app = App(
        id=app_id,
        tenant_id=tenant.id,
        name=dsl['app']['name'],
        mode=dsl['app']['mode'],
        icon=dsl['app'].get('icon', '\U0001f4c4'),
        icon_background=dsl['app'].get('icon_background', '#FFD93D'),
        description=dsl['app'].get('description', ''),
        enable_site=True,
        enable_api=True,
        max_active_requests=0,
        tracing=None,
        created_by=account.id,
        maintainer=account.id,
        updated_by=account.id,
    )
    db.session.add(new_app)
    db.session.flush()
    
    # 创建 workflow
    graph = dsl['workflow']['graph']
    features = dsl['workflow'].get('features', {})
    
    wf = Workflow(
        tenant_id=tenant.id,
        app_id=app_id,
        type='workflow',
        version='draft',
        graph=json.dumps(graph, ensure_ascii=False),
        features=json.dumps(features, ensure_ascii=False),
        environment_variables=json.dumps(dsl['workflow'].get('environment_variables', []), ensure_ascii=False),
        conversation_variables=json.dumps(dsl['workflow'].get('conversation_variables', []), ensure_ascii=False),
        created_by=account.id,
        updated_by=account.id,
    )
    db.session.add(wf)
    db.session.commit()
    
    print(f'SUCCESS: App created with ID {app_id}')
    print(f'Nodes: {len(graph.get("nodes",[]))}, Edges: {len(graph.get("edges",[]))}')
