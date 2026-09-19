import requests, json

body = {
    "query": "找Python后端",
    "inputs": {"email_address": "z@qq.com", "auth_code": "x", "raw_jd_text": "Python Django后端开发"},
    "response_mode": "blocking",
    "user": "zhou"
}
r = requests.post(
    "http://localhost/v1/chat-messages",
    json=body,
    headers={"Authorization": "Bearer app-Resume01TestToken"},
    timeout=600
)
data = r.json()
print(f"tokens={data['metadata']['usage']['total_tokens']}")
print(f"answer_len={len(data['answer'])}")
print(f"answer={data['answer'][:500]}")
