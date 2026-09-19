import yaml

with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'r', encoding='utf-8') as f:
    dsl = yaml.safe_load(f)

for ev in dsl['workflow'].get('environment_variables', []):
    if 'value_type' not in ev:
        ev['value_type'] = 'string'

with open(r'C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-workflow.yml', 'w', encoding='utf-8') as f:
    yaml.dump(dsl, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print('Fixed env vars with value_type')
