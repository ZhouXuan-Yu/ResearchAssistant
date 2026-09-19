import json, psycopg2

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()

# Get current graph
cur.execute("SELECT graph FROM workflows WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'")
row = cur.fetchone()
graph = row[0]

# Find and replace the system prompt
old_prompt_start = "你是一个HR筛选助手"
new_prompt = "你是一个HR简历筛选助手。根据用户问题自动选择模式：1.对比分析 Markdown表格+推荐 2.岗位匹配 按匹配度排序 3.简报汇总 汇总表 4.深度评估(默认)六维度评分(技术30%/项目25%/问题解决20%/成长10%/协作10%/稳定5%)。7分以上建议面试。Markdown输出。简洁专业。"

# Convert to escaped form
def to_escaped(s):
    return json.dumps(s, ensure_ascii=True)[1:-1]

old_start_escaped = to_escaped(old_prompt_start)
new_escaped = to_escaped(new_prompt)

# Find position of old prompt start
pos = graph.find(old_start_escaped)
if pos >= 0:
    # Find end of old prompt (terminated by \\n\\n or closing quote before next field)
    # The prompt ends where the next JSON field begins
    # Find the end by looking for the pattern that follows the prompt
    end_marker = '\\n\\n\\n"'
    end_pos = graph.find(end_marker, pos + len(old_start_escaped))
    if end_pos < 0:
        end_marker = '"\n        - id:'
        end_pos = graph.find(end_marker, pos + len(old_start_escaped))
    
    if end_pos > pos:
        # Build new graph: before old prompt + new prompt + after old prompt
        new_graph = graph[:pos] + new_escaped + graph[end_pos:]
        cur.execute("UPDATE workflows SET graph = %s WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft'", (new_graph,))
        conn.commit()
        print(f"Replaced prompt. Old length: {end_pos - pos}, New length: {len(new_escaped)}")
    else:
        print(f"Found start at {pos} but could not find end marker")
else:
    print(f"Prompt not found. Graph sample: {graph[500:800]}")

conn.close()
