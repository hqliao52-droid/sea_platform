import requests
from lxml import etree
import pandas as pd
import os
from datetime import datetime

# ====================== 你可以自定义的配置 ======================
URL = "http://www.baidu.com/search/rss.html"
SAVE_PATH = "./data/rss_list.xlsx"
# ===============================================================

def get_rss_structure():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        resp = requests.get(URL, headers=headers, timeout=10)
        resp.encoding = resp.apparent_encoding
        tree = etree.HTML(resp.text)
        top_ul = tree.xpath("/html/body/table[3]/tbody/tr/td[1]/div[7]/div[1]/div[1]/ul")[0]
    except Exception as e:
        print(f"❌ 网页获取失败：{e}")
        return []

    result = []
    current_id = 1
    # ✅ 修复：生成 MySQL 标准时间格式：2025-12-20 15:30:00
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 父分类
    for li in top_ul.xpath("./li"):
        parent_name = li.xpath("./span/text()")
        parent_input = li.xpath("./input/@value")
        parent_name = parent_name[0].strip() if parent_name else ""
        parent_url = parent_input[0].strip() if parent_input else ""

        if parent_name:
            parent_name += "（百度源）"
            result.append([
                current_id,
                parent_name,
                parent_url,
                None,       # category 空
                0,          # 父类 is_child=0
                None,       # is_active 空
                None,       # is_api_key 空
                10,         # 父类 update_rate=10
                None,       # hot_rate 空
                None,       # source_score 空
                now_time    # ✅ 正确时间
            ])
            current_id += 1

        # 子分类
        sub_lis = li.xpath(".//ul/li")
        for sub_li in sub_lis:
            sub_name = sub_li.xpath("./span/text()")
            sub_input = sub_li.xpath("./input/@value")
            sub_name = sub_name[0].strip() if sub_name else ""
            sub_url = sub_input[0].strip() if sub_input else ""

            if sub_name:
                sub_name += "（百度源）"
                result.append([
                    current_id,
                    sub_name,
                    sub_url,
                    None,
                    1,       # 子类 is_child=1
                    None,
                    None,
                    15,      # 子类 update_rate=15
                    None,
                    None,
                    now_time
                ])
                current_id += 1

    return result

if __name__ == "__main__":
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    try:
        import openpyxl
    except:
        os.system("pip install openpyxl")

    data = get_rss_structure()

    if not data:
        print("❌ 没有抓取到任何数据")
    else:
        columns = [
            "id", "name", "url", "category", "is_child",
            "is_active", "is_api_key", "update_rate",
            "hot_rate", "source_score", "created_at"
        ]
        df = pd.DataFrame(data, columns=columns)

        # ✅ 关键修复：导出时保留正确时间格式，不被 Excel 篡改
        with pd.ExcelWriter(
            SAVE_PATH,
            engine="openpyxl",
            datetime_format="yyyy-mm-dd hh:mm:ss"
        ) as writer:
            df.to_excel(writer, index=False)

        print(f"✅ 成功导出！文件：{SAVE_PATH}")
        print(f"📊 共抓取 {len(data)} 条 RSS")
        print(f"✅ 时间格式已修复，可直接导入 MySQL 无报错！")