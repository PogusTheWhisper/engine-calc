# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Engine tuning calculator. Vercel deployment: static HTML frontend (`public/index.html`) + Python serverless function (`api/calculate.py`). No build step, no dependencies — Python stdlib only.

## Commands

```bash
# Local dev (requires Vercel CLI)
vercel dev

# Deploy
vercel              # preview
vercel --prod       # production

# Manual API test
python3 -c "from api.calculate import calc_displacement; print(calc_displacement(57, 58.7))"
```

No test suite exists yet. No linter configured.

## Architecture

- `api/calculate.py` — single serverless handler. Pure calc functions (`calc_displacement`, `calc_valve_sizes`, `calc_bore_stroke_character`, `calc_fuel_specs`, `calc_performance_estimate`) + `handler(BaseHTTPRequestHandler)` for Vercel Python runtime. Query params: `bore`, `stroke`, `fuel` (optional: `91`, `95`, `E20`, `E85`).
- `public/index.html` — single-file UI (HTML/CSS/JS inline). Calls `/api/calculate`.
- `vercel.json` — routes `/api/*` → function, everything else → `index.html`.

Fuel specs (`FUEL_SPECS` dict) drive compression ratio, AFR, injector sizing, ignition timing. Performance estimates are heuristic (BMEP-based), not dyno-accurate — marked as guidance.
