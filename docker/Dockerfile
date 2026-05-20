FROM python:3.10-slim

WORKDIR /app

# 安装基础依赖（仅首次构建或 Dockerfile 变化时执行）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖（只有 requirements.txt 变化时才重新执行）
COPY requirements.txt .
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

# 使用国内镜像下载 Playwright 浏览器
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 安装 Chromium 浏览器（不自动安装大量系统依赖，速度更快）
RUN python -m playwright install chromium

# 复制项目代码（代码变化时只会重新执行这一层及之后的层）
COPY . .

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]