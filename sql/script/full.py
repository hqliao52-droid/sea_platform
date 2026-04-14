import requests
from bs4 import BeautifulSoup
import re

def fetch_full_text(url,rss_url):
    """
    【通用版】爬取任意网页的文章正文（支持新闻、政府、资讯、博客等所有网站）
    不绑定任何域名，自动识别正文，适配 28+ RSS 源
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # 1. 请求页面
        resp = requests.get(url, headers=headers, timeout=12)
        resp.raise_for_status()
        resp.encoding = get_proper_encoding(resp)  # 智能编码
        html = resp.text
        print(html)

        # 2. 解析DOM
        soup = BeautifulSoup(html, "html.parser")
        clean_soup(soup)  # 清理垃圾标签（导航、广告、侧边栏）

        content = None


        # ==============================================
        # 第一层：匹配全行业最常见的正文容器（覆盖80%网站）
        # 政府、新闻、门户、公众号、地方站通用
        # ==============================================
        common_selectors = [
            "article",                        # 标准HTML5文章标签
            ".article", "#article",
            ".content", "#content",
            ".post", ".entry", ".story",      # 博客/新闻通用
            ".main-content", ".article-content",
            ".text", ".detail", ".news-content",
            ".pages_content", ".TRS_Editor",  # 兼容旧政府网
            ".main", "#main",
            ".box-content", ".article-body",
            "#app main article",
            "#app .article-content",
            "#app .content-detail",
            "section#app main .article-body",
        ]

        for sel in common_selectors:
            tag = soup.select_one(sel)
            if tag and len(tag.get_text(strip=True)) > 20:  # 正文至少有20字
                content = tag.get_text(strip=True, separator="\n")
                break

        # ==============================================
        # 第二层：智能正文识别（找不到标签时自动找文字最多的区域）
        # ==============================================
        if not content:
            content = auto_detect_article(soup)

        # ==============================================
        # 第三层：兜底提取所有 <p> 标签（任何网站都有p）
        # ==============================================
        if not content:
            p_tags = soup.find_all("p")
            paragraphs = [p.get_text(strip=True) for p in p_tags if p.get_text(strip=True)]
            paragraphs = [p for p in paragraphs if len(p) > 10]  # 过滤短行
            content = "\n".join(paragraphs)

        # 最终清理
        content = clean_text(content)
        if len(content.strip()) > 50:
            result = {"content":content,"status":"success"}
        else:
            result = {"content":"文本长度过短！","status":"fail"}
            
        return result

    except Exception as e:
        print(f"[爬取失败] {url} | 错误：{str(e)[:50]}")
        return None

# ===================== 以下是工具函数，让通用爬取更稳定 =====================
def get_proper_encoding(resp):
    """智能识别编码，解决乱码"""
    if resp.apparent_encoding:
        return resp.apparent_encoding
    return "utf-8"

def clean_soup(soup):
    """删除广告、导航、脚本、样式"""
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
        tag.decompose()

def auto_detect_article(soup):
    """自动找文字密度最高的div（最核心的通用识别算法）"""
    max_text_len = 0
    best_div = None
    for div in soup.find_all("div"):
        text = div.get_text(strip=True)
        if len(text) > 800 and len(text) > max_text_len:  # 文章一般都大于800字符
            max_text_len = len(text)
            best_div = div
    return best_div.get_text(strip=True, separator="\n") if best_div else None

def clean_text(text):
    """清理多余空格、换行、制表符"""
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r" +", " ", text)
    return text


if __name__ == "__main__":
    url = "https://www.oschina.net/news/420244"
    rss_url = "https://www.oschina.net/news/rss"
    result = fetch_full_text(url,rss_url)
    print(result)