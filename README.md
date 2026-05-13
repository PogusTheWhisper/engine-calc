# Engine Calculator

Web-based engine tuning calculator. Enter bore, stroke, and fuel — get displacement, valve sizing, bore/stroke character, compression ratio, injector size, ignition timing, and rough HP/torque estimates.

Deployed on Vercel: static HTML frontend + Python serverless API. Zero dependencies (stdlib only).

## Stack

- **Frontend**: `public/index.html` — single-file HTML/CSS/JS, Thai UI
- **API**: `api/calculate.py` — Python serverless function (Vercel Python runtime)
- **Config**: `vercel.json` — routes `/api/*` → function, everything else → `index.html`

## API

```
GET /api/calculate?bore=57&stroke=58.7&fuel=95
```

Params:
- `bore` (mm, required, > 0)
- `stroke` (mm, required, > 0)
- `fuel` (optional): `91`, `95`, `E20`, `E85`

Returns JSON with displacement, valves, engine character, and (if fuel set) fuel specs + performance estimate.

## Local development

```bash
npm i -g vercel
vercel dev
```

Open `http://localhost:3000`.

## Deploy

```bash
vercel          # preview deploy
vercel --prod   # production deploy
```

First run prompts for project link.

## Notes

Performance estimates are heuristic (BMEP-based), not dyno-accurate. For guidance only.

## License

See `LICENSE`.
