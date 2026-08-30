# SEO and GEO audit — אור בדק בית

Audit date: 2026-08-30

## Executive result

The repository now passes the local technical SEO audit for all 17 indexable HTML pages. Every indexable page is represented once in `sitemap.xml`; the dedicated `404.html` is explicitly `noindex` and excluded. Crawl controls, unique canonicals, page titles, descriptions, H1s, social metadata, locale signals, internal links, images, and JSON-LD all pass the automated source checks.

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
| Internal crawlable links | Pass | No missing local files or fragment targets |
| Titles and descriptions | Pass | Present and unique on every indexable page |
| Primary headings | Pass | Exactly one non-empty H1 on every page |
| Language and direction | Pass | `he-IL` and RTL on all pages |
| Image accessibility | Pass | All images have `alt`; blog covers now have intrinsic dimensions |
| JSON-LD syntax | Pass | Every structured-data block parses as valid JSON |

Google's sitemap guidance requires absolute URLs and recommends listing the canonical URLs intended for Search. The sitemap is a discovery hint, not an indexing guarantee: [Google sitemap documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

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

1. Confirm the final production hostname and replace the assumed GitHub Pages base if necessary.
2. Verify HTTPS and one preferred host/version; permanently redirect all HTTP and alternate-host URLs to it.
3. Confirm a real missing URL returns HTTP `404` and the custom `404.html` content.
4. Open `/robots.txt`, `/sitemap.xml`, and `/llms.txt` publicly and verify they return `200` as plain text/XML.
5. Verify the site in Google Search Console and submit `/sitemap.xml` once.
6. Use URL Inspection on the home page, services, contact, blog, and several articles; request indexing after successful live tests.
7. Validate production pages with Google's Rich Results Test and monitor Enhancements / Page Indexing reports.
8. Measure production Core Web Vitals and HTTPS status in Search Console. Local source review cannot substitute for real-user field data.
9. Monitor indexed-versus-submitted sitemap counts. Investigate exclusions rather than repeatedly resubmitting an unchanged sitemap.

Google's current page-experience guidance emphasizes Core Web Vitals, HTTPS, mobile usability, and an unobstructed main experience: [Google page experience guidance](https://developers.google.com/search/docs/appearance/page-experience).

## Regression command

```bash
python3 scripts/seo_audit.py
```

The command exits non-zero if sitemap coverage, canonical alignment, index directives, metadata, H1 count, JSON-LD syntax, internal links, fragments, images, `robots.txt`, `llms.txt`, or 404 exclusions regress.
