from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import re


async def fetch_full_text(url):
    # 1. 先尝试 requests
    result = await fetch_by_requests(url)

    # 2. 成功则直接返回
    if result and result["status"] == "success":
        return result

    # 3. requests 失败，自动使用 Playwright
    print("requests 抓取失败，切换 Playwright...")
    return await fetch_by_playwright(url)


async def fetch_by_requests(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = await requests.get(url, headers=headers, timeout=12)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html = resp.text

        # 检测反爬页面
        if "百度安全验证" in html or "captcha" in html.lower() or "安全验证" in html:
            return {"status": "fail", "content": "触发反爬"}

        return extract_content(html)

    except Exception as e:
        print(f"requests 抓取失败: {e}")
        return {"status": "fail", "content": str(e)}


async def fetch_by_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--disable-blink-features=AutomationControlled"]
            )

            page = await browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )

            await page.goto(url, wait_until="networkidle", timeout=60000)

            html = page.content()

            await browser.close()

        if "百度安全验证" in html or "captcha" in html.lower() or "安全验证" in html:
            return {"status": "fail", "content": "Playwright 仍触发安全验证"}

        return extract_content(html)

    except Exception as e:
        print(f"Playwright 抓取失败: {e}")
        return {"status": "fail", "content": str(e)}


def extract_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # 清理无用标签
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
        tag.decompose()

    common_selectors = [
        "article",
        ".article",
        "#article",
        ".content",
        "#content",
        ".post",
        ".entry",
        ".story",
        ".main-content",
        ".article-content",
        ".text",
        ".detail",
        ".news-content",
        ".pages_content",
        ".TRS_Editor",
        ".main",
        "#main",
        ".box-content",
        ".article-body",
        ".bjh-content",  # 百家号常见选择器
        ".mainContent",
    ]

    content = None

    for sel in common_selectors:
        tag = soup.select_one(sel)
        if tag and len(tag.get_text(strip=True)) > 20:
            content = tag.get_text("\n", strip=True)
            break

    # 自动识别最大正文块
    if not content:
        max_len = 0
        best_div = None
        for div in soup.find_all("div"):
            text = div.get_text(strip=True)
            if len(text) > 800 and len(text) > max_len:
                max_len = len(text)
                best_div = div
        if best_div:
            content = best_div.get_text("\n", strip=True)

    # 提取 p 标签兜底
    if not content:
        paragraphs = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > 10
        ]
        content = "\n".join(paragraphs)

    if not content:
        return {"status": "fail", "content": "未提取到正文"}

    # 清理文本
    content = re.sub(r"\n+", "\n", content)
    content = re.sub(r"[ \t]+", " ", content).strip()

    if len(content) < 50:
        return {"status": "fail", "content": "文本长度过短"}

    return {"status": "success", "content": content}


def clean_baijiahao_text(text: str) -> str:
    lines = text.split("\n")

    bad_keywords = [
        "百度首页",
        "登录",
        "搜索",
        "复制",
        "相关搜索",
        "评论",
        "发表",
        "作者最新文章",
        "换一换",
        "举报/反馈",
        "收藏",
        "分享",
        "微信好友",
        "新浪微博",
        "扫码",
        "设为首页",
        "©",
        "Baidu",
        "热",
        "新",
        "阅读",
        "分钟前",
        "关注",
    ]

    cleaned = []
    for line in lines:
        line = line.strip()

        # 过滤空行
        if not line:
            continue

        # 过滤短垃圾行
        if len(line) < 4:
            continue

        # 过滤关键词行
        if any(k in line for k in bad_keywords):
            continue

        # 过滤纯时间 / 数字
        if re.match(r"^\d+(:\d+)?$", line):
            continue

        cleaned.append(line)

    # 合并
    result = "\n".join(cleaned)

    # 再压缩多余换行
    result = re.sub(r"\n+", "\n", result).strip()

    return result
