import time

from uuid import uuid4

from app.utils.log import logger

class RequestLogMiddleware:
    """请求级日志中间件：记录状态码与耗时，未捕获异常时留下完整堆栈。

    刻意用纯 ASGI 实现而不是 BaseHTTPMiddleware（@app.middleware("http")）：
    后者会包装 send，对 /chatMessage 的 SSE 流式响应有已知副作用
    （缓冲分块、让 request.is_disconnected() 失效）。
    这里只在 send 旁路读取状态码，不改变任何传输行为。
    """

    # 静态资源请求量大且无诊断价值，跳过以免刷屏
    SKIP_PREFIXES = ("/attach", "/static")

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path", "").startswith(
            self.SKIP_PREFIXES
        ):
            await self.app(scope, receive, send)
            return

        request_id = uuid4().hex[:8]
        # 存进 scope state，兜底异常处理器可以用 request.state.request_id 关联
        scope.setdefault("state", {})["request_id"] = request_id

        method = scope.get("method", "-")
        path = scope.get("path", "-")
        start = time.perf_counter()
        status = {"code": 500}

        async def send_with_status(message):
            if message["type"] == "http.response.start":
                status["code"] = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_with_status)
        except Exception:
            logger.opt(exception=True).error(
                "[{}] {} {} 抛出未捕获异常，耗时 {:.1f}ms",
                request_id,
                method,
                path,
                (time.perf_counter() - start) * 1000,
            )
            raise
        else:
            # 耗时包含 SSE 整条流的时长，长连接请求会在流结束后才落日志
            cost_ms = (time.perf_counter() - start) * 1000
            log = logger.warning if status["code"] >= 500 else logger.info
            log(
                "[{}] {} {} -> {} {:.1f}ms",
                request_id,
                method,
                path,
                status["code"],
                cost_ms,
            )