import yaml, json, os

# Read original DSL
with open('/tmp/original.yml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

workflow = data['workflow']
graph = workflow['graph']
features = workflow.get('features', {})

graph_json = json.dumps(graph, ensure_ascii=False)
features_json = json.dumps(features, ensure_ascii=False)

# Write to temp files for psql
with open('/tmp/g.json', 'w', encoding='utf-8') as f:
    f.write(graph_json)
with open('/tmp/f.json', 'w', encoding='utf-8') as f:
    f.write(features_json)

print("OK", len(graph_json), len(features_json))
