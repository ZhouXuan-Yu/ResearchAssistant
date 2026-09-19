"""简化版修复：end节点直接引用HTTP响应"""
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
    
    # 找节点ID
    H = None  # http
    for n in graph['nodes']:
        if n['data']['type'] == 'http-request':
            H = n['id']
    
    print(f'HTTP node: {H}')
    
    # 修复 end 节点的 value_selector，直接引用 HTTP 响应字段
    for n in graph['nodes']:
        if n['data']['type'] == 'end':
            title = n['data']['title']
            if '失败' in title:
                n['data']['outputs'] = [
                    {"variable": "error_status", "value_selector": [H, "body", "success"], "value_type": "string"},
                    {"variable": "error_info", "value_selector": [H, "body", "error"], "value_type": "string"},
                    {"variable": "error_code", "value_selector": [H, "status_code"], "value_type": "number"},
                ]
            else:
                n['data']['outputs'] = [
                    {"variable": "receipt_type", "value_selector": [H, "body", "receipt_type"], "value_type": "string"},
                    {"variable": "vendor_name", "value_selector": [H, "body", "vendor_name"], "value_type": "string"},
                    {"variable": "receipt_date", "value_selector": [H, "body", "date"], "value_type": "string"},
                    {"variable": "total_amount", "value_selector": [H, "body", "total_amount"], "value_type": "number"},
                    {"variable": "tax_amount", "value_selector": [H, "body", "tax_amount"], "value_type": "number"},
                    {"variable": "confidence", "value_selector": [H, "body", "confidence"], "value_type": "number"},
                ]
            print(f'Fixed: {title} → {[o["variable"] for o in n["data"]["outputs"]]}')
    
    # 同时禁用 code 节点（保留但不再连接到 end）
    # code 节点仍然连接到 if-else，但 end 节点直接从 HTTP 取数据
    
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print('Saved')
