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

## Deadline semantics

`application_windows.deadline_semantics` distinguishes `final_closure`, `round_deadline`, `priority_consideration`, `funding_consideration`, `recommended_submission`, `document_deadline`, `scholarship_deadline`, and `unspecified`. The default is deliberately **unspecified**, never inferred final closure. UI should use neutral deadline wording unless an explicit reviewed semantic is supplied. `semantics_review_required` flags narrative priority/recommended/funding wording for human/source review without automatically reclassifying it. These flagged or confirmed nonfinal considerations are excluded from the urgent closure list. `deadline-semantics-review.json` retains the open review queue. Recommendation-based admission routes are not the same as suggested submission dates.

`coverage.<scope>.exact_date_pairs` counts all source-evidenced exact application pairs and breaks them down by deadline semantics. It is not a closing-date-completeness metric. `firm_application_pairs` counts only explicitly reviewed `final_closure` and `round_deadline` pairs; unspecified is not treated as final. Per-semantic identity counts can overlap when a programme has multiple windows. Legacy `with_reviewed_exact_start_and_end` remains for backwards compatibility with the all-pairs definition, not a firm-closure claim.

## Review outcomes and identity limitations

`review_outcome_recorded` distinguishes an inspected but unresolved/unverified research note from an item never processed. `review_attempted_at` preserves its inspection date without implying source verification; `checked_at` remains null for unverified outcomes. Scoped coverage now includes `outcomes_recorded`, `without_review_outcome`, and `unresolved_identity_outcomes`. Legacy `inspected` means non-unverified status only; use outcomes_recorded for processing completion.

`review_annotations` durably retains proposed `resolved_programmes` and reciprocal `linked_review_updates`. Multi-programme notes remain unresolved original identities, with individual labels/windows where supplied; no new award IDs are invented. Related/alias evidence is prominently cross-linked in notes and exported in full without replacing another record's direct review. A confirmed combined-route relation is not a claim that distinct exit awards are the same degree. `queue-coverage.json` checks every inventory identity appears in exactly one queue and lists remaining unprocessed IDs.

## Availability guard

Programme and intake availability accept offered, not_offered, discontinued, currently_closed, not_verified. Explicit negative availability suppresses open/future/rolling display and excludes the entry from upcoming application endpoints without erasing historic dates or changing unknown endpoints. Closure of one historical application cycle is not programme discontinuance. `availability-review.json` exposes all negative programme/intake outcomes with scoped evidence. Different-institution successors and similarly named but different degrees must not inherit another programme's availability.

## Source observations and link safety

`source_observations` preserves each programme review's source-access status, timestamp, access method and direct-fetch status. An official indexed-text inspection can support an assertion even when direct fetching fails; these are distinct contexts. `sources.access_status` is an aggregate accessed-if-any observation, NOT the last attempt or a claim every reviewer accessed it. Per-programme projection and `source_observations` must agree.

`source_safety` and public `sources[].link_allowed`, `safety_status`, `safety_reason` prevent the precisely identified compromised former AIMS domain aimsammi.org (including www) from becoming a trusted clickable link. Original references remain plaintext provenance. Window/requirement `safe_source_urls` exclude those hosts, while `excluded_source_urls` preserves the URL and reason. Other unverified/blocked sources are not blanket-banned. Historical archive UI must apply the same exact-host filter.
