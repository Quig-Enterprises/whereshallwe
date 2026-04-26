# WhereShallWe — TODO

## Phase 1 — COMPLETE (2026-04-23)

Both sites live: whereshallwedance.com (53 dance venues) and whereshallweski.com (17 ski resorts).
Theme system, domain middleware, seed data, SSL, DNS, CI all done.
Plan file: /opt/claude-workspace/projects/plans/plan-whereshallwe-2026-04-23-multi-site-scaffold.md

---

## Phase 2 — plan-whereshallwe-2026-04-26-phase2.md

**Context:** Map route returns venues list (no map.html in themes). No auth or admin UI. Ski resort stat columns are all NULL.
**Plan file:** /opt/claude-workspace/projects/plans/plan-whereshallwe-2026-04-26-phase2.md
**Steps:**
1. Add map.html to wswd theme (dark plum/gold Mapbox map, venue markers)
2. Add map.html to wsws theme (navy/ski-red, snow depth badge on popups)
3. Update /map route handler to pass mapbox_token in context
4. Verify map pages on both live sites
5. Write migration 006 — ski resort stats (trail count, lift count, vertical drop, season dates)
6. Apply migration 006
7. Provision Sentinel PHP on Peter for whereshallwe (separate schema: sentinel_wsw)
8. Add nginx Sentinel blocks for whereshallwedance.com via cxq-hosting
9. Write migration 007 — public.users table
10. Write app/auth.py (WSWUserUpsert hook, SentinelAuth)
11. Add auth router to app/main.py, add Sentinel settings to config.py
12. Update nav in both theme base.html (login/logout link)
13. Build admin venue list page (GET /admin/venues, schema-scoped, requires admin capability)
14. Build admin venue edit page (GET/POST /admin/venues/{id}, ski stats for wsws)
15. Commit, push, deploy to Alfred and Peter
**Done when:** Both /map pages show Mapbox markers; /auth/login renders; /admin/venues requires auth; ski stats populated.
**Risks:** Sentinel provisioning on Peter for WSW must use separate DB schema to avoid DRH Sentinel collision. Map CSP already allows Mapbox. Admin UI must be gated — test 401 for unauthenticated requests.
