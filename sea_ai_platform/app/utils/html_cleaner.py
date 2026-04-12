# app/utils/html_cleaner.py

from bs4 import BeautifulSoup


def clean_html_to_text(html: str) -> str:
    """
    去除HTML标签，只保留文本内容
    将HTML转换为纯文本（用于AI处理）

    原理：
    1. BeautifulSoup解析HTML
    2. 去掉所有标签
    3. 保留文本内容
    """

    soup = BeautifulSoup(html, "html.parser")

    # 去掉 script / style（避免污染）
    for tag in soup(["script", "style"]):
        tag.decompose()

    # 获取纯文本
    text = soup.get_text(separator="\n")

    # 去除多余空行
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return "\n".join(lines)