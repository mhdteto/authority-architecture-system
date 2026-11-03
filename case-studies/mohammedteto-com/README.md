# Real first-party case: MohammedTeto.com

**A dated technical baseline, collected on 3 November 2026.** This is a maintainer-owned public website, not a client endorsement or a before/after success story. The three page observations below use real HTTP responses. They are separate from the fully fictional Alex Rowan / Cedar Notes teaching workflow elsewhere in this repository.

## Business question

Can a visitor or technical reviewer inspect the public foundations supporting an international AI reputation advisory practice and follow the path from method to open-source tools? Which conclusions can a small public-page checker actually support?

This case evaluates the homepage, method page and open-source tools page. It does not evaluate the full advisory service or verify the author's professional claims. Independence is limited: Mohammed Teto owns both the site and the tool suite.

## Collection and evidence

Collection started at **2026-11-03 18:53:20 UTC** (19:53:20 Africa/Casablanca). The frozen Search & AI Discoverability Checker is from commit `5221f938506866933b361e4e6301d31944021061`, release v1.0.0. The collection harness reuses already fetched responses across the three observations: **five unique live HTTP requests**, no redirects observed. It preserves the date, public response bodies and diagnostic headers; response cookies and infrastructure headers are excluded.

| Public page | HTTP | Canonicals observed | JSON-LD blocks / parse failures | H1s observed | Declared HTML language |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Homepage](https://mohammedteto.com/) | 200 | 1, self-referencing | 1 / 0 | 1 | en |
| [Method](https://mohammedteto.com/method/) | 200 | 1, self-referencing | 1 / 0 | 1 | en |
| [Open-source tools](https://mohammedteto.com/open-source-tools/) | 200 | 1, self-referencing | 1 / 0 | 1 | en |

Each page has a nonempty title and description. The homepage H1 describes AI reputation and executive authority; the method H1 describes authority as a system; the tools H1 explicitly names search and AI reputation. These are observations of first-party messaging, not external validation of expertise.

The checker observed robots.txt and the declared sitemap with HTTP 200. The supplemental XML parser found a sitemap index referencing four child sitemaps. **The child sitemaps and their listed pages were not fetched**, so inclusion of any particular page is unverified. Each page's internal-link sample reaches the tool's limit of 20; that is a capped sample, not a complete link count.

Homepage and method HTML declare `en`, `fr` and `x-default` alternatives. The tools page declares none. The French target pages were not fetched in this case, so their status, canonical, content and reciprocal annotations remain unverified. Absence of hreflang on an English-only page is not, by itself, a defect.

### Inspect the original outputs

- Homepage: [JSON](2026-11-03/home/report.json) · [HTML source/download](2026-11-03/home/report.html).
- Method: [JSON](2026-11-03/method/report.json) · [HTML source/download](2026-11-03/method/report.html).
- Tools: [JSON](2026-11-03/tools/report.json) · [HTML source/download](2026-11-03/tools/report.html).
- [Extracted titles, descriptions, H1s and language alternatives](2026-11-03/metadata.json).
- [Sitemap-index observation](2026-11-03/sitemap-observation.json).
- [Archived real public responses](2026-11-03/http-archive.json) · [SHA-256 manifest](2026-11-03/SHA256SUMS.json).

On GitHub, HTML links show source. Download the standalone report and open it locally for the rendered view. The archive contains public website content for reproducibility; it contains no synthetic engine answers or client records.

## Decisions and next checks

The limited observations support **retaining the observed canonical/title/H1 setup while extending verification**. They do not justify speculative markup changes simply to create an improvement narrative.

| Priority | Decision or follow-up | Evidence required to close it |
| :--- | :--- | :--- |
| P1 | Verify sitemap coverage for the three pages before proposing a sitemap change. | Read the declared child sitemaps; record actual listed URLs and their status/canonical. |
| P1 | Check English/French alternatives as actual content pairs. | Fetch both versions; inspect reciprocity, intended language, canonical and indexability. Add annotations to the tools page only if a real equivalent exists. |
| P1 | Establish a separate search/AI-answer baseline if visibility is the business question. | Dated engine/interface/model, prompts, language, market, answers and actual citations; preserve denominators and access conditions. |
| P2 | Review each material biography/service claim against suitable evidence. | Approved entity reference and manually reviewed claim-to-source relationships. HTTP and JSON-LD cannot establish truth. |

These are proposed checks, not fixes applied to the website. The site was not modified during this GitHub publication.

## Reproduce or follow up

From the repository root, verify the archived case without any network access:

```sh
python3 case-studies/mohammedteto-com/verify_case.py
```

The verifier checks hashes and replays all three real observations from their archived HTTP responses. It compares JSON, HTML and extracted metadata exactly. Replaying an archive is not a fresh live measurement.

To collect a new dated snapshot into a new directory:

```sh
python3 case-studies/mohammedteto-com/collect.py --output-dir case-studies/mohammedteto-com/follow-up-YYYY-MM-DD
```

Replace the date placeholder. The directory must not already exist. The script observes only the three fixed first-party URLs and their bounded technical resources. It does not change the website. Record any actual change with its deployment date before comparing a follow-up. Keep the tool commit, URLs and collection conditions comparable; preserve earlier snapshots. A changed response after an intervention is not by itself causal evidence of a search/AI outcome.

## What remains unknown

Index coverage, rankings, crawl behavior by actual providers, Core Web Vitals, traffic, qualified demand, AI retrieval and actual citations were not measured. JSON-LD parse success does not establish schema validity or rich-result eligibility. User-agent directives do not prove that a particular provider fetched or used a page. No percentage improvement, client outcome or before/after result is claimed.

[Run your own scoped observation with the starter](https://github.com/mhdteto/search-ai-audit-starter) · [Method and measurement protocol](../../docs/measurement-protocol.md) · [Independent advisory context](https://mohammedteto.com/).
