# DNS — roamsystems.co.uk (canonical inventory)

Captured 2026-06-12 via public DNS queries. The zone is hosted on Cloudflare
nameservers (`aldo.ns.cloudflare.com` / `haley.ns.cloudflare.com`) in a
Cloudflare account controlled by **Identity Pixel Design Ltd**
(spencer@identitypixel.com) — not the owner's account. Domain registration is
in the owner's GoDaddy account (customer no. 296089358, transferred from
Identity Pixel 2026-03-13).

All records are currently **DNS only (grey cloud)** — no Cloudflare proxying,
so Cloudflare redirect rules cannot fire until the apex is proxied.

## Records (public, verified)

| Name | Type | Value | Purpose |
|---|---|---|---|
| `roamsystems.co.uk` | A | `69.46.46.116` | Website apex → Railway static IP |
| `www` | CNAME | `cc10v6rc.up.railway.app` | Website www → Railway |
| `roamsystems.co.uk` | MX 0 | `roamsystems-co-uk.mail.protection.outlook.com` | Microsoft 365 email (sales@) |
| `roamsystems.co.uk` | TXT | `v=spf1 include:secureserver.net include:spf.protection.outlook.com ~all` | SPF |
| `roamsystems.co.uk` | TXT | `google-site-verification=FtmeIqon92vW2RJpLJuBtc1sUiJqd7fCx7-SeFFiKMA` | **Google Search Console domain-property verification — do not lose** |
| `roamsystems.co.uk` | TXT | `MS=ms23241555` | Microsoft 365 domain verification |
| `_dmarc` | TXT | `v=DMARC1; p=quarantine; rua=mailto:dmarc@roamsystems.co.uk` | DMARC |
| `autodiscover` | CNAME | `autodiscover.outlook.com` | M365 Outlook autodiscover |
| `enterpriseregistration` | CNAME | `enterpriseregistration.windows.net` | M365 device registration |
| `enterpriseenrollment` | CNAME | `enterpriseenrollment-s.manage.microsoft.com` | M365 device enrolment |
| `resend._domainkey` | TXT | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUSs47AntVp8JxcHvVdmn7qEpzGiduQXEkKiLcD0Gv2o44zpzGdhXxMOqy2qEwgGr1HI7rJ/MvAvGlRXvNEwOJ/ICsNhevDWVOmnchvaqlOwQw/g0HlrCU6TJslVKSLABRTSxAZ3CS7nohuTpagPNf7Ic2pcbbheBuBwfu3ZvMmQIDAQAB` | Resend DKIM (order-confirmation emails) |
| `send` | TXT | `v=spf1 include:amazonses.com ~all` | Resend SPF |
| `send` | MX 10 | `feedback-smtp.eu-west-1.amazonses.com` | Resend bounce handling |

Notes:
- `selector1/selector2._domainkey` (M365 DKIM) are **not** configured — not an
  error, just not set up.
- Public queries cannot enumerate unknown subdomains; if the zone is ever
  migrated, also rely on Cloudflare's import scan and verify email + checkout
  immediately after cutover.

## Open task this inventory supports

Non-www → www 301 redirect (SEO audit Task 2 remainder). Two routes:
1. Identity Pixel makes the change in their Cloudflare account: apex record →
   Proxied, SSL/TLS mode → Full, redirect rule `roamsystems.co.uk/*` → 301
   `https://www.roamsystems.co.uk/$1` (or "Redirect from Root to WWW" template).
2. Owner migrates the zone to their own Cloudflare account (registrar is
   theirs at GoDaddy): add zone → replicate the records above → switch
   nameservers at GoDaddy → then apply the proxy + rule as in (1).
