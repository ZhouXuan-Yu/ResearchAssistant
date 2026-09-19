"""通过 Dify 自己的模型创建 workflow 节点"""
import sys, json, uuid, time
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
    
    if not wf:
        print('Workflow not found')
    else:
        print(f'Found workflow: {wf.id}')
        print(f'Current graph nodes: {len(json.loads(wf.graph).get("nodes",[]))}')
        
        # 创建简单的 graph：start -> code -> end
        import json
        ts = int(time.time() * 1000)
        graph = {
            "nodes": [
                {
                    "id": str(ts),
                    "type": "custom",
                    "data": {
                        "type": "start",
                        "title": "开始",
                        "selected": False,
                        "variables": [
                            {
                                "variable": "receipt_image",
                                "label": "票据图片",
                                "type": "file",
                                "required": True,
                                "allowed_file_extensions": [".jpg", ".jpeg", ".png", ".bmp", ".webp"],
                                "allowed_file_types": ["image"],
                                "allowed_file_upload_methods": ["local_file", "remote_url"],
                                "options": [],
                                "max_length": 48,
                                "hint": "",
                                "default": "",
                                "placeholder": ""
                            }
                        ]
                    },
                    "position": {"x": 30, "y": 300},
                    "positionAbsolute": {"x": 30, "y": 300},
                    "width": 244,
                    "height": 90,
                    "selected": False,
                    "sourcePosition": "right",
                    "targetPosition": "left"
                },
                {
                    "id": str(ts + 1),
                    "type": "custom",
                    "data": {
                        "type": "http-request",
                        "title": "OCR识别",
                        "desc": "调用OCR服务",
                        "selected": False,
                        "method": "post",
                        "url": "http://host.docker.internal:8001/api/extract",
                        "authorization": {"type": "no-auth", "config": None},
                        "headers": "",
                        "params": "",
                        "body": {
                            "type": "form-data",
                            "data": [
                                {
                                    "key": "file",
                                    "type": "file",
                                    "file": ["receipt_image"],
                                    "value_type": "file"
                                }
                            ]
                        },
                        "timeout": {"connect": 15, "read": 60, "max_connect_timeout": 0, "max_read_timeout": 0},
                        "retry_config": {"max_retries": 2, "retry_enabled": True, "retry_interval": 2000}
                    },
                    "position": {"x": 350, "y": 300},
                    "positionAbsolute": {"x": 350, "y": 300},
                    "width": 244,
                    "height": 96,
                    "selected": False,
                    "sourcePosition": "right",
                    "targetPosition": "left"
                },
                {
                    "id": str(ts + 2),
                    "type": "custom",
                    "data": {
                        "type": "end",
                        "title": "结束",
                        "selected": False,
                        "outputs": [
                            {
                                "variable": "result",
                                "value_selector": [str(ts + 1), "body"],
                                "value_type": "object"
                            }
                        ]
                    },
                    "position": {"x": 670, "y": 300},
                    "positionAbsolute": {"x": 670, "y": 300},
                    "width": 244,
                    "height": 90,
                    "selected": False,
                    "sourcePosition": "right",
                    "targetPosition": "left"
                }
            ],
            "edges": [
                {
                    "id": f"{ts}-source-{ts+1}-target",
                    "source": str(ts),
                    "sourceHandle": "source",
                    "target": str(ts + 1),
                    "targetHandle": "target",
                    "type": "custom",
                    "data": {
                        "sourceType": "start",
                        "targetType": "http-request",
                        "isInLoop": False,
                        "isInIteration": False
                    },
                    "zIndex": 0,
                    "selected": False
                },
                {
                    "id": f"{ts+1}-source-{ts+2}-target",
                    "source": str(ts + 1),
                    "sourceHandle": "source", 
                    "target": str(ts + 2),
                    "targetHandle": "target",
                    "type": "custom",
                    "data": {
                        "sourceType": "http-request",
                        "targetType": "end",
                        "isInLoop": False,
                        "isInIteration": False
                    },
                    "zIndex": 0,
                    "selected": False
                }
            ],
            "viewport": {"x": 0, "y": 0, "zoom": 1}
        }
        
        # 用 setattr 直接设置，绕过 model setter
        wf.graph = json.dumps(graph, ensure_ascii=False)
        db.session.commit()
        print(f'Updated! Nodes: {len(graph["nodes"])}, Edges: {len(graph["edges"])}')
        print('Test this at: http://localhost/app/e56efe64-39bc-4c2b-9519-6a0ddccb98f9/workflow')
