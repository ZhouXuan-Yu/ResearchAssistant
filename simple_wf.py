"""彻底简化：去掉code节点，if→end直接引用HTTP响应"""
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
    
    ts = int(time.time() * 1000)
    S = str(ts)
    H = str(ts + 1)
    I = str(ts + 2)
    EV = str(ts + 3)
    EF = str(ts + 4)
    
    graph = {
        "nodes": [
            {"id": S, "type": "custom", "width": 244, "height": 90,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 30, "y": 300}, "positionAbsolute": {"x": 30, "y": 300},
             "data": {
                 "type": "start", "title": "开始", "selected": False,
                 "variables": [{
                     "variable": "receipt_image", "label": "票据图片",
                     "type": "file", "required": True,
                     "allowed_file_extensions": [".jpg",".jpeg",".png",".bmp",".webp"],
                     "allowed_file_types": ["image"],
                     "allowed_file_upload_methods": ["local_file","remote_url"],
                     "options": [], "max_length": 48, "hint": "", "default": "", "placeholder": ""
                 }]
             }},
            {"id": H, "type": "custom", "width": 244, "height": 96,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 350, "y": 280}, "positionAbsolute": {"x": 350, "y": 280},
             "data": {
                 "type": "http-request", "title": "OCR识别", "selected": False, "method": "post",
                 "url": "http://host.docker.internal:8001/api/extract",
                 "authorization": {"type": "no-auth", "config": None},
                 "headers": "", "params": "",
                 "body": {"type": "form-data", "data": [{"key": "file", "type": "file", "file": ["receipt_image"], "value_type": "file"}]},
                 "timeout": {"connect": 15, "read": 60, "max_connect_timeout": 0, "max_read_timeout": 0},
                 "retry_config": {"max_retries": 2, "retry_enabled": True, "retry_interval": 2000}
             }},
            {"id": I, "type": "custom", "width": 244, "height": 124,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 670, "y": 280}, "positionAbsolute": {"x": 670, "y": 280},
             "data": {
                 "type": "if-else", "title": "识别结果判断", "selected": False,
                 "cases": [
                     {"id": "case-ok", "title": "识别成功", "logical_operator": "and",
                      "conditions": [{"variable_selector": [H, "body", "success"], "comparison_operator": "=", "value": "true", "value_type": "string"}]},
                     {"id": "case-fail", "title": "识别失败", "logical_operator": "and",
                      "conditions": [{"variable_selector": [H, "body", "success"], "comparison_operator": "=", "value": "false", "value_type": "string"}]}
                 ]
             }},
            {"id": EV, "type": "custom", "width": 244, "height": 160,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 990, "y": 200}, "positionAbsolute": {"x": 990, "y": 200},
             "data": {
                 "type": "end", "title": "识别成功", "selected": False,
                 "outputs": [
                     {"variable": "receipt_type", "value_selector": [H, "body", "receipt_type"], "value_type": "string"},
                     {"variable": "vendor_name", "value_selector": [H, "body", "vendor_name"], "value_type": "string"},
                     {"variable": "receipt_date", "value_selector": [H, "body", "date"], "value_type": "string"},
                     {"variable": "total_amount", "value_selector": [H, "body", "total_amount"], "value_type": "number"},
                     {"variable": "tax_amount", "value_selector": [H, "body", "tax_amount"], "value_type": "number"},
                     {"variable": "confidence", "value_selector": [H, "body", "confidence"], "value_type": "number"},
                     {"variable": "raw_text", "value_selector": [H, "body", "raw_text"], "value_type": "string"},
                 ]
             }},
            {"id": EF, "type": "custom", "width": 244, "height": 120,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 990, "y": 420}, "positionAbsolute": {"x": 990, "y": 420},
             "data": {
                 "type": "end", "title": "识别失败", "selected": False,
                 "outputs": [
                     {"variable": "error", "value_selector": [H, "body", "error"], "value_type": "string"},
                     {"variable": "status_code", "value_selector": [H, "status_code"], "value_type": "number"},
                     {"variable": "suggestion", "value_selector": [H, "body", "warnings"], "value_type": "string"},
                 ]
             }}
        ],
        "edges": [
            {"id": f"e-{S}-{H}", "source": S, "sourceHandle": "source", "target": H, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "start", "targetType": "http-request", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            {"id": f"e-{H}-{I}", "source": H, "sourceHandle": "source", "target": I, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "http-request", "targetType": "if-else", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            {"id": f"e-{I}-ok-{EV}", "source": I, "sourceHandle": "case-ok", "target": EV, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "if-else", "targetType": "end", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            {"id": f"e-{I}-fail-{EF}", "source": I, "sourceHandle": "case-fail", "target": EF, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "if-else", "targetType": "end", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 1}
    }
    
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print(f'Done: {len(graph["nodes"])} nodes, {len(graph["edges"])} edges')
    for n in graph['nodes']:
        print(f'  [{n["id"]}] {n["data"]["type"]} → {n["data"]["title"]}')
