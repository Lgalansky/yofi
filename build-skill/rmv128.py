# Real Money build, step 131 (after rmv127.py): rosettes for the photos you made.
#  - Your photo reaches a Final (top 2 in its qualifier): navy Finalist rosette.
#    Your photo finishes 1st / 2nd / 3rd in a Final: gold / silver / bronze rosette.
#  - The result pop pins the rosette onto your photo ("Gold rosette won · it hangs on its frame in your Gallery").
#  - Gallery: each framed photo's rosettes hang down the right edge of its frame; the plaque shows its record
#    ("2 gold · 1 finalist").
#  Pick rosettes in the result reveal are unchanged.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# navy Finalist rosette
RA("function rosette(k) { const C = [", "function rosette(k) { if (k === 'f') return rosetteF(); const C = [")
# award: qualifier (through to the Final)
RA("if (pl <= 2) { const sl = rcSlotFor(p);", "if (pl <= 2) { rzAdd(p, 3); const sl = rcSlotFor(p);")
# award: Final top 3
RA("x.done = 1; x.place = pl; x.prize = pz; x.share = fsh;", "x.done = 1; x.place = pl; x.prize = pz; x.share = fsh; if (pl <= 3) rzAdd((S.photos || []).find(z => z.id === x.pid), pl - 1);")
# result pops: pin the rosette on the photo
RA("<div class=\"re-ok\"><img src=\"${p.src}\" alt=\"\"><i>${PP_MED[x.pl - 1]}</i></div><h2 class=\"pp-h\">Through to the Final!</h2>",
   "<div class=\"re-ok\"><img src=\"${p.src}\" alt=\"\"><i class=\"re-rz\">${rosette('f')}</i></div><h2 class=\"pp-h\">Through to the Final!</h2><p class=\"re-rzl\">🎀 Finalist rosette won · it hangs on its frame in your Gallery</p>")
RA("${pl <= 3 ? `<i>${PP_MED[pl - 1]}</i>` : ''}</div>\n    <h2 class=\"pp-h\">${esc(ph.t)} finished ${ppOrd(pl)}${pl <= 3 ? '!' : ''}</h2>",
   "${pl <= 3 ? `<i class=\"re-rz\">${rosette(pl - 1)}</i>` : ''}</div>\n    <h2 class=\"pp-h\">${esc(ph.t)} finished ${ppOrd(pl)}${pl <= 3 ? '!' : ''}</h2>${pl <= 3 ? `<p class=\"re-rzl\">🎀 ${['Gold', 'Silver', 'Bronze'][pl - 1]} rosette won · it hangs on its frame in your Gallery</p>` : ''}")
# Gallery: hang them on the frame + plaque record
RA("<div class=\"gx-pic\"><div class=\"gx-frame\">", "<div class=\"gx-pic\">${rzHang(p)}<div class=\"gx-frame\">")
RA("framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small></div></div>\n      <div class=\"gx-side\">",
   "framed ${new Date(p.framed).toLocaleDateString([], { day: 'numeric', month: 'short' })}</small>${rzLine(p)}</div></div>\n      <div class=\"gx-side\">")
s = s.replace("function fcNotify() {", r"""function rosetteF() { const C = ['#0F1A33', '#E3EAF5', '#1E3A6E'], pet = Array.from({ length: 16 }, (_, j) => { const a = j * Math.PI / 8; return `<circle cx="${(30 + 21 * Math.cos(a)).toFixed(1)}" cy="${(30 + 21 * Math.sin(a)).toFixed(1)}" r="7.5" fill="${C[2]}" stroke="${C[0]}" stroke-width=".8"/>`; }).join('');
  return `<svg viewBox="0 0 60 80" aria-hidden="true"><path d="M20 40 L10 78 L19 72 L26 79 L32 44Z" fill="#D9AE4F"/><path d="M40 40 L50 78 L41 72 L34 79 L28 44Z" fill="${C[2]}" stroke="${C[0]}" stroke-width=".8"/>${pet}<circle cx="30" cy="30" r="21" fill="${C[2]}"/><circle cx="30" cy="30" r="16.5" fill="${C[1]}" stroke="#D9AE4F" stroke-width="1.6"/><text x="30" y="35" text-anchor="middle" font-family="Nunito,system-ui,sans-serif" font-weight="900" font-size="9" letter-spacing=".5" fill="#14213D">FINAL</text></svg>`; }
function rzAdd(p, k) { if (!p) return; p.rz = p.rz || [0, 0, 0, 0]; p.rz[k] = (p.rz[k] || 0) + 1; }
function rzList(p) { const r = p.rz || [0, 0, 0, 0], L = []; [0, 1, 2, 3].forEach(k => { for (let n = 0; n < (r[k] || 0); n++) L.push(k === 3 ? 'f' : k); }); return L; }
function rzHang(p) { const L = rzList(p); if (!L.length) return ''; const show = L.slice(0, 4), more = L.length - show.length;
  return `<div class="rz-hang">${show.map((k, i) => `<i style="transform:rotate(${[-8, 5, -3, 9][i]}deg)">${rosette(k)}</i>`).join('')}${more > 0 ? `<em>+${more}</em>` : ''}</div>`; }
function rzLine(p) { const r = p.rz || [0, 0, 0, 0], t = [[r[0], 'gold'], [r[1], 'silver'], [r[2], 'bronze'], [r[3], 'finalist']].filter(x => x[0]).map(x => `${x[0]} ${x[1]}`); return t.length ? `<p class="rz-rec">🎀 ${t.join(' · ')}</p>` : ''; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .gx-pic{position:relative}
.rz-hang{position:absolute;right:-12px;top:10px;z-index:5;display:flex;flex-direction:column;align-items:center}
.rz-hang i{display:block;width:38px;height:50px;margin-top:-16px;filter:drop-shadow(0 3px 4px rgba(20,33,61,.4))}.rz-hang i:first-child{margin-top:0}
.rz-hang svg{width:100%;height:100%;display:block}
.rz-hang em{font-style:normal;font:900 .72rem Nunito,system-ui,sans-serif;background:#14213D;color:#F3D98B;-webkit-text-fill-color:#F3D98B;border-radius:999px;padding:1px 7px;margin-top:2px}
html body .rz-rec{margin:4px 0 0;font:900 .76rem/1.3 Nunito,system-ui,sans-serif;color:#7A5410;-webkit-text-fill-color:#7A5410}
html body .re-ok{position:relative}
html body .re-ok i.re-rz{position:absolute;right:-16px;top:-16px;left:auto;bottom:auto;width:60px;height:80px;font-size:0;background:none;box-shadow:none;border:0;padding:0;transform:none;filter:drop-shadow(0 4px 7px rgba(20,33,61,.45));animation:rzPin .7s cubic-bezier(.3,1.6,.5,1) .2s both}
html body .re-ok i.re-rz svg{width:100%;height:100%;display:block}
html body .re-rzl{margin:2px 0 8px;font:900 .9rem/1.35 Nunito,system-ui,sans-serif;color:#7A5410;-webkit-text-fill-color:#7A5410;text-align:center}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v128 ok')
# rosette on the result photo sits lower, clear of the kicker line
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .re-ok i.re-rz{top:14px!important;right:-26px!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v128 pass2 ok')
