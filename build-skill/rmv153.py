# Real Money build, step 156 (after rmv152.py): clear per-photo progress viewer at the top of voting.
#  "📷 Your photos in play" panel above the round bar, one row per photo (up to 3):
#   stage tracker Qualifier › Final › Prize; big wins bar (x of 8) with a gold finish marker; wins, losses, losses
#   to spare; last matchup; coins this photo has won (+5 🟡 per head-to-head win, +50 for qualifying);
#   finalist row has "🏁 Race · $1"; raced row shows place and cash won.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (win) q.w++; else q.l++;", "if (win) { q.w++; p.qc = (p.qc || 0) + 5; S.gems = (S.gems || 0) + 5; try { paintGems(); } catch (e) {} } else q.l++;")
RA("if (q.done === 'q') { rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.fin = 1; save();", "if (q.done === 'q') { rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.qc = (p.qc || 0) + 50; p.fin = 1; save();")
s = s.replace("function fcNotify() {", r"""function qlStripHTML() { const now = Date.now(), P = (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || (p.raced && now - p.raced.at < 3 * 3600e3) || (p.ql.done === 'x' && now - (p.ql.at || 0) < 3600e3))).slice(0, 3);
  if (!P.length) return '<div id="qlS"></div>';
  return `<div class="qv" id="qlS"><p class="qv-h">📷 Your photos in play</p>${P.map(p => { const q = p.ql, st = p.raced ? 3 : p.fin || q.done === 'q' ? 2 : 1, out = q.done === 'x';
    const tag = (i, l) => `<span class="${st > i ? 'done' : st === i ? (out && i === 1 ? 'out' : 'on') : ''}">${l}</span>`;
    let info;
    if (p.raced) info = `🏁 Final: <b>${ppOrd(p.raced.rank)}</b>${p.raced.prize ? ` · won <b class="cash">${money(p.raced.prize)}</b>` : ' · rosette kept'}`;
    else if (p.fin || q.done === 'q') info = `🎀 <b>Finalist!</b> Race it in a Final <button class="btn db-go cashb ql-btn" data-qfr="${p.id}">🏁 Race · $1</button>`;
    else if (out) info = `Out at ${q.w}–${q.l} · <b>${QF_WIN - q.w}</b> win${QF_WIN - q.w === 1 ? '' : 's'} short`;
    else info = `<b>${QF_WIN - q.w} more win${QF_WIN - q.w === 1 ? '' : 's'}</b> to the Final · ${QF_N - QF_WIN + 1 - q.l} loss${QF_N - QF_WIN + 1 - q.l === 1 ? '' : 'es'} to spare`;
    return `<div class="qv-r ${out ? 'out' : ''} ${st >= 2 && !out ? 'fin' : ''}"><img src="${p.src}" alt=""><div class="qv-b">
      <div class="qv-t"><b>${esc(rcName(p))}</b><em>🟡 +${p.qc || 0}</em></div>
      <div class="qv-st">${tag(1, 'Qualifier')}<i>›</i>${tag(2, 'Final')}<i>›</i>${tag(3, 'Prize')}</div>
      <div class="qv-bar"><i style="width:${Math.min(100, q.w / QF_WIN * 100)}%"></i><u>🏁</u></div>
      <div class="qv-n"><span class="w">✓ ${q.w} won</span><span class="l">✕ ${q.l} lost</span><span>${q.w} / ${QF_WIN} wins</span></div>
      <small>${info}</small>${!q.done && q.last ? `<small class="${q.last.win ? 'w' : 'l'}">${q.last.win ? '✓ just beat' : '✕ just lost to'} “${esc(q.last.t)}”${q.last.win ? ' · +5 🟡' : ''}</small>` : ''}</div></div>`; }).join('')}</div>`; }
(() => { const rj = renderJudge; renderJudge = function () { const r = rj.apply(this, arguments); try { const e = document.getElementById('qlS'), top = document.getElementById('vrTop'); if (e && top) top.parentNode.insertBefore(e, top); } catch (x) {} return r; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """html body .qv{margin:8px 2px 8px;padding:10px 12px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 2px #2F6B3F,0 4px 14px rgba(47,107,63,.12)}
.qv-h{margin:0 0 6px;font:900 .74rem Nunito,system-ui;letter-spacing:.08em;text-transform:uppercase;color:#22502F;text-align:left}
.qv-r{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid #E6EFE2}.qv-r:first-of-type{border-top:0;padding-top:2px}
.qv-r img{width:54px;height:68px;border-radius:9px;object-fit:cover;flex:none;box-shadow:0 0 0 2px #EADCC6}.qv-r.fin img{box-shadow:0 0 0 3px #D9AE4F}.qv-r.out img{filter:grayscale(.6);opacity:.75}
.qv-b{flex:1;min-width:0;text-align:left}.qv-t{display:flex;justify-content:space-between;align-items:center;gap:8px}.qv-t b{font:800 .98rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qv-t em{font-style:normal;font:900 .82rem Nunito,system-ui;color:#9A6B12;background:#FFF1C9;border-radius:999px;padding:2px 8px;white-space:nowrap}
.qv-st{display:flex;align-items:center;gap:4px;margin:4px 0 5px;font:800 .66rem Nunito,system-ui;text-transform:uppercase;letter-spacing:.04em}
.qv-st span{padding:2px 7px;border-radius:999px;background:#EEE6D8;color:#8A7B6C}.qv-st span.on{background:#14213D;color:#F3D98B}.qv-st span.done{background:#2F6B3F;color:#fff}.qv-st span.out{background:#C0533F;color:#fff}.qv-st i{font-style:normal;color:#B9AE9C}
.qv-bar{position:relative;height:14px;border-radius:7px;background:#E6EFE2;overflow:visible}.qv-bar i{display:block;height:100%;border-radius:7px;background:linear-gradient(90deg,#7FC48E,#2F6B3F);transition:width .5s}
.qv-bar u{position:absolute;right:-6px;top:50%;transform:translateY(-50%);text-decoration:none;font-size:.95rem}
.qv-n{display:flex;gap:10px;margin:4px 0 2px;font:800 .74rem Nunito,system-ui}.qv-n .w{color:#2F6B3F}.qv-n .l{color:#B0473A}.qv-n span:last-child{margin-left:auto;color:#14213D}
.qv-b small{display:block;font:700 .76rem/1.4 Nunito,system-ui;color:#3D4A5C}.qv-b small b{color:#14213D}.qv-b small b.cash{color:#2F6B3F}.qv-b small.w{color:#2F6B3F}.qv-b small.l{color:#A6402F}
html body .qv .ql-btn{margin-left:6px;padding:3px 10px;font-size:.76rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v153 ok')
# pass 2: compact rows when 2+ photos (pair stays on screen); small green Race button
s = open(d + 'yofi-real.html').read()
RA('return `<div class="qv" id="qlS"><p class="qv-h">', 'return `<div class="qv ${P.length > 1 ? \'cmp\' : \'\'}" id="qlS"><p class="qv-h">')
s = s.replace('</style>', """html body .qv.cmp .qv-r{padding:5px 0}html body .qv.cmp .qv-r img{width:38px;height:46px}html body .qv.cmp .qv-st,html body .qv.cmp .qv-n,html body .qv.cmp small.w,html body .qv.cmp small.l{display:none}
html body .qv.cmp .qv-t b{font-size:.86rem}html body .qv.cmp .qv-t em{font-size:.74rem;padding:1px 7px}html body .qv.cmp .qv-bar{height:9px;margin:3px 0 2px}html body .qv.cmp .qv-bar u{font-size:.75rem}
html body .qv .btn.ql-btn{display:inline-block;width:auto!important;min-height:0!important;padding:2px 10px!important;margin:0 0 0 6px!important;font-size:.74rem!important;line-height:1.6!important;background:#2F6B3F!important;color:#fff!important;border-radius:999px!important;box-shadow:none!important;vertical-align:1px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v153 pass2 ok')
