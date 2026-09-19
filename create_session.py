"""在 Dify 容器内直接生成登录会话"""
import sys
sys.path.insert(0, '/app/api')

from flask import Flask, session
from app import create_app
from extensions.ext_database import db
from models.account import Account, Tenant, TenantAccountJoin
from extensions.ext_storage import storage
import datetime
import uuid

app_result = create_app()
flask_app = app_result if not isinstance(app_result, tuple) else app_result[0]

with flask_app.app_context():
    # 获取账户
    account = db.session.query(Account).filter(Account.email == '1241515924@qq.com').first()
    print(f"Account: {account.id} {account.email} {account.status}")
    
    # 模拟登录 - 更新最后登录时间
    account.last_login_at = datetime.datetime.now()
    account.last_login_ip = '172.19.0.1'
    db.session.commit()
    print(f"Login time updated: {account.last_login_at}")
    
    # 获取 tenant
    join = db.session.query(TenantAccountJoin).filter(
        TenantAccountJoin.account_id == account.id
    ).first()
    print(f"Tenant join: {join.tenant_id if join else 'None'}")
    
    if join:
        tenant = db.session.query(Tenant).filter(Tenant.id == join.tenant_id).first()
        print(f"Tenant: {tenant.id} {tenant.name}")
    
    print("SUCCESS - Account ready for login")
