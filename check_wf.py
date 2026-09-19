import json, psycopg2
conn = psycopg2.connect('host=db_postgres dbname=dify user=postgres password=difyai123456')
cur = conn.cursor()
cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e'")
for r in cur.fetchall():
    try:
        g = json.loads(r[3])
        print(f'OK {r[0][:8]} {r[1]:10} nodes={len(g.get("nodes",[]))} edges={len(g.get("edges",[]))}')
    except Exception as e:
        print(f'ERR {r[0][:8]} {r[1]:10} {e}')
conn.close()
