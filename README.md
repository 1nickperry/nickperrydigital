# Nick Perry Digital

Static website for [nickperrydigital.com](https://nickperrydigital.com). Nick Perry's practice for websites and local SEO on Colorado's Western Slope.

The site is plain HTML and CSS. Tailwind compiles to `assets/css/site.css`. A small Node script turns markdown and JSON in `content/` into HTML at the repository root. Hostinger can serve that HTML with no build step on the server. Built files are committed.

## Pages

- Home, About, Pricing, Results, Services, Contact
- Service pages, including AI search optimization
- Results hub and placeholder case studies
- Locations hub and a landing page for each Western Slope town (cost section and FAQ with FAQPage schema)
- Blog, Privacy, Terms

Towns: Grand Junction, Fruita, Palisade, Clifton, Redlands, Montrose, Delta, Rifle, Glenwood Springs, Carbondale, Basalt, Aspen, Durango.

Top navigation: wordmark (home), About, Pricing, Results, Services, Contact, click-to-call phone.

Footer: Ready to grow band, then Company, Services, Our work, and Areas we serve, then Privacy and Terms.

## Offer

- Website build: $1,000 (SEO-ready site, Google Business Profile setup, 90 days of SEO)
- GBP + Website: $850 per month
- GBP + Website + AI Search: $1,500 per month
- Add-ons (Google Ads management, a larger site, logo and branding): custom quote
- Care plan: $150 per month, optional
- No long-term contract
- Call to action: Book a Free Strategy Call

Prices and the guarantee list live in `content/settings.json`.

## Local commands

```bash
npm install
npm run build
npm run dev
```

`npm run dev` rebuilds the site and serves it at http://localhost:4173.

`npm run build` compiles CSS, renders HTML, writes `sitemap.xml` and `robots.txt`, and checks the output.

## Editing content

Content lives in `content/`:

| Path | What it is |
| --- | --- |
| `content/settings.json` | Phone, email, booking link, form endpoint, prices, guarantees |
| `content/home.json` | Home page copy |
| `content/pages/` | About, contact, services intro, locations intro, results intro, privacy, terms |
| `content/services/` | One JSON file per service |
| `content/locations/` | One JSON file per town |
| `content/case-studies/` | Case studies |
| `content/blog/` | Markdown posts |

After you edit, run `npm run build` and commit the HTML as well as the content. The live site serves the HTML, not the JSON.

### Decap CMS

Open `/admin/` on the site (or http://localhost:4173/admin/ locally). The config is `admin/config.yml`.

Decap commits to GitHub. It does not compile HTML. After a content commit lands on `main`, the GitHub Action in `.github/workflows/build.yml` runs `npm run build` and pushes the HTML with `[skip ci]`. Hostinger then deploys that commit. You can also build on your own machine and push.

`local_backend: true` is set. For local editing without GitHub login:

```bash
npx decap-server
npm run dev
```

Run those in two terminals. Open the local `/admin/` URL. `decap-server` is only for your computer.

### GitHub OAuth (required for /admin on the live domain)

Decap's GitHub backend cannot complete OAuth from a static host. GitHub will not accept `https://nickperrydigital.com/admin/` as the OAuth client by itself. You need a small proxy that holds the client secret. Hostinger's static Git deploy cannot run that proxy.

1. Create a GitHub OAuth App: GitHub, Settings, Developer settings, OAuth Apps, New OAuth App.
2. Homepage URL: `https://nickperrydigital.com`.
3. Authorization callback URL: `https://YOUR-PROXY-DOMAIN/callback`.
4. Deploy an OAuth proxy you control. A common choice is the open-source provider at [decap-cms-github-oauth-provider](https://github.com/decaporg/decap-cms-github-oauth-provider) on a small Node host, a VPS, or a Cloudflare Worker port of the same flow. Set `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, and the origin `https://nickperrydigital.com`.
5. Put that proxy origin in `admin/config.yml` as `backend.base_url`. `auth_endpoint` stays `auth`. The repo is `1nickperry/nickperrydigital` and the branch is `main`.
6. The GitHub user who logs in needs write access to the repo.
7. The placeholder `https://oauth-proxy.example.com` will not log anyone in. Replace it before you use `/admin` in production.

Do not use a public shared OAuth proxy. That would put the repo token in someone else's hands.

Git Gateway is a Netlify feature. It does not apply on Hostinger.

## Portrait

Home and About use `assets/img/nick-perry.png` and, when present, `assets/img/nick-perry.webp`. The build writes the WebP (max width 1200, quality 74) from the PNG. If the PNG is missing, the layout shows a marked monogram instead of a fake photo.

## Placeholders

These are intentional until real values exist. The footer says so.

| Item | Current value | Where to change it |
| --- | --- | --- |
| Phone | `555-010-0190` (`+15550100190`) | `content/settings.json` `phoneDisplay` and `phoneTel` |
| Email | `hello@nickperrydigital.com` | `content/settings.json` `email` |
| Booking URL | empty | `content/settings.json` `bookingUrl` (https calendar link) |
| Form endpoint | empty | `content/settings.json` `formEndpoint` (for example a Formspree URL) |
| Case studies | three pages badged Placeholder | `content/case-studies/` |
| Press, quotes, client logos | empty states, no fake marks | `content/home.json` |

`555-010-0190` is in the reserved fictional range. It is not a working business line.

When `bookingUrl` is a normal https link, Contact embeds it in an iframe. When `formEndpoint` is set, the form posts there. Until then, submit shows a placeholder note instead of pretending the message was sent.

## Deploy on Hostinger with Git

The document root is this repository. `index.html`, `assets/`, and `admin/` sit at the root. Do not set a server build command. The CSS and HTML are already built.

1. In hPanel, open the hosting plan for nickperrydigital.com and go to Git.
2. Connect the GitHub repository `1nickperry/nickperrydigital`.
3. Branch: `main`.
4. Directory: the domain's `public_html` (the site root), not a nested app folder.
5. Leave any remote build or Node start command off. This is a static site.
6. Turn on auto-deploy so a push to `main` updates the site.
7. Point the domain's DNS at this hosting plan if it is not already.

Flow after launch: edit in Decap (or in git), the Action commits fresh HTML, Hostinger pulls `main`. The first deploy after a content edit can lag by one commit, because Decap commits the source and the Action commits the HTML right after.

`/admin/` is on the site but will not authenticate until the OAuth proxy in `admin/config.yml` is real. `robots.txt` disallows `/admin/`.

## Schema and files for search

- `ProfessionalService` JSON-LD on every page (name, area served, offers)
- `FAQPage` on each town page and each service page
- `BlogPosting` on posts
- `sitemap.xml` and `robots.txt` at the root
- Unique title and meta description per page
