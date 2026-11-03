# Review organizational evidence before strengthening a claim

## Business question

An organization wants its public description to emphasize expertise, international reach and a publication record. Which assertions have reviewed corroboration, which rely on the organization's own material, and which should be withheld until evidence is collected?

## Teaching scenario

**Entirely fictional:** Cedar Notes says it published a multilingual reading-journal series and operates offices on three continents. The register also contains a separate claim about Alex Rowan chairing a fictional forum, so the example demonstrates how a contradiction is preserved.

There are three claims and six invented reviewer declarations. Publishers, relationships, support labels, dates and notes are supplied inputs. No source page is fetched or independently verified by the mapper.

## Run the exact example

From `examples/fictional-workflow/` in a fresh repository copy:

```sh
python3 tools/authority-evidence-mapper/map_evidence.py --claims inputs/claims.csv --evidence inputs/evidence.csv --as-of 2026-11-01 --output-dir reports/evidence
```

Open `reports/evidence/report.html`; JSON and CSV outputs preserve the review details. Run locally without packages, API keys or network calls.

## Read the organizational claims

- The publication-series claim has an owned supporting entry, a partial entry with unknown relationship and no access date, and an independent entry marked unreviewed.
- Its count of independent-support publishers is **0**. An unreviewed independent URL does not become reviewed support.
- The three-continent office claim has **no evidence rows** and remains a missing-evidence gap.
- The separate forum-chair claim retains support and a contradiction together. Two supporting entries with the same normalized publisher count as **one** independent-support publisher, not two.

These outcomes describe input declarations. They neither prove that an assertion is true nor determine which conflicting source is correct. The age threshold refers to a recorded access date; it is not a universal expiry rule for evidence.

## Make the review decision

1. Open and read the original publication sources in a real engagement. Confirm the exact works, language editions, publisher and dates.
2. Review the independent inventory entry before assigning a support label. Do not turn an unreviewed URL into corroboration just because the publisher appears reputable.
3. Keep owned material useful for describing the organization's position, while recording its relationship explicitly.
4. Withhold the office claim until appropriate records establish the specific locations and current operating scope. International service coverage alone does not establish offices.
5. Resolve the forum contradiction using primary records and chronology before reusing that credential in a biography.

## Adapt the source strategy

The [International Reputation Source Map](https://github.com/mhdteto/international-reputation-source-map) provides real public entry points, not verified evidence for Cedar Notes. Choose sources relevant to the exact claim and jurisdiction. Record access conditions and scope; legal existence, a publication identifier or a directory presence does not establish general prestige or commercial success.

## Next step

Translate only approved, visibly supported identity and publication relationships into structured data. Then use the [multilingual citation tutorial](multilingual-citations.md) to inspect supplied answers under defined conditions. Neither the evidence register nor a clean JSON-LD report measures actual AI visibility.

[Interactive evidence view](https://mhdteto.github.io/authority-architecture-system/#evidence) · [Mapper and releases](https://github.com/mhdteto/authority-evidence-mapper) · [Input claims](../examples/fictional-workflow/inputs/claims.csv)
