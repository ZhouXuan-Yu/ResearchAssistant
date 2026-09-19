"""修复 if-else case_id 字段"""
import sys, json
sys.path.insert(0, '/app/api')
from flask import Flask
from extensions.ext_database import db
from models.workflow import Workflow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:difyai123456@docker-db_postgres-1:5432/dify'
db.init_app(app)

with app.app_context():
    wf = db.session.query(Workflow).filter(
        Workflow.app_id == 'e56efe64-39bc-4c2b-9519-6a0ddccb98f9',
        Workflow.type == 'workflow'
    ).first()
    
    graph = json.loads(wf.graph)
    
    for node in graph['nodes']:
        if node['data']['type'] == 'if-else':
            for case in node['data']['cases']:
                if 'id' in case and 'case_id' not in case:
                    case['case_id'] = case.pop('id')
                    print(f'Fixed: id → case_id = {case["case_id"]}')
    
    # 同时修复 edges 中引用的 sourceHandle
    for edge in graph['edges']:
        if edge['sourceHandle'] == 'case-ok':
            edge['sourceHandle'] = 'true'
        if edge['sourceHandle'] == 'case-fail':
            edge['sourceHandle'] = 'false'
    
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print('Saved')
