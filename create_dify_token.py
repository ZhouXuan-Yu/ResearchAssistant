"""Create a Dify Console API token by directly querying the DB."""
import uuid
import secrets
import hashlib
import datetime

# Generate a random token
raw_token = secrets.token_hex(32)
# Dify hashes tokens before storing
hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

# tenant_id from the database
tenant_id = "50c15e0b-2bb9-4db6-9e7d-e61e75190c72"
token_id = str(uuid.uuid4())
now = datetime.datetime.utcnow().isoformat()

# Print the SQL statement and the raw token
print("RAW_TOKEN:", raw_token)
print("HASHED:", hashed_token)
print("TOKEN_ID:", token_id)
print()
print("--- SQL ---")
print(f"INSERT INTO api_tokens (id, tenant_id, type, token, created_at) VALUES ('{token_id}', '{tenant_id}', 'console', '{hashed_token}', '{now}');")
