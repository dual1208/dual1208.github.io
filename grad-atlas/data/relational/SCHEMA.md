# Relational graduate-programme archive

One programme identity is a conservative institution/title grouping, not a claim that every semantic duplicate has been resolved. All 1,325 original public records remain preserved in programme_records. Excluded/research leads are not promoted to recommended programmes.

- institutions: institution/location identity.
- programmes: programme identity, classification and current review state.
- programme_records: all originating records and their sanitized historical content.
- intakes: programme, intake label, academic cycle and mode.
- application_windows: intake, round, applicant scope, window type; independent opening/closing date and evidence status; cutoff/time-zone provenance; source origin; display/archive selector.
- requirements: programme requirement assertions by category, with evidence status and display/archive selector.
- sources: URL identities; programme_sources, window_sources and requirement_sources are many-to-many provenance links.
- evidence: source-linked public requirement/date assertion text and origin.
- research_reviews: each programme's latest review status/date/limitations.
- duplicate_candidates: explicit reviewer-proposed duplicates pending identity review, never automatic merges.
- metadata and date_coverage view: coverage, limits and basic reporting.

## Date semantics

`exact` means an evidenced ISO calendar date, not necessarily a currently open cycle. `annual` has no safely assignable year; `rolling` has no invented fixed cutoff. `not_published` requires checking an official source and finding no published date, while `not_verified` means research is incomplete. `conflicting` retains incompatible claims rather than silently choosing. A separate window_status shows open/future/closed/unknown/rolling. An exact date imported from the historical archive remains evidence_origin=historical_archive, with no invented fresh check date. Displayed review_status is essential.

Application deadlines are distinct from supporting_documents, scholarship and enrolment events. Rounds and applicant categories are distinct windows. Unknown dates are null; never zero, year-only dates or fabricated month boundaries. Cutoff time zones are explicitly stated or marked inferred/unpublished.

## Outputs and rebuilding

`python scripts/inventory.py` reconstructs stable conservative identities and institution-grouped queues from the existing public catalogue and hardware report.
`python scripts/build_database.py` imports reviewed JSON and preserves archived assertions.
`python scripts/validate_database.py` checks integrity, provenance, full coverage and generic privacy patterns.

outputs/table.json is a grouped web projection: each programme includes windows, requirements, source URLs and review status. outputs/programmes.sqlite is the downloadable relational database. outputs/coverage.json separates fresh review outcomes from mere representation. Source review is ongoing: every identity is represented, but that does not mean every date is verified.

## Scoped coverage and aliases

`coverage.positive_programmes` tracks the 875 programme/candidate/hardware identities separately from `coverage.lead_only` (411 research leads). Each exposes reviewed/partial/blocked/unverified counts, inspected total, fresh exact date-pair and verified-requirement counts. An exact pair means at least one source-reviewed application window, not that all intakes have dates. Verified requirements means at least one verified requirement, not a complete admissions checklist.

`programme_aliases` records confirmed same-award aliases while preserving both original IDs and research reviews. `canonical_programme_id` and `alias_of` expose this relation; unresolved candidates stay in `duplicate_candidates`. Source metadata now refreshes archived entries with source-review access status and timestamp instead of retaining an old archive timestamp. Per-assertion evidence preserves the review timestamp.
