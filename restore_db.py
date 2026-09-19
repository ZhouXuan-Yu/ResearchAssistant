import json, sqlite3

# Read graph
with open('/tmp/graph.json') as f:
    graph = f.read()
with open('/tmp/features.json') as f:
    features = f.read()

# Use psql directly
import subprocess
sql = f"""INSERT INTO workflows (id, tenant_id, app_id, type, version, graph, features, created_by, environment_variables, conversation_variables) 
VALUES ('00000000-0000-0000-0000-000000000010', '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', '22b49776-b615-4a49-bd26-bd5ca8454d5e', 'workflow', 'draft', $GRAPH$, $FEATURES$, '50c15e0b-2bb9-4db6-9e7d-e61e75190c72', '{}', '{}');"""

# Use dollar quoting for safety
full_sql = sql.replace('$GRAPH$', graph).replace('$FEATURES$', features)

with open('/tmp/insert.sql', 'w') as f:
    f.write(full_sql)

# Execute
result = subprocess.run(
    ['psql', '-U', 'postgres', '-d', 'dify', '-f', '/tmp/insert.sql'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout[:200])
print("STDERR:", result.stderr[:200])
print("RC:", result.returncode)
