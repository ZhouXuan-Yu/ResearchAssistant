import psycopg2

public_key_pem = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArnlRApLjr2Sp1M/+nqWu
auiYNqTm0rFd1SiMmrRl+6lRpokzPNuLdHBfP79WjWslVCZK5cuKP7clsSMqx2Zr
hm6Q8uMsKY11sn78Osnb/DfqF2oiNhGZChJo2Z0Dqn8qJ4+LCYbM2O+5TykDovZd
kWUDKWBiroQGUf3ATthMvn+LqOk0ds8WNARGrT6XyZ41KbSmzlqwNnPXbFYWIcwz
JJKLtTlqGNXdpMSafdeHDBEkdMKEV6csRjIlrgywIIYHleF1zhwP4QlvRdd4+PQE
U0TS9AU/X+LCR8XF6a5o1MGUSeHuA4VhFvyaEkflZbsYGfkz34T/dt9jkaMzGfDc
GQIDAQAB
-----END PUBLIC KEY-----"""

conn = psycopg2.connect(host='localhost', port=5432, dbname='dify', user='postgres', password='difyai123456')
cur = conn.cursor()
cur.execute("UPDATE tenants SET encrypt_public_key = %s WHERE id = '50c15e0b-2bb9-4db6-9e7d-e61e75190c72'", (public_key_pem,))
conn.commit()
print(f'Updated: {cur.rowcount} rows')
cur.close()
conn.close()
