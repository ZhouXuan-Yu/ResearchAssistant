"""扩展 workflow 到完整版本"""
import sys, json, time, uuid
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
    
    # 节点ID命名
    S = str(ts)         # start
    H = str(ts + 1)     # http-request
    I = str(ts + 2)     # if-else (success/fail)
    CV = str(ts + 3)    # code (format vat)
    CR = str(ts + 4)    # code (format receipt)
    CG = str(ts + 5)    # code (format general)
    CF = str(ts + 6)    # code (fail)
    EV = str(ts + 7)    # end (vat)
    ER = str(ts + 8)    # end (receipt)
    EG = str(ts + 9)    # end (general)
    EF = str(ts + 10)   # end (fail)
    
    graph = {
        "nodes": [
            # ===== 1. 开始节点 =====
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
            
            # ===== 2. HTTP请求节点 =====
            {"id": H, "type": "custom", "width": 244, "height": 96,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 350, "y": 300}, "positionAbsolute": {"x": 350, "y": 300},
             "data": {
                 "type": "http-request", "title": "OCR识别", "desc": "调用Docker OCR服务",
                 "selected": False, "method": "post",
                 "url": "http://host.docker.internal:8001/api/extract",
                 "authorization": {"type": "no-auth", "config": None},
                 "headers": "", "params": "",
                 "body": {"type": "form-data", "data": [{"key": "file", "type": "file", "file": ["receipt_image"], "value_type": "file"}]},
                 "timeout": {"connect": 15, "read": 60, "max_connect_timeout": 0, "max_read_timeout": 0},
                 "retry_config": {"max_retries": 2, "retry_enabled": True, "retry_interval": 2000}
             }},
            
            # ===== 3. 条件分支 =====
            {"id": I, "type": "custom", "width": 244, "height": 124,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 670, "y": 300}, "positionAbsolute": {"x": 670, "y": 300},
             "data": {
                 "type": "if-else", "title": "结果判断", "desc": "判断OCR是否成功",
                 "selected": False,
                 "cases": [
                     {"id": "case-ok", "title": "识别成功", "logical_operator": "and",
                      "conditions": [{"variable_selector": [H, "body", "success"], "comparison_operator": "=", "value": "true", "value_type": "string"}]},
                     {"id": "case-fail", "title": "识别失败", "logical_operator": "and",
                      "conditions": [{"variable_selector": [H, "body", "success"], "comparison_operator": "=", "value": "false", "value_type": "string"}]}
                 ]
             }},
            
            # ===== 4. 代码节点 (成功格式化) =====
            {"id": CV, "type": "custom", "width": 244, "height": 52,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 990, "y": 200}, "positionAbsolute": {"x": 990, "y": 200},
             "data": {
                 "type": "code", "title": "格式化结果", "desc": "格式化识别结果",
                 "selected": False, "code_language": "python3",
                 "code": 'def main(ocr_data: dict) -> dict:\n    return {\n        "status": "success",\n        "type": ocr_data.get("receipt_type", "unknown"),\n        "vendor": ocr_data.get("vendor_name", "未知"),\n        "date": ocr_data.get("date", ""),\n        "total": ocr_data.get("total_amount"),\n        "tax": ocr_data.get("tax_amount"),\n        "confidence": round(ocr_data.get("confidence", 0) * 100, 1),\n        "warnings": ocr_data.get("warnings", [])\n    }',
                 "variables": [{"variable": "ocr_data", "value_selector": [H, "body"], "value_type": "object"}],
                 "outputs": [
                     {"name": "status", "type": "string", "value_type": "string"},
                     {"name": "type", "type": "string", "value_type": "string"},
                     {"name": "vendor", "type": "string", "value_type": "string"},
                     {"name": "total", "type": "number", "value_type": "number"},
                     {"name": "confidence", "type": "number", "value_type": "number"}
                 ]
             }},
            
            # ===== 5. 代码节点 (失败处理) =====
            {"id": CF, "type": "custom", "width": 244, "height": 52,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 990, "y": 400}, "positionAbsolute": {"x": 990, "y": 400},
             "data": {
                 "type": "code", "title": "失败处理", "desc": "返回错误信息",
                 "selected": False, "code_language": "python3",
                 "code": 'def main(http_response: dict) -> dict:\n    return {\n        "status": "error",\n        "message": http_response.get("error", "OCR识别失败"),\n        "suggestion": "请检查图片是否清晰、格式是否支持"\n    }',
                 "variables": [{"variable": "http_response", "value_selector": [H, "body"], "value_type": "object"}],
                 "outputs": [
                     {"name": "status", "type": "string", "value_type": "string"},
                     {"name": "message", "type": "string", "value_type": "string"}
                 ]
             }},
            
            # ===== 6. 结束节点 (成功) =====
            {"id": EV, "type": "custom", "width": 244, "height": 90,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 1310, "y": 200}, "positionAbsolute": {"x": 1310, "y": 200},
             "data": {
                 "type": "end", "title": "结束-成功", "selected": False,
                 "outputs": [
                     {"variable": "status", "value_selector": [CV, "status"], "value_type": "string"},
                     {"variable": "receipt_type", "value_selector": [CV, "type"], "value_type": "string"},
                     {"variable": "vendor", "value_selector": [CV, "vendor"], "value_type": "string"},
                     {"variable": "total", "value_selector": [CV, "total"], "value_type": "number"},
                     {"variable": "confidence", "value_selector": [CV, "confidence"], "value_type": "number"}
                 ]
             }},
            
            # ===== 7. 结束节点 (失败) =====
            {"id": EF, "type": "custom", "width": 244, "height": 90,
             "selected": False, "sourcePosition": "right", "targetPosition": "left",
             "position": {"x": 1310, "y": 400}, "positionAbsolute": {"x": 1310, "y": 400},
             "data": {
                 "type": "end", "title": "结束-失败", "selected": False,
                 "outputs": [
                     {"variable": "status", "value_selector": [CF, "status"], "value_type": "string"},
                     {"variable": "message", "value_selector": [CF, "message"], "value_type": "string"}
                 ]
             }}
        ],
        "edges": [
            # start → http
            {"id": f"{S}-source-{H}-target", "source": S, "sourceHandle": "source", "target": H, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "start", "targetType": "http-request", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            # http → if
            {"id": f"{H}-source-{I}-target", "source": H, "sourceHandle": "source", "target": I, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "http-request", "targetType": "if-else", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            # if (success) → code
            {"id": f"{I}-case-ok-{CV}-target", "source": I, "sourceHandle": "case-ok", "target": CV, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "if-else", "targetType": "code", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            # if (fail) → code-fail
            {"id": f"{I}-case-fail-{CF}-target", "source": I, "sourceHandle": "case-fail", "target": CF, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "if-else", "targetType": "code", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            # code → end-success
            {"id": f"{CV}-source-{EV}-target", "source": CV, "sourceHandle": "source", "target": EV, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "code", "targetType": "end", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
            # code-fail → end-fail
            {"id": f"{CF}-source-{EF}-target", "source": CF, "sourceHandle": "source", "target": EF, "targetHandle": "target",
             "type": "custom", "data": {"sourceType": "code", "targetType": "end", "isInLoop": False, "isInIteration": False}, "zIndex": 0, "selected": False},
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 1}
    }
    
    wf.graph = json.dumps(graph, ensure_ascii=False)
    db.session.commit()
    print(f'Updated! Nodes: {len(graph["nodes"])}, Edges: {len(graph["edges"])}')
    print('\nNode list:')
    for n in graph['nodes']:
        print(f'  [{n["id"]}] {n["data"]["type"]:15s} → {n["data"]["title"]}')
