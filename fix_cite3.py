import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT id, graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' ORDER BY updated_at DESC LIMIT 1")
pub_id, graph = cur.fetchone()

# Replace prompt entirely
old = r'\u4f60\u662f\u4e00\u4e2aHR\u7b80\u5386\u7b5b\u9009\u52a9\u624b'
pos = graph.find(old)
if pos < 0:
    print("NOT FOUND")
    conn.close()
    exit()

rest = graph[pos:]
next_field = rest.find('\n        - id:')
text_end = pos + rest.rfind('"', 0, next_field)

new_prompt = r'\u4f60\u662f\u4e00\u4e2aHR\u7b80\u5386\u7b5b\u9009\u52a9\u624b\u3002\u9ed8\u8ba4\u8f93\u51fa\u6838\u5fc3\u7b80\u62a5\u3002\n\n## \u6838\u5fc3\u7b80\u62a5\uff08\u9ed8\u8ba4\uff09\n| # | \u5019\u9009\u4eba | \u5339\u914d\u65b9\u5411 | \u6838\u5fc3\u6280\u80fd | \u4eae\u70b9 | \u98ce\u9669 | \u8bc4\u5206 | \u5efa\u8bae |\n|---|--------|---------|---------|------|------|------|------|\n\n\u6309\u8bc4\u5206\u4ece\u9ad8\u5230\u4f4e\u6392\u5217\u30027\u5206\u4ee5\u4e0a\u5efa\u8bae\u9762\u8bd5\u3002\n\n\u6bcf\u4f4d\u5019\u9009\u4eba\u540e\u5fc5\u987b\u9644\u5e26\u4e00\u6bb5 **\u7b80\u5386\u539f\u6587\u6458\u8981**\uff0c\u7528 Markdown \u5f15\u7528\u683c\u5f0f\uff1a\n> **\u7b80\u5386\u539f\u6587**\uff1a\u6458\u5f55\u7b80\u5386\u4e2d\u6700\u80fd\u4f53\u73b0\u5176\u6838\u5fc3\u80fd\u529b\u7684 3-5 \u53e5\u539f\u6587\u3002\n\n## \u5176\u4ed6\u6a21\u5f0f\n- \u5bf9\u6bd4\uff1a\u201c\u5bf9\u6bd4A\u548cB\u201d\n- \u5c97\u4f4d\u5339\u914d\uff1a\u201c\u8c01\u9002\u5408XX\u5c97\u4f4d\u201d\n\n\u7b80\u6d01\u4e13\u4e1a\uff0c\u8001\u677f10\u79d2\u770b\u5b8c\u3002'

new_graph = graph[:pos] + new_prompt + graph[text_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE id = %s", (new_graph, pub_id))
conn.commit()
print("DONE")
conn.close()
