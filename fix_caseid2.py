"""统一 if-else case_id 为 true/false"""
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
            node['data']['cases'][0]['case_id'] = 'true'
            node['data']['cases'][1]['case_id'] = 'false'
            print('case_ids → true / false')
    
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print('Done')
