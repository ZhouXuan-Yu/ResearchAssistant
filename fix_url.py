import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
graph = cur.fetchone()[0]

# Fix HTTP URL from emails to extractions
old_url = '/api/v1/emails'
new_url = '/api/v1/extractions'
if old_url in graph:
    graph = graph.replace(old_url, new_url)
    cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (graph,))
    conn.commit()
    print("URL updated: emails -> extractions")
else:
    print("URL already correct or not found")

conn.close()
