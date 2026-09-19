import yaml, json

with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'r', encoding='utf-8') as f:
    dsl = yaml.safe_load(f)

graph = dsl['workflow']['graph']

# 统计所有可能缺少 value_type 的位置
for node in graph['nodes']:
    t = node['data']['type']
    ndata = node['data']
    
    # 1. HTTP请求节点的 body.data 条目
    if t == 'http-request':
        body = ndata.get('body', {})
        for item in body.get('data', []):
            if 'value_type' not in item:
                print(f"[HTTP body.data] {node['id']}: item key={item.get('key')} missing value_type")
                item['value_type'] = 'file' if item.get('type') == 'file' else 'string'
    
    # 2. 结束节点 outputs
    if t == 'end':
        for out in ndata.get('outputs', []):
            if 'value_type' not in out:
                print(f"[End output] {node['id']}: var={out.get('variable')} missing value_type")
                # 根据变量名推断类型
                var = out.get('variable', '')
                if var in ['total_amount', 'total', 'tax', 'confidence']:
                    out['value_type'] = 'number'
                else:
                    out['value_type'] = 'string'
    
    # 3. 代码节点 outputs
    if t == 'code':
        for out in ndata.get('outputs', []):
            if 'value_type' not in out:
                print(f"[Code output] {node['id']}: name={out.get('name')} missing value_type")
                name = out.get('name', '')
                if name in ['total', 'total_amount', 'tax', 'confidence']:
                    out['value_type'] = 'number'
                else:
                    out['value_type'] = 'string'
    
    # 4. LLM节点 context
    if t == 'llm':
        ctx = ndata.get('context', {})
        if isinstance(ctx, dict) and ctx.get('enabled'):
            if 'variable_selector' in ctx and isinstance(ctx['variable_selector'], list) and len(ctx['variable_selector']) > 0:
                if 'value_type' not in ctx:
                    print(f"[LLM context] {node['id']}: missing value_type")
                    ctx['value_type'] = 'string'

# 保存
with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'w', encoding='utf-8') as f:
    yaml.dump(dsl, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("\nDSL updated with all value_type fixes")
