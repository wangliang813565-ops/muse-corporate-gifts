# MUSE gifts: daily GEO and buyer journal

Owner: this Codex chat. Business timezone: Asia/Dubai. Daily slot: 08:00 local.
Production: https://gifts.aimuse.ae/ and /ar/. Authoritative repository:
https://github.com/wangliang813565-ops/muse-corporate-gifts (main).
Local root: C:/dev/geo-upgrade-20260929/muse-corporate-gifts.
Only this gift site is within the daily publishing scope. Keep toys.aimuse.ae pages intact.

## One writer and existing release path

Use the native heartbeat attached to this chat; do not add a Windows task, GitHub article-writing schedule, or another content service.
Before editing, inspect git status, remote main, the latest deploy run, today's articles, and any in-progress work in this chat. A dirty tree is not permission to reset, discard, stage, or publish another owner's work. Resume the same unfinished article/deployment after an unknown result; do not create another one.

The sole article source is data/gift_knowledge.json (articles array). English and Arabic belong to one article id/topic_key/date. Generated content/en and content/ar Markdown, llms files and public gift-guide.json are outputs of scripts/sync_content.py. Change the source and run the builder; do not maintain a second editorial ledger.

## GEO first: actual buyer decisions

Run scripts/check_site.py --live once into output/YYYY-MM-DD-before.json using the actual project Python. It checks standard HTTPS, every sitemap HTML page up to 50, internal links and anchors, languages, direct answers, matching visible/schema FAQ, entity data, images, feeds and machine text. With more than 50 pages it checks stable entry points, recent articles and a daily rotating sample, recording the full site count and actual sampled paths; don't report that sample as a full audit. Local build validation covers all pages. Respect robots and limit fetches to at most five concurrent requests and 30 seconds each.

Use the question map and the latest report. Read actual buyer answers, not only scores or tags. Review one rotating decision cluster in depth: occasion/recipient fit; named product choices; brand packaging versus original manufacturing; samples/material/finish approvals; date-based planning; recipient handover. Fix factual or broken-link problems affecting the new work before publishing. Do not change crawler-training preferences, DNS or unrelated services as routine maintenance.

2026-10-16 onboarding identified an awaiting GitHub Pages certificate. Read /pages/health and /pages certificate state first. One refresh was already performed at 16:22:22 UTC; don't repeat it. Never bypass TLS or claim HTTP readback proves HTTPS. When the certificate is approved, enable HTTPS via the existing Pages API and verify standard HTTPS plus HTTP redirection. Otherwise retain the known blocker; a platform failure is not a content regression.

Search indexing, impressions, clicks, AI citations and enquiries require actual Search Console/analytics/search-answer evidence. If unavailable they remain unknown. llms.txt, valid schema, crawlable HTML or a checklist score is not proof of citation, ranking or revenue. Do not invent statistics or promise inclusion in AI answers. Search crawlers and training crawlers are different; wildcard Allow already permits search bots.

## One useful theme each Dubai day

Check every existing topic_key, id, slug and date first. At most one new blog theme per local date, with English and Arabic released together. The builder rejects duplicate themes and duplicate blog dates. It does not generate articles. Near-duplicate questions require editorial review even when the keys differ. Stable guides are updated in place; do not turn minor updates into a new article or change old dates just for freshness.

Choose a purchase decision that adds something useful: a comparison, recipient distinction, concrete selection or approval checklist, project sequence or seasonal timing. Start with a direct answer and link selected current product IDs to the collection and project brief. Match the current 29-product selection, including Chinese technology/manufacturing strengths and the three MUSE architectural oud forms. No date-fruit gifts, public prices, budget fields, invented inventory, universal MOQ, promised turnaround, brand dealership, certifications or customer cases. Personal-care gifts require recipient preference; games are not automatically suitable for children.

Verify changing facts from current official sources. Religious holiday dates follow UAE announcements. Distinguish annual occasion dates, that year's campaign window, procurement start and actual handover date. China factory holiday/shipping constraints are project planning considerations, not a promise of fixed production duration. Localise packaging/greetings for the UAE; do not reuse Chinese holiday imagery.

Article shape: id, kind=blog, topic_key, date (Dubai YYYY-MM-DD), published_at (actual planned first publication timestamp with +04:00), stable slug, existing image, related products, locales.en/ar. Each locale has title, description, answer, sections (title, paragraphs, bullets), faq (q,a), sources (title,url). Keep detailed internal source notes in the working report, not public copy. Meaningful revisions use updated_at only; preserve first publication date.

Possible distinct future questions, subject to existing-topic and evidence checks:
- UAE Flag Day team gifting: one coherent identity with restrained branding.
- Ramadan host gifts: qahwa service versus architectural oud burner.
- Eid employee gifts versus family gifts; personal preference and age fit.
- EKETOP kinetic top versus a smart puzzle for desk gifting.
- Laifen personal-care gifts: recipient choice and presentation decisions.
- Audio and wearable gifts: phone compatibility and recipient interests.
- Business-travel gifts: power accessories, luggage and packing decisions.
- Coffee enthusiasts: portable espresso versus manual grinder.
- Engineering clients: HOTO tools versus original precision-made desk pieces.
- Property handovers: useful tools, glass hospitality or leather presentation.
- Sample approval: artwork, material, finish, contents and packing checklist.
- Arabic and English names: a recipient proofing workflow.
- One campaign, employee/client/VIP tiers, consistent presentation.
- Packaging that remains useful after the event.
- Reordering the same corporate gift: retain the approved specification.

## Build, check, publish, read back

Python: C:/Users/wlang/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/python.exe (use -X utf8).
Hugo: C:/dev/geo-upgrade-20260929/tools/hugo-0.159.2/hugo.exe.

1. Run Python scripts/sync_content.py; build Hugo with --minify to a task-specific output build folder (not another dev server's public folder).
2. Run scripts/check_site.py --build BUILD --output output/YYYY-MM-DD-build.json. Review EN/AR visible copy, sources, product fit and dates manually; the script cannot prove factual or translation quality.
3. Save pre-release main SHA. Commit only this day's reviewed article and its generated files using the existing verified project identity. Push only muse-corporate-gifts main, then manually trigger deploy.yml. Wait on that same run. No tools creating messages to customers or sending WhatsApp tests.
4. Read final run status, remote source SHA, and run scripts/check_site.py --live --output output/YYYY-MM-DD-after.json. Fetch both actual new article URLs, list, feed, sitemap, llms and structured index; compare text to source. Inspect desktop/mobile UI when templates change. Re-read the production state first after any unknown write result.
5. If the new change causes a failure, revert only its exact commit through the same release route, preserving other writers. No broad reset or domain rebinding.
6. Record this same day's theme/URLs/source/revision/deployment/checks in output/YYYY-MM-DD-run.md. An existing blog date means finish its pending acceptance, not create a second article.

User authorisation covers this daily gift blog and GEO maintenance on this public site. It does not cover new accounts, spending, outbound messages, a new analytics service, unrelated site publication or permission changes. Normal publication does not need repeated approval. The initial manual release is not the next natural daily run. Keep the native schedule enabled after first publication, and accept its first actual trigger separately.

## Old toys blog relationship

Read-only inspection on 2026-10-16 found latest toys blog articles dated 2026-09-28. The historical producer was Hermes blog-weekly (Monday/Thursday); current upstream host status is unknown. This gift site does not copy its whole articles or claim the old chain is working. During daily topic research check its latest public blog; reuse a relevant topic only if it answers a different real corporate gift question with fresh original EN/AR content. Keep each site's canonical and purpose distinct. Do not modify the old scheduler or old site without its specific scope being authorised.

## Notifications

Remain quiet for unchanged GEO state. For a successful new blog, a short link is enough. Notify once for a new fault, material change, unresolved fact/permission issue, or needed user action. Do not send repeated unchanged TLS reminders. Do not create a new chat, archive this chat, or silently stop the daily schedule.
