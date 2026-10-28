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
    require(any(g.get("@type") in ("WebPage", "AboutPage") for g in graphs), path + ": WebPage")
    lang = "ar" if path.startswith("ar/") else "en"
    require(soup.select_one('meta[property="og:locale:alternate"]')["content"] == ("en_AE" if lang == "ar" else "ar_AE"), path + ": alternate locale")
    if path in ("", "ar/"):
        products = json.loads((ROOT / "data/corporate_gifts_v2.json").read_text(encoding="utf-8"))["products"]
        catalogue = next((g for g in graphs if g.get("@id") == CANONICAL + path + "#gift-catalogue"), {})
        require(catalogue.get("numberOfItems") == len(products), path + ": catalogue schema count")
        items = catalogue.get("itemListElement", [])
        require(len(items) == len(products), path + ": catalogue item count")
        for p, item in zip(products, items):
            card = soup.find(id="gift-" + p["id"])
            note = card.select_one(".vg-product-guide p") if card else None
            require(note and note.get_text(strip=True) == p["selection"][lang], path + p["id"] + ": visible selection note")
            require(item["description"] == p["text"][lang] and item["url"] == CANONICAL + path + "#gift-" + p["id"], path + p["id"] + ": catalogue schema mismatch")
        require(len(soup.select(".vg-buyer-routes a")) == 3, path + ": buyer routes")
        core_guides = {"uae-corporate-gifting-calendar", "premium-technology-gifts", "corporate-gift-customisation", "ramadan-eid-corporate-gifts", "corporate-gift-selection"}
        visible_guides = {a.get("href") for a in soup.select("[data-core-guides] .gk-card > a")}
        require(visible_guides == {"/" + path + "guides/" + slug + "/" for slug in core_guides}, path + ": stable buyer-guide navigation")
    if path.endswith("guides/uae-corporate-gifting-calendar/"):
        require(len(soup.select(".gk-occasion-cards article")) == 9, path + ": occasion comparison coverage")
    if "/blog/" in "/" + path and not path.endswith("blog/"):
        article = next(g for g in graphs if g.get("@type") == "BlogPosting")
        require(article.get("datePublished") and article.get("dateModified"), path + ": article dates")
        require(len(soup.select(".gk-body h2")) >= 3, path + ": useful article sections")
    if soup.select_one(".gk-article"):
        require(bool(soup.select_one(".gk-answer")), path + ": direct buyer answer")
        author_link = soup.select_one('.gk-byline a[href]')
        require(author_link and author_link['href'] == '/' + ('ar/' if lang == 'ar' else '') + 'about/#gift-team', path + ': accountable author link')
        faq = next(g for g in graphs if g.get("@type") == "FAQPage")
        visible = soup.select(".gk-faq details")
        require(len(visible) == len(faq["mainEntity"]), path + ": FAQ count")
        for detail, entity in zip(visible, faq["mainEntity"]):
            require(detail.summary.get_text(strip=True) == entity["name"], path + ": FAQ question mismatch")
            require(detail.p.get_text(strip=True) == entity["acceptedAnswer"]["text"], path + ": FAQ answer mismatch")
    if path in ("blog/", "ar/blog/", "guides/", "ar/guides/"):
        require(bool(soup.select_one(".gk-index")) and not soup.select_one(".gk-article"), path + ": wrong section template")
        entries = soup.select('.gk-guide-route a[href]') if path.endswith('guides/') else soup.select('.gk-index .gk-card a[href]')
        require(bool(entries), path + ": empty buying routes or article list")
    floating = soup.select_one("a.vg-whatsapp-float")
    require(floating and floating["href"] == "https://wa.me/971525682660", path + ": WhatsApp")
    privacy_path = '/' + ('ar/' if lang == 'ar' else '') + 'privacy/'
    require(soup.select_one(f'footer a[href="{privacy_path}"]'), path + ': site-specific privacy link')
    if path in ('about/', 'ar/about/'):
        require('MUSE Information Services L.L.C-FZ' in soup.main.get_text(' '), path + ': visible company identity')
        require(soup.find(id='project-approval') and soup.find(id='contact'), path + ': approval and contact details')
        require(any(g.get('@type') == 'AboutPage' and g.get('mainEntity', {}).get('@id') == CANONICAL + '#organization' for g in graphs), path + ': about entity relationship')
    if path in ('privacy/', 'ar/privacy/'):
        require('Google Analytics' in soup.main.get_text(' ') and '180' in soup.main.get_text(' '), path + ': actual analytics disclosure')
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
    verification = get("google30d7c935c23d8f9a.html").decode("utf-8").strip()
    require(verification == "google-site-verification: google30d7c935c23d8f9a.html", "Search Console ownership file missing or changed")
    require("Disallow: /\n" not in robots, "robots blocks all crawling")
    require(CANONICAL + "sitemap.xml" in robots, "sitemap missing from robots")
    paths = []
    index = ET.fromstring(get("sitemap.xml"))
    for node in index.findall("{*}sitemap/{*}loc"):
        for loc in ET.fromstring(get(node.text.removeprefix(CANONICAL))).findall("{*}url/{*}loc"):
            paths.append(loc.text.removeprefix(CANONICAL))
    if not paths: paths = [loc.text.removeprefix(CANONICAL) for loc in index.findall("{*}url/{*}loc")]
    require(len(paths) == len(set(paths)), "Duplicate canonical URLs in sitemap")
    require(all(not urlsplit(p).scheme and not urlsplit(p).query and not urlsplit(p).fragment and (not p or p.endswith('/')) for p in paths), "Noncanonical URL variant in sitemap")
    known_paths.update(paths)
    sampled = list(paths)
    if args.live and len(paths) > 50:
        # Keep stable entry points, then newest articles, then a daily rotating sample.
        content = json.loads(get("gift-guide.json"))
        priority = ["", "ar/", "about/", "ar/about/", "privacy/", "ar/privacy/", "blog/", "ar/blog/", "guides/", "ar/guides/"]
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
    for lang, hub in data.get("guide_hub", {}).items():
        hub_path = hub["url"].removeprefix(CANONICAL)
        require(hub_path in known_paths and hub["url"] in short, lang + ': guide hub discovery')
        require(hub["answer"] in full, lang + ': guide hub machine answer')
        if hub_path in sampled:
            hub_page = BeautifulSoup(get(hub_path), 'html.parser')
            require(hub["answer"] in hub_page.get_text(), lang + ': guide hub visible answer')
            for route in hub["routes"]:
                article = next(a for a in data["articles"] if a["id"] == route["id"])
                target = article["translations"][lang]["url"]
                require(any(urljoin(CANONICAL, a['href']) == target for a in hub_page.select('.gk-guide-route a[href]')), lang + ': missing buyer route ' + route["id"])
    for lang, pages in data.get("company_pages", {}).items():
        for name, link in pages.items():
            require(link in short and link in full and link.removeprefix(CANONICAL) in known_paths, lang + name + ': company index consistency')
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
    for p in source_products:
        for lang in ("en", "ar"):
            require(p["selection"][lang] in full, p["id"] + ": selection notes missing from machine text")
    for p in ("blog/index.xml", "ar/blog/index.xml"): ET.fromstring(get(p))
except Exception as exc:
    issues.append(f"{type(exc).__name__}: {exc}")
    result["https_verified"] = False
result.update({"checks": checks, "pages_checked": len(checks), "issues": issues, "passed": not issues})
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"passed": result["passed"], "pages_checked": len(checks), "issues": issues, "report": str(args.output)}, ensure_ascii=False))
sys.exit(0 if not issues else 1)
