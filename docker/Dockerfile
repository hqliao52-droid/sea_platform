# 使用slim版本减小镜像体积
FROM python:3.10-slim 

WORKDIR /app

# 安装系统依赖（如果需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 生产环境：不使用缓存
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 生产环境：移除--reload，添加worker参数
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]