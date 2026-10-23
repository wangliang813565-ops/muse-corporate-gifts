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

2026-10-16 onboarding identified an awaiting GitHub Pages certificate. One refresh was performed at 16:22:22 UTC; don't repeat it. By 21:57 Dubai the certificate was approved for gifts.aimuse.ae (expiry 2027-01-14), standard HTTPS returned 200, and the existing Pages API enabled enforcement. HTTP to the Arabic calendar URL returned 301 to the identical HTTPS path, then 200. Read the current state on subsequent runs; don't retain the earlier pending-certificate diagnosis as a current fault. Never bypass TLS or claim an API approval or HTTP readback alone proves production HTTPS and Google fetching.

Search indexing, impressions, clicks, AI citations and enquiries require actual Search Console/analytics/search-answer evidence. If unavailable they remain unknown. llms.txt, valid schema, crawlable HTML or a checklist score is not proof of citation, ranking or revenue. Do not invent statistics or promise inclusion in AI answers. Search crawlers and training crawlers are different; wildcard Allow already permits search bots.

## Actual Search Console baseline and follow-up

Read the current GEO skill and its references/google-search-console.md before interpreting reports. The verified URL-prefix property is https://gifts.aimuse.ae/ (added 2026-10-16). The toys property is a different site. Keep static/google30d7c935c23d8f9a.html intact; the release checker verifies the exact public verification file.

Actual onboarding findings on 2026-10-16: ownership verification succeeded; Search performance and indexing reports are processing, so queries, page impressions, clicks and rankings are unavailable, not zero. Google AI inclusion inherits aimuse.ae and is currently Include; no policy change is needed. Absence of a separate AI performance report is not evidence of zero AI impressions.

Google's live inspection of the HTTPS homepage at 21:34 Dubai failed with an invalid server SSL certificate and a site-level indexing issue. Fix and verify the production certificate before requesting indexing. An accepted verification file or sitemap submission is not proof that HTTPS pages can be fetched or indexed. Check the sitemap's actual processing/discovery status after certificate recovery, and re-submit only if needed; don't repeatedly submit while the same transport failure remains.

The certificate and HTTPS enforcement recovered at 21:57 Dubai. Google's 21:58 live homepage test changed to URL can be indexed; the subsequent homepage indexing request was accepted into the priority crawl queue. English /en/sitemap.xml and Arabic /ar/sitemap.xml each processed successfully and discovered seven URLs (14 distinct pages in total). All fourteen production pages passed the strict HTTPS content audit. The 21:34 failure and initial zero-discovery index snapshot are historical evidence; check the latest receipts in output before acting on them. Keep Google fetch eligibility, requested indexing and actual indexed status separate. Do not re-request the same URL just because the earlier historical report says unknown.

First recovery checks: / and /ar/, then both languages of /guides/uae-corporate-gifting-calendar/, /guides/premium-technology-gifts/ and /blog/eid-al-etihad-2026-october-gift-plan/. These are business-priority entry points, not a performance ranking inferred from missing data. Use live inspection on a representative page after recovery, request indexing only when eligible, then accept sitemap discovery and later indexed status separately.

In the existing daily run, read fresh GSC data when available and retain the last real state if access or processing prevents it. Start with 28 complete PT report days and country/device/page/query filters appropriate to UAE corporate buyers; a new property may not yet support a comparable period. Preserve report range, filters, latest final/preliminary day and original evidence in the existing output folder. Google AI impressions overlap Web totals, and neither report proves qualified enquiries. Use observed page/query mismatches to select specific edits; use business research explicitly when observations are insufficient. No extra scheduler, account, permission or analytics service is required.

2026-10-18 actual follow-up: a fresh tab in the same authorised Chrome browser restored GSC reading after an existing-tab attachment timeout; no new login/credentials/permissions were needed. Web performance with the 28-day selector had a chart covering only 2026-10-15 PT, displayed zero clicks/impressions and no query rows. This is not a usable post-HTTPS-recovery comparison period; CTR and rank are not meaningful without impressions. Index overview remained processing. Homepage URL Inspection now says **Crawled - currently not indexed**, with successful Googlebot Smartphone fetch, crawling/indexing allowed, declared canonical https://gifts.aimuse.ae/ and Google-selected canonical the inspected URL; UI last crawl 2026-10-16 22:00:40 (display timezone unspecified). Do not describe the homepage as indexed or its current fetch as SSL-failed. No repeat indexing request was made. Language sitemaps still show success, seven discovered each, last read 2026-10-16; that snapshot does not reflect later source page additions. Google AI inclusion was also re-read: inherits aimuse.ae, effective Include; settings unchanged. Evidence: output/2026-10-18-gsc-readback.txt. Comprehensive content work is based on verified catalogue and buyer-question gaps, not invented query rankings.

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

## Visit analytics and daily brief — authorised 2026-10-24

Wang Liang explicitly requested connecting visit statistics and including a concise daily summary. This supersedes the earlier no-new-analytics limitation for this specific gifts site setup and the links-only notification rule. Use the existing Google Analytics account 397996752 (liangwang), dedicated property **560591849**, web stream **16191730748**, measurement ID **G-CYNETCQ51B**, reporting timezone **Asia/Dubai**, currency AED. Do not use EVPlus property 541684031 or its traffic as gift-site data. No new account, credentials, users, Ads link or paid service is part of this setup.

Production templates load the tag only on gifts.aimuse.ae and after explicit analytics consent. English/Arabic choices, purposes and withdrawal are available in the on-page notice and footer Cookie settings. Automatic enhanced measurement is disabled in the stream; no automatic form/outbound-link collection, project briefs, WhatsApp text, names, email addresses or phone numbers are sent. Page URLs omit query strings/fragments, referring URLs are reduced to origin, advertising signals are disabled and cookies are scoped to this subdomain. Consent is remembered for 180 days; analytics cookies expire after 180 days without renewal. Therefore reports cover consenting, unblocked measured visits, not every visitor. No historical traffic can be recovered before collection started.

Read the authorised Analytics UI at https://analytics.google.com/analytics/web/#/a397996752p560591849/reports/intelligenthome and its reports. Record the exact observed metric name: total users or active users are not interchangeable; views are page views, sessions are separate. In each existing daily run, report 2–4 short lines with the latest complete Dubai date and available 7-day totals, top pages and source/country when supported, separately from GSC impressions/clicks with PT dates. A newly created property's pre-installation zeros do not prove no visitors. Processing or unavailable data remains unavailable; realtime tests are labelled operator verification, not customer acquisition. Do not manufacture a complete-day figure from the realtime window. Preserve UI evidence and report ranges in the existing output directory. Same-day duplicate runs reuse the brief unless something material changed.

Initial implementation, deployed tag, first received visit and the next natural daily analytics readback are separate acceptance steps. The current setup receipt is output/2026-10-24-analytics-setup.md. Retain the original schedule and publication workflow. Rollback only this setup commit if it causes a regression; the resource may remain unused without affecting other properties.
