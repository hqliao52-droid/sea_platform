import feedparser
from services.news_service import NewsOperator
from utils.convert_json import rss_date_convert
from utils.html_cleaner import clean_html_to_text

def spider_techcrunch():
    techcrunch = feedparser.parse("https://techcrunch.com/feed/")
    if techcrunch.entries == [] : return None

    for t in techcrunch.entries:
        published_at = rss_date_convert(t["published_parsed"])
        
        r = clean_html_to_text(t["summary"])

        news_data = {"title": t.title,
                    "url": t.link,
                    "source": t.title_detail.base,
                    "content": r,
                    "authors": ', '.join([x["name"] for x in t["authors"]]) if t.get("authors") else '',
                    "keywords": ', '.join([x["term"] for x in t["tags"]]) if t.get("tags") else '',
                    "category": ', '.join([x["term"] for x in t["tags"]]) if t.get("tags") else '',
                    "ai_summary": t.summary,
                    "summary": t.summary,
                    "published_at": published_at
                    }
        
        print("打印信息",news_data)
    
    return NewsOperator.insert_news(news_data)

def spider_rss(req_url):
    rss_result = feedparser.parse(req_url)

    if rss_result.entries == [] : return None

    pre_list = []
    for r in rss_result.entries:
        title = r["title"] if "title" in r else None
        url = r.link if "link" in r else None
        source = r.title_detail.base if "title_detail" in r else None
        content = clean_html_to_text(r["summary"]) if "summary" in r else None

        author_list = r["authors"] if "authors" in r else None
        if author_list != None:
            authors = ', '.join([x["name"] for x in r["authors"]]) if r["authors"] else ''
        else:
            authors = ''

        keywords_list = r["tags"] if "tags" in r else None
        if keywords_list != None:
            keywords = ', '.join([x["term"] for x in r["tags"]]) if r["tags"] else ''
        else:
            keywords = ''

        category_list = r["tags"] if "tags" in r else None
        if category_list != None:
            category = ', '.join([x["term"] for x in r["tags"]]) if r["tags"] else ''
        else:
            category = ''
        
        # TODO: AI摘要
        ai_summary = None

        summary = r["summary"] if "summary" in r else None

        published_at = rss_date_convert(r["published_parsed"])

        news_data = {"title": title,
                        "url": url,
                        "source": source,
                        "content": content,
                        "authors": authors,
                        "keywords": keywords,
                        "category": category,
                        "ai_summary": ai_summary,
                        "summary": summary,
                        "published_at": published_at
                    }
        
        pre_list.append(news_data)
    
    return NewsOperator.insert_mult_news(pre_list)
    