"""Забирает новости Японии на русском с nippon.com и пишет news.json рядом с приложением."""
import json, re, html, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://www.nippon.com/ru/feed/"
OUT = Path(__file__).resolve().parent.parent / "news.json"

def clean(s, n):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"

req = urllib.request.Request(FEED, headers={"User-Agent": "tokyo-app-news/1.0"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = []
for it in root.iter("item"):
    try:
        d = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc).isoformat()
    except Exception:
        d = None
    items.append({"t": clean(it.findtext("title"), 200), "d": clean(it.findtext("description"), 260),
                  "l": (it.findtext("link") or "").strip(), "date": d})
if items:
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(), "source": "nippon.com",
                               "items": items[:20]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(items[:20]), "news")
