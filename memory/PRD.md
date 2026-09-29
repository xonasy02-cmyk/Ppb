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

## User-reported correction: actual launchpad structure and trading
User complaint verbatim: “Gmn si bro ini kan launchpad masa gak ada mcap.volume holder dll, gak ada di klik page ke chart tokennya buy sell dll kaya launchpad pada umumnya gue minta jangan banyak page tapi gak semua jadi 1 juga kali bro,”
User clarification: “Ya. Buat halaman trading lengkap dengan simulasi buy/sell yang jelas ditandai, tanpa menggunakan dana nyata” and “Buat seperti launchpad sebenernya, sesuai kan pagenya jangan semua jadi 1 halaman depan intinya saja jangan buat semua jadi 1”.

### Revised architecture (supersedes the single-page decision above)
- `/`: concise editorial home, ecosystem summary, three featured tokens with market stats, short concept intro and launch CTA. NOT a full ecosystem/dashboard dumped on the homepage.
- `/bags`: dedicated token discovery with market cap, 24h volume, holders, changes and Bag progress; search, grid/list and 8 sort options.
- `/token/:id`: proper full-page trading terminal, not a modal. Legacy `/bags/:id` redirects here. Price/market cap/volume/liquidity/holders/24h change, chart, trades/holders/my trades/about, practice buy/sell, persistent position and Bag sidebar/history.
- `/launch`: dedicated creation page, original four-step draft flow preserved; no dialog overlay.
- `/ecosystem`: Carry, Global, native PAPERBAG and mechanism explainers grouped together using targeted nav anchors.
- `/leaderboard`: separate rankings page.
- Unknown paths get a real friendly 404 view instead of silently returning home.

### Trading implementation
- Market stats seeded additively for the six example tokens; sample USD prices and SOL quote at a fixed illustrative 150 USD/SOL. No external/live data service and no real mint.
- Lightweight Charts 5.2.1: deterministic illustrative candlesticks + volume, 1m/5m/15m/1h/4h, price/market-cap switch, line/candle switch, crosshair, pan/zoom/fit, responsive sizing and TradingView attribution.
- `/api/market/:id/candles`, `/trades`, `/holders` return explicitly illustrative data. All chart timeframes finish at the same quote. OHLC generated from a shared minute series.
- `/api/simulations` POST creates 100 virtual SOL; GET restores; POST `/:id/orders` executes simulated buy (SOL input) / sell (token amount); DELETE resets/removes toy state.
- Balances, weighted cost basis, realized P&L and trade history persist in one Mongo document. Atomic version compare-and-swap prevents overspending; UUID request IDs ensure idempotency. Input validation rejects bad side, zero/negative/nonfinite amounts, insufficient funds/holdings, unknown token.
- Simulated trades do NOT create actual tokens, change seeded market activity, fill Bags, or claim network fees/slippage. No wallet signing or auth added.
- Practice panel provides buy presets, percent sell presets, estimated output, clear error/success state, position stats and reset confirmation. Market activity distinguishes sample traders and the user's practice fills. Holder labels are not fabricated real addresses.
- Token share link and browser-persistent watch toggle.

### Current verification
- Initial build passed; screenshots confirmed market card layout and dedicated launch layout.
- Found and fixed chart library's invalid browser locale (`en-USposix`) by explicitly setting chart localization locale `en-US`.
- Browser inspection exercised a simulated buy, displayed its position and My trades, and navigation to standalone launch; subsequently verified by testing_agent as required below.
- Required testing_agent verification completed: `/app/test_reports/iteration_2.json`. Agent explicitly confirms the reported missing-launchpad/page-structure problem is resolved; no blockers.
- 30/30 backend regression tests passed, including dedicated market and simulation tests. Agent also validated duplicate order IDs and concurrent order guardrails.
- Frontend verified by testing agent: standalone routes, required token metrics, full-page terminal, chart timeframes and modes, simulation buy/sell/persistence, holder/activity tabs, draft lifecycle, share/watch, legacy redirects and404.
- Mobile/tablet390/375/320/768 passed with no document horizontal overflow.
- Small residual Lenis warning on cross-page hashes removed by disabling Lenis automatic anchor interception; React Router already scrolls only once the destination exists.
- Follow-up browser navigation check: Home → Carry → Global Bag → Bags → DOG terminal works without missing-anchor warnings. Final frontend production build compiled successfully (~259.5KB gzipped JS).

## Current handoff / next action
User-reported correction verified by testing_agent. No live wallets, launches, trading, swaps, burns or distributions are enabled; practice buy/sell is deliberately non-financial. Next substantive work: configured real market feeds and audited Pump.fun integration. Optional product improvement: a dedicated watched-token filter and price alerts, without adding navigation pages.