import requests
from lxml import etree
import pandas as pd
import os,random

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
        top_ul = tree.xpath("/html/body/table[3]/tbody/tr/td[1]/div[7]/div[1]/div[2]/ul")[0]
    except Exception as e:
        print(f"❌ 网页获取失败：{e}")
        return []

    result = []
    current_id = 72

    # ========= 1级：父分类 =========
    for li in top_ul.xpath("./li"):
        parent_name = li.xpath("./span/text()")
        parent_input = li.xpath("./input/@value")
        parent_name = parent_name[0].strip() if parent_name else ""
        parent_url = parent_input[0].strip() if parent_input else ""

        parent_id = current_id  # 保存当前父ID，给子级用

        parent_time = random.randint(10, 20)
        if parent_name:
            parent_name += "（百度源）"
            result.append([
                current_id, parent_name, parent_url, None,
                0,        # is_child 父=0
                0,        # parent_id 父=0
                None, None, parent_time, None, None, None
            ])
            current_id += 1

        # ========= 2级：子分类 =========
        sub_lis = li.xpath("./ul/li")
        for sub_li in sub_lis:
            sub_name = sub_li.xpath("./span/text()")
            sub_input = sub_li.xpath("./input/@value")
            sub_name = sub_name[0].strip() if sub_name else ""
            sub_url = sub_input[0].strip() if sub_input else ""

            sub_id = current_id  # 保存当前子ID，给孙级用
            sub_time = random.randint(20, 30)
            if sub_name:
                sub_name += "（百度源）"
                result.append([
                    current_id, sub_name, sub_url, None,
                    1,        # is_child 子=1
                    parent_id,# parent_id 子=父ID
                    None, None, sub_time, None, None, None
                ])
                current_id += 1

            # ========= 3级：孙子分类 =========
            grand_sub_lis = sub_li.xpath("./ul/li")
            for grand_sub_li in grand_sub_lis:
                g_sub_name = grand_sub_li.xpath("./span/text()")
                g_sub_input = grand_sub_li.xpath("./input/@value")
                g_sub_name = g_sub_name[0].strip() if g_sub_name else ""
                g_sub_url = g_sub_input[0].strip() if g_sub_input else ""
                g_sub_time = random.randint(30, 40)
                if g_sub_name:
                    g_sub_name += "（百度源）"
                    result.append([
                        current_id, g_sub_name, g_sub_url, None,
                        2,        # is_child 孙=2
                        sub_id,   # parent_id 孙=直接父ID（2级ID）
                        None, None, g_sub_time, None, None, None
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
        # 字段顺序已更新：加入 parent_id
        columns = [
            "id", "name", "url", "category",
            "is_child", "parent_id",  # 👈 新增在这里
            "is_active", "is_api_key", "update_rate",
            "hot_rate", "source_score", "created_at"
        ]
        df = pd.DataFrame(data, columns=columns)

        with pd.ExcelWriter(
            SAVE_PATH,
            engine="openpyxl",
            datetime_format="yyyy-mm-dd hh:mm:ss"
        ) as writer:
            df.to_excel(writer, index=False)

        print(f"✅ 成功导出！文件：{SAVE_PATH}")
        print(f"📊 共抓取 {len(data)} 条 RSS（1级+2级+3级）")
        print(f"✅ 已自动生成 parent_id 关联父子关系！")