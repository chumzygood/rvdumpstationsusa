# RV Dump Stations USA — national site, Texas first

Updated November 10, 2026 (EST), following Chanoch's national-site/domain/full-setup approval. This supersedes the earlier Texas-only naming recommendation. Domain purchase and Cloudflare DNS are being handled separately; this executor buys nothing.

## Scope and current inventory

Brand/domain: **RV Dump Stations USA**, https://rvdumpstationsusa.com.
Nationwide project with **Texas as the only live state**. The other 49 states appear as coming-soon text, without empty pages or unverified listings.

Current inventory: **76 operator-listed properties**:
- 64 Texas Parks and Wildlife Department state-park properties.
- 6 U.S. Army Corps of Engineers campgrounds.
- 6 travel centers: 3 Love's and 3 TA.

Count properties, not dump lanes. Closed Kickapoo Cavern and the Barton Warnock lead remain withheld. No Pilot, Buc-ee's or TxDOT location was added without adequate location-specific official evidence; see research/coverage-notes.md. This is a data-readiness starting scope, not a claim of comprehensive Texas coverage or national demand validation.

## Site and indexing

- `/`: national home, first-state coverage, live Texas link and coming-soon states.
- `/texas/`: searchable state directory.
- `/texas/cities/<locality>/`: actual station listings grouped by official city or explicitly labeled lake area.
- `/texas/stations/<id>/`: station/property details, seven questions, evidence, alerts and source-check date.
- `/about/`: methodology, limits, independence and relevant TossMap sister-project link.
- `/404.html`: recovery page.

All real content pages are **indexable**, with unique HTTPS canonicals, JSON-LD, internal links and sitemap entries. The 404 alone is noindex and excluded from the sitemap. No empty state pages exist. We do not noindex useful one-property city pages merely because they are small. Future city additions need real coverage; no fabricated copy or ranking guarantees. Highway pages wait for official road/exit evidence and meaningful inventory.

## Data and consumer questions

Stable ID; name/property; operator; official source type; official locality or named lake area; address and precision; primary/evidence URLs and snapshots; last-checked date; seven answers with per-field source/status; official property alerts. Unknown street addresses, exact station entrances and unsupported coordinates are not invented. USACE project-office addresses are not reused as campground addresses.

Ask consistently: dumping fee (guest/non-guest and admission separately), potable-water fill, non-guest access, dump-station seasonality, dump-station hours, station payment methods, and big-rig approach/clearance. Unknown stays unknown. Store hours, campground lengths and water hookups are never substituted. Most operational answers remain unconfirmed; review operator pages before driving.

## Hosting and deployment

Approved separate public repository: `chumzygood/rvdumpstationsusa`. GitHub Pages source: `main`, `/docs`; custom domain `rvdumpstationsusa.com` via docs/CNAME and Pages settings. Python build/tests run locally; push only when they pass. No force-push. No changes to TossMap's repository.

DNS instructions: DNS.md. Certificate and HTTPS readiness depend on the separately managed DNS. The site is not claimed live on the custom domain before that is verified.

## Later monetization

Potential clearly labeled featured positions for campgrounds/RV parks after useful coverage and referral demand. No paid ranking disguised as editorial quality. Government inventory is not a sponsorship prospect list. No outreach, sale, sponsorship, advertising spend, paid API or payment action now.

## Remaining work, not approval blockers for substantive indexing

Rendered mobile/desktop visual verification and independent multi-model persona testing were unavailable to this executor; do not claim they passed. Responsive code, target sizes, navigation, source checks, schemas, canonical/sitemap/robots rules and offline acceptance checks were improved/tested where possible. UI-REVIEW.md records the exact limitations.

Next content work: deepen access/fee evidence, verify more private operators and official government stations, then expand to additional states without publishing empty pages. No contacting operators without separate permission.
