FROM python:3.10-slim

WORKDIR /app

# 这一层很少变化
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 【关键】这一层只有在 requirements.txt 变化时才重新安装
COPY requirements.txt .
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

# 【关键】这一层很少重新执行（除非上面的层变化）
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
RUN python -m playwright install --with-deps chromium  # 会被缓存！

# 这一层经常变化
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]