FROM python:3.12-slim-bookworm AS builder

# 从官方镜像复制 uv 和 uvx 二进制文件，无需 pip install uv[reference:0]
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 为 uv 配置国内镜像源，并设置 Docker 环境下的推荐变量[reference:1]
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_HTTP_TIMEOUT=300

# 先只复制依赖声明文件，利用 Docker 层缓存：代码变动时无需重装依赖
COPY pyproject.toml uv.lock ./

# 安装生产依赖（不安装项目本身，不安装 dev 依赖）
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# 复制项目源码，并完成项目本身的安装
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim-bookworm

WORKDIR /app

# 从 builder 阶段仅复制虚拟环境，保持最终镜像精简（不含 uv、编译器）
COPY --from=builder /app/.venv /app/.venv

# 在镜像构建阶段安装 Playwright 浏览器及其 Linux 系统依赖
# --with-deps 会自动处理 Chromium 所需的库，替代原先手动 apt-get 安装的部分[reference:5]
RUN /app/.venv/bin/python -m playwright install --with-deps chromium

# 将 venv 的 bin 目录置于 PATH 最前，后续命令可直接使用 uvicorn 等
ENV PATH="/app/.venv/bin:$PATH"

# 如果项目运行时仍需其他系统依赖（如之前列表中的 libgtk-3-0 等），可在此处一并安装
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgtk-3-0 libgbm1 libasound2 \
#     && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]