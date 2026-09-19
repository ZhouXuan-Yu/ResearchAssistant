import yaml, json

with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'r', encoding='utf-8') as f:
    dsl = yaml.safe_load(f)

graph = dsl['workflow']['graph']
print("Version:", dsl.get('version'))
print("Current Dify:", "0.6.0")

for n in graph['nodes']:
    t = n['data']['type']
    if t == 'start':
        vars_list = n['data'].get('variables', [])
        print("\nStart node variables:")
        for v in vars_list:
            print(f"  {v['variable']}: keys={list(v.keys())}")
        break
