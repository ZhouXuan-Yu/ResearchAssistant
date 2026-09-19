import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
graph = cur.fetchone()[0]

# Search for the old prompt using unicode-escaped marker
old_marker_esc = 'HR\\u7b80\\u5386\\u7b5b\\u9009\\u52a9\\u624b'
pos = graph.find(old_marker_esc)
if pos < 0:
    # Try with actual Chinese
    old_marker = 'HR简历筛选助手'
    pos = graph.find(old_marker)
if pos < 0:
    print("NOT FOUND at all")
    conn.close()
    exit()

# Find the end: look for the end of the system message, before "user" role
end_marker = '"role": "user"'
end_pos = graph.find(end_marker, pos)
if end_pos < 0:
    print("END NOT FOUND")
    conn.close()
    exit()

# Go back from end_marker to find the closing quote of the text field
# The text field ends with '"' before some whitespace
text_end = graph.rfind('"', pos, end_pos)

new_prompt = "你是一个HR简历筛选助手。默认直接输出核心简报。\n\n## 核心简报格式\n| # | 候选人 | 匹配方向 | 核心技能 | 亮点 | 风险 | 评分 | 建议 |\n|---|--------|---------|---------|------|------|------|------|\n\n按评分从高到低排列。7分以上建议面试。\n\n## 其他模式\n- 对比：\"对比A和B\"\n- 岗位匹配：\"谁适合XX岗位\"\n\n简洁专业，老板10秒看完。"

escaped_new = json.dumps(new_prompt, ensure_ascii=True)[1:-1]

new_graph = graph[:pos] + escaped_new + graph[text_end:]
cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (new_graph,))
conn.commit()

# Sync to published
cur.execute("UPDATE workflows SET graph = (SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft') WHERE id='bdbc3c5f-e274-4f7f-b36b-a37dcc212b1a'")
conn.commit()
print("OK")
conn.close()
