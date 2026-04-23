import feedparser
import json
import hashlib
from datetime import datetime

RSS_URL = "https://www.city.katsushika.lg.jp/news.rss"
OUTPUT_PATH = "data/news.json"
MAX_ITEMS = 30

CATEGORY_RULES = [
    (['bousai', 'anzen', 'saigai'], ['防災', '避難', '地震', '洪水', '台風', 'ハザード', '警戒', '災害'], '防災', 'bousai'),
    (['kosodate', 'kodomo', 'hoiku', 'gakko'], ['子ども', '子育て', '保育', '学校', '育児', '児童'], '子育て', 'kosodate'),
    (['fukushi', 'kaigo', 'koreisha', 'shogai', 'kenkou'], ['福祉', '介護', '高齢', '障がい', '障害', '健康', 'シニア'], '福祉', 'fukushi'),
    (['kanko', 'event', 'matsuri', 'institution'], ['イベント', '祭り', 'まつり', '催し', '公演', '展示', 'コンサート', '開催'], 'イベント', 'event'),
    (['gomi', 'doro', 'kotsu', 'seikatsu'], ['ごみ', 'ゴミ', '道路', '工事', '交通', '粗大', '収集'], '生活情報', 'seikatsu'),
]
DEFAULT_CATEGORY = ('区政', 'kusei')


def categorize(url, title):
    url_lower = url.lower()
    for url_keys, title_keys, cat, slug in CATEGORY_RULES:
        if any(k in url_lower for k in url_keys):
            return cat, slug
        if any(k in title for k in title_keys):
            return cat, slug
    return DEFAULT_CATEGORY


def parse_date(entry):
    try:
        t = entry.published_parsed
        return datetime(*t[:6]).strftime('%Y-%m-%d')
    except Exception:
        return datetime.now().strftime('%Y-%m-%d')


def main():
    print(f"RSSを取得中: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)

    if feed.bozo:
        print(f"警告: RSS取得に問題が発生しました: {feed.bozo_exception}")

    items = []
    for entry in feed.entries[:MAX_ITEMS]:
        title = entry.get('title', '').strip()
        link = entry.get('link', '#')
        description = entry.get('description', '').strip()
        summary = description if description else f"{title}についての最新情報です。詳細はリンクよりご確認ください。"
        date = parse_date(entry)
        category, slug = categorize(link, title)
        item_id = hashlib.md5(link.encode()).hexdigest()[:8]
        items.append({
            'id': item_id,
            'title': title,
            'category': category,
            'categorySlug': slug,
            'date': date,
            'summary': summary,
            'url': link
        })

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(items)}件のニュースを {OUTPUT_PATH} に保存しました")


if __name__ == '__main__':
    main()
