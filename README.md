# Nick Perry Digital

Static HTML site for [nickperrydigital.com](https://nickperrydigital.com): Tailwind utilities, a custom Signal Dot design system, and Decap CMS. Built to deploy on Hostinger via Git (no server build step). The HTML in this repo is the live site.

## Stack

- Static HTML pages (pretty URLs as folders with `index.html`)
- Tailwind Play CDN plus `assets/css/site.css`
- Decap CMS at `/admin/`
- Placeholders for phone, booking link, and case studies in `content/settings.json`

## Local preview

```bash
python3 -m http.server 8080
```

Open http://localhost:8080

Regenerate pages after copy changes:

```bash
python3 scripts/build_site.py
```

## Decap CMS

1. Open `/admin/`
2. For local edits, run `npx decap-server` and keep `local_backend: true` in `admin/config.yml`
3. For production, connect the GitHub backend (`1nickperry/nickperrydigital`, branch `main`) with a GitHub OAuth app
4. Replace `[PHONE NUMBER]`, `[BOOKING LINK]`, and `[CONTACT EMAIL]` in **Site settings**

Hostinger Git auto-deploy should point at `main` after this branch is merged. Do not deploy until Nick is ready.

## Pricing (published)

- Website: $1,000
- GBP + Website: $850 / month
- GBP + Website + AI Search: $1,500 / month
- Care plan: $150 / month
