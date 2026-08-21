import uuid
import time


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
