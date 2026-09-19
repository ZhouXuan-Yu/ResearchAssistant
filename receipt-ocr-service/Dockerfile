# =====================
# Receipt OCR Service — Dockerfile (EasyOCR)
# =====================
FROM python:3.11-slim

LABEL maintainer="ZhouXuan"
LABEL description="Receipt OCR microservice based on EasyOCR + FastAPI"

WORKDIR /app

# 系统依赖（OpenCV 运行时）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# 应用代码
COPY app/ ./app/
COPY config.yaml .

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "info"]
