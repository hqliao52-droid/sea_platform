import uuid
import time
import json

from starlette.responses import StreamingResponse
from typing import AsyncGenerator, Any, Dict, Optional, List, Set

def generate_id(is_uuid: bool = False) -> str:
    """生成一个唯一的ID
    args:
        is_uuid 若为 True，则返回一个 UUID

    return:
        str: 生成的唯一ID
    """
    if is_uuid:
        return str(uuid.uuid4())
    ts = format(time.time_ns(), "x")
    rand = uuid.uuid4().hex[:8]
    val = (ts + rand)[:32]
    return f"{val[0:8]}-{val[8:12]}-{val[12:16]}-{val[16:20]}-{val[20:32]}"

class SSEEvent:
    """SSE 事件包构造器"""

    @staticmethod
    def metadata(field: str, content: Any) -> Dict[str, Any]:
        """构造元数据事件"""
        return {"type": "metadata", "field": field, "content": content}

    @staticmethod
    def delta(field: str, content: Any, index: Optional[int] = None) -> Dict[str, Any]:
        """构造增量数据事件"""
        event = {"type": "delta", "field": field, "content": content}
        if index is not None:
            event["index"] = index
        return event

    @staticmethod
    def error(code: int = 500, message: str = "") -> Dict[str, Any]:
        """构造错误事件"""
        return {"type": "error", "code": code, "message": message}

    @staticmethod
    def done(status: str = "success") -> Dict[str, Any]:
        """构造结束事件"""
        return {"type": "done", "status": status}

    @staticmethod
    def custom(event_type: str, **kwargs) -> Dict[str, Any]:
        """构造自定义事件（扩展用）"""
        return {"type": event_type, **kwargs}

    @staticmethod
    async def serialize(event: Dict[str, Any]) -> str:
        """将事件字典序列化为 SSE 格式字符串"""
        try:
            json_data = json.dumps(event, ensure_ascii=False)
            return f"data: {json_data}\n\n"
        except Exception as e:
            # 序列化失败时返回错误事件
            error_event = SSEEvent.error(code=500, message=f"Serialize error: {str(e)}")
            json_data = json.dumps(error_event, ensure_ascii=False)
            return f"data: {json_data}\n\n"

async def stream_json_fields(
    text_async_gen: AsyncGenerator[str, None], fields_list: List[str]
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    流式解析 JSON 对象里的目标字段值。
    - text_async_gen: async generator，产生 LLM 的文本增量
    - fields_list: 需要流式返回的字段名列表

    和“先拼完整 JSON 再 json.loads”不同，这里按字符增量解析。
    一旦识别到目标字段的 value，就立刻把新增内容向下游发送。

    约定：
    1. 输入是一个 JSON object。
    2. fields_list 只描述需要监听的 key，不绑定具体业务字段。
    3. value 可以是 string / number / bool / null / object / array。
    4. 对 string value，事件里的 content 是解码后的增量文本。
    5. 对非 string value，事件里的 content 是该 value 的 JSON 文本增量。
    """
    target_fields: Set[str] = set(fields_list)

    # 整体只解析一个顶层 JSON object，所以先等到第一个 { 再开始进入状态机。
    started = False
    object_depth = 0
    mode = "seek_object"

    # current_key: 当前刚解析出来的 key
    # active_field: 当前 value 是否属于 fields_list 里需要流式返回的字段
    current_key_chars: List[str] = []
    current_key: Optional[str] = None
    active_field: Optional[str] = None

    # 处理字符串场景下的转义字符，例如 \n、\"、\u4f60
    escape = False
    unicode_buffer: Optional[str] = None

    # 当 value 是 object / array 时，用它追踪当前嵌套层级，
    # 直到整个 value 闭合为止。
    nested_depth = 0

    def _decode_escaped_char(ch: str) -> str:
        escape_map = {
            '"': '"',
            "\\": "\\",
            "/": "/",
            "b": "\b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
        }
        return escape_map.get(ch, ch)

    async def _emit(field: Optional[str], content: str):
        if field and content:
            yield SSEEvent.delta(field=field, content=content)

    async for chunk in text_async_gen:
        for ch in chunk:
            if not started:
                if ch != "{":
                    continue
                started = True
                object_depth = 1
                mode = "seek_key_or_end"
                continue

            # 顶层 object 内，等待下一个 key，或者遇到 } 说明整个 JSON 已结束。
            if mode == "seek_key_or_end":
                if ch in " \r\n\t,":
                    continue
                if ch == "}":
                    object_depth -= 1
                    if object_depth == 0:
                        return
                    continue
                if ch == '"':
                    current_key_chars = []
                    escape = False
                    unicode_buffer = None
                    mode = "in_key"
                continue

            # 逐字符读取 key，支持 key 中的转义。
            if mode == "in_key":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        try:
                            current_key_chars.append(chr(int(unicode_buffer, 16)))
                        except ValueError:
                            current_key_chars.append("\\u" + unicode_buffer)
                        unicode_buffer = None
                        escape = False
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        current_key_chars.append(_decode_escaped_char(ch))
                        escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    current_key = "".join(current_key_chars)
                    mode = "after_key"
                    continue
                current_key_chars.append(ch)
                continue

            # key 结束后，继续等冒号 :，进入 value 解析。
            if mode == "after_key":
                if ch in " \r\n\t":
                    continue
                if ch == ":":
                    active_field = current_key if current_key in target_fields else None
                    current_key = None
                    mode = "before_value"
                continue

            # 看到 value 的第一个有效字符后，决定它是哪种类型：
            # string、普通字面量(number/bool/null)、或者 object/array。
            if mode == "before_value":
                if ch in " \r\n\t":
                    continue
                if ch == '"':
                    escape = False
                    unicode_buffer = None
                    mode = "in_string_value" if active_field else "skip_string_value"
                    continue
                if ch in "[{":
                    nested_depth = 1
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    mode = "in_nested_value"
                    continue

                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                mode = "in_literal_value"
                continue

            # string value: 边接收边发送，真正做到“还没闭合就先流出去”。
            if mode == "in_string_value":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        try:
                            decoded = chr(int(unicode_buffer, 16))
                        except ValueError:
                            decoded = "\\u" + unicode_buffer
                        unicode_buffer = None
                        escape = False
                        async for event in _emit(active_field, decoded):
                            yield event
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                        async for event in _emit(
                            active_field, _decode_escaped_char(ch)
                        ):
                            yield event
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    active_field = None
                    mode = "after_value"
                    continue
                async for event in _emit(active_field, ch):
                    yield event
                continue

            # 非目标字段的 string value 直接跳过，但仍要正确消费掉完整字符串。
            if mode == "skip_string_value":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        unicode_buffer = None
                        escape = False
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    mode = "after_value"
                continue

            # number / bool / null 这类字面量，直到逗号或 } 才算结束。
            if mode == "in_literal_value":
                if ch in ",}":
                    active_field = None
                    mode = "seek_key_or_end"
                    if ch == "}":
                        object_depth -= 1
                        if object_depth == 0:
                            return
                    continue
                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                continue

            # object / array value：原样透传 JSON 文本，并靠 nested_depth 判断何时闭合。
            if mode == "in_nested_value":
                if ch == '"':
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    escape = False
                    unicode_buffer = None
                    mode = "in_nested_string"
                    continue

                if ch in "[{":
                    nested_depth += 1
                elif ch in "]}":
                    nested_depth -= 1

                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event

                if nested_depth == 0:
                    active_field = None
                    mode = "after_value"
                continue

            # object / array 内部如果进入字符串，同样要避免把字符串里的 } ] 误判成结构结束。
            if mode == "in_nested_string":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        unicode_buffer = None
                        escape = False
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    continue
                if ch == "\\":
                    escape = True
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    continue
                if ch == '"':
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    mode = "in_nested_value"
                    continue
                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                continue

            # 一个 value 结束后，只可能继续遇到 , 或 }，然后回到顶层 key 解析。
            if mode == "after_value":
                if ch in " \r\n\t":
                    continue
                if ch == ",":
                    mode = "seek_key_or_end"
                    continue
                if ch == "}":
                    object_depth -= 1
                    if object_depth == 0:
                        return
                    mode = "seek_key_or_end"


async def stream_json_fields_latex(
    text_async_gen: AsyncGenerator[str, None], fields_list: List[str]
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    流式解析 JSON 对象里的目标字段值（专为 LaTeX 公式优化）。
    与原始版本(stream_json_fields)的区别：遇到非标准 JSON 转义（如 \p, \a）时，不再丢弃反斜杠，
    而是将 '\' 和后续字符原样发送，以保留 LaTeX 命令（如 \perp）。
    """
    target_fields: Set[str] = set(fields_list)

    started = False
    object_depth = 0
    mode = "seek_object"

    current_key_chars: List[str] = []
    current_key: Optional[str] = None
    active_field: Optional[str] = None

    escape = False
    unicode_buffer: Optional[str] = None
    nested_depth = 0

    # 改点：替换原有的 _decode_escaped_char 
    ESCAPE_MAP = {
        '"': '"',
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    def _handle_escaped_char_latex(ch: str) -> List[str]:
        """
        处理转义字符。
        - 如果是标准 JSON 转义（如 n, t, \），返回解码后的单个字符。
        - 如果是未知转义（如 p, P, a），返回 [反斜杠, 原字符] 以保留 LaTeX 命令。
        """
        if ch in ESCAPE_MAP:
            # 注意：这里返回列表，便于统一迭代
            return [ESCAPE_MAP[ch]]
        else:
            # LaTeX 兼容：保留反斜杠和后续字母，例如 \p -> ["\\", "p"]
            return ["\\", ch]

    async def _emit(field: Optional[str], content: str):
        if field and content:
            yield {"type": "delta", "field": field, "content": content}

    async for chunk in text_async_gen:
        for ch in chunk:
            # 状态机逻辑

            if not started:
                if ch != "{":
                    continue
                started = True
                object_depth = 1
                mode = "seek_key_or_end"
                continue

            if mode == "seek_key_or_end":
                if ch in " \r\n\t,":
                    continue
                if ch == "}":
                    object_depth -= 1
                    if object_depth == 0:
                        return
                    continue
                if ch == '"':
                    current_key_chars = []
                    escape = False
                    unicode_buffer = None
                    mode = "in_key"
                continue

            # 改点: in_key 分支
            if mode == "in_key":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        try:
                            current_key_chars.append(chr(int(unicode_buffer, 16)))
                        except ValueError:
                            current_key_chars.append("\\u" + unicode_buffer)
                        unicode_buffer = None
                        escape = False
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        # 原来: current_key_chars.append(_decode_escaped_char(ch))
                        # 现在: 循环添加保留的字符
                        for c in _handle_escaped_char_latex(ch):
                            current_key_chars.append(c)
                        escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    current_key = "".join(current_key_chars)
                    mode = "after_key"
                    continue
                current_key_chars.append(ch)
                continue

            if mode == "after_key":
                if ch in " \r\n\t":
                    continue
                if ch == ":":
                    active_field = current_key if current_key in target_fields else None
                    current_key = None
                    mode = "before_value"
                continue

            if mode == "before_value":
                if ch in " \r\n\t":
                    continue
                if ch == '"':
                    escape = False
                    unicode_buffer = None
                    mode = "in_string_value" if active_field else "skip_string_value"
                    continue
                if ch in "[{":
                    nested_depth = 1
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    mode = "in_nested_value"
                    continue

                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                mode = "in_literal_value"
                continue

            # 改点: in_string_value 分支
            if mode == "in_string_value":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        try:
                            decoded = chr(int(unicode_buffer, 16))
                        except ValueError:
                            decoded = "\\u" + unicode_buffer
                        unicode_buffer = None
                        escape = False
                        async for event in _emit(active_field, decoded):
                            yield event
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                        # 原来: async for event in _emit(active_field, _decode_escaped_char(ch))
                        # 现在: 将反斜杠和字符逐个发送
                        for c in _handle_escaped_char_latex(ch):
                            async for event in _emit(active_field, c):
                                yield event
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    active_field = None
                    mode = "after_value"
                    continue
                async for event in _emit(active_field, ch):
                    yield event
                continue

            # 非目标字段的字符串跳过
            if mode == "skip_string_value":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        unicode_buffer = None
                        escape = False
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == '"':
                    mode = "after_value"
                continue

            if mode == "in_literal_value":
                if ch in ",}":
                    active_field = None
                    mode = "seek_key_or_end"
                    if ch == "}":
                        object_depth -= 1
                        if object_depth == 0:
                            return
                    continue
                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                continue

            if mode == "in_nested_value":
                if ch == '"':
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    escape = False
                    unicode_buffer = None
                    mode = "in_nested_string"
                    continue

                if ch in "[{":
                    nested_depth += 1
                elif ch in "]}":
                    nested_depth -= 1

                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event

                if nested_depth == 0:
                    active_field = None
                    mode = "after_value"
                continue

            # 改点3: in_nested_string 分支（嵌套对象/数组内的字符串） 
            if mode == "in_nested_string":
                if unicode_buffer is not None:
                    unicode_buffer += ch
                    if len(unicode_buffer) == 4:
                        unicode_buffer = None
                        escape = False
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    continue
                if escape:
                    if ch == "u":
                        unicode_buffer = ""
                    else:
                        escape = False
                        if active_field:
                            # 原来: async for event in _emit(active_field, _decode_escaped_char(ch))
                            # 现在: 将反斜杠和字符逐个发送
                            for c in _handle_escaped_char_latex(ch):
                                async for event in _emit(active_field, c):
                                    yield event
                    continue
                if ch == "\\":
                    escape = True
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    continue
                if ch == '"':
                    if active_field:
                        async for event in _emit(active_field, ch):
                            yield event
                    mode = "in_nested_value"
                    continue
                if active_field:
                    async for event in _emit(active_field, ch):
                        yield event
                continue

            if mode == "after_value":
                if ch in " \r\n\t":
                    continue
                if ch == ",":
                    mode = "seek_key_or_end"
                    continue
                if ch == "}":
                    object_depth -= 1
                    if object_depth == 0:
                        return
                    mode = "seek_key_or_end"
