"""Build bilingual Hugo sources and machine indexes from the site's content data.

This is a deterministic content builder, not a scheduler or an article writer.
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://gifts.aimuse.ae/"


def read(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def frontmatter(values):
    return "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in values.items()) + "\n---\n\n"


def url(lang, section, slug=""):
    return BASE + ("ar/" if lang == "ar" else "") + section + "/" + (slug + "/" if slug else "")


def synchronise():
    knowledge = read("gift_knowledge.json")
    articles = knowledge["articles"]
    catalogue = read("corporate_gifts_v2.json")
    products = catalogue["products"]
    occasions = read("gift_occasions.json")["guides"]
    faqs = read("corporate_gifts.json")["faqs"]
    by_id = {p["id"]: p for p in products}
    expected = {ROOT / "content" / l / ("blog" if a["kind"] == "blog" else "guides") / (a["slug"] + ".md") for a in articles for l in ("en", "ar")}
    for l in ("en", "ar"):
        for section in ("blog", "guides"):
            for old in (ROOT / "content" / l / section).glob("*.md"):
                if "\nknowledgeId:" in old.read_text(encoding="utf-8") and old not in expected:
                    raise ValueError(f"Retired/renamed generated article still exists; review its removal or redirect: {old}")
    # A topic/date is shared by its two translations, never counted twice.
    ids, topics, days, paths = set(), set(), set(), set()
    for a in articles:
        assert a["id"] not in ids, "Duplicate article identity"
        assert a["topic_key"] not in topics, "Duplicate buyer question"
        ids.add(a["id"]); topics.add(a["topic_key"])
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a["slug"])
        assert a["kind"] in ("guide", "blog")
        if a.get("published_at"):
            published = datetime.fromisoformat(a["published_at"])
            assert published.tzinfo is not None, "Publication timezone required"
            assert published.astimezone(ZoneInfo("Asia/Dubai")).date().isoformat() == a["date"], "Publication date must match Dubai day"
            assert published <= datetime.now(published.tzinfo), "Future publication timestamp"
            if a.get("updated_at"):
                assert datetime.fromisoformat(a["updated_at"]) >= published, "Modification predates publication"
        if a["kind"] == "blog":
            assert a["date"] not in days, "More than one new theme on one Dubai day"
            assert a["date"] <= datetime.now(ZoneInfo("Asia/Dubai")).date().isoformat(), "Future post"
            days.add(a["date"])
        assert all(p in by_id for p in a["products"])
        assert (ROOT / "static" / a["image"].lstrip("/")).is_file()
        for lang in ("en", "ar"):
            c = a["locales"][lang]
            assert all(c.get(k) for k in ("title", "description", "answer", "sections", "faq"))
            section = "blog" if a["kind"] == "blog" else "guides"
            destination = ROOT / "content" / lang / section / (a["slug"] + ".md")
            assert destination not in paths
            paths.add(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            fields = {"title": c["title"], "description": c["description"], "translationKey": a["id"],
                      "type": "knowledge", "layout": "knowledge", "contentKind": a["kind"],
                      "knowledgeId": a["id"], "topic_key": a["topic_key"], "image": a["image"],
                      "images": [a["image"]], "imageWidth": 1536, "imageHeight": 1024,
                      "products": a["products"], "answer": c["answer"], "faq": c["faq"],
                      "sources": c.get("sources", []), "author": "MUSE Gift Team"}
            if c.get("seoTitle"): fields["seoTitle"] = c["seoTitle"]
            if a.get("occasion_index"): fields["occasionIndex"] = True
            if a.get("date"):
                fields["date"] = a.get("published_at", a["date"])
                fields["lastmod"] = a.get("updated_at", a.get("published_at", a["date"]))
            body = ""
            for s in c["sections"]:
                body += "## " + s["title"] + "\n\n"
                body += "\n\n".join(s.get("paragraphs", [])) + "\n\n"
                if s.get("bullets"):
                    body += "\n".join("- " + b for b in s["bullets"]) + "\n\n"
            destination.write_text(frontmatter(fields) + body.strip() + "\n", encoding="utf-8")

    for lang in ("en", "ar"):
        for section in ("blog", "guides"):
            titles = {"en": {"blog": "The Gift Journal", "guides": "Corporate gift buying guides"},
                      "ar": {"blog": "مجلة الهدايا", "guides": "أدلة شراء هدايا الشركات"}}
            intros = {"en": {"blog": "Practical ideas for UAE corporate gifts, presentation and the next occasion.",
                              "guides": "Choose gifts for the people, occasion and customisation your project needs."},
                      "ar": {"blog": "أفكار عملية لهدايا الشركات في الإمارات وتقديمها والتخطيط للمناسبة المقبلة.",
                              "guides": "اختر الهدايا بحسب المستلمين والمناسبة والتخصيص الذي يحتاجه مشروعك."}}
            folder = ROOT / "content" / lang / section
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "_index.md").write_text(frontmatter({"title": titles[lang][section], "description": intros[lang][section],
                "translationKey": "section-" + section, "type": "knowledge", "layout": "list", "image": "/images/corporate-gifts/v2/presentation-detail.webp"}), encoding="utf-8")

    # Keep existing product and occasion data in this same public index, adding articles.
    structured = {"site": BASE, "languages": ["en", "ar"], "company": "MUSE Information Services L.L.C-FZ",
                  "whatsapp": "+971525682660", "products": products, "occasions": occasions, "faqs": faqs}
    structured["categories"] = [c for c in catalogue["categories"] if c["id"] != "all"]
    structured["capabilities"] = {l: {"description": catalogue["ui"][l]["craftText"], "routes": catalogue["ui"][l]["craftSteps"], "url": url(l, "guides", "corporate-gift-customisation")} for l in ("en", "ar")}
    structured["articles"] = [{"id": a["id"], "topic_key": a["topic_key"], "kind": a["kind"],
        "date": a.get("date"), "updated_at": a.get("updated_at"), "products": a["products"], "translations": {l: {"url": url(l, "blog" if a["kind"] == "blog" else "guides", a["slug"]),
        "title": a["locales"][l]["title"], "answer": a["locales"][l]["answer"], "sections": a["locales"][l]["sections"],
        "faq": a["locales"][l]["faq"], "sources": a["locales"][l].get("sources", [])} for l in ("en", "ar")}} for a in articles]
    (ROOT / "static/gift-guide.json").write_text(json.dumps(structured, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    short = ["# MUSE Corporate Gifts Dubai", "", "> Corporate gift selection, branded presentation and original gift projects for the UAE.",
        "", "- [English collection](" + BASE + ")", "- [هدايا الشركات](" + BASE + "ar/)", "", "## Buying guides and gift journal"]
    full = ["# MUSE Corporate Gifts Dubai", "", "MUSE Information Services L.L.C-FZ, Dubai, UAE.",
        "WhatsApp: +971 52 568 2660. Email: musetrendytoy@gmail.com.",
        "Brand/model selection, permitted decoration, packaging, samples and delivery are agreed for each project."]
    for a in articles:
        for l in ("en", "ar"):
            c = a["locales"][l]; link = url(l, "blog" if a["kind"] == "blog" else "guides", a["slug"])
            short.append(f'- [{c["title"]}]({link})')
            full += ["", "## " + c["title"], link, c["answer"]]
            for s in c["sections"]:
                full += ["", "### " + s["title"], *s.get("paragraphs", []), *["- " + b for b in s.get("bullets", [])]]
            for f in c["faq"]:
                full += ["", "### " + f["q"], f["a"]]
            if c.get("sources"):
                full += ["", "### References" if l == "en" else "### مراجع"]
                full += [f'- [{s["title"]}]({s["url"]})' for s in c["sources"]]
    short += ["", "## UAE occasions"]
    for o in occasions:
        for l in ("en", "ar"):
            short.append(f'- [{o["title"][l]}]({BASE}{"ar/" if l == "ar" else ""}#occasion-{o["id"]})')
            full += ["", "## " + o["question"][l], BASE + ("ar/" if l == "ar" else "") + "#occasion-" + o["id"], o["answer"][l], o["plan"][l]]
    for p in products:
        full += ["", "## " + p["brand"] + " — " + p["title"]["en"], BASE + "#gift-" + p["id"]]
        for l in ("en", "ar"):
            if l == "ar": full.append(BASE + "ar/#gift-" + p["id"])
            full += [p["title"][l], p["text"][l], p["scene"][l]]
            if p.get("selection", {}).get(l): full.append(p["selection"][l])
            ui = catalogue["ui"][l]
            full.append(p.get("personalise", {}).get(l) or ui["originalCustom" if p["custom"] else "brandCustom"])
            if p.get("notice", {}).get(l): full.append(p["notice"][l])
    for f in faqs:
        for l in ("en", "ar"):
            full += ["", "## " + f["q"][l], f["a"][l]]
    for l in ("en", "ar"):
        c = structured["capabilities"][l]
        full += ["", "## MUSE capabilities" if l == "en" else "## قدرات ميوز", c["url"], c["description"]]
        for s in c["routes"]: full += ["### " + s["title"], s["text"]]
    short += ["", "- [Full bilingual buying answers](" + BASE + "llms-full.txt)", "- [Structured content](" + BASE + "gift-guide.json)", "", "WhatsApp: +971 52 568 2660. Email: musetrendytoy@gmail.com."]
    (ROOT / "static/llms.txt").write_text("\n".join(short) + "\n", encoding="utf-8")
    (ROOT / "static/llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
    print(json.dumps({"themes": len(articles), "blog_themes": sum(a["kind"] == "blog" for a in articles), "languages": ["en", "ar"], "source": "data/gift_knowledge.json"}))


if __name__ == "__main__":
    synchronise()
