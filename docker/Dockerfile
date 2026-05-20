# 使用 slim 版本减小镜像体积
FROM python:3.10-slim

WORKDIR /app

# 安装基础工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖（使用清华镜像）
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --default-timeout=1000 \
    -r requirements.txt

# 【关键】设置 Playwright 使用国内镜像
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 安装 Playwright Chromium 浏览器及其系统依赖
RUN python -m playwright install --with-deps chromium

# 复制项目代码
COPY . .

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]