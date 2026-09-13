# SEO and GEO audit — אור בדק בית

Audit date: 2026-09-13

## Executive result

The repository now passes the local technical SEO audit for all 17 indexable HTML pages. Every indexable page is represented once in `sitemap.xml`; the dedicated `404.html` is explicitly `noindex` and excluded. Crawl controls, unique canonicals, page titles, descriptions, H1s, social metadata, locale signals, internal links, images, and JSON-LD all pass the automated source checks.

Public page URLs now use extensionless paths such as `https://orbedek.co.il/about`. Netlify permanently redirects each former `.html` URL to its clean equivalent, and all internal links, canonicals, Open Graph URLs, structured data, `llms.txt`, and sitemap entries use the same format.

Google does not guarantee indexing merely because a page is in a sitemap. Deployment and Google Search Console checks in the final section are still required.

## Production URL

The production domain was confirmed from the site's Google Search Console property:

`https://orbedek.co.il/`

This base appears consistently in canonical links, Open Graph URLs, structured data, `sitemap.xml`, `robots.txt`, `llms.txt`, and the 404 page. If the production domain changes, replace this base everywhere and rerun:

```bash
python3 scripts/seo_audit.py
```

## Indexing and crawl audit

| Check | Result | Notes |
|---|---|---|
| Indexable page inventory | Pass | 17 public content pages |
| XML sitemap coverage | Pass | 17/17 indexable pages; absolute canonical URLs |
| 404 in sitemap | Pass | Excluded |
| robots.txt | Pass | Global crawl allowed; absolute sitemap directive |
| Page robots directives | Pass | All content pages use `index, follow`; 404 uses `noindex, follow` |
| Canonical URLs | Pass | Unique, self-referencing, and aligned with sitemap URLs |
| URL variants | Pass in source | Clean URLs are canonical; explicit `301` redirects cover every former `.html` URL |
| Internal crawlable links | Pass | No missing local files or fragment targets |
| Titles and descriptions | Pass | Present and unique on every indexable page |
| Primary headings | Pass | Exactly one non-empty H1 on every page |
| Language and direction | Pass | `he-IL` and RTL on all pages |
| Image accessibility | Pass | All images have `alt`; blog covers now have intrinsic dimensions |
| JSON-LD syntax | Pass | Every structured-data block parses as valid JSON |

Google's sitemap guidance requires absolute URLs and recommends listing the canonical URLs intended for Search. The sitemap is a discovery hint, not an indexing guarantee: [Google sitemap documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## 2026-09-13 indexing investigation

The Search Console example report showed the submitted `.html` URLs as **Crawled — currently not indexed** shortly after discovery. The `.html` suffix itself is valid and does not prevent indexing. The actionable issue was inconsistent URL signaling on the deployed Netlify site:

- Both `/about` and `/about.html` returned `200` with identical content.
- Netlify's HTML post-processing changed internal navigation links to clean paths such as `/about`.
- Canonical elements, Open Graph URLs, structured data, and the submitted sitemap still selected `/about.html`.
- `/about/` redirected to `/about`, creating an additional signal in favor of the clean form.

This split does not necessarily explain every non-indexed page, but it gives Google conflicting duplicate/canonical signals and is worth correcting. The implementation now selects extensionless URLs consistently and uses forced permanent redirects in `_redirects` so the physical `.html` files cannot shadow those rules. `netlify.toml` also records that Netlify Pretty URLs must stay enabled.

The live host otherwise passed the relevant crawl checks at the time of investigation: HTTP redirected to HTTPS, `www` redirected to the apex host, sitemap and robots files returned `200`, intended pages returned `200`, and an invented missing URL returned a real `404`. The site was also new enough that indexing latency and Google's assessment of page value remain plausible contributors; a successful crawl and sitemap submission do not guarantee indexing.

A secondary content risk remains: the ten guide pages contain roughly 308–394 words in their main content, follow a very similar structure, and several address closely related search intent. There is no technical minimum word count, but adding first-hand inspection examples, original photos, concrete measurements, author qualifications, and authoritative references would make the pages more distinctive and useful. Prioritize the home page and core service pages first, then strengthen overlapping guides before repeatedly requesting their indexing.

## Google Search requirements audit

Implemented in source:

- Crawlable HTML content and standard `<a href>` internal links.
- Explicit indexability on all intended content pages.
- Unique titles, descriptions, headings, and canonical URLs.
- Mobile viewport and responsive design.
- Crawl access to CSS, JavaScript, images, and the sample PDF.
- Valid structured data that matches visible business, author, service, FAQ, and article content.
- A `WebSite` entity for the preferred site name and a stable `LocalBusiness` / `ProfessionalService` entity.
- Large image previews and unrestricted snippets for eligible search and AI features.
- Open Graph and Twitter card metadata for share previews.
- A favicon and Apple touch icon.

The implementation follows [Google Search Essentials](https://developers.google.com/search/docs/essentials), [canonical URL guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), and [structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

FAQ structured data remains accurate and machine-readable. Google discontinued FAQ rich-result display in 2026, so it should not be treated as a promise of a special result or as a ranking factor.

## 404 audit

`404.html` is a dedicated, branded, responsive recovery page with:

- A clear not-found message.
- Home, services, and contact recovery links.
- The normal desktop/mobile navigation.
- `noindex, follow` and no canonical URL.
- No JavaScript console errors in desktop or mobile browser verification.
- No horizontal layout overflow at 1280 px or 390 px.

The production host must return an actual HTTP `404` status for missing URLs while serving this file. A `200` response showing a not-found message is a soft 404 and is not compliant. See [Google's soft-404 guidance](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors#soft-404-errors).

## GEO and local SEO audit

Here, GEO covers both geographic relevance and generative-engine visibility.

Geographic/local signals implemented:

- Consistent visible business name, phone, and Givatayim address.
- `LocalBusiness` / `ProfessionalService` schema with `PostalAddress`, `areaServed: Israel`, phone, founder, logo, and service catalog.
- `geo.region=IL`, a visible nationwide service area, Hebrew-Israel locale, and Givatayim placename on the about/contact pages.
- Service-specific landing pages and internal links rather than one generic services page.

No latitude/longitude was invented because verified coordinates are not stored in this repository. Exact coordinates can be added only after confirming the production Google Business Profile location.

External local SEO work still required:

- Keep the Google Business Profile name, address, phone, hours, category, and website URL identical to the site.
- Add the verified production website URL to the Business Profile.
- Build genuine reviews and consistent citations on relevant Israeli directories; do not add fabricated review schema.
- Confirm whether the street address is meant to be public. `placeholders.json` says `TODO_NO_PUBLIC_ADDRESS`, while the website publicly shows כצנלסון 148, גבעתיים.

## Generative engine / AI visibility audit

Implemented:

- A proposal-conformant `llms.txt` with an H1, concise summary, business facts, primary pages, and professional guide links.
- `rel="describedby"` discovery links from every indexable page to `llms.txt`.
- Entity-connected structured data for the site, business, founder, services, blog, contact page, profile page, and sample report.
- Direct-answer FAQ content, visible article dates and authors, descriptive headings, semantic HTML, and crawlable text.
- No crawler blocks for Googlebot or other agents covered by the global robots rule.

`llms.txt` is a community proposal, not a Google Search requirement. Google states that AI Overviews and AI Mode use the same SEO foundations and require no special AI file or AI-specific schema. Helpful, original, expert-led content and Search index eligibility matter more: [Google AI feature guidance](https://developers.google.com/search/docs/appearance/ai-features), [Google generative AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), and the [llms.txt proposal](https://llmstxt.org/).

Content opportunity: the articles are focused and readable, but stronger first-hand evidence would improve trust. Add original inspection photos with permission, anonymized examples, precise author qualifications, and source references where technically or legally relevant. Do not invent licenses, certifications, case results, statistics, or reviews.

## Required post-deployment checks

1. Deploy from this repository root and confirm Netlify reports all 17 `_redirects` rules as processed.
2. Confirm every clean URL returns `200`, each matching `.html` URL returns one `301` to the clean URL, and `/index.html` returns one `301` to `/`.
3. Verify HTTPS and one preferred host/version; permanently redirect all HTTP and alternate-host URLs to it.
4. Confirm a real missing URL returns HTTP `404` and the custom `404.html` content.
5. Open `/robots.txt`, `/sitemap.xml`, and `/llms.txt` publicly and verify they return `200` as plain text/XML.
6. Resubmit `/sitemap.xml` in Google Search Console after the clean-URL deployment.
7. Use URL Inspection on the clean home, services, contact, blog, and several article URLs; run the live test and request indexing for the most important pages.
8. Validate production pages with Google's Rich Results Test and monitor Enhancements / Page Indexing reports.
9. Measure production Core Web Vitals and HTTPS status in Search Console. Local source review cannot substitute for real-user field data.
10. Monitor indexed-versus-submitted sitemap counts. Investigate exclusions rather than repeatedly resubmitting an unchanged sitemap.

Google's current page-experience guidance emphasizes Core Web Vitals, HTTPS, mobile usability, and an unobstructed main experience: [Google page experience guidance](https://developers.google.com/search/docs/appearance/page-experience).

## Regression command

```bash
python3 scripts/seo_audit.py
```

The command exits non-zero if sitemap coverage, canonical alignment, index directives, metadata, H1 count, JSON-LD syntax, internal links, fragments, images, clean-URL redirects, Netlify Pretty URLs, `robots.txt`, `llms.txt`, or 404 exclusions regress.
