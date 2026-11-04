---
title: "+Signals"
type: moc
tags: ["moc", "signals"]
---

# 📡 Signals register

Syntheses **across** the knowledge base, grouped into [[+Themes|themes]]. Rules: [[SIGNALS]]. Feed: `signals.json` (run `python3 build_signals_json.py`).

## Themes and signals at a glance

Live from `signals.json` and `Themes/`. Hover for detail, click to open. To show this on your home page too, copy the block below into `+Home.md`.

```dataviewjs
// Themes and signals map — reads signals.json (computed trend/momentum) and the theme notes.
// Display only; edits nothing. Needs Dataview with "Enable JavaScript queries" switched on.
let data;
try { data = JSON.parse(await dv.io.load("signals.json")); }
catch (e) { dv.paragraph("⚠️ No `signals.json` yet — run `python3 build_signals_json.py` in the vault root."); return; }
const COLOURS = ["#4ade80","#38bdf8","#f87171","#a78bfa","#facc15","#fb923c","#f472b6","#2dd4bf","#818cf8","#a3e635","#fda4af","#94a3b8"];
const themes = {};
const tpages = dv.pages('"60 Signals/Themes"').where(p => p.type === "theme" && p.status === "active")
  .sort(p => parseInt(String(p.theme_id).slice(1)) || 0);
tpages.forEach((t, i) => {
  const name = String(t.title).replace(/^T\d+ - /, "");
  themes[name] = { id: t.theme_id, name, tagline: t.tagline, path: t.file.path, colour: t.colour || COLOURS[i % COLOURS.length], sigs: [] };
});
const notePath = {};
for (const p of dv.pages('"60 Signals"').where(p => p.signal_id)) notePath[p.signal_id] = p.file.path;
const SIZE = { weak: 6, emerging: 8, established: 10, strong: 12 };
const sigs = data.signals.filter(s => themes[s.theme]);
for (const s of sigs) themes[s.theme].sigs.push(s);
const esc = s => String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const tlist = Object.values(themes);

// ---------- chart ----------
// The impact axis starts just below your lowest-impact signal, so a register that
// clusters high still spreads out. Maturity always runs 0–10.
const W = 720, H = 440, L = 46, R = 16, T = 14, B = 42;
const minImpact = sigs.length ? Math.min(...sigs.map(s => s.impact)) : 0;
const X0 = 0, X1 = 10, Y0 = Math.max(0, Math.floor(minImpact) - 1), Y1 = 10.3;
const YSTEP = (10 - Y0) <= 4 ? 0.5 : 1;
const sx = v => L + (v - X0) / (X1 - X0) * (W - L - R);
const sy = v => T + (1 - (v - Y0) / (Y1 - Y0)) * (H - T - B);
const groups = {};
for (const s of sigs) (groups[s.maturity + "|" + s.impact] ??= []).push(s);
for (const g of Object.values(groups)) g.forEach((s, i) => {
  const a = (i / g.length) * 2 * Math.PI, r = g.length > 1 ? 11 : 0;
  s._x = sx(s.maturity) + r * Math.cos(a); s._y = sy(s.impact) + r * Math.sin(a);
});
let svg = `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;font-family:var(--font-interface)">`;
const mx = sx(5), my = sy((Y0 + 10) / 2);
svg += `<rect x="${mx}" y="${T}" width="${W-R-mx}" height="${my-T}" fill="var(--background-modifier-hover)"/>`;
for (let v = 0; v <= 10; v += 1) svg += `<line x1="${sx(v)}" x2="${sx(v)}" y1="${T}" y2="${H-B}" stroke="var(--background-modifier-border)" stroke-width="0.5"/><text x="${sx(v)}" y="${H-B+16}" text-anchor="middle" font-size="11" fill="var(--text-muted)">${v}</text>`;
for (let v = Y0; v <= 10; v += YSTEP) svg += `<line x1="${L}" x2="${W-R}" y1="${sy(v)}" y2="${sy(v)}" stroke="var(--background-modifier-border)" stroke-width="0.5"/><text x="${L-8}" y="${sy(v)+4}" text-anchor="end" font-size="11" fill="var(--text-muted)">${YSTEP < 1 ? v.toFixed(1) : v}</text>`;
svg += `<line x1="${mx}" x2="${mx}" y1="${T}" y2="${H-B}" stroke="var(--text-faint)" stroke-dasharray="4 4"/><line x1="${L}" x2="${W-R}" y1="${my}" y2="${my}" stroke="var(--text-faint)" stroke-dasharray="4 4"/>`;
const q = (x, y, t, a) => `<text x="${x}" y="${y}" text-anchor="${a}" font-size="11" fill="var(--text-faint)">${t}</text>`;
svg += q(L+6, T+14, "Early, high impact — watch closely", "start") + q(W-R-6, T+14, "Mature, high impact — act now", "end")
     + q(L+6, H-B-8, "Early, lower impact", "start") + q(W-R-6, H-B-8, "Mature, lower impact", "end");
svg += `<text x="${(L+W-R)/2}" y="${H-6}" text-anchor="middle" font-size="12" fill="var(--text-muted)">Maturity →</text>`;
svg += `<text transform="translate(12 ${(T+H-B)/2}) rotate(-90)" text-anchor="middle" font-size="12" fill="var(--text-muted)">Impact →</text>`;
const tri = (s, r) => s.trend === "rising" ? `<path d="M${s._x+r+2} ${s._y-r+4} l4 -6 l4 6 z" fill="var(--color-green)"/>`
  : s.trend === "declining" ? `<path d="M${s._x+r+2} ${s._y-r-2} l4 6 l4 -6 z" fill="var(--color-red)"/>` : "";
for (const s of [...sigs].sort((a, b) => (SIZE[b.strength]||8) - (SIZE[a.strength]||8))) {
  const r = SIZE[s.strength] || 8, th = themes[s.theme];
  svg += `<g class="sm-dot" data-theme="${esc(th.id)}" data-sig="${esc(s.id)}" style="cursor:pointer">`
    + `<circle cx="${s._x}" cy="${s._y}" r="${r}" fill="${th.colour}" fill-opacity="0.8" stroke="var(--background-primary)" stroke-width="1.5"/>${tri(s, r)}`
    + `<title>${esc(s.title)}\n${esc(th.id)} ${esc(th.name)} · maturity ${s.maturity} · impact ${s.impact} · ${esc(s.trend)}</title></g>`;
}
svg += `</svg>`;

const legend = tlist.map(t => `<span class="sm-leg" data-theme="${esc(t.id)}" style="display:inline-flex;align-items:center;gap:5px;margin:0 12px 6px 0;cursor:pointer;font-size:12px;color:var(--text-muted)"><span style="width:10px;height:10px;border-radius:50%;background:${t.colour}"></span>${esc(t.id)} ${esc(t.name)}</span>`).join("");
const key = `<div style="font-size:12px;color:var(--text-faint);margin:2px 0 8px">Bubble size = strength (weak → strong) · <span style="color:var(--color-green)">▲</span> rising · <span style="color:var(--color-red)">▼</span> declining · no marker = steady · hover a bubble for its name, click to open · hover a theme to highlight it</div>`;
const readout = `<div class="sm-read" style="min-height:1.6em;font-size:13px;color:var(--text-normal);margin:4px 0 0"></div>`;

// ---------- theme cards ----------
const ARROW = { rising: ["▲","var(--color-green)"], declining: ["▼","var(--color-red)"], steady: ["▶","var(--text-faint)"] };
const cards = tlist.map(t => {
  const ss = [...t.sigs].sort((a, b) => b.impact - a.impact);
  const up = ss.filter(s => s.trend === "rising").length, dn = ss.filter(s => s.trend === "declining").length;
  const rows = ss.map(s => { const [g, c] = ARROW[s.trend] || ARROW.steady;
    return `<div class="sm-row" data-sig="${esc(s.id)}" style="display:flex;gap:8px;align-items:center;font-size:12.5px;padding:3px 0;border-top:1px solid var(--background-modifier-border);cursor:pointer"><span style="color:${c};font-size:10px;width:10px">${g}</span><span style="flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(s.title)}</span><span style="color:var(--text-muted)">${Number(s.impact).toFixed(1)}</span></div>`; }).join("");
  return `<div style="background:var(--background-secondary);border-radius:10px;padding:10px 12px;border-top:3px solid ${t.colour}">`
    + `<div style="display:flex;align-items:baseline;gap:6px"><a class="sm-theme" data-path="${esc(t.path)}" style="font-weight:600;flex:1;cursor:pointer">${esc(t.id)} · ${esc(t.name)}</a><span style="font-size:11px;white-space:nowrap"><span style="color:var(--color-green)">${up}▲</span> <span style="color:var(--color-red)">${dn}▼</span></span></div>`
    + `<div style="font-size:12px;color:var(--text-muted);margin:2px 0 6px;line-height:1.35">${esc(t.tagline)}</div>${rows}</div>`;
}).join("");

const rising = sigs.filter(s => s.trend === "rising").length, declining = sigs.filter(s => s.trend === "declining").length;
const gen = String(data.generated_at || "").slice(0, 10);
const stat = (l, v, c) => `<div style="background:var(--background-secondary);border-radius:8px;padding:6px 12px"><div style="font-size:11px;color:var(--text-muted)">${l}</div><div style="font-size:20px;font-weight:600;${c?`color:${c}`:""}">${v}</div></div>`;

const root = dv.el("div", "");
root.innerHTML = `<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:10px">${stat("Active signals", sigs.length)}${stat("Themes", tlist.length)}${stat("Rising", rising, "var(--color-green)")}${stat("Declining", declining, "var(--color-red)")}</div>`
  + `<div>${legend}</div>${key}${svg}${readout}`
  + `<div style="font-size:11px;color:var(--text-faint);margin:2px 0 14px">Data: signals.json${gen ? `, generated ${gen}` : ""}. Trend arrows come from signals.json, not signal-note frontmatter.</div>`
  + `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px">${cards}</div>`;

// ---------- interaction ----------
const byId = Object.fromEntries(sigs.map(s => [s.id, s]));
const open = p => p && app.workspace.openLinkText(p, dv.currentFilePath, false);
const read = root.querySelector(".sm-read");
const dots = [...root.querySelectorAll(".sm-dot")];
const focus = id => dots.forEach(d => d.style.opacity = !id || d.dataset.theme === id ? "1" : "0.12");
root.querySelectorAll(".sm-leg").forEach(el => { el.onmouseenter = () => focus(el.dataset.theme); el.onmouseleave = () => focus(null); });
dots.forEach(d => {
  const s = byId[d.dataset.sig], th = themes[s.theme];
  d.onmouseenter = () => read.innerHTML = `<b>${esc(s.title)}</b> <span style="color:var(--text-muted)">· ${esc(th.id)} ${esc(th.name)} · maturity ${s.maturity} · impact ${s.impact} · ${esc(s.trend)}</span>`;
  d.onclick = () => open(notePath[s.id]);
});
root.querySelectorAll(".sm-row").forEach(el => el.onclick = () => open(notePath[el.dataset.sig]));
root.querySelectorAll(".sm-theme").forEach(el => el.onclick = () => open(el.dataset.path));
```

## Run log
<!-- newest first; the weak-signals agent writes a few lines here each run -->
- 2026-10-01 — *example entry.* No themes changed. One signal proposed: [[SIG - Cheaper Than Forecast]].

## Active signals

```dataview
TABLE WITHOUT ID file.link AS "Signal", theme AS "Theme", strength AS "Strength", maturity AS "Maturity", impact AS "Impact", horizon AS "Horizon", last_updated AS "Updated"
FROM "60 Signals"
WHERE type = "signal" AND status != "retired"
SORT impact DESC
```

## Retired

```dataview
LIST FROM "60 Signals" WHERE type = "signal" AND status = "retired"
```
