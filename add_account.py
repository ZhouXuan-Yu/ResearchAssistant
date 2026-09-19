from app.db.engine import get_engine, get_session, init_session_factory
from app.db.models import Account
from app.config import load_config
from app.crypto import encrypt_password
from pathlib import Path
from datetime import datetime, timezone

config = load_config(Path('config.yaml'))
engine = get_engine(config.database_path)
init_session_factory(engine)
session = get_session()

existing = session.query(Account).filter(Account.email_address == '1241515924@qq.com').first()
if existing:
    existing.password_encrypted = encrypt_password('amabklqqsyhqcjfg', config.encryption_key)
    existing.is_active = True
    print(f'更新已有账户: ID={existing.id}')
else:
    account = Account(
        label='QQ邮箱-简历',
        email_address='1241515924@qq.com',
        imap_host='imap.qq.com',
        imap_port=993,
        imap_ssl=True,
        smtp_host='smtp.qq.com',
        smtp_port=587,
        smtp_tls=True,
        username='1241515924@qq.com',
        password_encrypted=encrypt_password('amabklqqsyhqcjfg', config.encryption_key),
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(account)
    print('账户创建成功!')

session.commit()

for a in session.query(Account).filter(Account.is_active == True).all():
    print(f'活跃账户: {a.email_address} ({a.imap_host}:{a.imap_port})')

session.close()
print('Done')
