"""
简历-招聘 Crawl API Mock 服务
端口: 8899
模拟工作流中依赖的后端API端点
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import uuid
from datetime import datetime

app = FastAPI(title="Crawl API Mock", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟存储
mock_candidates_db = [
    {
        "id": "cand-001",
        "name": "张三",
        "phone": "13800001111",
        "email": "zhangsan@example.com",
        "education": {"degree": "硕士", "school": "北京大学", "major": "计算机科学"},
        "experience": {"years": 5, "last_company": "字节跳动", "title": "高级前端工程师"},
        "skills": ["React", "TypeScript", "Node.js", "Python"],
        "raw_text": "张三，5年前端开发经验，精通React和TypeScript，曾主导字节跳动某中台项目..."
    },
    {
        "id": "cand-002",
        "name": "李四",
        "phone": "13900002222",
        "email": "lisi@example.com",
        "education": {"degree": "本科", "school": "清华大学", "major": "软件工程"},
        "experience": {"years": 3, "last_company": "阿里巴巴", "title": "后端开发工程师"},
        "skills": ["Java", "Spring Boot", "MySQL", "Redis", "Docker"],
        "raw_text": "李四，3年Java后端开发，熟悉微服务架构，参与过双十一大促系统开发..."
    },
    {
        "id": "cand-003",
        "name": "王五",
        "phone": "13700003333",
        "email": "wangwu@example.com",
        "education": {"degree": "博士", "school": "复旦大学", "major": "人工智能"},
        "experience": {"years": 2, "last_company": "腾讯", "title": "算法研究员"},
        "skills": ["PyTorch", "TensorFlow", "NLP", "推荐系统"],
        "raw_text": "王五，AI方向博士，研究方向为自然语言处理与推荐系统，发表顶会论文3篇..."
    },
    {
        "id": "cand-004",
        "name": "赵六",
        "phone": "13600004444",
        "email": "zhaoliu@example.com",
        "education": {"degree": "本科", "school": "浙江大学", "major": "电子信息工程"},
        "experience": {"years": 7, "last_company": "华为", "title": "技术总监"},
        "skills": ["C++", "嵌入式", "Linux内核", "团队管理"],
        "raw_text": "赵六，7年嵌入式开发经验，带领10人团队完成多个芯片项目..."
    },
]


@app.get("/health")
async def health():
    return {"status": "ok", "service": "crawl-api-mock", "port": 8899}


@app.post("/api/v1/crawl")
async def crawl(request: Request):
    """
    拉取邮件 — 模拟爬取邮箱中的简历邮件
    Dify 工作流第二个节点调用
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    email_address = body.get("email_address", "unknown@example.com")
    auth_code = body.get("auth_code", "***")
    raw_jd_text = body.get("raw_jd_text", "")

    print(f"[CRAWL] email={email_address}, jd_len={len(raw_jd_text)}")

    return {
        "success": True,
        "message": f"成功从 {email_address} 拉取邮件",
        "total_emails_fetched": 12,
        "resume_emails": 4,
        "extraction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/extractions")
async def get_extractions(per_page: int = 50):
    """
    获取候选人列表
    """
    items = []
    for i, c in enumerate(mock_candidates_db):
        items.append({
            "id": c["id"],
            "data": {
                "name": c["name"],
                "phone": c["phone"],
                "email": c["email"],
                "education": c["education"],
                "experience": c["experience"],
                "skills": c["skills"],
            },
            "raw_text": c["raw_text"],
            "extracted_at": datetime.now().isoformat(),
        })

    return {
        "success": True,
        "total": len(items),
        "per_page": per_page,
        "items": items[:per_page],
    }


@app.post("/api/v1/talent-pool")
async def write_talent_pool(request: Request):
    """
    写回人才库
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    print(f"[TALENT-POOL] write: {json.dumps(body, ensure_ascii=False)[:200]}")

    return {
        "success": True,
        "written_id": str(uuid.uuid4()),
        "message": "候选人信息已写入人才库",
    }


@app.post("/api/v1/candidates")
async def post_candidates(request: Request):
    """备选端点: 写回人才库"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    print(f"[CANDIDATES] write: {json.dumps(body, ensure_ascii=False)[:200]}")
    return {"success": True, "written_id": str(uuid.uuid4())}


if __name__ == "__main__":
    print("=" * 50)
    print("Crawl API Mock 启动在 http://0.0.0.0:8899")
    print("端点:")
    print("  POST /api/v1/crawl        — 拉取邮件")
    print("  GET  /api/v1/extractions   — 获取候选人")
    print("  POST /api/v1/talent-pool   — 写回人才库")
    print("  POST /api/v1/candidates    — 写回人才库(备选)")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8899, log_level="info")
