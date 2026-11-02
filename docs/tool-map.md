# Choose the next resource

The repositories cover different decisions. Links between them describe a workflow; the tools do not automatically exchange data, crawl all profiles, query AI engines or verify the truth of claims.

| Question | Resource | Next decision |
| --- | --- | --- |
| How should the whole review be organized? | [Authority Architecture System](https://github.com/mhdteto/authority-architecture-system) | Define the entity, languages, markets, claims and measurement conditions. |
| How does this apply to a leader? | [Executive Authority Playbook](https://github.com/mhdteto/executive-authority-playbook) | Establish the public identity and review priorities. |
| What technical signals does one page expose? | [Search & AI Discoverability Checker](https://github.com/mhdteto/search-ai-discoverability-checker) | Review access and page observations without inferring indexing or citations. |
| Where do supplied profiles differ? | [Entity Consistency Auditor](https://github.com/mhdteto/entity-consistency-auditor) | Review mismatches against an approved reference, with local context. |
| What supports or contradicts a material claim? | [Authority Evidence Mapper](https://github.com/mhdteto/authority-evidence-mapper) | Resolve conflicting reviews and missing evidence. |
| How should approved entity relationships be modeled? | [Entity Structured Data Kit](https://github.com/mhdteto/entity-structured-data-kit) | Match markup to verified visible content; subset lint is not full validation. |
| Which explicit URLs occur in supplied answers? | [AI Citation Tracker](https://github.com/mhdteto/ai-citation-tracker) | Keep engine, model, interface, language, market and denominators separate. |
| Where might a reviewer find a relevant public record? | [International Reputation Source Map](https://github.com/mhdteto/international-reputation-source-map) | Inspect the specific record and its scope; the catalogue is a starting point. |

## Try the sequence

The [complete fictional workflow](../examples/fictional-workflow/README.md) includes five frozen source scripts, public version references, entirely invented inputs and 17 original output files. It runs offline. Each participating tool repository also contains its own `examples/connected-workflow/` folder and a CI reproduction check.

For real work, write the [measurement protocol](measurement-protocol.md) before collecting answers. A stable identity, evidence register or clean JSON-LD report does not establish an AI recommendation or a search ranking.
