# Review an executive's identity before changing a profile

## Business question

An international leader appears under different names and roles across a biography, a French profile, a directory and an event page. Which differences need correction, and which are approved alternatives? This workflow supports the identity foundation of an authority review.

## Teaching scenario

**Entirely fictional:** Alex Rowan is Cedar Notes' Research Director. Four invented profile observations are supplied. The owner-approved reference explicitly permits the French role “Directeur de recherche” and the organization variant “Cedar Notes Publishing.” These approvals are inputs, not discoveries made by the tool.

The directory observation uses “A. Rowan” and “Chief Scientist.” The event observation has a name but no role, organization or description. None of the placeholder example-domain URLs was researched as evidence.

## Run the exact example

From `examples/fictional-workflow/` in a fresh copy of this repository:

```sh
python3 tools/entity-consistency-auditor/audit.py --identity inputs/identity.json --profiles inputs/profiles.csv --as-of 2026-11-01 --output-dir reports/identity
```

Open `reports/identity/report.html`. The same run writes JSON and CSV outputs. The CLI runs offline on the supplied inputs.

## Read the actual output

- 6 fields match the reference.
- 2 fields match explicit approved aliases.
- 2 fields are mismatches: the abbreviated name and different role in the directory observation.
- 3 fields are missing from the event observation.
- 3 nonempty descriptions require manual review; the fourth description is missing.

These are field counts across four profiles, not counts of people, an accuracy percentage or an authority score. Case and whitespace normalization does not automatically approve translations, abbreviations or legal-name changes.

## Make the review decision

1. Read the original record and its date before deciding whether the directory role is outdated, a different identity or a valid historical role.
2. Ask the entity owner whether “A. Rowan” is an acceptable alias in this exact context. Do not approve it merely to eliminate a mismatch.
3. Collect the missing event information from an appropriate source. Empty fields do not become agreement.
4. Read biography descriptions for factual support, chronology and context. The software intentionally does not make semantic judgments.
5. Record the correction owner, supporting evidence and review date; update only the profile or approved reference that should actually change.

## Adapt across markets

The sample aliases apply to all observations in that run. When a translated role is approved only for one market, use separate approved records and runs. Preserve original scripts, accents, organization suffixes and dates unless an authorized alternative is documented. An exact match to an incorrect reference is still not truth verification.

## Next step

Use the [organization-evidence tutorial](organization-evidence.md) to connect material claims to actual reviewed sources. Define the observation protocol before asking whether any correction changed search or AI representation. No ranking or citation result is measured here.

[Interactive identity view](https://mhdteto.github.io/authority-architecture-system/#identity) · [Original tool and releases](https://github.com/mhdteto/entity-consistency-auditor) · [Full sample inputs](../examples/fictional-workflow/inputs/identity.json)
