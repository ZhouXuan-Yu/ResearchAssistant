import yaml, json
with open('/tmp/original.yml') as f:
    data = yaml.safe_load(f)
graph = data['workflow']['graph']
graph_json = json.dumps(graph, ensure_ascii=False)
features_json = json.dumps(data['workflow']['features'], ensure_ascii=False)
print("GRAPH_LEN:", len(graph_json))
# Save to file for psql
with open('/tmp/graph.json', 'w') as f:
    f.write(graph_json)
with open('/tmp/features.json', 'w') as f:
    f.write(features_json)
print("DONE")
