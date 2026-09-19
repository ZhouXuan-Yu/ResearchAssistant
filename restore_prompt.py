import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

# The prompt that worked in previous successful test
good_prompt = "你是一个HR简历筛选助手。根据用户问题自动选择模式：1.对比分析 Markdown表格+推荐 2.岗位匹配 按匹配度排序 3.简报汇总 汇总表 4.深度评估(默认)六维度评分(技术30%/项目25%/问题解决20%/成长10%/协作10%/稳定5%)。7分以上建议面试。Markdown输出。简洁专业。默认简报汇总。"

cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
graph = cur.fetchone()[0]

# Find any existing prompt between HR and the next JSON field
import re
# Match: HR...anything...before "role": "user" or end of text field
pattern = r'(HR[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\\a-zA-Z0-9\u0020-\u007e]+?)(?=\s*\\n\s*\d|"\s*,|\s*"role")'
m = re.search(pattern, graph)
if m:
    old_text = m.group(1)
    escaped_new = json.dumps(good_prompt, ensure_ascii=True)[1:-1]
    new_graph = graph.replace(old_text, escaped_new, 1)
    cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (new_graph,))
    conn.commit()
    cur.execute("UPDATE workflows SET graph = (SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft') WHERE id='bdbc3c5f-e274-4f7f-b36b-a37dcc212b1a'")
    conn.commit()
    print("RESTORED")
else:
    print("NOT FOUND")

conn.close()
