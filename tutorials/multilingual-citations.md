# Interpret explicit citations across languages and markets

## Business question

A team has answer observations from more than one language and market. How can it inspect which answers contain explicit URLs without turning a small, mixed sample into a claim about international visibility or engine quality?

## Teaching scenario

**Entirely fictional:** six invented answers from “Fictional Atlas / demo-1 / web” describe Cedar Notes. Four are English / United Kingdom; two are French / France. Five raw citation rows include two fragment variants of the same URL inside one answer. No real AI engine was queried and no client result is presented.

## Run the exact example

From `examples/fictional-workflow/` in a fresh repository copy:

```sh
python3 tools/ai-citation-tracker/tracker.py --answers inputs/answers.csv --citations inputs/citations.csv --as-of 2026-11-01 --output reports/citations
```

Open `reports/citations/report.html`. JSON plus answer, citation, hostname and group CSVs make the denominators and URL observations inspectable. The command runs offline.

## Read the actual counts

- English / United Kingdom: **4 answers**, **2 cited answers**, **3 normalized explicit citations** summed across answers. Cited-answer rate: **2 / 4 = 50%**.
- French / France: **2 answers**, **1 cited answer**, **1 citation**. Cited-answer rate: **1 / 2 = 50%**.
- The two fragment variants inside uk-1 collapse to one normalized citation URL. The same research URL in a different answer still counts for that answer.
- Answers with no citation remain in their group's denominator.

An explicit URL is not proof that the cited page supports the accompanying claim. Hostnames are not registrable domains, and different queries on the same hostname can be distinct URLs. Read the tool's normalization rules before comparing counts with another system.

## Make the interpretation decision

Both sample fractions happen to equal 50%. This does not establish equal engine behavior, a population-wide market rate, or a before/after improvement. The sample sizes differ and the entire sample is fabricated. Do not pool the language/market groups to infer international performance.

For a real collection, freeze the prompt wording and version, local intent, planned repetitions, dates and time zones. Record engine, model if disclosed, interface, search mode and account conditions where known. A consumer interface and an API are different observation contexts; a translation may not represent an equivalent experiment.

## Check the sources separately

After counting, read each cited source, match the actual entity and review whether the source supports the particular statement. Record missing sources, inaccessible pages, contradictions and uncertainty rather than replacing them with a credibility score. An uncited answer does not show whether a source was used internally.

## Next step

Use the [measurement protocol](../docs/measurement-protocol.md) to design an actual dated collection. The interactive explorer can filter and export this published fictional sample; it does not collect answers, perform live monitoring or query providers.

[Interactive citation view](https://mhdteto.github.io/authority-architecture-system/#citations) · [Tracker and releases](https://github.com/mhdteto/ai-citation-tracker) · [Synthetic answers](../examples/fictional-workflow/inputs/answers.csv)
