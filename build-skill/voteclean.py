# Cleaner Vote screen (Skill). Run after popqueue.py.
# Vote keeps three things: one rank line at the top, the two photos, and one card line under them.
# - Removed from Vote: the "Your photo · goal" touch-up card, the ticket strip, the wins bar with
#   three boxes (replaced by small progress dots to the next box) and the "Your eye" line.
# - Rank line: your best card's place today among cards ranked by today's vote wins, and how many
#   wins to the top 10. Tap it for the top 10 (simulated rivals in this prototype).
# - Card line: your best card, today's wins and coins, tier, points to the next tier, Touch up ›.
# Usage: python3 build-skill/voteclean.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function rankBoard(' in s: sys.exit('voteclean already applied')
assert 'const POPQ =' in s, 'run popqueue.py first'
JS = r'''
/* ---------- cleaner Vote screen: rank line + photos + card line ---------- */
function rankBoard() {
  const now = new Date(), frac = Math.min(1, (now.getHours() * 60 + now.getMinutes()) / (21 * 60)), seed = todayKey().split('-').reduce((a, x) => a * 31 + +x, 7);
  const rnd = i => { const x = Math.sin(seed + i * 97.13) * 10000; return x - Math.floor(x); };
  const mine = new Set(S.photos.map(x => x.src)), pics = SEED.filter(x => x.src && !mine.has(x.src));
  const others = OPP.slice(0, 14).map((o, i) => ({ h: '@' + o.h, src: pics[i % pics.length].src, w: Math.round((6 + 40 * Math.pow(rnd(i), 1.6)) * (0.25 + 0.75 * frac)), tier: rnd(i + 50) > .6 ? 2 : rnd(i + 50) > .3 ? 1 : 0 }));
  const D = cwDay(), best = S.photos.filter(x => x.s).sort((a, b) => (D.by[b.id] || 0) - (D.by[a.id] || 0) || b.s.total - a.s.total)[0];
  const me = best ? { me: 1, h: 'Your card', src: best.src, w: D.by[best.id] || 0, tier: cardTier(best.s.total), p: best } : null;
  const all = others.concat(me ? [me] : []).sort((a, b) => b.w - a.w || (a.me ? 1 : -1));
  const rank = me ? all.indexOf(me) + 1 : 0, tenth = all[9];
  return { all, me, rank, toTop: me && rank > 10 ? tenth.w - me.w + 1 : 0 };
}
function paintVoteClean() {
  const j = $('#judge'); if (!j) return;
  j.querySelectorAll('.wcard, .vstrip, .eye, .jfoot').forEach(e => e.style.display = 'none');
  const B = rankBoard(), head = j.querySelector('.tot-h');
  let r = j.querySelector('.vc-rank');
  if (B.me) {
    if (!r) { r = document.createElement('button'); r.className = 'vc-rank'; r.onclick = openRankBoard; if (head) head.before(r); else j.prepend(r); }
    r.innerHTML = `<img src="${B.me.src}" alt=""><span><b>${esc(B.me.h)} #${B.rank}</b> in today’s top cards</span><em>${B.rank <= 10 ? 'Top 10 ✓' : `${B.toTop} win${B.toTop === 1 ? '' : 's'} to top 10`}</em>`;
  } else if (r) r.remove();
  let d = j.querySelector('.vc-dots'); const tot = j.querySelector('.tot');
  if (!d && tot) { d = document.createElement('div'); d.className = 'vc-dots'; d.setAttribute('aria-label', 'Right picks in a row'); tot.after(d); }
  if (d) { const c = S.combo || 0, nx = STK.find(n => n > c) || STK[STK.length - 1], prev = [0].concat(STK).filter(n => n <= c).pop() || 0, need = nx - prev;
    d.innerHTML = [...Array(need)].map((_, i) => `<i class="${i < c - prev ? 'on' : ''}"></i>`).join('') + '<span>🎁</span>'; }
  paintCardStrip();
}
paintCardStrip = function () {
  const j = $('#judge'); if (!j) return; let el = j.querySelector('.pc-strip');
  if (!S.photos.some(x => x.s)) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement('button'); el.className = 'pc-strip'; const d = j.querySelector('.vc-dots') || j.querySelector('.tot'); if (d) d.after(el); else j.appendChild(el); }
  const D = cwDay(), best = S.photos.filter(x => x.s).sort((a, b) => (D.by[b.id] || 0) - (D.by[a.id] || 0) || b.s.total - a.s.total)[0], k = cardTier(best.s.total), t = CARD_T[k], nx = CARD_T[k + 1], w = D.by[best.id] || 0;
  el.innerHTML = `<img src="${best.src}" alt=""><span><b>Your card · ${w} win${w === 1 ? '' : 's'} · +${w * t.pay}</b><small>${t.n} ×${t.x}${nx ? ` · ${nx.at - best.s.total} to ${nx.n}` : ''}</small></span><em>Touch up ›</em>`;
  el.onclick = () => { S.cur = best.id; S.pcView = 'touch'; save(); go('studio'); renderStudio(); };
};
function openRankBoard() {
  const B = rankBoard(), top = B.all.slice(0, 10), mine = B.me && B.rank > 10 ? [B.me] : [];
  const row = (x, i) => `<div class="vc-r${x.me ? ' me' : ''}"><span class="n">${i}</span><img src="${x.src}" alt=""><span><b>${esc(x.h)}</b><small>${CARD_T[x.tier].n}</small></span><strong>${x.w}<small>wins</small></strong></div>`;
  openSheet(`<div class="vc-board"><h2>Top cards today</h2><p class="sub">Ranked by votes each card won today. Resets at midnight.</p>
    ${top.map((x, i) => row(x, i + 1)).join('')}${mine.length ? `<p class="vc-gap">···</p>${row(B.me, B.rank)}` : ''}
    ${B.me ? `<button class="btn block vc-go" id="vcTu">Touch up your card to win more</button>` : ''}<div style="text-align:center"><button class="link" data-shclose>Back to voting</button></div></div>`);
  document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
  if ($('#vcTu')) $('#vcTu').onclick = () => { closeSheet(); S.cur = B.me.p.id; S.pcView = 'touch'; save(); go('studio'); renderStudio(); };
}
const _renderJudgeV = renderJudge;
renderJudge = function () { const r = _renderJudgeV.apply(this, arguments); try { paintVoteClean(); } catch (e) {} return r; };
const _voteV = vote;
vote = async function () { const r = await _voteV.apply(this, arguments); try { paintVoteClean(); } catch (e) {} return r; };
'''
end = "  shownGems = S.gems;\n})();\n})();"
assert s.count(end) == 1
s = s.replace(end, JS + end)
CSS = r'''
.vc-rank,html:not(.yg) .vc-rank{background:#2D4E86!important;color:#fff!important}.vc-rank{display:flex;align-items:center;gap:10px;width:100%;margin:2px 0 10px;padding:7px 8px 7px 8px;border:0;border-radius:999px;background:#2D4E86;color:#fff;font:inherit;text-align:left}
html.yg .vc-rank{background:#2A1B47!important;box-shadow:inset 0 0 0 1.5px #5A4A78}
.vc-rank img{width:30px;height:36px;object-fit:cover;border-radius:7px;flex:none}
.vc-rank span{font-size:.9rem;line-height:1.25;min-width:0}.vc-rank b{color:#FFD86B}
.vc-rank em{margin-left:auto;flex:none;font-style:normal;font-weight:800;font-size:.8rem;background:#F3C447;color:#2A1600;border-radius:999px;padding:6px 11px;white-space:nowrap}
.vc-dots{display:flex;gap:6px;justify-content:center;align-items:center;margin:12px 0 0}.vc-dots i{width:9px;height:9px;border-radius:50%;background:rgba(0,0,0,.15)}html.yg .vc-dots i{background:rgba(255,255,255,.2)}.vc-dots i.on{background:#E9A514}.vc-dots span{font-size:.9rem}
#judge .pc-strip{margin-top:12px}#judge .pc-strip em{color:#2D4E86}html.yg #judge .pc-strip em{color:#FFD86B}
.vc-board h2{margin:0 0 2px}.vc-board .sub{margin:0 0 10px;opacity:.75;font-size:.9rem}
.vc-r{display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:12px}.vc-r.me{background:rgba(45,78,134,.12);box-shadow:inset 0 0 0 2px #2D4E86}
.vc-r .n{width:22px;text-align:center;font-weight:900}.vc-r img{width:36px;height:44px;object-fit:cover;border-radius:7px}.vc-r b{display:block;font-size:.95rem}.vc-r small{opacity:.7;font-size:.75rem}
.vc-r strong{margin-left:auto;text-align:right;font-size:1.05rem}.vc-r strong small{display:block;font-weight:600}
.vc-gap{text-align:center;opacity:.5;margin:2px 0}#sheetBody .vc-go,html .btn.block.vc-go{margin-top:12px;background:#F3C447!important;color:#2A1600!important;box-shadow:none!important}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('voteclean ok')
