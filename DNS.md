# Cloudflare DNS for rvdumpstationsusa.com

Official GitHub instructions checked November 10, 2026 (EST):
https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

Set these records in Cloudflare; initially use **DNS only** (gray cloud), TTL Auto, so GitHub can validate DNS and issue its certificate without proxy interference.

| Type | Name | Target |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | chumzygood.github.io |

Optional IPv6, in addition to the A records:

| Type | Name | Target |
|---|---|---|
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |

Do not put a repository name in the www target. Do not add wildcard records. Review conflicting apex/www defaults before changing them; preserve unrelated email/DNS records. No DNS changes were performed by this executor.

The GitHub Pages custom domain is the apex `rvdumpstationsusa.com`. GitHub should redirect www to apex once both records and TLS are ready. After DNS propagation/certificate issuance, enable Enforce HTTPS if it is not yet available. GitHub notes DNS/certificate setup may take up to 24 hours. Domain verification with GitHub's account-specific TXT record is recommended for takeover protection; obtain the exact generated token through account settings rather than guessing it.
