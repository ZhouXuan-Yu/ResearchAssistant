"""直接在 Dify 容器内调用 DSL 导入"""
import sys, yaml, json
sys.path.insert(0, '/app/api')

from app import create_app
from services.app_dsl_service import AppDslService
from models.model import App, Account
from extensions.ext_database import db

# 读取 YAML
with open('/tmp/workflow.yml', 'r', encoding='utf-8') as f:
    yaml_content = f.read()

app_result = create_app()

# 获取 flask app
if isinstance(app_result, tuple):
    flask_app = app_result[0]
    # 对于 WSGIApp，获取其内部的 Flask app
    if hasattr(flask_app, 'app'):
        flask_app = flask_app.app
    elif hasattr(flask_app, '_app'):
        flask_app = flask_app._app

# 获取当前租户和账户
with flask_app.app_context():
    from models.account import Tenant, TenantAccountJoin
    tenant = db.session.query(Tenant).first()
    account = db.session.query(Account).filter(Account.email == '1241515924@qq.com').first()
    print(f"Tenant: {tenant.id}, Account: {account.id}")
    
    try:
        result = AppDslService.import_app(tenant.id, account.id, yaml_content)
        print(f"Import result: {json.dumps(result, default=str)[:500]}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
