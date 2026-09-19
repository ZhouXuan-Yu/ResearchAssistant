import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

# Get the latest published workflow
cur.execute("SELECT id, graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' ORDER BY updated_at DESC LIMIT 1")
row = cur.fetchone()
pub_id, graph = row[0], row[1]

# Append citation instruction - look for "老板10秒看完" marker (Unicode escaped)
marker = r'\u8001\u677f10\u79d2\u770b\u5b8c'
pos = graph.find(marker)
if pos < 0:
    # try other markers
    for m in [r'\u7b80\u6d01\u4e13\u4e1a', r'\u9ed8\u8ba4\u8f93\u51fa']:
        pos = graph.find(m)
        if pos >= 0: break

if pos < 0:
    print("NOT FOUND")
    conn.close()
    exit()

# Find end of the text field (closing quote before next JSON field)
# Search for the next '"' that precedes a comma+newline or field name
rest = graph[pos:]
# Find the pattern: text ends with a quote, then comma, then new field
end_search = rest.find('\n        - id:')  # next prompt_template entry
if end_search < 0:
    end_search = rest.find('\n    "role": "user"')  # user role entry
if end_search < 0:
    print("END NOT FOUND")
    conn.close()
    exit()

text_end = pos + rest.rfind('"', 0, end_search)

appendix = r'\n\n## \u7b80\u5386\u539f\u6587\u5f15\u7528\n\u6bcf\u4f4d\u5019\u9009\u4eba\u4e0b\u65b9\u7528 `<details>` \u6298\u53e0\u6807\u7b7e\u5f15\u7528\u7b80\u5386\u539f\u6587\u5173\u952e\u6bb5\u843d\uff0c\u9ed8\u8ba4\u6298\u53e0\uff0c\u70b9\u51fb\u5c55\u5f00\u3002\u683c\u5f0f\uff1a\n<details>\n<summary>\ud83d\udcc4 \u5019\u9009\u4eba\u59d3\u540d \u7b80\u5386\u539f\u6587</summary>\n> \u5f15\u7528\u7b80\u5386\u4e2d\u6700\u80fd\u4f53\u73b0\u6838\u5fc3\u80fd\u529b\u7684 3-5 \u53e5\u539f\u6587\n</details>'

new_graph = graph[:text_end] + appendix + graph[text_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE id = %s", (new_graph, pub_id))
conn.commit()
print(f"DONE, updated {pub_id}")
conn.close()
