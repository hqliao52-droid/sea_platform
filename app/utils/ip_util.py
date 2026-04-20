from fastapi import Request

'''从请求中拿IP
    1、先拿请求头，headers --> HTTP请求里有很多 header，比如: X-Forwarded-For: 1.1.1.1, 2.2.2.2    X-Real-IP: 1.1.1.1
    2、优先取 X-Forwarded-For 这个字段通常是用户真实IP, 代理1, 代理2, ... eg:203.0.113.5, 10.0.0.1  只取第一个IP（往往是真实IP，后续是代理链）
    3、如果取不到，再取 X-Real-IP 
    4、最后兜底：如果没有代理，直接用客户端IP
'''
def get_real_ip(request: Request):
    headers = request.headers

    x_forwarded_for = headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip

    return request.client.host