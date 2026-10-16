"""Check the real generated or published pages; no ranking/citation claims."""
import argparse
import concurrent.futures
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://gifts.aimuse.ae/"
parser = argparse.ArgumentParser()
parser.add_argument("--build", type=Path)
parser.add_argument("--live", action="store_true")
parser.add_argument("--transport", choices=("https", "http"), default="https", help="Explicit HTTP readback is not HTTPS acceptance")
parser.add_argument("--output", type=Path, default=ROOT / "output" / "latest-audit.json")
args = parser.parse_args()
assert args.build or args.live
issues = []
checks = []
cache = {}
known_paths = set()


def get(path):
    path = path.lstrip("/")
    if path in cache: return cache[path]
    if args.live:
        response = requests.get(CANONICAL.replace("https:", args.transport + ":", 1) + path, timeout=30)
        assert response.status_code == 200, f"{path}: HTTP {response.status_code}"
        value = response.content
    else:
        file = args.build / unquote(path)
        if not path or path.endswith("/"): file = file / "index.html"
        assert file.is_file(), f"Missing {path}"
        value = file.read_bytes()
    cache[path] = value
    return value


def require(condition, message):
    if not condition: issues.append(message)


def inspect(path):
    raw = get(path).decode("utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    require(len(soup.select("h1")) == 1, path + ": one H1 required")
    require(len(soup.select('link[rel="canonical"]')) == 1, path + ": canonical count")
    require(soup.select_one('link[rel="canonical"]')["href"] == CANONICAL + path, path + ": canonical target")
    require(bool(soup.select_one('meta[name="description"]')["content"].strip()), path + ": description")
    for key in ("og:title", "og:description", "og:image", "og:locale", "og:url"):
        require(len(soup.select(f'meta[property="{key}"]')) == 1, path + ": duplicate/missing " + key)
    require(len(soup.select('meta[name="twitter:card"]')) == 1, path + ": twitter card")
    require(not soup.select('meta[name="robots"][content*="noindex"]'), path + ": noindex")
    links = {l.get("hreflang"): l["href"] for l in soup.select('link[rel="alternate"][hreflang]')}
    enpath = path.removeprefix("ar/")
    require(links == {"en": CANONICAL + enpath, "ar": CANONICAL + "ar/" + enpath, "x-default": CANONICAL + enpath}, path + ": translation mapping")
    require(soup.html.get("lang") == ("ar" if path.startswith("ar/") else "en"), path + ": lang")
    if path.startswith("ar/"): require(soup.html.get("dir") == "rtl", path + ": RTL")
    require("localhost" not in raw and "127.0.0.1" not in raw and "gifs.aimuse" not in raw, path + ": nonproduction URL")
    require(not re.search(r"AED|US\$|درهم|ميزاني|date-jewelbox|تمور", soup.get_text(" "), re.I), path + ": excluded gift or price")
    graphs = []
    for node in soup.select('script[type="application/ld+json"]'):
        data = json.loads(node.string or node.get_text())
        graphs += data.get("@graph", [data])
    require(any(g.get("@type") == "Organization" for g in graphs), path + ": organization")
    require(any(g.get("@type") == "WebPage" for g in graphs), path + ": WebPage")
    if "/blog/" in "/" + path and not path.endswith("blog/"):
        article = next(g for g in graphs if g.get("@type") == "BlogPosting")
        require(article.get("datePublished") and article.get("dateModified"), path + ": article dates")
        require(len(soup.select(".gk-body h2")) >= 3, path + ": useful article sections")
    if soup.select_one(".gk-article"):
        require(bool(soup.select_one(".gk-answer")), path + ": direct buyer answer")
        faq = next(g for g in graphs if g.get("@type") == "FAQPage")
        visible = soup.select(".gk-faq details")
        require(len(visible) == len(faq["mainEntity"]), path + ": FAQ count")
        for detail, entity in zip(visible, faq["mainEntity"]):
            require(detail.summary.get_text(strip=True) == entity["name"], path + ": FAQ question mismatch")
            require(detail.p.get_text(strip=True) == entity["acceptedAnswer"]["text"], path + ": FAQ answer mismatch")
    if path in ("blog/", "ar/blog/", "guides/", "ar/guides/"):
        require(bool(soup.select_one(".gk-index")) and not soup.select_one(".gk-article"), path + ": wrong section template")
        require(bool(soup.select(".gk-index .gk-card")), path + ": empty article list")
    floating = soup.select_one("a.vg-whatsapp-float")
    require(floating and floating["href"] == "https://wa.me/971525682660", path + ": WhatsApp")
    # Follow all same-site HTML links and fragment targets, not just the sitemap.
    for anchor in soup.select("a[href]"):
        href = anchor["href"]
        target = urlsplit(urljoin(CANONICAL + path, href))
        if target.netloc != "gifts.aimuse.ae": continue
        resource = target.path.lstrip("/")
        if not resource.endswith("/") and resource: continue
        require(resource in known_paths, path + ": linked page absent from sitemap " + href)
        if target.fragment:
            linked = BeautifulSoup(get(resource), "html.parser")
            require(bool(linked.find(id=unquote(target.fragment))), path + ": broken anchor " + href)
    for img in soup.select("img[src]"):
        require(img.has_attr("alt"), path + ": missing image alt")
        target = urlsplit(urljoin(CANONICAL, img["src"]))
        if target.netloc == "gifts.aimuse.ae": get(target.path)
    checks.append({"path": path, "title": soup.title.get_text(), "schema_types": [g.get("@type") for g in graphs], "bytes": len(raw.encode()), "answer_present": bool(soup.select_one(".gk-answer"))})


result = {"time_utc": datetime.now(timezone.utc).isoformat(), "mode": "live" if args.live else "build", "base": CANONICAL,
          "transport": args.transport if args.live else "local", "https_verified": bool(args.live and args.transport == "https"),
          "search_indexing": "unknown", "ai_citations": "unknown", "search_referrals": "unknown", "qualified_enquiries": "unknown"}
try:
    robots = get("robots.txt").decode()
    require("Disallow: /\n" not in robots, "robots blocks all crawling")
    require(CANONICAL + "sitemap.xml" in robots, "sitemap missing from robots")
    paths = []
    index = ET.fromstring(get("sitemap.xml"))
    for node in index.findall("{*}sitemap/{*}loc"):
        for loc in ET.fromstring(get(node.text.removeprefix(CANONICAL))).findall("{*}url/{*}loc"):
            paths.append(loc.text.removeprefix(CANONICAL))
    if not paths: paths = [loc.text.removeprefix(CANONICAL) for loc in index.findall("{*}url/{*}loc")]
    known_paths.update(paths)
    sampled = list(paths)
    if args.live and len(paths) > 50:
        # Keep stable entry points, then newest articles, then a daily rotating sample.
        content = json.loads(get("gift-guide.json"))
        priority = ["", "ar/", "blog/", "ar/blog/", "guides/", "ar/guides/"]
        ordered = sorted(content["articles"], key=lambda a: a.get("date") or "", reverse=True)
        for article in ordered[:10]:
            priority += [v["url"].removeprefix(CANONICAL) for v in article["translations"].values()]
        priority = list(dict.fromkeys(p for p in priority if p in known_paths))
        rest = [p for p in paths if p not in priority]
        start = datetime.now(timezone.utc).date().toordinal() % len(rest)
        rest = rest[start:] + rest[:start]
        sampled = (priority + rest)[:50]
    result["sitemap_pages"] = len(paths)
    result["sampled_paths"] = sampled
    result["full_html_audit"] = len(sampled) == len(paths)
    for path in sampled: inspect(path)
    data = json.loads(get("gift-guide.json"))
    require(len(data["products"]) == 29 and len(data["occasions"]) == 9, "Product or occasion coverage changed")
    require(bool(data.get("articles")), "Articles missing from machine index")
    full = get("llms-full.txt").decode("utf-8")
    short = get("llms.txt").decode("utf-8")
    for a in data["articles"]:
        for l, v in a["translations"].items():
            require(v["url"] in short and v["url"] in full and v["answer"] in full, a["id"] + ": index synchronisation")
            article_path = v["url"].removeprefix(CANONICAL)
            require(article_path in known_paths, a["id"] + ": article missing from sitemap")
            if article_path in sampled:
                page = BeautifulSoup(get(article_path), "html.parser")
                answer = page.select_one(".gk-answer")
                require(answer and answer.get_text(strip=True) == v["answer"], a["id"] + ": live answer mismatch")
    source_products = json.loads((ROOT / "data/corporate_gifts_v2.json").read_text(encoding="utf-8"))["products"]
    source_occasions = json.loads((ROOT / "data/gift_occasions.json").read_text(encoding="utf-8"))["guides"]
    require(data["products"] == source_products and data["occasions"] == source_occasions, "Product/occasion machine data drift")
    for p in ("blog/index.xml", "ar/blog/index.xml"): ET.fromstring(get(p))
except Exception as exc:
    issues.append(f"{type(exc).__name__}: {exc}")
    result["https_verified"] = False
result.update({"checks": checks, "pages_checked": len(checks), "issues": issues, "passed": not issues})
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"passed": result["passed"], "pages_checked": len(checks), "issues": issues, "report": str(args.output)}, ensure_ascii=False))
sys.exit(0 if not issues else 1)
