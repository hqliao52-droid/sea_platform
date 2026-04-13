# 使用python 3.10 作为基础镜像
FROM python:3.10 

# 设置工作目录
WORKDIR /app

# 复制requirements.txt 文件到工作目录
COPY requirements.txt .

# 安装requirements.txt 中的所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

# 启动FastAPI 应用
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]