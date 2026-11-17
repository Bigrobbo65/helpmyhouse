# Help My House — Website Build Log

Documentation of the build session for **helpmyhouse.co.uk**, a home‑improvement,
maintenance and emergency‑callout service covering **Hertfordshire & North London**.

---

## 1. Brief

> "Help My House is a home improvement service that carries out across‑the‑board new
> works, improvements and maintenance including emergency callouts in Hertfordshire and
> North London. All skill sets are covered. A website is needed to show these skills and
> services. Research local handymen in Hertfordshire, research local websites, build a
> website, and launch it locally to preview before it goes live."

- **Domain:** helpmyhouse.co.uk
- **Theme:** Orange (per `website.txt`)
- **Positioning:** One trusted team for every job around the home — all trades covered.

---

## 2. Research (local competitors)

Searched and scraped local Hertfordshire / North London trade sites to inform structure,
services and trust signals:

| Source | Takeaways used |
| --- | --- |
| [HB Handyman Herts](https://www.handymanherts.co.uk/) | 30+ yrs experience, £5m liability, "all property maintenance" breadth |
| [LHE Property Maintenance](https://lhepropertymaintenance.co.uk/) | Service list (building, plumbing, tiling, plastering…), testimonials, "get a quote" CTA |
| [Handyman WGC](https://www.handymanwgc.uk/) | Indoor/outdoor/commercial split, "honest, reliable, trustworthy" tone, hourly pricing |
| [Xtra Maintenance](https://www.xtramaintenance.co.uk/) | 24/7 emergency callout positioning |

**Common patterns adopted:** 24/7 emergency strip, "all trades, one team" message,
insurance/guarantee trust badges, areas‑covered list, quote/callback forms, star reviews.

---

## 3. What was built

A polished, fully responsive single‑page static site (no framework, no build step).

**Files**

| File | Purpose |
| --- | --- |
| `index.html` | The website (single page, all sections) |
| `styles.css` | Styling — orange theme, responsive down to mobile |
| `script.js` | Mobile nav toggle, form handling (front‑end demo), footer year |
| `assets/principle.jpg` | Owner headshot used in the hero |
| `serve.ps1` | Tiny PowerShell static web server for local preview |
| `.claude/launch.json` | Launch config that runs `serve.ps1` on port 4173 |

**Page sections (top → bottom)**

1. Emergency strip (24/7 callout + phone)
2. Sticky header — logo, nav, "Get a free quote" CTA
3. Hero — headline, trust stats, callback form, **owner badge (Trev Cupbord — CEO & Senior Engineer)**
4. Trust bar (insured / guaranteed / fast / free quotes)
5. Services — 9 cards (plumbing, electrical, carpentry, decorating, kitchens & bathrooms,
   building/new works, gardens, handyman/maintenance, + highlighted 24/7 emergency)
6. Emergency band (rapid‑response CTA)
7. Why us (4 reasons) + How it works (4 steps)
8. Areas covered (16 Herts / N London towns + illustrated map)
9. Reviews (3 sample testimonials)
10. Contact / quote form
11. Footer + floating mobile call button

---

## 4. Technical notes & decisions

- **No Node or Python** is installed on the machine, so the usual `npx http-server` /
  `python -m http.server` preview options were unavailable.
- **Solution:** a dependency‑free static file server written in PowerShell
  (`serve.ps1`, using `System.Net.HttpListener`), launched via `.claude/launch.json`
  on **http://localhost:4173/**.
- **OneDrive quirk:** the project lives under a OneDrive‑synced folder. Creating/copying
  **binary** files and deleting files via the shell was intermittently blocked
  ("access denied" / "could not find file"). Text files write fine. The owner photo was
  therefore placed in `assets/` directly and referenced as a normal static asset.

---

## 5. Before going live — checklist

These are placeholders to replace before the site is published to helpmyhouse.co.uk:

- [ ] **Phone** `0800 123 4567` → real number (appears in ~6 places)
- [ ] **Email** `hello@helpmyhouse.co.uk` → real inbox
- [x] **Owner name** set to "Trev Cupbord" (tagline still to confirm)
- [ ] **Reviews** — replace the 3 sample testimonials with real customer quotes
- [ ] **Stats** (4.9★, 15+ yrs, £5m cover) — confirm actual figures
- [ ] **Forms** are front‑end only — wire to an email service (e.g. Formspree) or backend
- [ ] **Work photos** — add a gallery of completed jobs (kitchens, roofs, bathrooms) for
      stronger conversion
- [ ] **Deploy** — static site; suitable for Netlify / Cloudflare Pages / GitHub Pages

---

## 6. Local preview

```powershell
# From the project root
powershell -NoProfile -ExecutionPolicy Bypass -File serve.ps1 -Port 4173
# then open http://localhost:4173/
```

Or use the Claude Code Launch preview panel (config in `.claude/launch.json`).
