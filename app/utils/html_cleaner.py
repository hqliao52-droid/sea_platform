# app/utils/html_cleaner.py

from bs4 import BeautifulSoup
import bleach

ALLOWED_TAGS = [
    'p', 'br', 'div',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'b', 'em', 'i', 'u', 'del',
    'ul', 'ol', 'li',
    'img', 'a',
    'blockquote'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt'],
}
DENY_TAGS = ['script', 'iframe', 'frame', 'object', 'embed', 'style', 'link', 'svg', 'math']

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


def clean_html_for_all_platform(html_content):
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in DENY_TAGS:
        for t in soup.find_all(tag):
            t.decompose()  # 彻底移除

    cleaned = bleach.clean(
        str(soup),
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True
    )
    return cleaned.strip()
