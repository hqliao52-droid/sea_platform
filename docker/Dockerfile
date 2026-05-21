FROM python:3.10-slim

WORKDIR /app

# =========================
# 1. 换 Debian 源（关键提速）
# =========================
RUN sed -i 's|deb.debian.org|mirrors.tencentyun.com|g' /etc/apt/sources.list.d/debian.sources || true

# =========================
# 2. 安装系统依赖（最小化）
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# 3. Python依赖（使用国内源）
# =========================
COPY requirements.txt .

RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

# =========================
# 4. 关键：Playwright 国内镜像（必须生效）
# =========================
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright

# =========================
# 5. 安装浏览器（核心步骤）
# =========================
RUN python -m playwright install chromium

# =========================
# 6. 复制代码
# =========================
COPY . .

# =========================
# 7. 启动
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]