# Grad Atlas

A static, source-led graduate programme research explorer. Designed for GitHub Pages at `/grad-atlas/`, with relative assets and no backend, external fonts, analytics, or account system.

## Contents

- 649 canonical programme records.
- 214 candidate observations, which may overlap programmes or revisit routes.
- 450 research leads, including pending and excluded leads, shown only when explicitly selected.
- 64 routes in the latest Singapore / Hong Kong research batch.

These counts are different units, **not 1,313 unique programmes**. Missing source links, historical years, uncertainties and screening decisions are retained. Pure mathematics is outside the positive search scope. Verify all application details with the official institution.

## Use

Search across programme names, institutions, fields and research details. Filter by country, field, university, record kind, Singapore/Hong Kong, or the latest regional batch. Open a record to inspect evidence, dates and structured details. Save records to a browser-local shortlist. `/` focuses search; Escape dismisses details. Filters are shareable through URL query parameters, records through URL fragments.

Public exports:
- `data/catalogue.json`: sanitized research records and provenance.
- `data/catalogue.sqlite`: a compact database created from the sanitized export, not a copy of the private source database.

Large source databases and private evidence remain separate. The site contains no credentials, personal account details, raw response captures, or private Drive links.

## Run and test

From this directory:

    python3 -m http.server 8765
    npm test

The browser QA script assumes the repository's parent directory is served on port8765, so the app is at `/grad-atlas/`. It needs Playwright and Chromium available in the test environment:

    node grad-atlas/tests/browser.cjs

Model tests cover record counts, scope exclusion, latest regional batch, search and filtering, shortlist behavior, sorting, safe source URLs and corrupt storage. Browser verification status is tracked separately; a model-test pass is not a rendered visual check.

## Publishing

Place this directory at `grad-atlas/` in the existing GitHub Pages repository. Do not replace unrelated root files or CNAME settings. Preserve relative paths. No workflow or build step is required when the existing repository deploys its branch root.

## Updates

Regenerate `data/catalogue.json` and `data/catalogue.sqlite` using the reviewed export process. Keep source dates and limitations. Do not treat candidate observations as new distinct programmes or collapse conflicting facts silently. Run the tests and check the published page after deployment.
