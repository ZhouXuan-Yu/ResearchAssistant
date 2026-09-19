import psycopg2, json
c = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = c.cursor()
cur.execute("SELECT graph FROM workflows WHERE id='e5977d63-0534-476b-9db0-4f660f087fd0'")
g = json.loads(cur.fetchone()[0])
for n in g['nodes']:
    if n['data'].get('type') == 'llm':
        print(n['data']['title'], n['data']['model']['completion_params'].get('max_tokens'))
c.close()
