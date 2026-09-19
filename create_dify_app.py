import sys, json, uuid, os
sys.path.insert(0, '/app/api')

from app import create_app
from extensions.ext_database import db
from models.workflow import Workflow
from models.model import App
from models.account import Account, Tenant

app_result = create_app()
if isinstance(app_result, tuple):
    flask_app = app_result[0]
else:
    flask_app = app_result

with flask_app.app_context():
    tenant = db.session.query(Tenant).first()
    account = db.session.query(Account).first()
    
    app_id = str(uuid.uuid4())
    new_app = App(
        id=app_id,
        tenant_id=tenant.id,
        name='票据识别智能助手',
        mode='workflow',
        icon='\U0001f4c4',
        icon_background='#FFD93D',
        description='OCR票据识别自动化任务',
        created_by=account.id,
        updated_by=account.id,
    )
    db.session.add(new_app)
    db.session.flush()
    
    wf = Workflow(
        tenant_id=tenant.id,
        app_id=app_id,
        type='workflow',
        version='draft',
        graph=json.dumps({"nodes": [], "edges": [], "viewport": {"x": 0, "y": 0, "zoom": 1}}),
        features=json.dumps({"file_upload": {"enabled": True, "image": {"enabled": True, "number_limits": 1, "transfer_methods": ["local_file", "remote_url"]}}}),
        environment_variables='[]',
        conversation_variables='{}',
        created_by=account.id,
        updated_by=account.id,
    )
    db.session.add(wf)
    db.session.commit()
    
    print('SUCCESS')
    print('APP_ID=' + app_id)
