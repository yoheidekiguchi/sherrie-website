# Sherrie De Kiguchi Campaign Website — Design Spec

**Date:** 2026-06-11
**Owner:** Yohei (managed via Claude Code)
**Subject:** Sherrie De Kiguchi
**Status:** Approved design — ready to build

---

## 1. Goal

A simple, warm, personal campaign profile website that:
- Introduces Sherrie De Kiguchi and what she stands for
- Centralises her social media presence (FB, IG, X, YouTube) into one place
- Stays static and zero-cost — no CMS, no backend, no build step
- Can be updated by editing one HTML file via Claude Code

## 2. Platform & Deployment

| Item | Choice |
|------|--------|
| Source | Single static `index.html` (plus one image) |
| Hosting | Cloudflare Pages (free tier) |
| Repo | GitHub `sherrie-website` (public, `main` branch) |
| Domain | `sherrie.dekiguchi.com` (subdomain of dekiguchi.com) |
| DNS | CNAME `sherrie` → `<project>.pages.dev` in Squarespace DNS |
| Build | None — Cloudflare serves the file as-is |
| Updates | Edit `index.html` → `git push` → Cloudflare auto-deploys |

### Deployment steps
1. Create public GitHub repo `sherrie-website`
2. Push `index.html` + `sherrie-headshot.jpg` to `main`
3. In Cloudflare dashboard → Pages → Connect to Git → select repo → deploy (no build command, output dir `/`)
4. In Squarespace DNS for `dekiguchi.com`, add CNAME: host `sherrie` → target `<project>.pages.dev`
5. In Cloudflare Pages → Custom domains → add `sherrie.dekiguchi.com` (Cloudflare provisions TLS automatically)

## 3. Visual Design

**Style:** Warm & Personal — no party colours, completely neutral politically.

| Token | Value |
|-------|-------|
| Primary | `#ff6b35` (orange) |
| Primary dark | `#e85a24` |
| Background | `#fff8f0` (cream) |
| Card background | `#ffffff` |
| Card border | `#fde8d8` |
| Text primary | `#1a1a1a` |
| Text muted | `#555` |
| Font | system-ui / Segoe UI / Roboto / Helvetica stack |
| Max content width | 1100px |
| Border radius | 12px (cards), 999px (pills) |

Rules:
- No emojis in headings or body copy.
- Emojis allowed only on social platform follow buttons where users expect them (FB / IG / X / YT icons — SVG, not unicode).
- Hero uses an orange gradient: `linear-gradient(135deg, #ff6b35, #ff8c5a)`.
- Issue cards have a left border (`4px solid #ff6b35`) to tie back to the primary colour.

## 4. Page Structure (top to bottom)

1. **Sticky nav** — cream background, subtle shadow on scroll. Left: "Sherrie De Kiguchi" wordmark. Right: About / Issues / Follow anchor links.
2. **Hero** — orange gradient, centred. Round headshot photo (`sherrie-headshot.jpg`, CSS fallback initials circle if missing). Name `Sherrie De Kiguchi`. Subtitle `Campaigner for Safer, Fairer Britain`. Four pill social follow buttons inline below.
3. **About Sherrie** — white card with orange left border. Italic pull quote on top, paragraph below.
4. **What Sherrie Stands For** — 2×2 grid of issue cards (Public Safety / Justice for Victims / Child Protection / Immigration). Each card has a heading and one sentence. On mobile, stacks to 1 column.
5. **Social feeds** —
   - Facebook full-width (official Page Plugin iframe)
   - Instagram + Twitter side-by-side (Curator.io free embed + official Twitter timeline)
   - YouTube full-width (channel uploads playlist iframe)
   - Mobile: all stack to full-width
6. **Follow strip** — orange gradient CTA band with all 4 follow buttons repeated.
7. **Footer** — dark (`#1a1a1a`), small text: copyright + tagline.

## 5. Content (final copy)

### Hero
- Title: `Sherrie De Kiguchi`
- Subtitle: `Campaigner for Safer, Fairer Britain`

### About
> *"I believe in speaking plainly, standing firm, and never backing down when it matters most."*

Sherrie De Kiguchi is a campaigner and public advocate committed to tackling child sexual exploitation, demanding justice for victims, and building safer communities. She speaks out on the issues that others avoid — from grooming gang accountability to a broken immigration system — because she believes ordinary people deserve a voice that fights for them.

### Issues
- **Public Safety** — Safer streets, stronger communities, and real accountability in policing.
- **Justice for Victims** — Ending cover-up culture. Victims must be heard, believed, and protected.
- **Child Protection** — Zero tolerance for grooming gangs. Full accountability for institutions that failed survivors.
- **Immigration** — A controlled, fair immigration system that works for the people of Britain.

## 6. Social Accounts

| Platform | Handle | URL | Followers (current) |
|---|---|---|---|
| Facebook | Page ID 883706581482868 | https://www.facebook.com/profile.php?id=883706581482868 | TBD |
| Instagram | @sherriedekiguchi | https://instagram.com/sherriedekiguchi | 152 |
| Twitter/X | @SherriedeK | https://x.com/SherriedeK | TBD |
| YouTube | @SherrieDeKiguchi | https://www.youtube.com/@SherrieDeKiguchi | TBD |

## 7. Embed Strategy

| Feed | Method |
|------|--------|
| Facebook | Official Page Plugin iframe (`https://www.facebook.com/plugins/page.php?href=...&tabs=timeline`) — shows live feed from the page |
| Instagram | Curator.io free tier embed (Instagram Graph API is too restricted for unauthenticated direct embeds). Placeholder script tag included; the Curator feed ID must be filled in by Yohei after creating the free Curator account |
| Twitter/X | Official Twitter widget — `<a class="twitter-timeline" href="https://twitter.com/SherriedeK">` + `widgets.js` |
| YouTube | `<iframe>` of the channel uploads playlist (uses the channel ID — uploads playlist ID = channel ID with `UC` replaced by `UU`). Until the channel ID is resolved, the iframe falls back to a `youtube.com/embed/videoseries?list=` of the channel handle search |

Notes:
- All embeds are lazy-loaded (`loading="lazy"`) where supported.
- If any embed fails, the card shows a "View on [Platform]" link as a fallback (a `<noscript>`/error-state link inside each card).

## 8. Headshot

- File: `sherrie-headshot.jpg` placed next to `index.html` at repo root.
- Rendered as a 180px circle (160px on mobile) inside the hero.
- CSS fallback: if `<img>` fails to load, an `::after` initials circle ("SD") displays with the same dimensions and a cream background.

## 9. Responsiveness

| Breakpoint | Behaviour |
|------------|-----------|
| ≥ 900px | 2-column issue grid; IG + X side-by-side |
| 600 – 899px | 2-column issue grid; IG + X stack |
| < 600px | Everything single column; nav links shrink; hero font scales down |

## 10. Performance & Quality

- No build step, no framework, no CSS preprocessor.
- Only third-party scripts: Facebook SDK (deferred), Twitter widgets.js (deferred), Curator.io (deferred), YouTube iframe.
- All custom CSS inline in `<style>` to avoid an extra request.
- Lighthouse target: Performance ≥ 90, Accessibility ≥ 95.
- Semantic HTML (`<header>`, `<main>`, `<section>`, `<footer>`), proper heading hierarchy, all interactive elements keyboard-accessible.
- `<meta>` tags: charset, viewport, description, OG title/description/image (uses `sherrie-headshot.jpg`).

## 11. File Layout

```
~/Desktop/sherrie-website/
├── index.html                  # Production site
├── sherrie-headshot.jpg        # Headshot (provided separately)
└── docs/superpowers/specs/
    └── 2026-06-11-sherrie-website-design.md  # This spec
```

## 12. Open Items / Follow-ups

- Curator.io feed ID — Yohei to create free account at curator.io and supply feed ID (placeholder in HTML for now).
- Final headshot file — to be saved as `sherrie-headshot.jpg` at repo root.
- Follower counts on FB / X / YouTube — currently TBD; only IG (152) is shown in the initial version.
- Optional later: contact form / newsletter signup (out of scope for v1).

---

**Approval gate:** Yohei reviews this spec → on approval, build `index.html` and open locally for preview.
