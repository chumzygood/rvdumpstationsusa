# RV Dump Stations USA

National official-source RV dump-station directory, starting with Texas.
Canonical domain: https://rvdumpstationsusa.com/

## Build

```sh
python3 scripts/seed_data.py
python3 scripts/build.py
python3 scripts/test_build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Python 3.10+. Seed/build/tests are offline and standard-library only. `docs/` is the GitHub Pages publishing directory. Source collection scripts additionally use requests/BeautifulSoup and run only when explicitly requested. A rebuild does not advance last-checked dates.

## Structure and indexing

- `/`: United States homepage; Texas live, all other states coming soon without empty pages.
- `/texas/`: state directory and searchable inventory.
- `/texas/cities/<locality>/`: substantive local listings, including explicitly labeled lake areas where municipal locality is unconfirmed.
- `/texas/stations/<id>/`: property-level station facts, seven consistent questions and official evidence.
- `/about/`: methodology, independence, limits, and sister project TossMap.
- `/404.html`: recovery page; noindex.

Every real content page has an HTTPS canonical, JSON-LD and a sitemap entry, and is indexable. Only the 404 is noindex. No blank state landing pages exist. Robots allows crawling and identifies the sitemap. No promise of Google indexing or rankings.

## Verification

Count properties, not physical dump lanes. A government/operator-listed amenity is not proof of real-time operation, public access, station hours, potable fill, price, payment method or big-rig clearance. Unknowns remain explicit. Store hours and payment lists are not substituted for dump-station facts. Street addresses are labeled property-level; USACE lake-area listings with unconfirmed street addresses link directly to agency directions and omit unsupported address fields from schema. Operator closure alerts are prominent.

`research/` stores public evidence, per-page error audits and source snapshots. Some USACE pages blocked direct requests but were readable through the public webpage-fetch tool; curated official excerpts are labeled accordingly. `collect_extra.py` uses those frozen USACE excerpts rather than claiming a new live fetch. Review and update snapshots/dates manually during a verified refresh.

The former local preview was preserved outside this repository at `/workspace/rv-dump-directory-local-preview-20261110`. TossMap was not modified. No credentials, payments, contact submissions or outreach are involved. Domain registration/DNS are handled separately by the owner.

See `PLAN.md`, `UI-REVIEW.md`, `research/coverage-notes.md`, and `DNS.md` for launch details and remaining limitations. Do not confuse automated checks with completed rendered mobile or multi-model usability tests.
