import sys
sys.path.insert(0, '/app/api')

from app import create_app
from extensions.ext_database import db
from models.account import Account
from werkzeug.security import check_password_hash
import base64

app_result = create_app()
flask_app = app_result if not isinstance(app_result, tuple) else app_result[0]

with flask_app.app_context():
    # 直接测试认证逻辑
    accounts = db.session.query(Account).filter(Account.email == '1241515924@qq.com').all()
    print(f"Found {len(accounts)} accounts")
    
    for acc in accounts:
        print(f"Account: {acc.id}, email={acc.email}, status={acc.status}, name={acc.name}")
        stored = base64.b64decode(acc.password).decode()
        print(f"  Hash: {stored[:50]}...")
        ok = check_password_hash(stored, '123456')
        print(f"  '123456' match: {ok}")
        
        # 测试各种情况
        for p in ['123456', '15939702654tjl!']:
            ok2 = check_password_hash(stored, p)
            print(f"  '{p}' match: {ok2}")
