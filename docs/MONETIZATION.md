# ezCore Monetization Plan

> **Status:** planning draft — **not part of v1.0.0 and not a commitment.**
> ezCORE ships free and fully local; cloud sync and any paid tier are
> deferred past v1.1 and nothing here is decided. Kept for history.

> **Version:** 1.0
> **Date:** 2026-09-16
> **Status:** Draft

---

## Overview

ezCore is **free to play** — the core emulator, local saves, and basic UI are always free. The **Pro tier** ($4.99/month or $29.99/year) unlocks cloud saves, auto-scan, auto-cheats, 3D UI effects, themes, and cosmetic items.

---

## Free vs Pro

| Feature | Free | Pro |
|---|---|---|
| Core emulator | ✅ | ✅ |
| Local save states | ✅ (3 slots) | ✅ (10 slots) |
| Cloud saves | ❌ | ✅ |
| Cloud storage | — | 1 GB |
| Auto scan (ROM identification) | ❌ | ✅ |
| Auto cheats | ❌ | ✅ |
| 3D UI | Basic (flat) | Full (3D shelves, transitions) |
| Themes | 1 (Ink dark) | All (6+) |
| Pro badge | ❌ | ✅ |
| Skins & in-game items | ❌ | ✅ |
| Save sharing | ❌ | ✅ |
| Priority support | ❌ | ✅ |
| Fast forward | 1x | 1x-8x |
| Rewind buffer | 10s | 30s |
| Shader presets | 3 | All |

---

## Pricing

| Tier | Price | Savings |
|---|---|---|
| Free | $0 | — |
| Pro Monthly | $4.99/month | — |
| Pro Yearly | $29.99/year | 50% vs monthly |
| Pro Lifetime | $49.99 (launch offer) | 80% vs yearly |

### Launch Promotion

- **Lifetime Pro:** $49.99 (first 1000 users only)
- **Yearly Pro:** $19.99 (first 30 days only)
- After launch: prices increase to standard

---

## In-Game Items

### Skins (Cosmetic)

| Skin | Price | Type |
|---|---|---|
| Neon Grid theme | $1.99 | Theme |
| Wood Shelf theme | $1.99 | Theme |
| Cyberpunk theme | $2.99 | Theme |
| Glass Shelf style | $0.99 | Shelf |
| Metal Shelf style | $0.99 | Shelf |
| Gold box frame | $0.99 | Frame |
| Holographic box frame | $1.99 | Frame |
| Pixel box frame | $0.99 | Frame |

### In-Game Items

| Item | Price | Type |
|---|---|---|
| Pro badge | Included with Pro | Badge |
| Early Supporter badge | Free (beta users) | Badge |
| Animated avatar (Retro) | $0.99 | Avatar |
| Animated avatar (Neon) | $1.99 | Avatar |
| Custom cursor: Pixel | $0.99 | Cursor |
| Custom cursor: Neon | $0.99 | Cursor |
| 3D background: Particles | $1.99 | Background |
| 3D background: Stars | $0.99 | Background |

### Bundles

| Bundle | Price | Contents | Savings |
|---|---|---|
| Starter Bundle | $4.99 | 3 themes + 2 frames | 30% |
| Collector Bundle | $9.99 | All themes + all frames | 50% |
| Ultimate Bundle | $19.99 | Everything | 60% |

---

## Payment Integration

### Desktop (Windows/macOS/Linux)

- **Stripe** — web-based checkout flow (locked in — ADR-010)
- Payment methods: Credit/debit card, Apple Pay, Google Pay
- Stripe handles all PCI compliance
- No platform fees (unlike App Store's 15-30%)

### Mobile (Android/iOS)

- **RevenueCat** — unified in-app purchase platform (locked in — ADR-010)
- One integration for both App Store and Play Store
- Handles receipt validation, subscription management, and renewals
- Apple takes 15% (small business program), Google takes 15%

### Why Stripe + RevenueCat

| Platform | Processor | Why |
|---|---|---|
| Desktop | Stripe | Best checkout, no platform fees, full PCI compliance |
| Mobile | RevenueCat | Unified API for both stores, receipt validation built in |

### Account System

- One account across all platforms
- Pro status tied to account, not device
- Payment on desktop → Pro on all devices
- Payment on mobile → Pro on all devices
- **Login is optional** — guest mode works fully without an account (ADR-007)

---

## Revenue Projections

### Year 1 (Conservative)

| Metric | Value |
|---|---|
| Total users | 10,000 |
| Pro conversion | 5% |
| Pro users | 500 |
| Average revenue/user | $20/month |
| MRR | $10,000 |
| ARR | $120,000 |

### Year 1 (Moderate)

| Metric | Value |
|---|---|
| Total users | 50,000 |
| Pro conversion | 8% |
| Pro users | 4,000 |
| Average revenue/user | $15/month |
| MRR | $60,000 |
| ARR | $720,000 |

### Year 1 (Optimistic)

| Metric | Value |
|---|---|
| Total users | 200,000 |
| Pro conversion | 10% |
| Pro users | 20,000 |
| Average revenue/user | $12/month |
| MRR | $240,000 |
| ARR | $2,880,000 |

---

## Marketing Strategy

### Launch Channels

1. **GitHub** — open-source reputation, stars, contributors
2. **Reddit** — r/emulation, r/retrogaming, r/FlutterDev
3. **Twitter/X** — dev logs, screenshots, launch announcement
4. **YouTube** — gameplay trailers, UI demos
5. **itch.io** — indie game community
6. **Product Hunt** — launch day visibility

### Content Strategy

- **Dev logs:** Weekly blog posts showing progress
- **UI showcases:** Short videos of 3D UI in action
- **Core spotlights:** Deep dive into each supported system
- **User stories:** How users use ezCore

### Community

- Discord server for community
- Core contributor program
- Skin design contest (community-created skins)
- Bug bounty program

---

## Cost Structure

| Cost | Monthly |
|---|---|
| Firebase (Spark) | Free (up to 50K users) |
| Firebase (Blaze) | $25-50 (scales with usage) |
| Stripe fees | 2.9% + $0.30 per transaction |
| Apple/Google fees | 15% of in-app purchases |
| Server (cloud sync) | $50-100 |
| CDN (core downloads) | $50-100 |
| **Total** | **$125-250/month** |

---

## Open Questions

1. **Account system:** Email/password, OAuth (Google/Apple), or both?
2. **Payment processor:** Stripe, RevenueCat, or both?
3. **Free tier limits:** 3 save slots is enough? Or 5?
4. **Lifetime Pro:** How many lifetime slots to offer?
5. **Refund policy:** 14-day money-back guarantee?
6. **Family sharing:** Allow Pro sharing across family members?
