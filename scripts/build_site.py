#!/usr/bin/env python3
"""Generate the Nick Perry Digital static site."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = []

PHONE = "[PHONE NUMBER]"
BOOKING = "[BOOKING LINK]"
SITE = "Nick Perry Digital"


def rel(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def asset(depth: int, path: str) -> str:
    return f"{rel(depth)}{path}"


def hero_src(depth: int, key: str) -> tuple[str, str]:
    names = {
        "rings": "hero-01-signal-rings",
        "ivory": "hero-02-ivory-mark",
        "grid": "hero-03-dot-grid",
        "split": "hero-04-split-layout",
        "orbit": "hero-05-orbit",
    }
    stem = names[key]
    return (
        asset(depth, f"assets/images/hero/{stem}-1440x900.png"),
        asset(depth, f"assets/images/hero/{stem}-2560x1440.png"),
    )


def nav_items(depth: int, current: str) -> list[tuple[str, str, str]]:
    r = rel(depth)
    return [
        ("Home", f"{r}index.html", "home"),
        ("About", f"{r}about/", "about"),
        ("Pricing", f"{r}pricing/", "pricing"),
        ("Results", f"{r}results/", "results"),
        ("Services", f"{r}services/", "services"),
        ("Contact", f"{r}contact/", "contact"),
    ]


def header(depth: int, current: str) -> str:
    r = rel(depth)
    links = []
    mobile = []
    for label, href, key in nav_items(depth, current):
        current_attr = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
        mobile.append(f'<a href="{href}"{current_attr}>{label}</a>')
    phone = (
        f'<a class="phone-link" href="#phone-placeholder" data-phone-href data-phone-display>{PHONE}</a>'
    )
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-nav>
  <div class="wrap header-inner">
    <a class="logo" href="{r}index.html"><img src="{asset(depth, "assets/images/logo/horizontal-dark.svg")}" alt="Nick Perry Digital" width="220" height="60"></a>
    <nav class="nav-desktop" aria-label="Primary">
      {"".join(links[1:])}
      {phone}
    </nav>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <nav class="nav-drawer" data-nav-drawer aria-label="Mobile">
    {"".join(mobile)}
    {phone}
  </nav>
</header>
"""


def footer(depth: int) -> str:
    r = rel(depth)
    company = [
        ("About", f"{r}about/"),
        ("Pricing", f"{r}pricing/"),
        ("Nick Perry", f"{r}nick-perry/"),
        ("Results", f"{r}results/"),
        ("Insights", f"{r}insights/"),
        ("Awards", f"{r}awards/"),
        ("Contact", f"{r}contact/"),
    ]
    services = [
        ("Brand Identity & Style Guide", f"{r}services/brand-creation/"),
        ("Web Design & Development", f"{r}services/web-design/"),
        ("Local SEO", f"{r}services/local-seo/"),
        ("Google Business Profile", f"{r}services/google-business-profile/"),
        ("Google Ads (PPC)", f"{r}services/google-ads/"),
        ("Reputation Management", f"{r}services/reputation-management/"),
        ("WordPress Care & Hosting", f"{r}services/website-maintenance/"),
        ("Lead Generation", f"{r}services/lead-generation/"),
    ]
    work = [
        ("All Results", f"{r}results/"),
        ("Case study placeholder 01", f"{r}case-studies/placeholder-01-local-service/"),
        ("Case study placeholder 02", f"{r}case-studies/placeholder-02-professional/"),
        ("Case study placeholder 03", f"{r}case-studies/placeholder-03-home-services/"),
        ("Case study placeholder 04", f"{r}case-studies/placeholder-04-hospitality/"),
        ("Dispensary SEO", f"{r}case-studies/dispensary-seo/"),
        ("Best SEO Companies in Grand Junction", f"{r}best-seo-company-grand-junction/"),
    ]
    areas = [
        ("Grand Junction", f"{r}locations/grand-junction/"),
        ("Fruita", f"{r}locations/fruita/"),
        ("Palisade", f"{r}locations/palisade/"),
        ("Clifton", f"{r}locations/clifton/"),
        ("Redlands", f"{r}locations/redlands/"),
        ("Montrose", f"{r}locations/montrose/"),
        ("Delta", f"{r}locations/delta/"),
        ("Olathe", f"{r}locations/olathe/"),
        ("Cedaredge", f"{r}locations/cedaredge/"),
        ("Paonia", f"{r}locations/paonia/"),
        ("Rifle", f"{r}locations/rifle/"),
        ("Glenwood Springs", f"{r}locations/glenwood-springs/"),
        ("Carbondale", f"{r}locations/carbondale/"),
        ("Basalt", f"{r}locations/basalt/"),
        ("Aspen", f"{r}locations/aspen/"),
        ("Durango", f"{r}locations/durango/"),
    ]

    def col(title: str, items: list[tuple[str, str]]) -> str:
        lis = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in items)
        return f"<div><h3>{title}</h3><ul>{lis}</ul></div>"

    return f"""
<section class="cta-band">
  <div class="wrap">
    <p class="kicker">Next step</p>
    <h2>Ready to Grow?</h2>
    <p>Book a free strategy call. Thirty minutes, no long-term contract, and a clear next step whether we work together or not.</p>
    <div class="actions" style="justify-content:center">
      <a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>{BOOKING}</a>
      <a class="btn-secondary" href="#phone-placeholder" data-phone-href data-phone-display>{PHONE}</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap footer-grid">
    {col("Company", company)}
    {col("Services", services)}
    {col("Our Work", work)}
    {col("Areas We Serve", areas)}
  </div>
  <div class="wrap legal">
    <p>© <span data-year></span> Nick Perry Digital. Western Slope web design and local SEO.</p>
    <p><a href="{r}privacy-policy/">Privacy Policy</a> · <a href="{r}terms-of-service/">Terms of Service</a></p>
  </div>
</footer>
"""


def page(
    *,
    out: str,
    title: str,
    description: str,
    keyword: str,
    depth: int,
    current: str,
    body: str,
    canonical: str,
    schema: str = "",
) -> None:
    r = rel(depth)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keyword}">
  <link rel="canonical" href="https://nickperrydigital.com{canonical}">
  <link rel="icon" href="{asset(depth, "favicon-32.png")}" type="image/png">
  <link rel="apple-touch-icon" href="{asset(depth, "apple-touch-icon.png")}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      corePlugins: {{ preflight: false }},
      theme: {{
        extend: {{
          colors: {{
            navy: {{ DEFAULT: "#1B2A4A", deep: "#0F1A30" }},
            ivory: "#F5F3EE",
            gold: "#C9A44C"
          }},
          fontFamily: {{
            display: ["Fraunces", "serif"],
            sans: ["Outfit", "system-ui", "sans-serif"]
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="{asset(depth, "assets/css/site.css")}">
  {schema}
</head>
<body data-root="{r.rstrip("/") or "."}">
  {header(depth, current)}
  <main id="main">
    {body}
  </main>
  {footer(depth)}
  <script src="{asset(depth, "assets/js/site.js")}"></script>
</body>
</html>
"""
    if "—" in html or "–" in html:
        raise SystemExit(f"Em/en dash found in {out}")
    dest = ROOT / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    PAGES.append(
        {
            "file": out,
            "slug": canonical,
            "title": title,
            "keyword": keyword,
        }
    )


def hero(depth: int, key: str, eyebrow: str, heading: str, lede: str) -> str:
    src, src2 = hero_src(depth, key)
    return f"""
<section class="hero">
  <div class="hero-media">
    <img src="{src}" srcset="{src} 1440w, {src2} 2560w" sizes="100vw" alt="" width="1440" height="900">
    <div class="hero-shade"></div>
  </div>
  <div class="wrap hero-copy">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{heading}</h1>
    <p>{lede}</p>
    <div class="actions">
      <a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>{BOOKING}</a>
      <a class="btn-secondary" href="{rel(depth)}pricing/">See pricing</a>
    </div>
  </div>
</section>
"""


def as_seen_in() -> str:
    slots = "".join(
        f'<div class="logo-slot"><span class="placeholder-label">Placeholder</span><br>Publication logo {i}</div>'
        for i in range(1, 5)
    )
    return f"""
<section class="section section-white">
  <div class="wrap">
    <p class="kicker">As Seen In</p>
    <h2>Press and mention slots</h2>
    <p class="muted">Logos will be added when there is a real placement to show. Nothing here is invented.</p>
    <div class="logo-row" style="margin-top:24px">{slots}</div>
  </div>
</section>
"""


def testimonials() -> str:
    cards = []
    for i, topic in enumerate(["Local service", "Professional firm", "Home services"], 1):
        cards.append(
            f"""
            <article class="placeholder-card">
              <span class="placeholder-label">Testimonial placeholder {i}</span>
              <p>A real quote from a {topic.lower()} client will go here once the work is published and the client agrees to be named.</p>
              <p class="muted">Attribution placeholder. Name and business withheld until a case study is ready.</p>
            </article>
            """
        )
    return f"""
<section class="section section-ivory">
  <div class="wrap">
    <p class="kicker">Words of Praise</p>
    <h2>Client comments, when they exist</h2>
    <p class="muted">This site does not invent reviews. These cards stay marked until real words are on file.</p>
    <div class="grid-3" style="margin-top:28px">{"".join(cards)}</div>
  </div>
</section>
"""


def trusted_by() -> str:
    slots = "".join(
        f'<div class="logo-slot"><span class="placeholder-label">Placeholder</span><br>Client mark {i}</div>'
        for i in range(1, 5)
    )
    return f"""
<section class="section section-white">
  <div class="wrap">
    <p class="kicker">Trusted By</p>
    <h2>Client marks, coming later</h2>
    <p class="muted">No client names are listed until those projects are ready to publish.</p>
    <div class="trust-row" style="margin-top:24px">{slots}</div>
  </div>
</section>
"""


def featured_work(depth: int) -> str:
    r = rel(depth)
    items = [
        ("Local service business", f"{r}case-studies/placeholder-01-local-service/"),
        ("Professional services", f"{r}case-studies/placeholder-02-professional/"),
        ("Home services", f"{r}case-studies/placeholder-03-home-services/"),
        ("Hospitality", f"{r}case-studies/placeholder-04-hospitality/"),
    ]
    cards = "".join(
        f"""<article class="work-card placeholder-card"><span class="placeholder-label">Case study placeholder</span><h3>{title}</h3><p class="muted">Outcome, industry, and screenshots will be added when this project is cleared to publish.</p><a href="{href}">Open placeholder</a></article>"""
        for title, href in items
    )
    return f"""
<section class="section section-ivory">
  <div class="wrap">
    <p class="kicker">Featured Work</p>
    <h2>Portfolio tiles reserved</h2>
    <div class="grid-4" style="margin-top:28px">{cards}</div>
  </div>
</section>
"""


def faq_block(items: list[tuple[str, str]]) -> str:
    rows = []
    for i, (q, a) in enumerate(items, 1):
        rows.append(
            f"""
            <div class="faq-item">
              <button class="faq-q" type="button" aria-expanded="false" aria-controls="faq-{i}">{q}</button>
              <div class="faq-a" id="faq-{i}"><p>{a}</p></div>
            </div>
            """
        )
    return f'<section class="section section-white"><div class="wrap prose"><p class="kicker">Questions</p><h2>FAQ</h2><div data-accordion>{"".join(rows)}</div></div></section>'


def faq_schema(items: list[tuple[str, str]]) -> str:
    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in items
    ]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def local_schema() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Nick Perry Digital",
        "url": "https://nickperrydigital.com/",
        "image": "https://nickperrydigital.com/assets/images/logo/icon-light-512.png",
        "priceRange": "$$",
        "areaServed": [
            "Grand Junction CO",
            "Fruita CO",
            "Palisade CO",
            "Montrose CO",
            "Western Slope Colorado",
        ],
        "description": "Web design and local SEO for businesses on Colorado's Western Slope.",
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def service_cards(depth: int) -> str:
    r = rel(depth)
    items = [
        ("01", "Brand Creation", "Logos, color, type, and a short style guide so the site, trucks, and ads match.", f"{r}services/brand-creation/"),
        ("02", "Web Design & Development", "Fast sites built to be found and to make the next call obvious.", f"{r}services/web-design/"),
        ("03", "Local SEO", "Service pages, citations, and internal links for the towns you actually cover.", f"{r}services/local-seo/"),
        ("04", "Google Business Profile", "Categories, photos, posts, and a review rhythm that supports the map pack.", f"{r}services/google-business-profile/"),
        ("05", "Google Ads", "Search campaigns aimed at calls and form fills, not vanity clicks.", f"{r}services/google-ads/"),
        ("06", "SEO (Organic)", "Technical cleanup and content that grows beyond the map pack.", f"{r}services/seo/"),
        ("07", "Reputation Management", "A simple ask-and-respond system so reviews stay current.", f"{r}services/reputation-management/"),
        ("08", "Conversion Rate Optimization", "Clearer pages and forms so the traffic you already have works harder.", f"{r}services/conversion-rate-optimization/"),
        ("09", "WordPress Care & Hosting", "Updates, backups, and edits for $150 a month.", f"{r}services/website-maintenance/"),
        ("10", "Lead Generation", "Offers, tracking, and follow-up that turn visits into booked work.", f"{r}services/lead-generation/"),
    ]
    cards = "".join(
        f'<article class="service-card"><p class="service-num">{n}</p><h3>{t}</h3><p class="muted">{d}</p><p><a href="{h}">Learn more</a></p></article>'
        for n, t, d, h in items
    )
    return f'<div class="grid-2">{cards}</div>'


def proven_results(depth: int) -> str:
    r = rel(depth)
    return f"""
<section class="section section-navy">
  <div class="wrap">
    <p class="kicker">Proven Results</p>
    <h2>Case studies will live here</h2>
    <p>Until a project is cleared to publish, these cards stay labeled as placeholders. No stats, names, or screenshots are invented.</p>
    <div class="grid-2" style="margin-top:28px">
      <article class="placeholder-card">
        <span class="placeholder-label">Case study placeholder</span>
        <h3>Local service visibility</h3>
        <p>Headline, metric, and story reserved. <a href="{r}case-studies/placeholder-01-local-service/">View slot</a></p>
      </article>
      <article class="placeholder-card">
        <span class="placeholder-label">Case study placeholder</span>
        <h3>Lead flow for a home-service firm</h3>
        <p>Headline, metric, and story reserved. <a href="{r}case-studies/placeholder-03-home-services/">View slot</a></p>
      </article>
    </div>
  </div>
</section>
"""


def build_home() -> None:
    d = 0
    body = f"""
    {hero(d, "rings", "Grand Junction and the Western Slope", "Websites and local SEO that win you customers", "Nick Perry Digital builds sites and runs local search for businesses across the Grand Valley and the Western Slope. Published pricing. Month to month. A free strategy call to start.")}
    {as_seen_in()}
    <section class="section section-ivory">
      <div class="wrap split">
        <div>
          <p class="kicker">The person doing the work</p>
          <h2>A Western Slope web design and SEO practice</h2>
          <p class="muted">Most local businesses need three things from the web: show up when someone searches, look trustworthy when they click, and make it easy to call. That is the whole job.</p>
          <p class="muted">This practice covers the site itself and the search work behind it: Google Search, Google Maps, and the AI tools people now ask for recommendations. No invented years-in-business claim. No borrowed awards. Just the offer, in writing.</p>
          <div class="actions">
            <a class="btn-ghost" href="about/">About Nick</a>
            <a class="btn-ghost" href="nick-perry/">Bio page</a>
          </div>
        </div>
        <figure class="portrait">
          <img src="assets/images/nick/me-but-stencil.png" alt="Line portrait of Nick Perry" width="800" height="1000">
        </figure>
      </div>
    </section>
    <section class="section section-white">
      <div class="wrap">
        <p class="kicker">What we do</p>
        <h2>Services built for local operators</h2>
        {service_cards(d)}
      </div>
    </section>
    {proven_results(d)}
    {testimonials()}
    {trusted_by()}
    {featured_work(d)}
    """
    page(
        out="index.html",
        title="Grand Junction Web Design & SEO | Nick Perry Digital",
        description="Web design and local SEO for Grand Junction and the Western Slope. $1,000 websites, month-to-month SEO plans, and a free strategy call.",
        keyword="grand junction web design",
        depth=d,
        current="home",
        body=body,
        canonical="/",
        schema=local_schema(),
    )


def build_about() -> None:
    d = 1
    body = f"""
    {hero(d, "ivory", "About", "About Nick Perry Digital", "A web design and local SEO practice for Grand Junction, the Grand Valley, and the Western Slope. Clear scope, short sprints, and results you can see in the call log.")}
    <section class="section section-ivory">
      <div class="wrap split">
        <div class="prose">
          <h2>Why this market</h2>
          <p>Western Slope search does not behave like Denver search. People will drive from Fruita to Palisade for the right shop. They lean on Maps and reviews. A site that only talks to a national template misses how this valley actually buys.</p>
          <p>Nick Perry Digital is built for that pattern: one person you can reach, published prices, and work you own from day one.</p>
        </div>
        <figure class="portrait">
          <img src="{asset(d, "assets/images/nick/me-but-stencil.png")}" alt="Line portrait of Nick Perry" width="800" height="1000">
        </figure>
      </div>
    </section>
    <section class="section section-white">
      <div class="wrap prose">
        <h2>What we do</h2>
        <ul>
          <li>Web design: mobile-first sites that load on a weak signal and make the next call obvious.</li>
          <li>Local SEO and Google Business Profile: structure, content, citations, and a tuned profile for the map pack and AI search.</li>
          <li>Google Ads: campaigns measured against leads, not clicks.</li>
          <li>Reviews and reputation: a steady ask and a plan for responding.</li>
        </ul>
        <h2>How we work</h2>
        <ul>
          <li>Plan: short discovery, a local keyword map, site structure, and tracking.</li>
          <li>Build: the website, the profile, the tracking, and the review flow, launched together.</li>
          <li>Grow: local links that matter, regular updates, and changes based on real numbers.</li>
        </ul>
        <p>You own the domain, hosting, website, Analytics, Search Console, Tag Manager, and ad accounts. Month to month after launch.</p>
      </div>
    </section>
    <section class="section section-ivory">
      <div class="wrap">
        <h2>Local work</h2>
        <p class="muted">Published case studies will be linked here. Until then, the Results page holds labeled placeholders only.</p>
        <p><a href="{rel(d)}results/">See the Results page</a></p>
      </div>
    </section>
    <section class="section section-white">
      <div class="wrap">
        <h2>What sets this practice apart</h2>
        <div class="grid-2">
          <article class="card"><h3>Local and reachable</h3><p class="muted">One point of contact, weekly check-ins, and a call you can book without a sales ladder.</p></article>
          <article class="card"><h3>Built to convert</h3><p class="muted">Service pages, trust blocks, and clean calls to action, judged by leads rather than vanity traffic.</p></article>
          <article class="card"><h3>Ownership</h3><p class="muted">Admin access from day one and a live dashboard for calls and forms.</p></article>
          <article class="card"><h3>Low risk</h3><p class="muted">Fixed-scope build, month-to-month SEO, and a satisfaction guarantee on the work.</p></article>
        </div>
      </div>
    </section>
    """
    page(
        out="about/index.html",
        title="About Nick Perry Digital | Grand Junction Web Design & SEO",
        description="About Nick Perry Digital, a Western Slope web design and local SEO practice with published pricing and month-to-month work.",
        keyword="about nick perry digital",
        depth=d,
        current="about",
        body=body,
        canonical="/about/",
    )


def build_nick() -> None:
    d = 1
    body = f"""
    {hero(d, "ivory", "People", "Nick Perry", "The person behind Nick Perry Digital. Web design and local SEO for Grand Junction and the Western Slope.")}
    <section class="section section-ivory">
      <div class="wrap split">
        <figure class="portrait">
          <img src="{asset(d, "assets/images/nick/me-but-stencil.png")}" alt="Line portrait of Nick Perry" width="800" height="1000">
        </figure>
        <div class="prose">
          <h2>Bio</h2>
          <p>Nick Perry runs Nick Perry Digital. This page is the founder bio. It does not invent a resume, a founding year, or awards. Those details will be added when Nick publishes them.</p>
          <p>The work is websites, local SEO, Google Business Profile care, and paid search for businesses that want more of the right calls. Pricing is public. The first strategy call is free.</p>
          <p>If you want the practice story rather than the person page, start on <a href="{rel(d)}about/">About</a>.</p>
          <div class="actions">
            <a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>{BOOKING}</a>
          </div>
        </div>
      </div>
    </section>
    """
    page(
        out="nick-perry/index.html",
        title="Nick Perry | Founder, Nick Perry Digital",
        description="Bio page for Nick Perry, the founder of Nick Perry Digital.",
        keyword="nick perry digital founder",
        depth=d,
        current="about",
        body=body,
        canonical="/nick-perry/",
    )


def build_pricing() -> None:
    d = 1
    faqs = [
        ("What does the website build include?", "A $1,000 local site with SEO-minded structure and Google Business Profile setup help. Larger or custom builds get a fixed quote after the strategy call."),
        ("Are the monthly plans under contract?", "No. Both SEO plans are month to month."),
        ("What is the care plan?", "$150 a month for hosting, security, updates, and routine edits. Ask about free hosting on eligible static builds."),
        ("How fast should results show?", "Map pack movement often starts in 30 to 90 days. Organic rankings take longer. Weekly check-ins and a plain-English monthly report keep the work visible."),
    ]
    body = f"""
    {hero(d, "grid", "Pricing", "Simple pricing for Western Slope businesses", "Show up, stand out, and turn searchers into customers. Straightforward numbers. No long-term contracts.")}
    <section class="section section-ivory">
      <div class="wrap">
        <p class="muted">Monthly plans can be added to a new site or an existing one.</p>
        <div class="grid-3">
          <article class="price-card">
            <p class="kicker">Website</p>
            <p class="price">$1,000 <span>one-time</span></p>
            <p>A one-time website build. Clear services, click-to-call, and a structure search can understand. Includes Google Business Profile setup help.</p>
            <p class="muted">Best for: businesses that need a site they own, not a locked template.</p>
            <div class="actions"><a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>Book a call</a></div>
          </article>
          <article class="price-card">
            <p class="kicker">Local SEO</p>
            <p class="price">$850 <span>per month</span></p>
            <p>A monthly growth plan covering Google Business Profile management and ongoing website SEO.</p>
            <p class="muted">Best for: every local service business that needs Maps and the site working together.</p>
            <div class="actions"><a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>Book a call</a></div>
          </article>
          <article class="price-card">
            <p class="kicker">Local SEO + AI Search</p>
            <p class="price">$1,500 <span>per month</span></p>
            <p>Everything in Local SEO, plus AI search optimization (AEO/GEO), AI visibility reporting, and local link and PR outreach.</p>
            <p class="muted">Best for: businesses that want Google and AI answers before competitors catch up.</p>
            <div class="actions"><a class="btn" href="#booking-placeholder" data-booking-href data-booking-label>Book a call</a></div>
          </article>
        </div>
      </div>
    </section>
    <section class="section section-white">
      <div class="wrap">
        <h2>What is in each monthly plan</h2>
        <div class="table-scroll" style="overflow:auto">
        <table class="feature-table">
          <thead><tr><th>Feature</th><th>GBP + Website</th><th>Plus AI Search</th></tr></thead>
          <tbody>
            <tr><td colspan="3"><strong>One-time setup</strong></td></tr>
            <tr><td>Google Business Profile setup and optimization</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Review request setup</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Local Service Ads setup (when eligible)</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Business citations setup</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Website audit and competitor review</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>AI visibility audit</td><td></td><td class="check">Yes</td></tr>
            <tr><td colspan="3"><strong>Monthly service</strong></td></tr>
            <tr><td>Google Business Profile management</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Weekly Google posts</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Review strategy and spam fighting</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>On-site SEO and content</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Monthly plain-English report</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>Weekly check-ins</td><td class="check">Yes</td><td class="check">Yes</td></tr>
            <tr><td>AI search optimization (AEO / GEO)</td><td></td><td class="check">Yes</td></tr>
            <tr><td>AI visibility monitoring</td><td></td><td class="check">Yes</td></tr>
            <tr><td>Local link and PR outreach*</td><td></td><td class="check">Yes</td></tr>
          </tbody>
        </table>
        </div>
        <p class="muted">* Outreach is included. Placement fees charged by a publisher or event are billed separately.</p>
      </div>
    </section>
    <section class="section section-ivory">
      <div class="wrap">
        <h2>Add-ons</h2>
        <div class="grid-3">
          <article class="card"><h3>Google Ads management</h3><p class="muted">Custom quote based on the account and ad spend.</p></article>
          <article class="card"><h3>Website design and development</h3><p class="muted">$1,000 for a standard local build. Custom quotes for larger work.</p></article>
          <article class="card"><h3>Logo and branding</h3><p class="muted">Custom quote for identity, style guide, and print files.</p></article>
        </div>
        <p style="margin-top:28px">Care plan: $150 a month for hosting, security, updates, and edits. Ask about free hosting.</p>
      </div>
    </section>
    {faq_block(faqs)}
    """
    page(
        out="pricing/index.html",
        title="Web Design & SEO Pricing | Grand Junction, CO | Nick Perry Digital",
        description="Published pricing: $1,000 websites, $850 and $1,500 monthly SEO plans, and a $150 care plan. No long-term contracts.",
        keyword="grand junction seo pricing",
        depth=d,
        current="pricing",
        body=body,
        canonical="/pricing/",
        schema=faq_schema(faqs),
    )


def build_results() -> None:
    d = 1
    cards = [
        ("placeholder-01-local-service", "Local service visibility", "Local services"),
        ("placeholder-02-professional", "Professional services search", "Professional"),
        ("placeholder-03-home-services", "Home-service lead flow", "Home services"),
        ("placeholder-04-hospitality", "Hospitality and food", "Hospitality"),
        ("dispensary-seo", "Dispensary SEO notes", "Cannabis retail"),
        ("placeholder-05-ecommerce", "Retail and ecommerce", "Retail"),
    ]
    grid = "".join(
        f'<article class="placeholder-card"><span class="placeholder-label">Case study placeholder</span><h3>{title}</h3><p class="muted">Industry: {ind}. No metric is shown because no result has been published yet.</p><p><a href="{rel(d)}case-studies/{slug}/">Open placeholder</a></p></article>'
        for slug, title, ind in cards
    )
    body = f"""
    {hero(d, "grid", "Results", "Work, once it is ready to show", "This page will hold published case studies. Until then every tile is a reserved slot. No names, screenshots, or numbers are invented.")}
    <section class="section section-ivory">
      <div class="wrap">
        <div class="grid-2">{grid}</div>
      </div>
    </section>
    """
    page(
        out="results/index.html",
        title="Results | Nick Perry Digital Case Studies",
        description="Reserved case study slots for Nick Perry Digital. Published results will appear here when clients clear them.",
        keyword="nick perry digital results",
        depth=d,
        current="results",
        body=body,
        canonical="/results/",
    )


def build_services_hub() -> None:
    d = 1
    body = f"""
    {hero(d, "split", "Services", "Services", "Websites that look right, load fast, and turn visitors into leads. Then the search work: local SEO, a tuned Google Business Profile, ads, and care.")}
    <section class="section section-ivory">
      <div class="wrap">
        <p class="muted">If you run a home-service or local business on the Western Slope, this stack is built for you.</p>
        {service_cards(d)}
        <p style="margin-top:28px"><a href="{rel(d)}services/ai-search-optimization/">Also: AI Search Optimization</a></p>
      </div>
    </section>
    """
    page(
        out="services/index.html",
        title="Services | Nick Perry Digital",
        description="Web design, local SEO, Google Business Profile, ads, reputation, CRO, care, and lead generation for Western Slope businesses.",
        keyword="grand junction digital marketing services",
        depth=d,
        current="services",
        body=body,
        canonical="/services/",
    )


def build_contact() -> None:
    d = 1
    body = f"""
    {hero(d, "orbit", "Contact", "Contact", "Call, write, or book a free strategy call. If you are nearby, the call can be in person at a local coffee shop instead of a video link.")}
    <section class="section section-ivory">
      <div class="wrap grid-2">
        <div>
          <h2>Let's Get Started</h2>
          <p>Call <a href="#phone-placeholder" data-phone-href data-phone-display>{PHONE}</a> now.</p>
          <p>You can also send a message or schedule a meeting with the booking placeholder below.</p>
          <p class="note">Booking calendar: <a href="#booking-placeholder" data-booking-href data-booking-label>{BOOKING}</a>. Replace this placeholder with the live calendar embed when the link is ready.</p>
          <p class="muted">In-person note: if you are in Grand Junction or nearby, say so in the message and we can meet at a local coffee shop instead of a screen.</p>
        </div>
        <form class="form card" data-contact-form>
          <label>Name <input name="name" required></label>
          <label>Email <input type="email" name="email" required></label>
          <label>Message <textarea name="message" required></textarea></label>
          <button class="btn" type="submit">Send message</button>
          <p class="note" data-form-note hidden></p>
          <p class="muted">Form endpoint placeholder: connect a Hostinger or form service later. Nothing is sent until that is live.</p>
        </form>
      </div>
    </section>
    """
    page(
        out="contact/index.html",
        title="Contact Nick Perry Digital | Book a Free Strategy Call",
        description="Contact Nick Perry Digital. Free strategy call, message form, and click-to-call placeholder.",
        keyword="contact nick perry digital",
        depth=d,
        current="contact",
        body=body,
        canonical="/contact/",
    )


def build_legal() -> None:
    d = 1
    privacy = f"""
    {hero(d, "grid", "Legal", "Privacy Policy", "How this site handles information. Written in plain language. No invented tracking claims.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>Nick Perry Digital operates this website. Contact details will be completed when the phone number and email placeholders are replaced.</p>
      <h2>What is collected</h2>
      <p>If you use the contact form, the name, email, and message you type are collected so the inquiry can be answered. If analytics or Search Console are added later, those tools may collect standard usage data such as pages viewed and approximate location. This policy will be updated when those tools go live.</p>
      <h2>What is not done</h2>
      <p>This site does not sell personal information. Placeholders for booking and phone are not tracking pixels.</p>
      <h2>Third parties</h2>
      <p>Fonts load from Google Fonts. Tailwind CSS may load from a CDN. Decap CMS, if used, talks to GitHub. Each of those services has its own policy.</p>
      <h2>Contact</h2>
      <p>Questions: use the <a href="{rel(d)}contact/">contact page</a> or the phone placeholder in the header.</p>
    </div></section>
    """
    terms = f"""
    {hero(d, "grid", "Legal", "Terms of Service", "The simple terms for using this site and hiring Nick Perry Digital.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>By using nickperrydigital.com you agree to these terms. Project work is scoped in writing before it starts. Monthly SEO plans are month to month and can be canceled before the next billing date.</p>
      <h2>Ownership</h2>
      <p>You own your domain, content, website files, and ad accounts. Admin access is provided from day one on paid work.</p>
      <h2>No guarantees of rank</h2>
      <p>Search engines and AI tools are not for sale. The guarantee is the work: a clear plan, weekly check-ins, and honest reporting.</p>
      <h2>Placeholders</h2>
      <p>Phone, booking, and form endpoints on this site may still be placeholders. They are not offers by themselves.</p>
    </div></section>
    """
    page(out="privacy-policy/index.html", title="Privacy Policy | Nick Perry Digital", description="Privacy policy for nickperrydigital.com.", keyword="privacy policy", depth=d, current="home", body=privacy, canonical="/privacy-policy/")
    page(out="terms-of-service/index.html", title="Terms of Service | Nick Perry Digital", description="Terms of service for Nick Perry Digital.", keyword="terms of service", depth=d, current="home", body=terms, canonical="/terms-of-service/")


def build_awards() -> None:
    d = 1
    body = f"""
    {hero(d, "ivory", "Awards", "Awards and recognition", "This page will list awards and press when they are earned. Nothing is invented here.")}
    <section class="section section-ivory">
      <div class="wrap">
        <article class="placeholder-card">
          <span class="placeholder-label">Awards placeholder</span>
          <h2>No awards are listed yet</h2>
          <p>When Nick Perry Digital receives a public award or a press mention that can be linked, it will appear here with the source. This page exists so the site matches a full agency structure, not to imply recognition that has not happened.</p>
        </article>
      </div>
    </section>
    """
    page(out="awards/index.html", title="Awards | Nick Perry Digital", description="Awards page for Nick Perry Digital. Recognition will be listed when it is earned.", keyword="nick perry digital awards", depth=d, current="about", body=body, canonical="/awards/")


INSIGHTS = [
    ("local-service-marketing-checklist", "Local service marketing checklist for the Western Slope", "western slope local service marketing", "A practical checklist for trades and local operators who want more of the right calls."),
    ("seo-for-electricians-western-colorado", "SEO for electricians in Western Colorado", "seo for electricians western colorado", "How electricians get found for emergency and planned electrical work."),
    ("how-to-get-roofing-leads-grand-junction", "How to get roofing leads in Grand Junction", "roofing leads grand junction", "Search, profile, and site habits that help roofers get found after a storm or a bid request."),
    ("hvac-digital-marketing-western-colorado", "HVAC digital marketing on the Western Slope", "hvac digital marketing western colorado", "What HVAC companies need from a site, a profile, and ads in this climate."),
    ("hvac-lead-generation-grand-junction", "HVAC lead generation in Grand Junction", "hvac lead generation grand junction", "How heat and monsoon seasons change the way HVAC leads show up."),
    ("seo-for-plumbers-grand-junction", "SEO for plumbers in Grand Junction", "seo for plumbers grand junction", "Map pack, service pages, and reviews for plumbing companies."),
    ("google-business-profile-for-real-estate-agents", "Google Business Profile for real estate agents", "google business profile real estate agents", "How agents and teams should treat their Google profile."),
    ("google-business-profile-remodeling-contractors", "Google Business Profile for remodeling contractors", "google business profile remodeling contractors", "Categories, photos, and services that help remodelers get found."),
    ("local-seo-kitchen-bath-remodelers", "Local SEO for kitchen and bath remodelers", "local seo kitchen bath remodelers", "Service pages and local proof for kitchen and bath firms."),
    ("kitchen-bath-remodeling-leads", "Kitchen and bath remodeling leads", "kitchen bath remodeling leads", "Where remodel leads come from and how a site should handle them."),
    ("domain-listings-scam", "Domain listing scams, a short warning", "domain listing scam", "How fake domain invoices work and what to do instead."),
    ("google-ads-for-real-estate", "Google Ads for real estate teams", "google ads for real estate", "A cautious guide to paid search for agents who already have a tracking plan."),
]


def insight_body(slug: str, title: str, excerpt: str) -> str:
    extras = {
        "local-service-marketing-checklist": [
            "Start with the basics you control this week: claim the Google Business Profile, pick the right primary category, add the towns you actually serve, and put a working click-to-call number on every page.",
            "Write one page per service. A plumber who offers drain cleaning, water heaters, and re-pipe work needs three pages, not one paragraph that lists all three.",
            "Ask for reviews after finished jobs. Reply to every review. Photos from real job sites beat stock images.",
            "Only then spend on ads. Paid search works better when the landing page matches the query and the phone is tracked.",
        ],
        "seo-for-electricians-western-colorado": [
            "Emergency searches happen at night and on phones. The site has to show hours, a phone number, and the towns you will actually drive to.",
            "Separate panels, lighting, EV chargers, and generators. Those queries are different people with different urgency.",
            "A complete Google Business Profile with recent photos of trucks and panels helps more than a blog post about electrical theory.",
            "If you cover Clifton and Fruita as well as Grand Junction, say so on the profile and on location copy. Do not build doorway pages that swap a city name and nothing else.",
        ],
        "how-to-get-roofing-leads-grand-junction": [
            "Storm weeks compress demand. The businesses that already have a complete profile, reviews, and a fast mobile site take the overflow.",
            "Useful pages: roof repair, roof replacement, insurance claims help, and the materials you actually install.",
            "Before and after photos from Mesa County jobs are stronger than generic mountain skylines.",
            "Track calls from the website and from the profile separately so you know which one paid for the week.",
        ],
        "hvac-digital-marketing-western-colorado": [
            "Western Slope HVAC is seasonal and split between emergency repair and planned replacement. The site should serve both without hiding the phone number behind a form.",
            "Call out heat pumps, swamp coolers, and high-elevation installs if you do that work. National templates often skip it.",
            "Tune-up pages can introduce replacement without feeling like a bait switch. Financing and rebate notes belong near the quote form.",
            "Maps still decide a lot of after-hours work. Categories, service list, and reviews matter as much as the homepage.",
        ],
        "hvac-lead-generation-grand-junction": [
            "July and January do not behave the same. Emergency ads can make sense in peak weeks. The rest of the year, SEO and the profile do more of the lifting.",
            "A good HVAC site routes emergency calls to a tap-to-call button and sends planned installs to a short form.",
            "Do not invent wait-time promises. Say what you can keep: service area, hours, and how dispatch works.",
            "If you use ServiceTitan, Housecall Pro, or Jobber, the site should hand the lead to that system instead of a personal inbox that goes quiet on Saturday.",
        ],
        "seo-for-plumbers-grand-junction": [
            "Plumbing searches are often urgent and local. The map pack is the first fight. The website is the second.",
            "Build pages for drain cleaning, water heaters, leaks, and sewer work if those are real services.",
            "Reviews that mention a neighborhood (Redlands, Orchard Mesa, Fruita) help more than generic five-star text.",
            "Keep the NAP (name, address, phone) identical on the site, the profile, and the directories you already have.",
        ],
        "google-business-profile-for-real-estate-agents": [
            "A team profile and a personal profile are different tools. Use the one that matches how clients search for you.",
            "Categories, service areas, and listing photos should match the neighborhoods you actually farm.",
            "Weekly posts can highlight open houses and sold notes without turning the profile into a second blog you will abandon.",
            "Reviews from real buyers and sellers, with replies, are the trust layer agents skip when the market is busy.",
        ],
        "google-business-profile-remodeling-contractors": [
            "Pick a primary category that matches the work you want more of, then add secondary categories you truly offer.",
            "Add services with short descriptions. Empty service lists waste space Google already gave you.",
            "Photo cadence matters. Kitchens in progress, finished baths, and crew shots beat a single logo tile.",
            "Q&A on the profile is a good place for licensing, service area, and how bids work.",
        ],
        "local-seo-kitchen-bath-remodelers": [
            "Kitchen and bath queries are researched. People compare two or three firms. Your pages have to answer materials, timeline, and how a bid starts.",
            "Project photos with the town in the caption are useful. Project pages can rank when they are real jobs, not invented rooms.",
            "Internal links from the homepage to kitchen, bath, and the towns you serve keep the site understandable.",
            "Pair the site with a complete profile. Remodelers who only polish the website still lose the map pack.",
        ],
        "kitchen-bath-remodeling-leads": [
            "Leads come from search, ads, and referrals. The site should treat each one differently: a short form for planned remodels, a phone number for urgent repairs if you also do those.",
            "Qualify without friction. Rooms, timing, and a photo upload beat a ten-field form.",
            "Follow-up is part of lead generation. A same-day reply is a service, not a marketing trick.",
            "This article does not claim a conversion rate. Your numbers will come from your own call tracking.",
        ],
        "domain-listings-scam": [
            "Some businesses get official-looking mail or email that says a domain is about to expire or that a stranger is about to register a lookalike. Many of these are invoices for a directory listing you never ordered.",
            "Check the registrar you already use. If the domain is marked auto-renew there, you can ignore the letter.",
            "Do not call the number on the notice. Look up the registrar yourself and log in on a bookmark you already trust.",
            "If you are unsure, bring the letter to the strategy call. It is a common scare tactic, not an SEO emergency.",
        ],
        "google-ads-for-real-estate": [
            "Paid search for real estate is easy to waste. Broad keywords like homes for sale burn budget. Geo and listing-type modifiers keep the clicks closer to intent.",
            "Do not run ads until call and form tracking work. Otherwise you are buying noise.",
            "Landing pages should match the ad. A Palisade farm ad should not drop people on a generic team homepage.",
            "Ads are an add-on quote, not part of the $850 plan. The monthly SEO plans stay focused on organic and the profile.",
        ],
    }
    paras = extras.get(slug, [excerpt])
    html = "".join(f"<p>{p}</p>" for p in paras)
    return f"""
    {hero(1, "split", "Insights", title, excerpt)}
    <section class="section section-ivory"><div class="wrap prose">
      {html}
      <p>None of these notes invent a client result. They are process notes you can use whether you hire Nick Perry Digital or not.</p>
    </div></section>
    """


def build_insights() -> None:
    d = 1
    cards = "".join(
        f'<article class="card"><h3><a href="{rel(d)}{slug}/">{title}</a></h3><p class="muted">{excerpt}</p></article>'
        for slug, title, _kw, excerpt in INSIGHTS
    )
    body = f"""
    {hero(d, "split", "Insights", "Insights", "Notes on local search, websites, and lead flow for Western Slope businesses. Educational copy only. No invented client stats.")}
    <section class="section section-ivory"><div class="wrap"><div class="grid-2">{cards}</div></div></section>
    """
    page(out="insights/index.html", title="Insights | Nick Perry Digital", description="Articles on local SEO, Google Business Profile, and lead generation for Western Slope businesses.", keyword="western slope seo insights", depth=d, current="home", body=body, canonical="/insights/")
    for slug, title, kw, excerpt in INSIGHTS:
        page(
            out=f"{slug}/index.html",
            title=f"{title} | Nick Perry Digital",
            description=excerpt,
            keyword=kw,
            depth=d,
            current="home",
            body=insight_body(slug, title, excerpt),
            canonical=f"/{slug}/",
        )
        md = ROOT / "content" / "insights" / f"{slug}.md"
        md.write_text(
            f"---\ntitle: {title}\nslug: {slug}\ndate: 2026-10-13\nexcerpt: {excerpt}\nkeyword: {kw}\n---\n\n{excerpt}\n",
            encoding="utf-8",
        )


SERVICES = [
    {
        "slug": "brand-creation",
        "nav": "services",
        "h1": "Grand Junction logo and brand identity",
        "title": "Grand Junction Logo Design & Brand Identity | Nick Perry Digital",
        "keyword": "grand junction logo design",
        "desc": "Logo, color, type, and a short style guide for Western Slope businesses.",
        "lede": "Your brand is the first impression on the truck, the storefront, the website, and the Google listing. This service makes those pieces match.",
        "hero": "ivory",
        "points": [
            "Logo with primary, secondary, and icon versions",
            "Color and type that hold up on a truck door and on a phone screen",
            "A short style guide so vendors use the same files",
            "Optional cards, signage, and profile graphics",
            "Final files you own",
        ],
        "close": "Most identity work pairs with a new site so the brand and the pages launch together. Quotes are custom. See the add-ons on the pricing page.",
    },
    {
        "slug": "web-design",
        "nav": "services",
        "h1": "Web design and development",
        "title": "Web Design & Development | Nick Perry Digital",
        "keyword": "grand junction web design company",
        "desc": "$1,000 local websites built to load fast, rank, and make the next call obvious.",
        "lede": "Fast, SEO-ready sites that look right on a phone and turn visitors into leads. You own the files.",
        "hero": "rings",
        "points": [
            "Mobile-first layout with click-to-call and short forms",
            "One page per service, written in plain language",
            "WordPress or a lightweight static build, whichever fits",
            "Analytics and Search Console handed over at launch",
            "$1,000 for a standard local build",
        ],
        "close": "Larger or custom projects get a fixed quote after the strategy call. The care plan is $150 a month if you want hosting and edits handled.",
    },
    {
        "slug": "local-seo",
        "nav": "services",
        "h1": "Local SEO services",
        "title": "Local SEO Services | Nick Perry Digital",
        "keyword": "grand junction local seo",
        "desc": "Local SEO for Grand Junction and the Western Slope. $850 foundation plan, $1,500 with AI search.",
        "lede": "Location pages, citations, and internal links that rank in nearby searches without spammy doorway pages.",
        "hero": "rings",
        "points": [
            "A keyword map for the services people here actually type",
            "On-site service and town pages",
            "Citations that match your real name, address, and phone",
            "Review rhythm and spam cleanup",
            "Monthly report in plain English",
        ],
        "close": "The foundation plan is $850 a month. Adding AI search optimization is $1,500 a month. Both are month to month.",
    },
    {
        "slug": "google-business-profile",
        "nav": "services",
        "h1": "Google Business Profile management",
        "title": "Google Business Profile Management | Nick Perry Digital",
        "keyword": "google business profile management grand junction",
        "desc": "Optimize, post, and manage reviews so the profile can win the map pack.",
        "lede": "Optimize, post, and manage reviews to support the map pack and turn searches into calls.",
        "hero": "grid",
        "points": [
            "Categories, services, and service areas that match the ground you cover",
            "Photo plan and weekly posts",
            "Review requests that do not feel like nagging",
            "Q&A and spam fighting",
            "Included in both monthly plans",
        ],
        "close": "A profile cannot carry a broken website. Most clients run this with the site SEO in the $850 plan.",
    },
    {
        "slug": "google-ads",
        "nav": "services",
        "h1": "Google Ads (PPC)",
        "title": "Google Ads Management | Nick Perry Digital",
        "keyword": "google ads grand junction",
        "desc": "High-intent search campaigns with call tracking for Western Slope businesses.",
        "lede": "High-intent search campaigns with call tracking and landing pages that match the query.",
        "hero": "split",
        "points": [
            "Keyword and geo setup that matches the towns you serve",
            "Local Service Ads setup when the category allows it",
            "Call and form tracking before spend scales",
            "Landing pages that repeat the promise in the ad",
            "Custom monthly quote",
        ],
        "close": "Ads are an add-on, not a bundled surprise. You keep the ad account.",
    },
    {
        "slug": "seo",
        "nav": "services",
        "h1": "SEO (organic)",
        "title": "Organic SEO | Nick Perry Digital",
        "keyword": "organic seo grand junction",
        "desc": "Technical fixes and content that grow organic rankings beyond local pack.",
        "lede": "Technical fixes and content strategy that grow broader organic rankings and keep traffic after the map pack is stable.",
        "hero": "grid",
        "points": [
            "Technical cleanup: speed, index, and internal links",
            "Content for services people research before they call",
            "Support for AI-readable structure",
            "Search Console shared with you",
            "Folded into the monthly plans",
        ],
        "close": "Organic SEO here is not a separate mystery retainer. It lives inside the $850 and $1,500 plans.",
    },
    {
        "slug": "reputation-management",
        "nav": "services",
        "h1": "Reputation management",
        "title": "Reputation Management | Nick Perry Digital",
        "keyword": "reputation management grand junction",
        "desc": "A simple review engine and response playbook for local businesses.",
        "lede": "A simple review engine and response playbook that supports trust and local rankings.",
        "hero": "orbit",
        "points": [
            "Ask timing after a finished job",
            "Reply guidelines for good and hard reviews",
            "Spam and fake-review flags",
            "Photo and keyword hygiene on the profile",
            "Included with monthly SEO",
        ],
        "close": "This is not a bought-review service. Only real customers are asked.",
    },
    {
        "slug": "conversion-rate-optimization",
        "nav": "services",
        "h1": "Conversion rate optimization",
        "title": "Conversion Rate Optimization | Nick Perry Digital",
        "keyword": "conversion rate optimization websites",
        "desc": "UX and testing work that turns existing traffic into more calls and forms.",
        "lede": "Heatmaps, testing, and UX tweaks that squeeze more leads from the same traffic.",
        "hero": "split",
        "points": [
            "Click-to-call and form placement",
            "Service page clarity",
            "Mobile speed and tap targets",
            "Thank-you and follow-up paths",
            "Changes measured against calls and forms",
        ],
        "close": "CRO is part of ongoing website work. It does not require a new invented baseline number to start.",
    },
    {
        "slug": "website-maintenance",
        "nav": "services",
        "h1": "WordPress care and hosting",
        "title": "WordPress Care & Hosting | Nick Perry Digital",
        "keyword": "wordpress care plan grand junction",
        "desc": "$150 a month for hosting, security, updates, and edits. Ask about free hosting.",
        "lede": "Secure hosting, backups, updates, and speed care so the site stays fast and quiet.",
        "hero": "orbit",
        "points": [
            "Updates and backups",
            "Security monitoring",
            "Routine copy and image edits",
            "Uptime watch",
            "$150 a month",
        ],
        "close": "Ask about free hosting on eligible static builds. You can also take the site elsewhere. Ownership stays with you.",
    },
    {
        "slug": "lead-generation",
        "nav": "services",
        "h1": "Lead generation",
        "title": "Lead Generation | Nick Perry Digital",
        "keyword": "lead generation grand junction",
        "desc": "Offers, forms, ads, and follow-up that turn visits into booked jobs.",
        "lede": "Offers, forms, and follow-up that turn site visits and ad clicks into booked work.",
        "hero": "rings",
        "points": [
            "Offer and landing page fit",
            "Call tracking",
            "Local Service Ads when eligible",
            "Form routing into the tools you already use",
            "Reporting that counts leads, not just sessions",
        ],
        "close": "Lead generation is the outcome of the site, the profile, and optional ads working together. See digital marketing and pricing for how the pieces stack.",
    },
    {
        "slug": "ai-search-optimization",
        "nav": "services",
        "h1": "AI search optimization",
        "title": "AI Search Optimization & AEO | Nick Perry Digital",
        "keyword": "ai search optimization aeo geo",
        "desc": "AEO and GEO work so AI tools can find and quote a local business. $1,500 plan.",
        "lede": "When someone asks ChatGPT, Gemini, or Google AI who to hire, the answer comes from pages, profiles, reviews, and directories. This work makes those sources clear.",
        "hero": "orbit",
        "points": [
            "AI visibility audit across major assistants",
            "Entity and schema cleanup",
            "Pages written so they can be quoted",
            "Citation cleanup in sources models already read",
            "Monthly mention tracking",
        ],
        "close": "The $1,500 plan includes this work plus the foundation SEO. No one can guarantee an AI mention. The work is the signals and the report.",
    },
]


def build_services() -> None:
    d = 2
    for s in SERVICES:
        faqs = [
            (f"How does {s['h1']} start?", "A free strategy call. If the fit is wrong, you will hear that on the call."),
            ("How is this priced?", "Website builds are $1,000. Monthly SEO is $850 or $1,500. Care is $150. Ads and branding are custom quotes."),
            ("Do I own the work?", "Yes. Admin access from day one. Files, profiles, and ad accounts stay in your name."),
        ]
        points = "".join(f"<li>{p}</li>" for p in s["points"])
        body = f"""
        {hero(d, s["hero"], "Service", s["h1"], s["lede"])}
        <section class="section section-ivory"><div class="wrap prose">
          <h2>What is included</h2>
          <ul>{points}</ul>
          <p>{s["close"]}</p>
        </div></section>
        {faq_block(faqs)}
        """
        page(
            out=f"services/{s['slug']}/index.html",
            title=s["title"],
            description=s["desc"],
            keyword=s["keyword"],
            depth=d,
            current="services",
            body=body,
            canonical=f"/services/{s['slug']}/",
            schema=faq_schema(faqs),
        )


LOCATIONS = [
    {
        "slug": "grand-junction",
        "name": "Grand Junction",
        "keyword": "web design seo grand junction",
        "nearby": "Fruita, Palisade, Clifton, and the Redlands",
        "intro": "Grand Junction is the hub of the Grand Valley. Searches here mix locals, people driving in from Mesa County, and visitors who will only call the business that looks current on a phone.",
        "why": "A Grand Junction page has to do more than repeat the homepage. It should name the services, the neighborhoods, and the fact that Maps often decides the first call. National templates skip Orchard Mesa, the Redlands, and the drive from Clifton.",
        "help": "Trades, professional firms, restaurants, medical and dental, real estate teams, and retailers who serve the whole valley.",
        "hero": "rings",
    },
    {
        "slug": "fruita",
        "name": "Fruita",
        "keyword": "seo company fruita co",
        "nearby": "Grand Junction, Loma, and the Colorado National Monument side of the valley",
        "intro": "Fruita is two towns at once: the one that fills up when bikes come off I-70, and the one that lives here all year. Those two customers search differently.",
        "why": "Piggybacking only on Grand Junction leaves Fruita driveway searches to whoever has a local footprint. Service areas, photos, and a Fruita page help the profile match where the work actually happens.",
        "help": "Home services, bike and outdoor shops, restaurants and lodging, dental and other professional offices, and yard work that has to survive high desert wind.",
        "hero": "orbit",
    },
    {
        "slug": "palisade",
        "name": "Palisade",
        "keyword": "web design seo palisade co",
        "nearby": "Grand Junction, Clifton, and the East Orchard Mesa farms",
        "intro": "Palisade is fruit, wine, and a Main Street that works hardest when visitors are in town. Locals still need a plumber in January.",
        "why": "Visitor searches are mobile and map-first. Resident searches are quieter and more loyal. A Palisade site should speak to both without sounding like a tourism brochure that forgot the service area.",
        "help": "Wineries and tasting rooms, lodging, restaurants, farm stands, and the trades that keep harvest and home life moving.",
        "hero": "ivory",
    },
    {
        "slug": "clifton",
        "name": "Clifton",
        "keyword": "seo clifton colorado",
        "nearby": "Grand Junction, Palisade, and Fruitvale",
        "intro": "Clifton sits on the east side of the Grand Valley. A lot of service calls start here even when the shop address is in Grand Junction.",
        "why": "If you work Clifton every day, the profile and the site should say so. Proximity still matters in Maps. A missing service area is a quiet way to lose the driveway search.",
        "help": "Home services, auto, medical, and retailers who serve I-70 East households.",
        "hero": "grid",
    },
    {
        "slug": "redlands",
        "name": "Redlands",
        "keyword": "seo redlands grand junction",
        "nearby": "Grand Junction, Fruita, and the Monument Road corridor",
        "intro": "The Redlands is a Grand Junction neighborhood with its own search habits: homeowners, views of the Monument, and a lot of service work behind a residential address.",
        "why": "Google often treats the Redlands as part of Grand Junction, but residents still type the name. A page and a few reviews that mention the Redlands help more than a generic Mesa County blurb.",
        "help": "Home services, remodelers, landscaping, and professional services used by Redlands households.",
        "hero": "split",
    },
    {
        "slug": "montrose",
        "name": "Montrose",
        "keyword": "seo montrose co",
        "nearby": "Olathe, Delta, Ridgway, and the Uncompahgre Valley",
        "intro": "Montrose is a full market of its own, not a suburb of Grand Junction. People here search locally first, then look south and north if they have to.",
        "why": "A Grand Junction-only profile will not carry Montrose driveway searches. The business needs Montrose pages, Montrose photos, and reviews from this valley.",
        "help": "Trades, agriculture-adjacent services, outdoor and lodging businesses, and professional offices on Townsend and Main.",
        "hero": "rings",
    },
    {
        "slug": "delta",
        "name": "Delta",
        "keyword": "web design seo delta colorado",
        "nearby": "Olathe, Cedaredge, Paonia, and Montrose",
        "intro": "Delta is a working town between the Grand Valley and the North Fork. Search volume is smaller, which also means the map pack is more winnable.",
        "why": "Many Delta businesses also serve Olathe and the North Fork. The site should name those towns on purpose, not hide them in a footer.",
        "help": "Agriculture, trades, medical, and Main Street retail.",
        "hero": "grid",
    },
    {
        "slug": "olathe",
        "name": "Olathe",
        "keyword": "seo olathe colorado",
        "nearby": "Delta, Montrose, and the Uncompahgre corridor",
        "intro": "Olathe is known for sweet corn and for sitting between two larger towns. Local searches still happen here, especially for food, farm, and home services.",
        "why": "If your trucks already run this stretch of 50, the profile should list Olathe. A page that mentions harvest traffic and residential work is more honest than a copied Delta page.",
        "help": "Farm-adjacent businesses, trades, and food operators who serve both locals and seasonal traffic.",
        "hero": "ivory",
    },
    {
        "slug": "cedaredge",
        "name": "Cedaredge",
        "keyword": "seo cedaredge co",
        "nearby": "Delta, Eckert, and the Surface Creek side of Grand Mesa",
        "intro": "Cedaredge sits under Grand Mesa. Searches mix residents, second-home owners, and people coming up for the mesa.",
        "why": "A Delta-only strategy leaves Surface Creek searches on the table. Photos, categories, and a Cedaredge page help Maps understand you work here.",
        "help": "Home services, lodging, orchards and farm stands, and professional services for the Surface Creek community.",
        "hero": "orbit",
    },
    {
        "slug": "paonia",
        "name": "Paonia",
        "keyword": "seo paonia colorado",
        "nearby": "Hotchkiss, Delta, and the North Fork Valley",
        "intro": "Paonia is fruit, wine, and a small downtown that punches above its size. Searchers are often already in the valley or planning a trip.",
        "why": "North Fork businesses get found when the site and the profile talk like the valley: seasons, produce, and the drive from Delta or over McClure.",
        "help": "Orchards, wineries, lodging, restaurants, and the trades that keep irrigation and old houses working.",
        "hero": "ivory",
    },
    {
        "slug": "rifle",
        "name": "Rifle",
        "keyword": "web design seo rifle co",
        "nearby": "Silt, Glenwood Springs, and the I-70 energy and hunting corridor",
        "intro": "Rifle sits on I-70 with a local economy that is not the same as a resort town and not the same as Grand Junction.",
        "why": "Energy, outdoor, and home-service searches here are practical. A site that only talks like a ski-town agency will miss the work.",
        "help": "Trades, outdoor and sporting, restaurants, and professional services along Railroad and the highway.",
        "hero": "split",
    },
    {
        "slug": "glenwood-springs",
        "name": "Glenwood Springs",
        "keyword": "seo glenwood springs co",
        "nearby": "Carbondale, New Castle, and the Roaring Fork and I-70 junction",
        "intro": "Glenwood Springs mixes locals, I-70 travelers, and people in town for the springs. Those three groups do not search the same way.",
        "why": "A hospitality business and a plumber in Glenwood need different pages. The profile should match the actual category, not a generic Roaring Fork blurb.",
        "help": "Lodging, restaurants, medical, outdoor, and home services.",
        "hero": "orbit",
    },
    {
        "slug": "carbondale",
        "name": "Carbondale",
        "keyword": "seo carbondale colorado",
        "nearby": "Glenwood Springs, Basalt, and the Crystal River Valley",
        "intro": "Carbondale sits between the resort towns and the rest of the Roaring Fork. Local businesses still need to be findable when someone types the town name.",
        "why": "Aspen-only marketing leaks. Carbondale residents search Carbondale first. Service areas and a town page keep you in that set.",
        "help": "Professional services, restaurants, trades, and outdoor businesses.",
        "hero": "grid",
    },
    {
        "slug": "basalt",
        "name": "Basalt",
        "keyword": "seo basalt colorado",
        "nearby": "Carbondale, El Jebel, and the mid-valley Roaring Fork",
        "intro": "Basalt is a mid-valley town with locals and second-home traffic. Search is competitive for some categories and wide open for others.",
        "why": "Mid-valley work is lost when a profile only lists Aspen. Name Basalt, Willits, and the roads you actually drive.",
        "help": "Home services, restaurants, professional offices, and outdoor retail.",
        "hero": "split",
    },
    {
        "slug": "aspen",
        "name": "Aspen",
        "keyword": "web design seo aspen co",
        "nearby": "Snowmass, Basalt, and the upper Roaring Fork",
        "intro": "Aspen search is high intent and often high cost if you jump straight to ads. The site and the profile still have to be solid first.",
        "why": "Resort-town search mixes visitors and residents. Categories, hours, and language should match who you can actually serve this week.",
        "help": "Hospitality, professional services, luxury home services, and retail.",
        "hero": "ivory",
    },
    {
        "slug": "durango",
        "name": "Durango",
        "keyword": "seo durango colorado",
        "nearby": "Bayfield, the Animas Valley, and the Four Corners",
        "intro": "Durango is a Four Corners market. It is not run from a Grand Junction doorway page, and this site does not pretend otherwise.",
        "why": "If you serve Durango, you need Durango pages, Durango photos, and reviews from La Plata County. The rest of this site can still share process and pricing.",
        "help": "Outdoor and lodging, trades, restaurants, and professional services in the Animas Valley.",
        "hero": "rings",
    },
]


def build_locations() -> None:
    d = 1
    cards = "".join(
        f'<article class="service-card"><h3><a href="{rel(d)}locations/{loc["slug"]}/">{loc["name"]}, CO</a></h3><p class="muted">Web design, local SEO, and Google Business Profile work for {loc["name"]}.</p></article>'
        for loc in LOCATIONS
    )
    body = f"""
    {hero(d, "orbit", "Areas", "Areas we serve", "Primary towns across the Grand Valley, the North Fork, the I-70 corridor, and the Four Corners. If your town is missing, reach out. Nearby work is common.")}
    <section class="section section-ivory"><div class="wrap"><div class="grid-3">{cards}</div></div></section>
    """
    page(out="locations/index.html", title="Areas We Serve | Nick Perry Digital", description="Web design and local SEO across Grand Junction, the Grand Valley, Montrose, and the Western Slope.", keyword="western slope web design seo", depth=d, current="home", body=body, canonical="/locations/")

    d = 2
    for loc in LOCATIONS:
        faqs = [
            (f"Are you based in {loc['name']}?", f"Nick Perry Digital works with {loc['name']} businesses and the nearby towns of {loc['nearby']}. The strategy call can be remote or in person when travel makes sense."),
            (f"How much does SEO cost for a {loc['name']} business?", "The foundation plan is $850 a month for Google Business Profile management plus website SEO. The plan that adds AI search optimization is $1,500 a month. No long-term contracts."),
            (f"Is SEO worth it in {loc['name']}?", "Smaller markets often have less competition in the map pack. Many businesses here also serve neighboring towns, so the same work can cover more than one search."),
            (f"How do I show up in {loc['name']} and nearby towns?", "The profile needs service areas that match where you really work, plus real pages rather than a single page with the city name swapped. Reviews from both places help."),
            ("How long before I see results?", "Google Business Profile movement often shows in four to eight weeks. Organic rankings usually take longer. The promise is the work and the reporting, not a purchased rank."),
            ("What does a website cost?", "A standard local website is $1,000. The optional care plan is $150 a month."),
        ]
        body = f"""
        {hero(d, loc["hero"], loc["name"] + ", Colorado", f"Web design and SEO in {loc['name']}, CO", loc["intro"])}
        <section class="section section-ivory"><div class="wrap prose">
          <h2>Why {loc['name']} needs its own search presence</h2>
          <p>{loc["why"]}</p>
          <h2>What the work includes</h2>
          <ul>
            <li>A local keyword map for what {loc['name']} customers actually search</li>
            <li>Google Business Profile work: categories, service areas, photos, posts, and reviews</li>
            <li>Service pages with clear calls to action and mobile load times that survive a weak signal</li>
            <li>Coverage for {loc['name']} plus {loc['nearby']}, without doorway spam</li>
            <li>Call and form tracking so you can see which pages earn the leads</li>
          </ul>
          <h2>Businesses this fits</h2>
          <p>{loc["help"]}</p>
          <h2>Plans</h2>
          <p>GBP + Website is $850 a month. GBP + Website + AI Search is $1,500 a month. A standard website build is $1,000. Care is $150 a month.</p>
        </div></section>
        {faq_block(faqs)}
        """
        page(
            out=f"locations/{loc['slug']}/index.html",
            title=f"Web Design & SEO in {loc['name']}, CO | Nick Perry Digital",
            description=f"Web design and local SEO for businesses in {loc['name']}, Colorado. Published pricing and a free strategy call.",
            keyword=loc["keyword"],
            depth=d,
            current="home",
            body=body,
            canonical=f"/locations/{loc['slug']}/",
            schema=faq_schema(faqs),
        )


def money_process() -> str:
    steps = [
        ("Strategy call", "Thirty minutes, free. If the fit is wrong, you will hear that on the call."),
        ("Structure and content", "Pages, services, and tracking before visual design."),
        ("Design and build", "A look that fits the business, then a build tested on real phones."),
        ("Launch, then ongoing SEO", "Launch is the start. Monthly plans keep the profile and the pages moving."),
    ]
    rows = "".join(
        f'<div class="process-step"><div class="step-num">{i}</div><div><h3>{t}</h3><p class="muted">{b}</p></div></div>'
        for i, (t, b) in enumerate(steps, 1)
    )
    return f'<div class="process">{rows}</div>'


def build_money() -> None:
    d = 1

    gjwd_faqs = [
        ("How much does web design cost in Grand Junction?", "A standard local build is $1,000. That includes an SEO-minded site and Google Business Profile setup help. Larger projects get a fixed quote before work begins."),
        ("How long does a website take?", "Most local builds take a few weeks. Content is the usual bottleneck. Fast decisions mean a faster launch."),
        ("What platform do you build on?", "WordPress when you need an editor and plugins. Lightweight static sites when that is faster and cheaper to host. Either way, you own the files."),
        ("Can you help with ChatGPT and AI search?", "AI tools read your pages, profile, reviews, and directories. That groundwork is the same discipline as local SEO. The $1,500 plan tracks AI visibility on purpose."),
        ("Will you maintain the site after launch?", "The optional care plan is $150 a month for hosting, security, updates, and edits. You can also take the site in-house."),
        ("Do you only work in Grand Junction?", "Grand Junction is the hub. The same offer covers Fruita, Palisade, Clifton, Montrose, and the rest of the towns in Areas We Serve."),
    ]
    gjwd = f"""
    {hero(d, "rings", "Grand Junction", "Grand Junction web design, built from scratch", "Serving Mesa County: Grand Junction, Fruita, Palisade, Clifton, and the Redlands.")}
    {as_seen_in()}
    <section class="section section-ivory"><div class="wrap split">
      <div class="prose">
        <h2>Why this page exists</h2>
        <p>Too many solid Grand Junction companies are held back by slow, dated sites. The work is good. The site hides the phone number. Meanwhile a competitor with a clearer page gets the call.</p>
        <p>Nick Perry Digital builds the site around a simple job: show up in search, explain the services, and make it easy to call or book. You own the files. Admin access from day one.</p>
      </div>
      <figure class="portrait"><img src="{asset(d, "assets/images/nick/me-but-stencil.png")}" alt="Line portrait of Nick Perry" width="800" height="1000"></figure>
    </div></section>
    <section class="section section-white"><div class="wrap">
      <h2>What makes this web design different</h2>
      <div class="grid-2">
        <article class="card"><h3>Fast on mobile</h3><p class="muted">Most visits are on a phone, often in a driveway. Pages are built to load on a weak signal.</p></article>
        <article class="card"><h3>Clear service pages</h3><p class="muted">One page per service, with the towns you serve spelled out. That is also what AI tools quote.</p></article>
        <article class="card"><h3>Built to convert</h3><p class="muted">Click to call, short forms, and a layout that points to the next step.</p></article>
        <article class="card"><h3>You keep it</h3><p class="muted">WordPress or static. If you leave, you take the site. That is the only honest setup.</p></article>
      </div>
    </div></section>
    <section class="section section-ivory"><div class="wrap"><h2>How a site gets built</h2>{money_process()}</div></section>
    {proven_results(d)}
    <section class="section section-white"><div class="wrap prose">
      <h2>What a website costs</h2>
      <p>A standard SEO-minded local site is $1,000. Google Business Profile setup help is part of the build. Larger work is a fixed quote after the call.</p>
      <p>Ongoing support is optional. The care plan is $150 a month. Ask about free hosting on eligible static builds.</p>
    </div></section>
    {testimonials()}
    {trusted_by()}
    {featured_work(d)}
    {faq_block(gjwd_faqs)}
    """
    page(out="grand-junction-web-design/index.html", title="Grand Junction Web Design Company | Nick Perry Digital", description="Grand Junction web design from $1,000. Fast local sites you own, plus optional SEO and care.", keyword="grand junction web design", depth=d, current="home", body=gjwd, canonical="/grand-junction-web-design/", schema=faq_schema(gjwd_faqs))

    gjseo_faqs = [
        ("How much does SEO cost in Grand Junction?", "The foundation plan is $850 a month for Google Business Profile management plus website SEO. The plan with AI search optimization is $1,500 a month. Month to month."),
        ("How long until I see results?", "Many accounts see profile movement in 30 to 90 days. Organic rankings compound after that. Anyone promising page one in two weeks is selling something that will not last."),
        ("Can you get my business recommended by ChatGPT?", "AI tools recommend businesses they can verify. Pages, profile, reviews, and directories are the inputs. The $1,500 plan tracks those mentions. Nobody controls the model."),
        ("What is the difference between SEO and local SEO?", "Local SEO is for searches with local intent and the map pack. That is where most Grand Junction service businesses win or lose."),
        ("Do you guarantee rankings?", "No. The guarantee is the work: a plan, weekly check-ins, and honest reporting."),
        ("Do I need a new website to do SEO?", "Not always. If the site is holding you back, the $1,000 build is on the table."),
    ]
    gjseo = f"""
    {hero(d, "rings", "Grand Junction SEO", "Grand Junction SEO for businesses that actually work here", "Serving Mesa County: Grand Junction, Fruita, Palisade, Clifton, and the Redlands.")}
    {as_seen_in()}
    <section class="section section-ivory"><div class="wrap prose">
      <h2>How local SEO is done here</h2>
      <p>Map the demand. Fix the foundations. Show progress every week. No gimmicks and no purchased ranking claims.</p>
      <ul>
        <li>Local keyword map for services people in Grand Junction actually search</li>
        <li>Google Business Profile: categories, services, photos, posts, reviews</li>
        <li>Site structure, service pages, and mobile speed</li>
        <li>Mesa County coverage without doorway pages</li>
        <li>Tracking for calls and forms</li>
      </ul>
      <h2>What local SEO costs</h2>
      <p>Foundation plan: $850 a month. With AI search: $1,500 a month. If the site itself is the blocker, start with the $1,000 website.</p>
    </div></section>
    {proven_results(d)}
    {testimonials()}
    {trusted_by()}
    {faq_block(gjseo_faqs)}
    """
    page(out="grand-junction-seo/index.html", title="Grand Junction SEO Company | Nick Perry Digital", description="Local SEO in Grand Junction. $850 and $1,500 month-to-month plans. Free strategy call.", keyword="grand junction seo", depth=d, current="home", body=gjseo, canonical="/grand-junction-seo/", schema=faq_schema(gjseo_faqs))

    gjdm_faqs = [
        ("What is included in digital marketing?", "The site, local SEO, the Google Business Profile, optional ads, and reputation work. Pieces are scoped. You are not forced into a bundle you do not need."),
        ("How is this priced?", "Website $1,000. SEO $850 or $1,500 a month. Ads and branding quoted. Care $150."),
        ("Do you run social media?", "This practice is built around search, the site, and the profile. Social can wait unless it clearly supports those."),
    ]
    gjdm = f"""
    {hero(d, "split", "Grand Junction", "Grand Junction digital marketing", "Web design, local SEO, Google Business Profile, and ads working as one system for Mesa County businesses.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>Most businesses do not need a dozen channels. They need the site, the map pack, and optional ads aimed at calls. Nick Perry Digital keeps the stack small on purpose.</p>
      <h2>The stack</h2>
      <ul>
        <li><a href="{rel(d)}grand-junction-web-design/">Web design</a></li>
        <li><a href="{rel(d)}grand-junction-seo/">Local SEO</a></li>
        <li><a href="{rel(d)}services/google-business-profile/">Google Business Profile</a></li>
        <li><a href="{rel(d)}services/google-ads/">Google Ads</a></li>
        <li><a href="{rel(d)}services/lead-generation/">Lead generation</a></li>
      </ul>
    </div></section>
    {proven_results(d)}
    {faq_block(gjdm_faqs)}
    """
    page(out="grand-junction-digital-marketing/index.html", title="Grand Junction Digital Marketing | Nick Perry Digital", description="Digital marketing for Grand Junction: websites, local SEO, Google Business Profile, and ads.", keyword="grand junction digital marketing", depth=d, current="home", body=gjdm, canonical="/grand-junction-digital-marketing/", schema=faq_schema(gjdm_faqs))

    mont_faqs = [
        ("Do you work in Montrose or only Grand Junction?", "Montrose is a primary market on this site. The work is the same stack: site, profile, and local SEO."),
        ("What does SEO cost in Montrose?", "The plans are $850 or $1,500 a month, month to month. Website builds are $1,000."),
        ("Should I rank in Grand Junction too?", "Only if you actually take that work. Service areas should match the trucks, not a wish list."),
    ]
    mont = f"""
    {hero(d, "rings", "Montrose", "Montrose SEO", "Local SEO and websites for Montrose, Olathe, and the Uncompahgre Valley. Not a copied Grand Junction page with the city name swapped.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>Montrose searches locally first. A profile based only in Mesa County will not carry a Montrose driveway search. This page exists so the town has its own keyword map, service areas, and content.</p>
      <p>See also the <a href="{rel(d)}locations/montrose/">Montrose location page</a> and <a href="{rel(d)}locations/olathe/">Olathe</a>.</p>
      <h2>Plans</h2>
      <p>GBP + Website $850 a month. Plus AI search $1,500 a month. Website $1,000.</p>
    </div></section>
    {proven_results(d)}
    {faq_block(mont_faqs)}
    """
    page(out="montrose-seo/index.html", title="Montrose SEO | Nick Perry Digital", description="SEO services for Montrose, Colorado. Month-to-month local SEO and $1,000 websites.", keyword="montrose seo", depth=d, current="home", body=mont, canonical="/montrose-seo/", schema=faq_schema(mont_faqs))

    hvac_faqs = [
        ("Do you only work with HVAC companies in Western Colorado?", "The HVAC page is written for Colorado contractors. The same offer can apply elsewhere if the work is a fit."),
        ("How long until a new HVAC website produces calls?", "A clearer phone number and emergency path can help the same day for people already on the site. Organic and map pack movement take longer."),
        ("What does an HVAC website cost?", "The standard local website is $1,000. Monthly SEO is $850 or $1,500. Care is $150."),
        ("Can I keep ServiceTitan or Housecall Pro?", "Yes. The site should hand leads to the dispatch tool you already use."),
    ]
    hvac = f"""
    {hero(d, "split", "HVAC", "HVAC website design in Colorado", "Sites for HVAC companies that need to book service calls, explain replacement, and show up in Maps. No made-up contractor case studies on this page.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>A useful HVAC website does three jobs: make emergency calls easy, help tune-up shoppers understand replacement, and support the Google Business Profile. National templates sold to every trade skip all three.</p>
      <h2>Why Colorado HVAC is different</h2>
      <p>The Front Range, the Western Slope, and the mountain corridors are not the same market. Heat pumps, swamp coolers, altitude, and second homes change the copy. This practice is written for the Western Slope first.</p>
      <h2>What gets built</h2>
      <ul>
        <li>Visible phone numbers and an emergency path</li>
        <li>Service pages for repair, replacement, and maintenance</li>
        <li>Google Business Profile categories, services, and photos</li>
        <li>Optional Local Service Ads and search ads</li>
      </ul>
    </div></section>
    {faq_block(hvac_faqs)}
    """
    page(out="hvac-website-design-colorado/index.html", title="HVAC Website Design in Colorado | Nick Perry Digital", description="HVAC websites and local SEO for Colorado contractors. $1,000 builds and month-to-month SEO.", keyword="hvac website design colorado", depth=d, current="home", body=hvac, canonical="/hvac-website-design-colorado/", schema=faq_schema(hvac_faqs))

    best_faqs = [
        ("How do I choose an SEO company in Grand Junction?", "Look for local knowledge, published pricing, and a willingness to show the work without guaranteeing ranks. Be skeptical of long lock-ins."),
        ("How much does SEO cost in Grand Junction?", "Plans on this site are $850 and $1,500 a month. Other local firms set their own fees. One-time audits vary."),
        ("How long does SEO take?", "Profile movement often starts within a couple of months. Organic compounding takes longer. Treat 30-day rank promises as a warning."),
        ("Local agency or national?", "For most Mesa County service businesses, a local practice is easier to hold accountable and more likely to know Palisade from Clifton."),
        ("What is local SEO versus regular SEO?", "Local SEO is map pack, proximity, reviews, and service-area pages. Regular SEO is broader. Most trades here need local first."),
        ("How do I know if the work is happening?", "You should see Search Console, profile insights, and a plain-English monthly note. Rank screenshots without context are not enough."),
        ("Should I do it myself?", "You can claim the profile, ask for reviews, and fix the NAP. Technical work and content while running a business is harder. Split the labor if that helps."),
        ("Is this list paid?", "No. Nick Perry Digital is listed first because this is our site. Other local firms are named because they publicly operate here, not because of a paid slot."),
    ]
    best = f"""
    {hero(d, "grid", "Guide", "Best SEO companies in Grand Junction, CO", "A buyer's guide, not a fake trophy page. Nick Perry Digital is listed first because this is our site. Other local firms are named because they publicly work in this market.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>Grand Junction search results for SEO are full of agencies that are not from here. This page focuses on how to choose, then lists Nick Perry Digital with published pricing, and names other local firms you can evaluate on your own.</p>
      <h2>What to look for</h2>
      <ul>
        <li>Someone you can actually call</li>
        <li>Pricing you can read before a pitch</li>
        <li>Work samples that are not invented</li>
        <li>No rank guarantee</li>
      </ul>
      <h2>Nick Perry Digital</h2>
      <p>Web design and local SEO for Grand Junction and the Western Slope. Website builds from $1,000. Monthly plans at $850 and $1,500. Care plan $150. Free strategy call. Phone and booking links are still placeholders on this site until they are replaced in the CMS.</p>
      <h2>Other local firms to compare</h2>
      <p>These businesses publicly market digital or SEO services in the Grand Junction area. This is not a ranked contest and not an endorsement. Check their current work yourself:</p>
      <ul>
        <li>Chuckwalla Digital, Grand Junction</li>
        <li>Walk to Success Marketing, Grand Junction</li>
        <li>Ryan/Sawyer Marketing, Grand Junction</li>
        <li>Longpoint Digital, Grand Junction / Palisade</li>
      </ul>
      <p>If a firm should be added or has closed, use the contact page. This list will stay factual.</p>
    </div></section>
    {faq_block(best_faqs)}
    """
    page(out="best-seo-company-grand-junction/index.html", title="Best SEO Company in Grand Junction, CO | Nick Perry Digital", description="How to choose an SEO company in Grand Junction, with Nick Perry Digital pricing and other local firms named for comparison.", keyword="best seo company grand junction", depth=d, current="home", body=best, canonical="/best-seo-company-grand-junction/", schema=faq_schema(best_faqs))


CASE_STUDIES = [
    ("placeholder-01-local-service", "Local service visibility", "local service seo case study", "Reserved slot for a local service business. No client name or metric until the work is cleared to publish."),
    ("placeholder-02-professional", "Professional services search", "professional services seo case study", "Reserved slot for a professional firm. Outcome and screenshots stay empty on purpose."),
    ("placeholder-03-home-services", "Home-service lead flow", "home service leads case study", "Reserved slot for a home-service company. Lead counts will appear only from real reporting."),
    ("placeholder-04-hospitality", "Hospitality and food", "restaurant website case study", "Reserved slot for a hospitality or food business."),
    ("placeholder-05-ecommerce", "Retail and ecommerce", "ecommerce seo case study", "Reserved slot for a retail or ecommerce project."),
]


def build_case_studies() -> None:
    d = 2
    for slug, title, kw, summary in CASE_STUDIES:
        body = f"""
        {hero(d, "grid", "Case study placeholder", title, summary)}
        <section class="section section-ivory"><div class="wrap">
          <article class="placeholder-card">
            <span class="placeholder-label">Do not invent a result here</span>
            <h2>Waiting on a real project</h2>
            <p>This URL exists so the Results grid and footer can point somewhere. Replace this copy, add screenshots, and remove the placeholder label when a client agrees to be named.</p>
            <p class="muted">Industry notes can go here later. Stats cannot go here until they come from Search Console or the client's own numbers.</p>
          </article>
        </div></section>
        """
        page(out=f"case-studies/{slug}/index.html", title=f"{title} | Case Study Placeholder | Nick Perry Digital", description=summary, keyword=kw, depth=d, current="results", body=body, canonical=f"/case-studies/{slug}/")
        (ROOT / "content" / "case-studies" / f"{slug}.md").write_text(
            f"---\ntitle: {title}\nslug: {slug}\nindustry: placeholder\nplaceholder: true\nsummary: {summary}\n---\n\n{summary}\n",
            encoding="utf-8",
        )

    disp = f"""
    {hero(d, "split", "Industry", "Dispensary SEO in Grand Junction", "Notes on local search for cannabis retail. This is an industry page, not a claimed client case study.")}
    <section class="section section-ivory"><div class="wrap prose">
      <p>Dispensary search is local, regulated, and heavy on Maps. A useful site still needs clear hours, location, and product categories that match what people type. This page does not name a client or show a traffic chart.</p>
      <p>When a real dispensary project is cleared to publish, it can replace or sit beside this placeholder. Until then, treat this URL as educational.</p>
      <h2>What usually matters</h2>
      <ul>
        <li>A complete Google Business Profile that follows current category rules</li>
        <li>Pages for the location people actually visit</li>
        <li>Reviews that are real</li>
        <li>No doorway spam across nearby towns</li>
      </ul>
    </div></section>
    """
    page(out="case-studies/dispensary-seo/index.html", title="Dispensary SEO | Grand Junction | Nick Perry Digital", description="Educational notes on dispensary SEO in Grand Junction. Not a fabricated client case study.", keyword="dispensary seo grand junction", depth=d, current="results", body=disp, canonical="/case-studies/dispensary-seo/")


def build_404() -> None:
    d = 0
    body = f"""
    {hero(d, "orbit", "404", "This page is missing", "The link may be old, or the page has not been built yet. Try the home page, services, or contact.")}
    <section class="section section-ivory"><div class="wrap actions">
      <a class="btn-ghost" href="index.html">Home</a>
      <a class="btn-ghost" href="contact/">Contact</a>
    </div></section>
    """
    page(out="404.html", title="Page not found | Nick Perry Digital", description="Missing page.", keyword="404", depth=d, current="home", body=body, canonical="/404.html")


def write_support_files() -> None:
    urls = "\n".join(
        f"  <url><loc>https://nickperrydigital.com{p['slug']}</loc></url>"
        for p in PAGES
        if p["slug"] != "/404.html"
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: https://nickperrydigital.com/sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / ".htaccess").write_text(
        "DirectoryIndex index.html\nErrorDocument 404 /404.html\nOptions -MultiViews\nRewriteEngine On\nRewriteCond %{REQUEST_FILENAME} !-f\nRewriteCond %{REQUEST_FILENAME} !-d\nRewriteCond %{REQUEST_FILENAME}.html -f\nRewriteRule ^(.*)$ $1.html [L]\n",
        encoding="utf-8",
    )
    (ROOT / "package.json").write_text(
        json.dumps(
            {
                "name": "nickperrydigital",
                "private": True,
                "description": "Static HTML + Tailwind + Decap CMS site for Hostinger Git deploy.",
                "scripts": {"build": "python3 scripts/build_site.py", "cms": "npx decap-server"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    inventory = ROOT / "content" / "page-inventory.json"
    inventory.write_text(json.dumps(PAGES, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    build_home()
    build_about()
    build_nick()
    build_pricing()
    build_results()
    build_services_hub()
    build_contact()
    build_legal()
    build_awards()
    build_insights()
    build_services()
    build_locations()
    build_money()
    build_case_studies()
    build_404()
    write_support_files()
    print(f"Wrote {len(PAGES)} pages")
    for p in PAGES:
        print(f"{p['slug']}\t{p['title']}\t{p['keyword']}")


if __name__ == "__main__":
    main()





