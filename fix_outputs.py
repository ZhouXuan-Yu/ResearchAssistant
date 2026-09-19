"""修复 workflow 输出变量冲突"""
import sys, json, time
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
    nodes = graph['nodes']
    
    # 找到关键节点ID
    node_map = {}
    for n in nodes:
        node_map[n['data']['type']] = n['id']
    
    CV = node_map.get('code')  # 第一个 code 节点 = 格式化结果
    CF = None  # 第二个 code 节点 = 失败处理
    for n in nodes:
        if n['data']['type'] == 'code' and n['data']['title'] == '失败处理':
            CF = n['id']
    
    print(f"Success code node: {CV}")
    print(f"Fail code node: {CF}")
    
    # 修复结束节点
    for n in nodes:
        if n['data']['type'] == 'end':
            title = n['data']['title']
            if '失败' in title:
                # 失败分支 - 变量名加前缀避免冲突
                for out in n['data']['outputs']:
                    if out['variable'] == 'status':
                        out['variable'] = 'error_status'
                    if out['variable'] == 'message':
                        out['variable'] = 'error_message'
                print(f"Fixed end-fail: {[o['variable'] for o in n['data']['outputs']]}")
            
            if '成功' in title:
                print(f"End-success outputs: {[o['variable'] for o in n['data']['outputs']]}")
                print(f"  value_selectors: {[o['value_selector'] for o in n['data']['outputs']]}")
    
    # 保存
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print("Fixed and saved")
