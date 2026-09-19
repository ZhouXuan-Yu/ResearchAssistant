import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
graph = cur.fetchone()[0]

# Find system prompt marker
marker = '\\u9ed8\\u8ba4\\u8f93\\u51fa\\u6838\\u5fc3\\u7b80\\u62a5'  # "默认输出核心简报"
pos = graph.find(marker)
if pos < 0:
    marker = 'HR\\u7b80\\u5386\\u7b5b\\u9009\\u52a9\\u624b'  # fallback
    pos = graph.find(marker)
if pos < 0:
    print("NOT FOUND")
    conn.close()
    exit()

# Find end of system prompt text
end_marker = '"role": "user"'
end_pos = graph.find(end_marker, pos)
if end_pos < 0:
    print("END NOT FOUND")
    conn.close()
    exit()

text_end = graph.rfind('"', pos, end_pos)

# Append to existing prompt
appendix = "\\n\\n## \\u7b80\\u5386\\u539f\\u6587\\u5f15\\u7528\\n\\u6bcf\\u4f4d\\u5019\\u9009\\u4eba\\u4e0b\\u65b9\\u7528 `<details>` \\u6298\\u53e0\\u6807\\u7b7e\\u5f15\\u7528\\u7b80\\u5386\\u539f\\u6587\\u5173\\u952e\\u6bb5\\u843d\\uff0c\\u9ed8\\u8ba4\\u6298\\u53e0\\uff0c\\u70b9\\u51fb\\u5c55\\u5f00\\u3002\\u683c\\u5f0f\\uff1a\\n```\\n<details>\\n<summary>\\ud83d\\udcc4 \\u5019\\u9009\\u4eba\\u59d3\\u540d \\u7b80\\u5386\\u539f\\u6587</summary>\\n> \\u5f15\\u7528\\u7b80\\u5386\\u4e2d\\u6700\\u80fd\\u4f53\\u73b0\\u6838\\u5fc3\\u80fd\\u529b\\u7684 3-5 \\u53e5\\u539f\\u6587\\n</details>\\n```"

new_graph = graph[:text_end] + appendix + graph[text_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (new_graph,))
conn.commit()

# sync published
cur.execute("UPDATE workflows SET graph = (SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft' AND type='workflow') WHERE id='4c917968-9587-4ba3-a392-830ca2eb8375'")
conn.commit()
print("DONE")
conn.close()
