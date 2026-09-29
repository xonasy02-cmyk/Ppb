# Paperbag — product and implementation record

## Original problem statement
Build the full Paperbag launchpad using the existing design and visual language at https://paper-bag.vercel.app/, not a redesigned identity. Preserve minimal, clean, playful paper/cardboard, bold editorial typography, whitespace, paper-bag mascot, texture and smooth motion. Positioning: “Every token carries a bag.” Hero: “BIG IDEAS. FULL BAGS.” Tokens launch through Pump.fun/PF, trading activity fills creator-selected Bags, SHARE rewards holders in the chosen asset or BURN buys/burns the project token, then cycles reset. Target accounting is always SOL; public progress uses the chosen Fill Asset. Never expose the exact creator/Bag/Global fee percentages. Carry follows activity, only realized positive settled profits return to project Bags, losses never promise rewards. Include animated Carry ecosystem, Global asset vaults (no target/progress/reset) with 24-hour distribution information for PAPERBAG holders, fixed native PAPERBAG 80% Share/20% Buyback & Burn cycle, visual economics, sortable Bag Index, five leaderboard categories, token-specific pages/history, four-step launch flow, mobile-first motion. Navigation: Launch, Bags, Carry, Global Bag, Leaderboard, PAPERBAG, Connect Wallet.

## Explicit user choices
- Complete interface and persistent data flows first; leave real transactions unavailable until the protocol is configured.
- Use the reference site, recreate matching assets as needed.
- “Buat jangan terlalu rumit tapi simple jangan buat terlalu banyak page karna akan membuat org bingung” — keep it simple, few pages.
- High craft: kinetic masked hero text, photography, subtle parallax, slow marquee, Framer Motion, Lenis, consistent brand.
- Communicate progress with user in Indonesian; public product copy is English as specified.

## Architecture decisions
- React/FastAPI/MongoDB. Existing protected database and public backend URL unchanged.
- One anchored homepage. Token detail modal has shareable /bags/:id route. Launch and wallet status are accessible Radix dialogs, not additional pages.
- Original SVG mascot recreated exactly; original DM Sans/Space Grotesk/Caveat and cream/kraft/yellow identity retained. Generated paper-bag studio photograph adds tactile visual richness.
- All live launch endpoints fail closed (503); no wallet connection, signing, trading, mint address or fake trading pair.
- Clearly labeled illustrative projects, rankings, economics and animation. Six persistent example projects. No market-data integration.
- Draft create/read/update/delete persists in MongoDB. Opaque UUID draft ID remembered in this browser; no account or wallet authentication. Do not store secrets in public draft metadata. HTTPS social links validated.
- Token images persist in Emergent object storage, only references stored in MongoDB. API proxies image reads; 5MB PNG/JPEG/WebP limits and signature checks. Storage integration key in backend environment only.
- Internal Decimal accounting primitives for creator fees, fixed native split, realized positive Carry profit, not exposed as marketing metadata. No on-chain settlement implemented.
- 24-hour Global Bag is presentation/configuration only; no scheduled distribution of real funds and no simulated timer claiming a live payout.

## Implemented
- Hero, original favicon, paper grain, photography/parallax, masked line reveal, smooth scrolling, editorial marquee.
- Five-stage animated fill/open/distribution/reset explanation with manual phase selection.
- Bag search, five sorting options, expandable index, individual details, chosen-asset progress, mode, SOL target, Carry P&L, complete historical cycles, copyable route.
- Carry map with activity/profit sequence, clickable projects, playback control, financial risk copy.
- Global vaults and fixed 24H cadence, native fixed 80/20 card, flow diagram.
- Five leaderboard categories, FAQ, final launch CTA, responsive mobile nav.
- Four-step launch drafting: preview wallet gate, token metadata/image/socials, SOL target & fill/global assets & SHARE/BURN, review, save/edit/restore/delete draft.
- API validation/error/empty/loading states; all Mongo queries exclude BSON _id from returned documents.

## API map
GET /api/, /api/config, /api/projects?sort=&search=, /api/projects/:id, /api/overview, /api/global, /api/native, /api/leaderboard?category=
POST /api/drafts; GET/PUT/DELETE /api/drafts/:id
POST /api/uploads; GET /api/files/:id
POST /api/launch → 503 until configured

## Prioritized backlog
P0 next phase: configured Solana RPC, wallet integration, audited Pump.fun fee routing/launch, mint verification and launch confirmation before any live funds.
P0: wallet-signed ownership/security/rate limiting for live drafts and upload control; audited holder eligibility and settlement; real asset mint registry and conversion quotes (DOGE/SHIB only via verified supported Solana representations).
P1: live fee indexing with idempotent event ledger, asset conversion, holder snapshots, distributions, buyback/burn receipts, next-cycle rollovers.
P1: production Carry strategy, activity allocation, realized P&L settlement with loss carryforward and reconciliation; no fake profit claims.
P1: platform scheduled tasks for 24-hour Global distributions only after live protocol exists. Load scheduled-recurring-tasks skill then; do not use in-app timers.
P2: creator draft library tied to verified wallet, richer history links, holder notification opt-in.

## Verification
- Production frontend build passed.
- API external overview/config/sorting checked successfully.
- Browser hero, anchor navigation, Bag card and details screenshots checked.
- Full independent backend/frontend testing completed; report: /app/test_reports/iteration_1.json.
- 22/22 backend API and Decimal unit tests passed twice, including real external image upload/download, persistence, input validation and fail-closed launch endpoint.
- Desktop and mobile 390/375/320px verified by testing agent: navigation, bags/search/sorting, direct route/reload, leaderboard, FAQ, full save/restore/edit/discard draft lifecycle passed; no layout/design issues reported.
- Fixed reported Carry SVG coordinate console error by replacing mutable SVG coordinates with a stable CSS-transformed SVG dot. Pause now also stops line/dot/scan CSS animations.
- Browser follow-up: full Carry sequence plus pause/resume, Global/native display, and launch settings pass; zero page errors or console errors.
- Removed fallback storage service host; storage now requires platform INTEGRATION_PROXY_URL. Upload/download regression remains green.
- Final production frontend build compiled successfully (about 194.5KB gzipped JavaScript).

## Current handoff / next action
First version complete within user-selected non-transactional scope. No live wallets, token launches, trading, swaps, burns or distributions enabled. Next substantive work is protocol integration only after real configuration and security requirements are provided. Suggested optional product enhancement: opt-in full-Bag notifications, without adding more navigation pages.