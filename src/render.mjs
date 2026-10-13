import { md } from "./content.mjs";

export function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[char]));
}

export function money(amount) {
  return `$${Number(amount).toLocaleString("en-US")}`;
}

function jsonLd(data) {
  return JSON.stringify(data).replace(/</g, "\\u003c");
}

function safeHttpUrl(value) {
  if (!value) return "";
  try {
    const url = new URL(value);
    if (url.protocol === "https:" || url.protocol === "http:") return url.href;
  } catch {
    return "";
  }
  return "";
}

function telHref(value) {
  const clean = String(value || "").replace(/[^\d+]/g, "");
  return clean ? `tel:${clean}` : "/contact/";
}

const NAV = [
  { id: "about", href: "/about/", label: "About" },
  { id: "pricing", href: "/pricing/", label: "Pricing" },
  { id: "results", href: "/results/", label: "Results" },
  { id: "services", href: "/services/", label: "Services" },
  { id: "contact", href: "/contact/", label: "Contact" },
];

function sectionFromRoute(route) {
  if (route.startsWith("/about")) return "about";
  if (route.startsWith("/pricing")) return "pricing";
  if (route.startsWith("/results") || route.startsWith("/case-studies")) return "results";
  if (route.startsWith("/services")) return "services";
  if (route.startsWith("/contact")) return "contact";
  if (route.startsWith("/blog")) return "blog";
  if (route.startsWith("/locations")) return "locations";
  return "";
}

function iconCheck() {
  return `<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M7.6 13.2 4.4 10l-1.2 1.2 4.4 4.4L17 6.2 15.8 5z"/></svg>`;
}

function markCell(on) {
  if (on) {
    return `<span class="inline-flex text-pine">${iconCheck()}<span class="sr-only">Included</span></span>`;
  }
  return `<span class="text-sm text-muted"><span class="sr-only">Not included</span><span aria-hidden="true">No</span></span>`;
}

function portrait(data, { eager = false, className = "" } = {}) {
  const alt = "Nick Perry, stencil portrait";
  if (!data.hasPortrait) {
    return `<div class="grid aspect-[4/5] place-items-center rounded-3xl bg-pine text-paper ${className}">
      <div class="px-6 text-center">
        <p class="font-serif text-5xl">NP</p>
        <p class="mt-3 text-sm leading-relaxed text-paper/80">Nick Perry</p>
      </div>
    </div>`;
  }
  const loading = eager ? "eager" : "lazy";
  const priority = eager ? ' fetchpriority="high"' : "";
  const source = data.hasWebp
    ? `<source srcset="/assets/img/nick-perry.webp" type="image/webp" />`
    : "";
  return `<picture>
    ${source}
    <img src="/assets/img/nick-perry.png" alt="${esc(alt)}" width="960" height="1200" class="aspect-[4/5] w-full rounded-3xl object-cover object-[center_18%] ${className}" loading="${loading}"${priority} />
  </picture>`;
}

function crumbs(items) {
  if (!items || !items.length) return "";
  const html = items
    .map((item, index) => {
      const last = index === items.length - 1;
      const inner = last
        ? `<span aria-current="page">${esc(item.label)}</span>`
        : `<a class="underline decoration-pine/30 underline-offset-2 hover:decoration-pine" href="${esc(item.href)}">${esc(item.label)}</a>`;
      return `<li class="inline">${index ? '<span aria-hidden="true"> / </span>' : ""}${inner}</li>`;
    })
    .join("");
  return `<nav aria-label="Breadcrumb" class="text-sm text-muted"><ol class="flex flex-wrap gap-x-1">${html}</ol></nav>`;
}

function crumbSchema(items, domain) {
  if (!items || items.length < 2) return null;
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label,
      item: new URL(item.href, domain).href,
    })),
  };
}

function faqSchema(faqs) {
  if (!faqs || !faqs.length) return null;
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((faq) => ({
      "@type": "Question",
      name: faq.q,
      acceptedAnswer: { "@type": "Answer", text: faq.a },
    })),
  };
}

function localBusiness(data) {
  const { settings, locations } = data;
  const domain = settings.domain.replace(/\/$/, "");
  const offers = [
    {
      "@type": "Offer",
      name: settings.websiteBuild.name,
      price: String(settings.websiteBuild.price),
      priceCurrency: "USD",
      description: settings.websiteBuild.summary,
    },
    ...settings.plans.map((plan) => ({
      "@type": "Offer",
      name: plan.name,
      price: String(plan.price),
      priceCurrency: "USD",
      description: plan.summary,
      priceSpecification: {
        "@type": "UnitPriceSpecification",
        price: String(plan.price),
        priceCurrency: "USD",
        unitText: "MONTH",
      },
    })),
    {
      "@type": "Offer",
      name: settings.carePlan.name,
      price: String(settings.carePlan.price),
      priceCurrency: "USD",
      description: settings.carePlan.summary,
      priceSpecification: {
        "@type": "UnitPriceSpecification",
        price: String(settings.carePlan.price),
        priceCurrency: "USD",
        unitText: "MONTH",
      },
    },
  ];
  return {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    name: settings.siteName,
    url: domain + "/",
    image: data.hasPortrait ? `${domain}/assets/img/nick-perry.png` : `${domain}/assets/favicon.svg`,
    telephone: settings.phoneTel,
    email: settings.email,
    description: settings.description,
    priceRange: settings.priceRange,
    founder: { "@type": "Person", name: settings.personName },
    address: {
      "@type": "PostalAddress",
      addressRegion: settings.addressRegion,
      addressCountry: settings.addressCountry,
    },
    areaServed: locations.map((town) => ({
      "@type": "City",
      name: `${town.name}, Colorado`,
    })),
    makesOffer: offers,
  };
}

function faqBlock(faqs) {
  const items = faqs
    .map(
      (faq) => `<details class="group border-b border-line py-4">
        <summary class="cursor-pointer list-none font-semibold text-ink [&::-webkit-details-marker]:hidden">
          <span class="flex items-start justify-between gap-4">${esc(faq.q)}<span aria-hidden="true" class="text-pine group-open:rotate-45">+</span></span>
        </summary>
        <p class="mt-3 leading-relaxed text-muted">${esc(faq.a)}</p>
      </details>`
    )
    .join("");
  return `<div>${items}</div>`;
}

function ctaButtons(settings, light = false) {
  const primary = light ? "btn-light" : "btn";
  const secondary = light
    ? "btn-ghost border-paper text-paper hover:bg-paper hover:text-pine"
    : "btn-ghost";
  return `<div class="flex flex-wrap gap-3">
    <a class="${primary}" href="${esc(settings.ctaHref)}">${esc(settings.ctaLabel)}</a>
    <a class="${secondary}" href="${telHref(settings.phoneTel)}">Call ${esc(settings.phoneDisplay)}</a>
  </div>`;
}

function layout(data, page) {
  const { settings } = data;
  const domain = settings.domain.replace(/\/$/, "");
  const canonical = new URL(page.route, domain + "/").href;
  const active = sectionFromRoute(page.route);
  const phone = telHref(settings.phoneTel);
  const navLinks = NAV.map((item) => {
    const current = item.id === active ? ' aria-current="page"' : "";
    const cls = item.id === active ? "text-pine" : "text-ink hover:text-pine";
    return `<a class="text-sm font-semibold ${cls}" href="${item.href}"${current}>${item.label}</a>`;
  }).join("");
  const mobileLinks = NAV.map((item) => {
    const current = item.id === active ? ' aria-current="page"' : "";
    return `<a class="block py-2 text-base font-semibold" href="${item.href}"${current}>${item.label}</a>`;
  }).join("");

  const serviceLinks = data.services
    .map(
      (service) =>
        `<li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/services/${esc(service.slug)}/">${esc(service.menuTitle || service.title)}</a></li>`
    )
    .join("");
  const workLinks = [
    `<li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/results/">All results</a></li>`,
    ...data.caseStudies.map(
      (study) =>
        `<li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/case-studies/${esc(study.slug)}/">${esc(study.title)}</a></li>`
    ),
  ].join("");
  const areaLinks = data.locations
    .map(
      (town) =>
        `<li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/locations/${esc(town.slug)}/">${esc(town.name)}</a></li>`
    )
    .join("");

  const schemas = [localBusiness(data), ...(page.schemas || [])].filter(Boolean);
  const schemaTags = schemas
    .map((schema) => `<script type="application/ld+json">${jsonLd(schema)}</script>`)
    .join("");
  const robots = page.noindex ? "noindex, follow" : "index, follow";
  const ogImage = data.hasPortrait ? `${domain}/assets/img/nick-perry.png` : `${domain}/assets/favicon.svg`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${esc(page.title)}</title>
  <meta name="description" content="${esc(page.description)}" />
  <link rel="canonical" href="${esc(canonical)}" />
  <meta name="robots" content="${robots}" />
  <meta name="theme-color" content="#1f4d3a" />
  <meta property="og:title" content="${esc(page.title)}" />
  <meta property="og:description" content="${esc(page.description)}" />
  <meta property="og:type" content="${page.ogType || "website"}" />
  <meta property="og:url" content="${esc(canonical)}" />
  <meta property="og:image" content="${esc(ogImage)}" />
  <meta property="og:site_name" content="${esc(settings.siteName)}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="/assets/css/site.css" />
  ${schemaTags}
</head>
<body>
  <a class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-white focus:px-4 focus:py-2" href="#content">Skip to content</a>
  <div class="h-1 bg-pine"></div>
  <header class="sticky top-0 z-40 border-b border-line bg-paper/95 backdrop-blur">
    <div class="wrap flex items-center justify-between gap-4 py-3">
      <a href="/" class="no-underline" aria-label="${esc(settings.siteName)} home">
        <span class="block font-serif text-xl leading-none tracking-tight text-ink">Nick Perry</span>
        <span class="mt-1 block text-[11px] font-semibold uppercase tracking-[0.22em] text-pine">Digital</span>
      </a>
      <nav class="hidden items-center gap-6 xl:flex" aria-label="Primary">
        ${navLinks}
        <a class="text-sm font-semibold text-pine" href="${phone}" title="Placeholder phone number">${esc(settings.phoneDisplay)}</a>
      </nav>
      <div class="flex items-center gap-3 xl:hidden">
        <a class="text-sm font-semibold text-pine" href="${phone}">Call</a>
        <button id="menu-btn" class="rounded-full border border-line px-3 py-1.5 text-sm font-semibold" type="button" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
      </div>
    </div>
    <div id="mobile-nav" class="wrap hidden border-t border-line pb-4 xl:hidden" hidden>
      <nav aria-label="Mobile">
        ${mobileLinks}
        <a class="mt-2 inline-block font-semibold text-pine" href="${phone}">${esc(settings.phoneDisplay)}</a>
      </nav>
    </div>
  </header>
  <main id="content">
    ${page.body}
  </main>
  <section class="bg-pine text-paper" aria-labelledby="ready-heading">
    <div class="wrap flex flex-col gap-6 py-14 md:flex-row md:items-end md:justify-between">
      <div class="max-w-xl">
        <h2 id="ready-heading" class="font-serif text-4xl tracking-tight">Ready to Grow?</h2>
        <p class="mt-3 text-lg leading-relaxed text-paper/85">${esc(settings.ctaBandText)}</p>
      </div>
      ${ctaButtons(settings, true)}
    </div>
  </section>
  <footer class="bg-ink text-paper">
    <div class="wrap grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <h2 class="font-serif text-xl">Company</h2>
        <ul class="mt-4 space-y-2">
          <li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/about/">About</a></li>
          <li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/pricing/">Pricing</a></li>
          <li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/results/">Results</a></li>
          <li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/blog/">Blog</a></li>
          <li><a class="text-sm text-paper/80 no-underline hover:text-white hover:underline" href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2 class="font-serif text-xl">Services</h2>
        <ul class="mt-4 space-y-2">${serviceLinks}</ul>
      </div>
      <div>
        <h2 class="font-serif text-xl">Our Work</h2>
        <ul class="mt-4 space-y-2">${workLinks}</ul>
      </div>
      <div>
        <h2 class="font-serif text-xl">Areas We Serve</h2>
        <ul class="mt-4 space-y-2">${areaLinks}</ul>
      </div>
    </div>
    <div class="border-t border-white/10">
      <div class="wrap flex flex-col gap-3 py-6 text-sm text-paper/70 md:flex-row md:items-center md:justify-between">
        <p>${esc(settings.siteName)}. ${esc(settings.region)}. Phone, email, and the booking link are placeholders until they are updated in site settings.</p>
        <p class="flex gap-4">
          <a class="text-paper/80 underline decoration-white/30 underline-offset-2 hover:text-white" href="/privacy/">Privacy</a>
          <a class="text-paper/80 underline decoration-white/30 underline-offset-2 hover:text-white" href="/terms/">Terms</a>
        </p>
      </div>
    </div>
  </footer>
  <script>
    (function () {
      var btn = document.getElementById("menu-btn");
      var panel = document.getElementById("mobile-nav");
      if (!btn || !panel) return;
      btn.addEventListener("click", function () {
        var open = panel.hasAttribute("hidden");
        if (open) {
          panel.removeAttribute("hidden");
          panel.classList.remove("hidden");
          btn.setAttribute("aria-expanded", "true");
        } else {
          panel.setAttribute("hidden", "");
          panel.classList.add("hidden");
          btn.setAttribute("aria-expanded", "false");
        }
      });
    })();
  </script>
</body>
</html>
`;
}

function pageShell(data, opts) {
  const domain = data.settings.domain.replace(/\/$/, "");
  const schemas = [...(opts.schemas || [])];
  const crumbLd = crumbSchema(opts.crumbs, domain);
  if (crumbLd) schemas.push(crumbLd);
  return {
    route: opts.route,
    title: opts.title,
    description: opts.description,
    html: layout(data, {
      ...opts,
      schemas,
      body: opts.body,
    }),
  };
}

function serviceBySlug(data, slug) {
  return data.services.find((service) => service.slug === slug);
}

function studyCard(study) {
  return `<article class="card flex h-full flex-col">
    <p class="badge">Placeholder</p>
    <h3 class="mt-4 font-serif text-2xl leading-snug"><a class="text-ink no-underline hover:text-pine" href="/case-studies/${esc(study.slug)}/">${esc(study.title)}</a></h3>
    <p class="mt-2 text-sm font-semibold text-pine">${esc(study.industry)} · ${esc(study.region)}</p>
    <p class="mt-3 flex-1 leading-relaxed text-muted">${esc(study.summary)}</p>
    <a class="mt-4 text-sm font-semibold text-pine no-underline hover:underline" href="/case-studies/${esc(study.slug)}/">View the layout</a>
  </article>`;
}

function costFaqs(town, settings) {
  const build = money(settings.websiteBuild.price);
  const base = money(settings.plans[0].price);
  const ai = money(settings.plans[1].price);
  const care = money(settings.carePlan.price);
  const shared = [
    {
      q: `How much does a website or SEO cost for a ${town.name} business?`,
      a: `A standard website build is ${build}. That includes an SEO-ready site, Google Business Profile setup, and 90 days of SEO. Monthly support is ${base} for GBP + Website, or ${ai} for GBP + Website + AI Search. The care plan is ${care} a month and it is optional. Google Ads management, a larger website, and logo work are custom quotes. There is no long-term contract.`,
    },
    {
      q: `How long does the work usually take to show movement in ${town.name}?`,
      a: `Listing cleanup and a new site can change what people see within a few weeks. Rankings and calls usually take longer. The 90 days of SEO after a build are there so launch day is not the end of the work. I will not promise a week-one ranking.`,
    },
    {
      q: "Do I have to keep the care plan?",
      a: `No. The ${care} care plan is optional after the included 90 days. It covers hosting, security updates, software updates, and small edits. You can take the site with you. You own the site, the domain, and the content.`,
    },
    {
      q: "Will you guarantee the top spot on Google or a mention in ChatGPT?",
      a: "No. I can control the site, the listing, the citations, and the reporting. I cannot control Google or an AI product. If someone promises a specific rank or a guaranteed chatbot mention, treat that as a sales line, not a plan.",
    },
  ];
  if (town.slug === "grand-junction") {
    shared.splice(1, 0, {
      q: "Do I need a separate Google listing for each nearby town?",
      a: "No. One real location gets one Google Business Profile. If you serve Fruita, Palisade, Clifton, or the Redlands, set the service area and publish pages that tell the truth about that work. Duplicate listings for towns where you have no office are a good way to get the profile suspended.",
    });
  } else {
    shared.splice(1, 0, {
      q: `Do you actually work in ${town.name}, or only in Grand Junction?`,
      a: `I work with businesses on Colorado's Western Slope, including ${town.name} in ${town.county}. ${town.near} You do not need a Grand Junction storefront to hire me.`,
    });
  }
  if (town.extraQ && town.extraA) {
    shared.push({ q: town.extraQ, a: town.extraA });
  }
  return shared;
}

function renderHome(data) {
  const { settings, home, services, locations, caseStudies } = data;
  const featured = caseStudies.find((study) => study.featured) || caseStudies[0];
  const serviceCards = services
    .map(
      (service) => `<article class="card">
        <h3 class="font-serif text-2xl leading-snug"><a class="text-ink no-underline hover:text-pine" href="/services/${esc(service.slug)}/">${esc(service.title)}</a></h3>
        <p class="mt-3 leading-relaxed text-muted">${esc(service.summary)}</p>
      </article>`
    )
    .join("");
  const towns = locations
    .map(
      (town) =>
        `<a class="rounded-full border border-line bg-card px-3 py-1.5 text-sm font-semibold text-ink no-underline hover:border-pine hover:text-pine" href="/locations/${esc(town.slug)}/">${esc(town.name)}</a>`
    )
    .join("");
  const guarantees = settings.guarantees
    .map(
      (item, index) => `<li class="flex gap-4 border-t border-line py-4">
        <span class="font-serif text-2xl text-pine">${index + 1}</span>
        <p class="leading-relaxed">${esc(item)}</p>
      </li>`
    )
    .join("");
  const studies = caseStudies.map(studyCard).join("");
  const body = `
    <section class="wrap grid items-center gap-12 py-14 lg:grid-cols-2 lg:py-20">
      <div>
        <p class="kicker">${esc(home.heroEyebrow)}</p>
        <h1 class="display mt-3">${esc(home.heroTitle)}</h1>
        <p class="lede mt-5">${esc(home.heroText)}</p>
        <div class="mt-8">${ctaButtons(settings)}</div>
      </div>
      <div class="relative">
        <div class="absolute -left-4 top-6 hidden h-full w-full rounded-3xl bg-pine/15 lg:block" aria-hidden="true"></div>
        <div class="relative">${portrait(data, { eager: true })}</div>
      </div>
    </section>
    <section class="border-y border-line bg-card" aria-labelledby="press-heading">
      <div class="wrap py-8">
        <h2 id="press-heading" class="kicker">${esc(home.pressTitle)}</h2>
        <p class="mt-3 max-w-3xl text-muted">${esc(home.pressText)}</p>
      </div>
    </section>
    <section class="wrap grid gap-8 py-16 lg:grid-cols-[1.2fr_0.8fr] lg:items-start">
      <div>
        <h2 class="h2">${esc(home.introTitle)}</h2>
        <div class="prose-np mt-4 text-muted">${md(home.introText)}</div>
      </div>
      <aside class="card">
        <p class="kicker">Published prices</p>
        <ul class="mt-4 space-y-3 text-sm leading-relaxed">
          <li><span class="font-semibold text-ink">Website build ${money(settings.websiteBuild.price)}.</span> SEO-ready site, Google Business Profile setup, and 90 days of SEO.</li>
          <li><span class="font-semibold text-ink">${esc(settings.plans[0].name)} ${money(settings.plans[0].price)}/mo.</span></li>
          <li><span class="font-semibold text-ink">${esc(settings.plans[1].name)} ${money(settings.plans[1].price)}/mo.</span></li>
          <li><span class="font-semibold text-ink">Care plan ${money(settings.carePlan.price)}/mo.</span> Optional. No long-term contract.</li>
        </ul>
        <a class="mt-5 inline-block text-sm font-semibold text-pine no-underline hover:underline" href="/pricing/">See the full pricing page</a>
      </aside>
    </section>
    <section class="bg-card py-16" aria-labelledby="services-heading">
      <div class="wrap">
        <h2 id="services-heading" class="h2">${esc(home.servicesTitle)}</h2>
        <p class="lede mt-4 max-w-3xl">${esc(home.servicesText)}</p>
        <div class="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">${serviceCards}</div>
      </div>
    </section>
    <section class="wrap py-16" aria-labelledby="towns-heading">
      <h2 id="towns-heading" class="h2">${esc(home.townsTitle)}</h2>
      <p class="lede mt-4 max-w-3xl">${esc(home.townsText)}</p>
      <div class="mt-6 flex flex-wrap gap-2">${towns}</div>
    </section>
    <section class="border-y border-line bg-card py-16" aria-labelledby="guarantee-heading">
      <div class="wrap max-w-3xl">
        <h2 id="guarantee-heading" class="h2">${esc(home.guaranteesTitle)}</h2>
        <p class="lede mt-4">${esc(home.guaranteesText)}</p>
        <ol class="mt-6">${guarantees}</ol>
      </div>
    </section>
    <section class="wrap py-16" aria-labelledby="results-heading">
      <h2 id="results-heading" class="h2">${esc(home.resultsTitle)}</h2>
      <p class="lede mt-4 max-w-3xl">${esc(home.resultsText)}</p>
      <div class="mt-8 max-w-xl">${featured ? studyCard(featured) : ""}</div>
    </section>
    <section class="bg-card py-16" aria-labelledby="praise-heading">
      <div class="wrap grid gap-10 lg:grid-cols-2">
        <div>
          <h2 id="praise-heading" class="h2">${esc(home.praiseTitle)}</h2>
          <p class="lede mt-4">${esc(home.praiseText)}</p>
        </div>
        <div>
          <h2 class="h2">${esc(home.trustedTitle)}</h2>
          <p class="lede mt-4">${esc(home.trustedText)}</p>
        </div>
      </div>
    </section>
    <section class="wrap py-16" aria-labelledby="featured-heading">
      <h2 id="featured-heading" class="h2">${esc(home.featuredTitle)}</h2>
      <p class="lede mt-4 max-w-3xl">${esc(home.featuredText)}</p>
      <div class="mt-8 grid gap-4 md:grid-cols-3">${studies}</div>
    </section>`;
  return pageShell(data, {
    route: "/",
    title: home.metaTitle,
    description: home.metaDescription,
    body,
  });
}

function renderPricing(data) {
  const { settings } = data;
  const build = settings.websiteBuild;
  const care = settings.carePlan;
  const planCards = settings.plans
    .map((plan) => {
      const ring = plan.featured ? "border-pine ring-1 ring-pine" : "";
      return `<article class="card flex h-full flex-col ${ring}">
        ${plan.featured ? '<p class="badge">AI search included</p>' : '<p class="kicker">Monthly</p>'}
        <h3 class="mt-3 font-serif text-2xl">${esc(plan.name)}</h3>
        <p class="mt-4 font-serif text-5xl tracking-tight">${money(plan.price)}</p>
        <p class="text-sm text-muted">per month</p>
        <p class="mt-4 leading-relaxed text-muted">${esc(plan.summary)}</p>
        <p class="mt-4 text-sm"><span class="font-semibold">Best for:</span> ${esc(plan.bestFor)}</p>
        <a class="btn mt-6 w-fit" href="${esc(settings.ctaHref)}">${esc(settings.ctaLabel)}</a>
      </article>`;
    })
    .join("");
  const rows = settings.comparisonGroups
    .map((group) => {
      const head = `<tr class="bg-paper"><th colspan="3" class="px-3 py-3 text-left font-serif text-lg">${esc(group.title)}</th></tr>`;
      const body = group.rows
        .map(
          (row) => `<tr class="border-t border-line">
            <th scope="row" class="px-3 py-3 font-medium">${esc(row.label)}</th>
            <td class="px-3 py-3 text-center">${markCell(row.foundation)}</td>
            <td class="px-3 py-3 text-center">${markCell(row.ai)}</td>
          </tr>`
        )
        .join("");
      return head + body;
    })
    .join("");
  const addons = settings.addons
    .map(
      (addon) => `<article class="card">
        <h3 class="font-serif text-xl">${esc(addon.name)}</h3>
        <p class="mt-2 text-sm font-semibold text-pine">Custom quote</p>
        <p class="mt-3 leading-relaxed text-muted">${esc(addon.note)}</p>
      </article>`
    )
    .join("");
  const guarantees = settings.guarantees
    .map((item) => `<li class="border-t border-line py-3 leading-relaxed">${esc(item)}</li>`)
    .join("");
  const includes = build.includes.map((item) => `<li>${esc(item)}</li>`).join("");
  const careItems = care.includes.map((item) => `<li>${esc(item)}</li>`).join("");
  const body = `
    <section class="wrap py-14">
      ${crumbs([{ href: "/", label: "Home" }, { href: "/pricing/", label: "Pricing" }])}
      <h1 class="display mt-4">Pricing</h1>
      <p class="lede mt-4 max-w-3xl">${esc(settings.pricingIntro)}</p>
      <p class="mt-4 max-w-3xl font-semibold text-ink">No long-term contracts. Monthly plans stop at the end of a month.</p>
    </section>
    <section class="wrap pb-6" aria-labelledby="build-heading">
      <article class="rounded-3xl bg-pine p-8 text-paper md:p-10">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-paper/70">One-time</p>
        <div class="mt-3 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 id="build-heading" class="font-serif text-4xl">${esc(build.name)}</h2>
            <p class="mt-3 max-w-xl text-lg text-paper/85">${esc(build.summary)}</p>
          </div>
          <p class="font-serif text-6xl tracking-tight">${money(build.price)}</p>
        </div>
        <ul class="mt-6 grid gap-2 text-sm md:grid-cols-2">${includes}</ul>
      </article>
    </section>
    <section class="wrap grid gap-4 py-8 lg:grid-cols-2" aria-label="Monthly plans">
      ${planCards}
    </section>
    <section class="wrap py-8" aria-labelledby="compare-heading">
      <h2 id="compare-heading" class="h2">What the monthly plans include</h2>
      <div class="mt-6 overflow-x-auto rounded-2xl border border-line bg-card">
        <table class="w-full min-w-[640px] border-collapse text-left text-sm">
          <caption class="sr-only">Comparison of the two monthly plans</caption>
          <thead>
            <tr class="border-b border-line">
              <th class="px-3 py-3">Included work</th>
              <th class="px-3 py-3 text-center">${esc(settings.plans[0].name)}<br />${money(settings.plans[0].price)}/mo</th>
              <th class="px-3 py-3 text-center">${esc(settings.plans[1].name)}<br />${money(settings.plans[1].price)}/mo</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
      <p class="mt-4 text-sm leading-relaxed text-muted">${esc(settings.comparisonNote)}</p>
    </section>
    <section class="wrap py-8" aria-labelledby="addons-heading">
      <h2 id="addons-heading" class="h2">Add-ons</h2>
      <p class="lede mt-3 max-w-3xl">These are not bundled into the posted prices. Each one is a custom quote.</p>
      <div class="mt-6 grid gap-4 md:grid-cols-3">${addons}</div>
    </section>
    <section class="wrap grid gap-6 py-8 lg:grid-cols-[1.2fr_0.8fr]" aria-labelledby="care-heading">
      <div>
        <h2 id="care-heading" class="h2">${esc(care.name)}: ${money(care.price)} a month</h2>
        <p class="lede mt-3">${esc(care.summary)}</p>
        <ul class="mt-4 list-disc space-y-2 pl-5">${careItems}</ul>
      </div>
      <div class="card">
        <h2 class="font-serif text-2xl">Guarantees</h2>
        <ul class="mt-4">${guarantees}</ul>
      </div>
    </section>`;
  return pageShell(data, {
    route: "/pricing/",
    title: "Pricing | Nick Perry Digital",
    description: settings.pricingMetaDescription,
    crumbs: [
      { href: "/", label: "Home" },
      { href: "/pricing/", label: "Pricing" },
    ],
    body,
  });
}

function renderProsePage(data, page, route, extra = "") {
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: route, label: page.title },
  ];
  const portraitBlock =
    page.layout === "portrait"
      ? `<aside class="order-first lg:sticky lg:top-24 lg:order-none">${portrait(data)}<p class="mt-3 text-sm text-muted">Nick Perry</p></aside>`
      : "";
  const grid = page.layout === "portrait" ? "lg:grid-cols-[minmax(0,1fr)_280px]" : "";
  const body = `
    <section class="wrap py-14">
      ${crumbs(crumbsItems)}
      <div class="mt-6 grid gap-10 ${grid}">
        <article class="prose-np">
          <h1 class="display">${esc(page.title)}</h1>
          ${page.html}
          ${extra}
        </article>
        ${portraitBlock}
      </div>
    </section>`;
  return pageShell(data, {
    route,
    title: page.metaTitle || `${page.title} | Nick Perry Digital`,
    description: page.metaDescription || page.description || "",
    crumbs: crumbsItems,
    body,
  });
}

function renderServicesHub(data) {
  const intro = data.pages.services;
  const cards = data.services
    .map(
      (service) => `<article class="card flex h-full flex-col">
        <h2 class="font-serif text-2xl"><a class="text-ink no-underline hover:text-pine" href="/services/${esc(service.slug)}/">${esc(service.title)}</a></h2>
        <p class="mt-3 flex-1 leading-relaxed text-muted">${esc(service.summary)}</p>
        <a class="mt-4 text-sm font-semibold text-pine no-underline hover:underline" href="/services/${esc(service.slug)}/">Read the service page</a>
      </article>`
    )
    .join("");
  const body = `
    <section class="wrap py-14">
      ${crumbs([{ href: "/", label: "Home" }, { href: "/services/", label: "Services" }])}
      <h1 class="display mt-4">${esc(intro.title)}</h1>
      <div class="prose-np mt-4 max-w-3xl">${intro.html}</div>
      <div class="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">${cards}</div>
    </section>`;
  return pageShell(data, {
    route: "/services/",
    title: intro.metaTitle,
    description: intro.metaDescription,
    crumbs: [
      { href: "/", label: "Home" },
      { href: "/services/", label: "Services" },
    ],
    body,
  });
}

function renderService(data, service) {
  const gets = (service.gets || []).map((item) => `<li>${esc(item)}</li>`).join("");
  const steps = (service.steps || [])
    .map(
      (step, index) => `<li class="card">
        <p class="kicker">Step ${index + 1}</p>
        <h3 class="mt-2 font-serif text-xl">${esc(step.title)}</h3>
        <p class="mt-2 leading-relaxed text-muted">${esc(step.text)}</p>
      </li>`
    )
    .join("");
  const pairs = (service.pairs || [])
    .map((slug) => serviceBySlug(data, slug))
    .filter(Boolean)
    .map(
      (item) =>
        `<a class="rounded-full border border-line px-3 py-1.5 text-sm font-semibold no-underline hover:border-pine hover:text-pine" href="/services/${esc(item.slug)}/">${esc(item.menuTitle || item.title)}</a>`
    )
    .join("");
  const faqs = service.faqs || [];
  const route = `/services/${service.slug}/`;
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: "/services/", label: "Services" },
    { href: route, label: service.title },
  ];
  const body = `
    <section class="wrap py-14">
      ${crumbs(crumbsItems)}
      <p class="kicker mt-6">Service</p>
      <h1 class="display mt-3">${esc(service.title)}</h1>
      <p class="lede mt-4 max-w-3xl">${esc(service.summary)}</p>
      <div class="prose-np mt-6 max-w-3xl">${service.html}</div>
    </section>
    <section class="bg-card py-14">
      <div class="wrap grid gap-10 lg:grid-cols-2">
        <div>
          <h2 class="h2">What you get</h2>
          <ul class="mt-4 list-disc space-y-2 pl-5 leading-relaxed">${gets}</ul>
        </div>
        <div>
          <h2 class="h2">How it works</h2>
          <ol class="mt-4 grid gap-3">${steps}</ol>
        </div>
      </div>
    </section>
    <section class="wrap py-14">
      <h2 class="h2">Often paired with</h2>
      <div class="mt-4 flex flex-wrap gap-2">${pairs}</div>
      <p class="mt-6 text-sm text-muted">Posted prices live on the <a class="font-semibold text-pine" href="/pricing/">pricing page</a>.</p>
    </section>
    <section class="wrap max-w-3xl pb-16" aria-labelledby="faq-heading">
      <h2 id="faq-heading" class="h2">${esc(service.title)} questions</h2>
      <div class="mt-4">${faqBlock(faqs)}</div>
    </section>`;
  const serviceSchema = {
    "@context": "https://schema.org",
    "@type": "Service",
    name: service.title,
    description: service.summary,
    provider: { "@type": "ProfessionalService", name: data.settings.siteName },
    areaServed: data.settings.region,
    url: new URL(route, data.settings.domain).href,
  };
  return pageShell(data, {
    route,
    title: service.metaTitle,
    description: service.metaDescription,
    crumbs: crumbsItems,
    schemas: [serviceSchema, faqSchema(faqs)],
    body,
  });
}

function renderLocationsHub(data) {
  const intro = data.pages.locations;
  const cards = data.locations
    .map(
      (town) => `<article class="card">
        <h2 class="font-serif text-2xl"><a class="text-ink no-underline hover:text-pine" href="/locations/${esc(town.slug)}/">${esc(town.name)}, CO</a></h2>
        <p class="mt-2 text-sm font-semibold text-pine">${esc(town.county)}</p>
        <p class="mt-3 leading-relaxed text-muted">${esc(town.card)}</p>
      </article>`
    )
    .join("");
  const body = `
    <section class="wrap py-14">
      ${crumbs([{ href: "/", label: "Home" }, { href: "/locations/", label: "Areas we serve" }])}
      <h1 class="display mt-4">${esc(intro.title)}</h1>
      <div class="prose-np mt-4 max-w-3xl">${intro.html}</div>
      <div class="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">${cards}</div>
    </section>`;
  return pageShell(data, {
    route: "/locations/",
    title: intro.metaTitle,
    description: intro.metaDescription,
    crumbs: [
      { href: "/", label: "Home" },
      { href: "/locations/", label: "Areas we serve" },
    ],
    body,
  });
}

function renderLocation(data, town) {
  const faqs = costFaqs(town, data.settings);
  const route = `/locations/${town.slug}/`;
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: "/locations/", label: "Areas we serve" },
    { href: route, label: town.name },
  ];
  const businesses = (town.businesses || []).map((item) => `<li>${esc(item)}</li>`).join("");
  const build = data.settings.websiteBuild;
  const care = data.settings.carePlan;
  const body = `
    <section class="wrap py-14">
      ${crumbs(crumbsItems)}
      <p class="kicker mt-6">${esc(town.county)}</p>
      <h1 class="display mt-3">Websites and local SEO in ${esc(town.name)}, Colorado</h1>
      <div class="prose-np mt-6 max-w-3xl">${town.html}</div>
    </section>
    <section class="bg-card py-14">
      <div class="wrap grid gap-8 lg:grid-cols-2">
        <div>
          <h2 class="h2">Businesses this usually fits</h2>
          <p class="mt-3 leading-relaxed text-muted">These are the kinds of companies that tend to need the work. They are not a client list.</p>
          <ul class="mt-4 list-disc space-y-2 pl-5">${businesses}</ul>
        </div>
        <div>
          <h2 class="h2">What it costs in ${esc(town.name)}</h2>
          <ul class="mt-4 space-y-3 leading-relaxed">
            <li><span class="font-semibold">${esc(build.name)}, ${money(build.price)} once.</span> ${esc(build.summary)}</li>
            <li><span class="font-semibold">${esc(data.settings.plans[0].name)}, ${money(data.settings.plans[0].price)} a month.</span></li>
            <li><span class="font-semibold">${esc(data.settings.plans[1].name)}, ${money(data.settings.plans[1].price)} a month.</span></li>
            <li><span class="font-semibold">${esc(care.name)}, ${money(care.price)} a month, optional.</span> ${esc(care.summary)}</li>
            <li>Add-ons, including Google Ads management, a larger site, and logo work, are a custom quote.</li>
            <li>No long-term contract.</li>
          </ul>
          <a class="mt-5 inline-block font-semibold text-pine no-underline hover:underline" href="/pricing/">Compare the plans</a>
        </div>
      </div>
    </section>
    <section class="wrap max-w-3xl py-16" aria-labelledby="town-faq">
      <h2 id="town-faq" class="h2">Questions from ${esc(town.name)}</h2>
      <div class="mt-4">${faqBlock(faqs)}</div>
    </section>`;
  return pageShell(data, {
    route,
    title: town.metaTitle,
    description: town.metaDescription,
    crumbs: crumbsItems,
    schemas: [faqSchema(faqs)],
    body,
  });
}

function renderResults(data) {
  const intro = data.pages.results;
  const cards = data.caseStudies.map(studyCard).join("");
  const body = `
    <section class="wrap py-14">
      ${crumbs([{ href: "/", label: "Home" }, { href: "/results/", label: "Results" }])}
      <h1 class="display mt-4">${esc(intro.title)}</h1>
      <div class="prose-np mt-4 max-w-3xl">${intro.html}</div>
      <div class="mt-10 grid gap-4 md:grid-cols-3">${cards}</div>
    </section>`;
  return pageShell(data, {
    route: "/results/",
    title: intro.metaTitle,
    description: intro.metaDescription,
    crumbs: [
      { href: "/", label: "Home" },
      { href: "/results/", label: "Results" },
    ],
    body,
  });
}

function renderCaseStudy(data, study) {
  const route = `/case-studies/${study.slug}/`;
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: "/results/", label: "Results" },
    { href: route, label: study.title },
  ];
  const body = `
    <article class="wrap max-w-3xl py-14">
      ${crumbs(crumbsItems)}
      <p class="badge mt-6">Placeholder project</p>
      <h1 class="display mt-4">${esc(study.title)}</h1>
      <p class="mt-3 text-sm font-semibold text-pine">${esc(study.industry)} · ${esc(study.region)}</p>
      <p class="mt-6 rounded-2xl border border-copper/30 bg-copper/5 p-4 leading-relaxed">This page is a layout sample. It is not a client, not a testimonial, and not a result. Names, quotes, and numbers will be added only when a real project is cleared for publication.</p>
      <h2 class="h2 mt-10">The kind of situation a real story would open with</h2>
      <p class="mt-4 leading-relaxed text-muted">${esc(study.situation)}</p>
      <h2 class="h2 mt-10">What the write-up would cover</h2>
      <p class="mt-4 leading-relaxed text-muted">${esc(study.approach)}</p>
      <h2 class="h2 mt-10">Outcomes</h2>
      <p class="mt-4 leading-relaxed text-muted">${esc(study.outcomeNote)}</p>
      <p class="mt-8"><a class="btn" href="${esc(data.settings.ctaHref)}">${esc(data.settings.ctaLabel)}</a></p>
    </article>`;
  return pageShell(data, {
    route,
    title: study.metaTitle,
    description: study.metaDescription,
    crumbs: crumbsItems,
    body,
  });
}

function renderContact(data) {
  const page = data.pages.contact;
  const { settings } = data;
  const endpoint = safeHttpUrl(settings.formEndpoint);
  const booking = safeHttpUrl(settings.bookingUrl);
  const bookingBlock = booking
    ? `<iframe title="Book a free strategy call" src="${esc(booking)}" class="h-[720px] w-full rounded-2xl border border-line bg-white" loading="lazy"></iframe>`
    : `<div class="card">
        <p class="badge">Placeholder</p>
        <h2 class="mt-3 font-serif text-2xl">Booking calendar</h2>
        <p class="mt-3 leading-relaxed text-muted">The booking link is not set. Add a calendar URL in site settings and this panel becomes the live scheduler. Until then, use the form or the placeholder phone number.</p>
      </div>`;
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: "/contact/", label: "Contact" },
  ];
  const body = `
    <section class="wrap py-14">
      ${crumbs(crumbsItems)}
      <h1 class="display mt-4">${esc(page.title)}</h1>
      <div class="prose-np mt-4 max-w-3xl">${page.html}</div>
      <dl class="mt-8 grid gap-4 sm:grid-cols-2">
        <div class="card">
          <dt class="kicker">Phone placeholder</dt>
          <dd class="mt-2 font-serif text-2xl"><a class="text-ink no-underline hover:text-pine" href="${telHref(settings.phoneTel)}">${esc(settings.phoneDisplay)}</a></dd>
        </div>
        <div class="card">
          <dt class="kicker">Email placeholder</dt>
          <dd class="mt-2 font-serif text-2xl"><a class="text-ink no-underline hover:text-pine" href="mailto:${esc(settings.email)}">${esc(settings.email)}</a></dd>
        </div>
      </dl>
    </section>
    <section class="bg-card py-14">
      <div class="wrap grid gap-10 lg:grid-cols-2">
        <div>
          <h2 class="h2">Send a message</h2>
          <form id="contact-form" class="mt-6 grid gap-4" method="post" action="${endpoint || "#"}">
            <div>
              <label class="text-sm font-semibold" for="name">Name</label>
              <input class="mt-1 w-full rounded-xl border border-line bg-white px-3 py-2" id="name" name="name" type="text" autocomplete="name" required />
            </div>
            <div>
              <label class="text-sm font-semibold" for="email">Email</label>
              <input class="mt-1 w-full rounded-xl border border-line bg-white px-3 py-2" id="email" name="email" type="email" autocomplete="email" required />
            </div>
            <div>
              <label class="text-sm font-semibold" for="message">Message</label>
              <textarea class="mt-1 w-full rounded-xl border border-line bg-white px-3 py-2" id="message" name="message" rows="6" required></textarea>
            </div>
            <p class="hidden" aria-hidden="true">
              <label>Company <input name="company" tabindex="-1" autocomplete="off" /></label>
            </p>
            <button class="btn w-fit" type="submit">Send message</button>
            <p id="form-note" class="text-sm text-muted" role="status"></p>
          </form>
        </div>
        <div id="booking" class="scroll-mt-24">
          <h2 class="h2">Book a free strategy call</h2>
          <p class="mt-3 leading-relaxed text-muted">Pick a time when the calendar is connected. The call is free and there is no contract attached to it.</p>
          <div class="mt-4">${bookingBlock}</div>
        </div>
      </div>
    </section>
    <script>
      (function () {
        var form = document.getElementById("contact-form");
        var note = document.getElementById("form-note");
        var endpoint = ${JSON.stringify(endpoint)};
        if (!form || endpoint) return;
        form.addEventListener("submit", function (event) {
          event.preventDefault();
          if (form.company && form.company.value) return;
          note.textContent = "The contact form is a placeholder until a form address is added in site settings. Email and phone on this page are placeholders too.";
        });
      })();
    </script>`;
  return pageShell(data, {
    route: "/contact/",
    title: page.metaTitle,
    description: page.metaDescription,
    crumbs: crumbsItems,
    body,
  });
}

function renderBlogIndex(data) {
  const posts = data.posts
    .map(
      (post) => `<article class="border-t border-line py-6">
        <p class="text-sm font-semibold text-pine">${esc(post.date)}</p>
        <h2 class="mt-2 font-serif text-2xl"><a class="text-ink no-underline hover:text-pine" href="/blog/${esc(post.slug)}/">${esc(post.title)}</a></h2>
        <p class="mt-2 leading-relaxed text-muted">${esc(post.description)}</p>
      </article>`
    )
    .join("");
  const body = `
    <section class="wrap max-w-3xl py-14">
      ${crumbs([{ href: "/", label: "Home" }, { href: "/blog/", label: "Blog" }])}
      <h1 class="display mt-4">Notes from the Western Slope</h1>
      <p class="lede mt-4">Practical writing about websites, Google Business Profiles, and local search. No client stories are invented here to make a point.</p>
      <div class="mt-8">${posts}</div>
    </section>`;
  return pageShell(data, {
    route: "/blog/",
    title: "Blog | Nick Perry Digital",
    description: "Notes on websites, Google Business Profiles, and local search for Western Slope businesses.",
    crumbs: [
      { href: "/", label: "Home" },
      { href: "/blog/", label: "Blog" },
    ],
    body,
  });
}

function renderPost(data, post) {
  const route = `/blog/${post.slug}/`;
  const crumbsItems = [
    { href: "/", label: "Home" },
    { href: "/blog/", label: "Blog" },
    { href: route, label: post.title },
  ];
  const schema = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    headline: post.title,
    datePublished: post.date,
    description: post.description,
    author: { "@type": "Person", name: data.settings.personName },
    publisher: { "@type": "Organization", name: data.settings.siteName },
    mainEntityOfPage: new URL(route, data.settings.domain).href,
  };
  const body = `
    <article class="wrap max-w-3xl py-14">
      ${crumbs(crumbsItems)}
      <p class="kicker mt-6">${esc(post.date)}</p>
      <h1 class="display mt-3">${esc(post.title)}</h1>
      <p class="lede mt-4">${esc(post.description)}</p>
      <div class="prose-np mt-6">${post.html}</div>
    </article>`;
  return pageShell(data, {
    route,
    title: `${post.title} | Nick Perry Digital`,
    description: post.description,
    ogType: "article",
    crumbs: crumbsItems,
    schemas: [schema],
    body,
  });
}

function renderNotFound(data) {
  const body = `
    <section class="wrap py-20">
      <p class="kicker">404</p>
      <h1 class="display mt-3">That page is not here.</h1>
      <p class="lede mt-4">Try the services list, the towns, or the contact page.</p>
      <p class="mt-6"><a class="btn" href="/">Back to the home page</a></p>
    </section>`;
  return pageShell(data, {
    route: "/404.html",
    title: "Page not found | Nick Perry Digital",
    description: "The page you requested is not on Nick Perry Digital.",
    noindex: true,
    body,
  });
}

export function renderSite(data) {
  const pages = [
    renderHome(data),
    renderPricing(data),
    renderProsePage(data, data.pages.about, "/about/"),
    renderProsePage(data, data.pages.privacy, "/privacy/"),
    renderProsePage(data, data.pages.terms, "/terms/"),
    renderServicesHub(data),
    ...data.services.map((service) => renderService(data, service)),
    renderLocationsHub(data),
    ...data.locations.map((town) => renderLocation(data, town)),
    renderResults(data),
    ...data.caseStudies.map((study) => renderCaseStudy(data, study)),
    renderContact(data),
    renderBlogIndex(data),
    ...data.posts.map((post) => renderPost(data, post)),
    renderNotFound(data),
  ];
  return pages;
}

export function renderSitemap(pages, domain) {
  const today = new Date().toISOString().slice(0, 10);
  const urls = pages
    .filter((page) => page.route !== "/404.html")
    .map((page) => {
      const loc = new URL(page.route, domain.replace(/\/$/, "") + "/").href;
      return `  <url><loc>${esc(loc)}</loc><lastmod>${today}</lastmod></url>`;
    })
    .join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;
}

export function renderRobots(domain) {
  const base = domain.replace(/\/$/, "");
  return `User-agent: *
Allow: /
Disallow: /admin/

Sitemap: ${base}/sitemap.xml
`;
}
