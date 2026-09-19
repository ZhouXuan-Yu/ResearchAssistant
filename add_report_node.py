"""为 简历-招聘01 添加汇总报告代码节点"""
import psycopg2, json, uuid, copy

conn = psycopg2.connect("host=db_postgres dbname=dify user=postgres password=difyai123456")
cur = conn.cursor()
app_id = 'f229fc82-992d-4de1-8d75-4ed76c0e9730'
ITER_ID = '1782725226412'

cur.execute("SELECT id, type, version, graph FROM workflows WHERE app_id=%s", (app_id,))
for wid, typ, ver, graph_str in cur.fetchall():
    graph = json.loads(graph_str) if isinstance(graph_str, str) else graph_str
    
    # 检查是否已有汇总报告节点
    has_report = any(n['data'].get('title') == '汇总报告' for n in graph['nodes'])
    if has_report:
        print(f"  [{wid[:8]}] Already has 汇总报告, skipping")
        continue
    
    # 创建汇总报告code节点
    report_id = '1782790100001'
    report_node = {
        "id": report_id,
        "type": "custom",
        "width": 241,
        "height": 51,
        "position": {"x": 520, "y": -80},
        "positionAbsolute": {"x": 520, "y": -80},
        "selected": False,
        "sourcePosition": "right",
        "targetPosition": "left",
        "data": {
            "type": "code",
            "title": "汇总报告",
            "code_language": "python3",
            "selected": False,
            "outputs": {"report": {"type": "string", "children": None}},
            "variables": [
                {"variable": "match_outputs", "value_selector": [ITER_ID, "output"], "value_type": "array[string]"}
            ],
            "code": """import json, re

def _parse(text: str) -> dict:
    if not text: return {"name":"?","match_score":0,"tier":"归档","match_reason":"","key_points":[],"summary_50":""}
    t = text.strip()
    t = re.sub(r\"^```(?:json)?\\s*\", \"\", t, flags=re.I)
    t = re.sub(r\"\\s*```$\", \"\", t)
    try: return json.loads(t)
    except: return {"name":"?","match_score":0,"tier":"归档","match_reason":t[:200],"key_points":[],"summary_50":""}

def main(match_outputs: list) -> dict:
    parsed = [_parse(r) for r in (match_outputs or [])]
    parsed.sort(key=lambda x: x.get(\"match_score\") or 0, reverse=True)
    
    lines = [\"# 简历筛选报告\\n\"]
    
    for i, p in enumerate(parsed, 1):
        name = p.get(\"name\") or \"未知\"
        score = p.get(\"match_score\") or 0
        tier = p.get(\"tier\") or \"-\"
        emoji = \"🟢\" if score >= 80 else (\"🟡\" if score >= 60 else \"🔴\")
        lines.append(f\"### {emoji} {i}. {name} · {score}分 · {tier}\")
        
        if p.get(\"summary_50\"):
            lines.append(f\"> {p['summary_50']}\\n\")
        if p.get(\"match_reason\"):
            lines.append(f\"**匹配分析**：{p['match_reason']}\\n\")
        
        kps = p.get(\"key_points\") or []
        if kps:
            lines.append(\"**要点**：\" + \" · \".join(str(k) for k in kps[:8]) + \"\\n\")
        
        # 维度评分
        dims = [(\"技术\", \"tech_score\"), (\"项目\", \"project_score\"), (\"学历\", \"edu_score\"), (\"软实力\", \"soft_score\"), (\"加分\", \"bonus_score\")]
        scores_str = \" | \".join(f\"{d}: {p.get(k,0)}\" for d,k in dims)
        lines.append(f\"`{scores_str}`\\n\")
        
        lines.append(\"---\\n\")
    
    if not parsed:
        lines.append(\"⚠️ 未产生有效评分，请检查匹配打分节点\\n\")
    
    return {\"report\": \"\\n\".join(lines)}"""
        }
    }
    
    # 插入节点
    graph['nodes'].append(report_node)
    
    # 修改边: 遍历候选人 → 汇总报告 → 结束
    # 删除旧的 遍历候选人→结束 边
    graph['edges'] = [e for e in graph['edges'] 
                      if not (e['source'] == ITER_ID and e['target'] == 'answer')]
    
    # 添加 遍历候选人→汇总报告
    graph['edges'].append({
        "id": str(uuid.uuid4()),
        "source": ITER_ID, "sourceHandle": "source",
        "target": report_id, "targetHandle": "target",
        "type": "custom", "zIndex": 0,
        "data": {"isInLoop": False, "sourceType": "iteration", "targetType": "code"}
    })
    
    # 添加 汇总报告→结束
    graph['edges'].append({
        "id": str(uuid.uuid4()),
        "source": report_id, "sourceHandle": "source",
        "target": "answer", "targetHandle": "target",
        "type": "custom", "zIndex": 0,
        "data": {"isInLoop": False, "sourceType": "code", "targetType": "answer"}
    })
    
    # 修改结束节点引用
    for node in graph['nodes']:
        if node['data'].get('title') == '结束':
            node['data']['answer'] = '{{#1782790100001.report#}}'
    
    new_graph = json.dumps(graph, ensure_ascii=False)
    cur.execute("UPDATE workflows SET graph=%s, updated_at=NOW() WHERE id=%s", (new_graph, wid))
    print(f"  [{wid[:8]}] Added 汇总报告 node + rewired edges")

conn.commit()
conn.close()
print("Done")
