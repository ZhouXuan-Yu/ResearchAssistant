import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT id, graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' ORDER BY updated_at DESC LIMIT 1")
pub_id, graph = cur.fetchone()

# Find and remove old appendix
old_appendix = r'\n\n## \u7b80\u5386\u539f\u6587\u5f15\u7528'
pos = graph.find(old_appendix)
if pos >= 0:
    # Find end of appendix (to the next JSON field or end)
    end = graph.find('\n        - id:', pos)
    if end < 0:
        end = graph.find('\n    "role": "user"', pos)
    if end > pos:
        graph = graph[:pos] + graph[end:]
        print("Removed old appendix")

# Find end of system prompt to append citation requirement
marker = r'\u8001\u677f10\u79d2\u770b\u5b8c'
pos = graph.find(marker)
if pos < 0:
    print("NOT FOUND")
    conn.close()
    exit()

# Find closing quote after the prompt
rest = graph[pos:]
next_field = rest.find('\n        - id:')
if next_field < 0:
    next_field = rest.find('\n    "role":')
text_end = pos + rest.rfind('"', 0, next_field)

# Short, mandatory citation instruction
citation = r'\n\n\u6bcf\u4f4d\u5019\u9009\u4eba\u5fc5\u987b\u9644\u5e26\u7b80\u5386\u539f\u6587\u5f15\u7528\uff0c\u7528 `<details>` \u6298\u53e0\uff1a\n<details>\n<summary>\ud83d\udcc4 \u59d3\u540d \u7b80\u5386\u539f\u6587</summary>\n> \u5f15\u7528 3-5 \u53e5\u6700\u80fd\u4f53\u73b0\u5176\u6838\u5fc3\u80fd\u529b\u7684\u539f\u6587\n</details>'

new_graph = graph[:text_end] + citation + graph[text_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE id = %s", (new_graph, pub_id))
conn.commit()
print("DONE")
conn.close()
