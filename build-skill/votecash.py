# Vote screen layout (Skill preview). Runs after votegoal.py.
# Top: the goal bar. Middle: "Which is better?" with a small streak widget (dots to the next gift + the gift).
# Below the photos: cash games only - one card, chosen in this order:
#   1. a friend's challenge waiting for your answer ("@larry challenged you · $1 each · View matchup")
#   2. the champion of your best photo's category ("Can Milo beat @kim, the Pets champion? · $1 entry · $12.40 pot")
#   3. the next tournament ("Quick tournament · starts in 04:12 · $1 entry · $25 guaranteed")
#   Champion and tournament take turns between pairs; viewing is free, money is only taken on the entry button inside.
#   The "Head-to-head in N votes" line moves down under the card. The big Wins x1 / gift strip is hidden.
# Usage: python3 build-skill/votecash.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function vgGoal(' not in s: sys.exit('run votegoal.py first')
if 'function vcCard(' in s: sys.exit('vote cash already applied')

JS = r'''
/* ---------- vote: small streak + one cash card under the photos ---------- */
function vcStreak() {
  const c = S.combo || 0, ms = [3, 6, 10], nx = ms.find(m => c < m) || 10, pv = [0, ...ms].filter(m => m < nx).pop(), done = Math.min(c, 10) - pv, n = nx - pv;
  return `<button class="vcs${done >= n - 1 ? ' near' : ''}" id="vcStk" aria-label="Streak ${c}. ${c >= 10 ? 'Top reward reached' : `${nx - c} more crowd picks in a row for ×${nx} coins`}">${[...Array(n)].map((_, i) => `<i class="${i < done ? 'on' : ''}"></i>`).join('')}<span class="vcs-sep"></span><span class="vcs-g">🎁<small>×${nx}</small></span></button>`;
}
function vcCard() {
  const fr = S.fr && (S.fr.ch || []).find(c => c.st === 'yours');
  if (fr) return { img: fr.theirSrc, t: `@${fr.f} challenged you`, s: `${stakeTxt(fr.stake)} each · winner takes ${prizeTxt(fr.stake)}`, cta: 'View matchup', go: () => fcAccept(fr) };
  S.vcTurn = (S.vcTurn || 0) + 1;
  const F = fighters(), best = F[0];
  if (best && S.vcTurn % 2) { const cat = best.cat || 'any', K = kingOf(cat), nm = GAL.PATH.includes(best.cat) ? alName(best) : 'your photo';
    return { img: K.src, t: `Beat the ${catLabel(cat)} champion`, s: `$1 entry · ${money(K.bounty)} pot`, who: `@${K.h} · vs your ${nm}`, cta: 'View matchup', go: () => openKing(cat), champ: 1 }; }
  const t = tSlots()[0];
  return { art: 1, t: 'Quick tournament', when: t.at, s: `$1 entry · US$${t.gtd} guaranteed`, cta: 'View tournament', go: () => openTourney() };
}
function vcPaint() {
  const j = $('#judge'), card = j && j.querySelector('#jcard'); if (!card) return;
  const h = j.querySelector('.tot-h'); if (h && !h.querySelector('#vcStk')) { const t = h.querySelector('h2'); if (t) { const row = document.createElement('div'); row.className = 'vch'; t.replaceWith(row); row.appendChild(t); row.insertAdjacentHTML('beforeend', vcStreak()); } }
  const st = $('#vcStk'); if (st) st.onclick = () => { const c = S.combo || 0, nx = [3, 6, 10].find(m => c < m); toast(nx ? `Pick the crowd favourite ${nx - c} more time${nx - c === 1 ? '' : 's'} in a row and your votes pay ×${nx}` : 'Top streak: your votes pay ×10'); };
  j.querySelectorAll('.vc, .vc-nxu').forEach(e => e.remove());
  const c = vcCard(); if (!c) return;
  const el = document.createElement('button'); el.className = 'vc';
  el.innerHTML = `${c.art ? `<span class="vc-art" aria-hidden="true">🏆</span>` : `<img src="${c.img}" alt="">`}<span class="vc-tx"><b>${esc(c.t)}</b>${c.when ? `<span class="vc-when">🕒 Starts in <span data-tat="${c.when}">${tLeft(c.when)}</span></span>` : ''}<small>${esc(c.s)}</small>${c.who ? `<em class="vc-who">${esc(c.who)}</em>` : ''}</span><span class="vc-cta">${c.cta}</span>`;
  el.onclick = c.go; card.insertAdjacentElement('afterend', el);
  const nu = h && h.querySelector('.nxu'); if (nu) nu.remove();
  const n = typeof nextUp === 'function' && nextUp(); if (n) el.insertAdjacentHTML('afterend', `<p class="vc-nxu">${n.k === 'tour' ? '🏆 Tournament' : n.k === 'cash' ? '🏅 Head-to-head' : '🟡 Practice challenge'} ${n.left === 1 ? 'after this vote' : `in <b>${n.left}</b> votes`}</p>`);
}
const _renderJudgeC2 = renderJudge;
renderJudge = function () { const r = _renderJudgeC2.apply(this, arguments); try { vcPaint(); } catch (e) {} return r; };
setInterval(() => { document.querySelectorAll('.vc [data-tat]').forEach(e => { e.textContent = tLeft(+e.dataset.tat); }); }, 1000);
'''
i = s.index("  shownGems = S.gems;\n})();\n})();"); s = s[:i] + JS + s[i:]

CSS = r'''
/* vote: streak widget + cash card */
#judge.has-goal .wcard{display:none!important}
#judge .jfoot .stk{display:none!important}
.vch{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 4px}.vch h2{margin:0!important;text-align:left}
.vcs{flex:none;display:flex;align-items:center;gap:5px;border:0;background:none;padding:6px 2px;cursor:pointer}
.vcs i{width:10px;height:10px;border-radius:50%;background:#DCCFB6}.vcs i.on{background:#9E2F2A}
.vcs-sep{width:1.5px;height:20px;background:#CDBFA8;margin:0 4px}
.vcs-g{position:relative;font-size:1.25rem;line-height:1}.vcs-g small{position:absolute;right:-12px;bottom:-6px;font:800 .62rem "Nunito Sans",sans-serif;color:#9E2F2A}
.vcs.near .vcs-g{animation:vcwob .9s ease-in-out infinite}@keyframes vcwob{50%{transform:rotate(-12deg) scale(1.15)}}
html.yg .vcs i{background:rgba(255,255,255,.2)}html.yg .vcs i.on{background:#FF2D8E}html.yg .vcs-g small{color:#FF7AB8}
.vc{display:flex;align-items:center;gap:12px;width:100%;margin:12px 0 4px;box-sizing:border-box;padding:9px;border:0;border-radius:18px;text-align:left;cursor:pointer;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE,0 6px 14px -10px rgba(60,40,20,.5);font-family:"Nunito Sans",sans-serif;color:#2D2521!important}
.vc img,.vc-art{flex:none;width:72px;height:72px;border-radius:12px;object-fit:cover}
.vc-art{display:grid;place-items:center;background:#2D4E86;font-size:2.2rem}
.vc-tx{flex:1;min-width:0}.vc-tx b{display:block;font:800 1.05rem/1.18 Fraunces,serif;color:#2D2521!important}
.vc-tx small{display:block;margin-top:3px;font-size:.86rem;color:#4E433C!important}
.vc-when{display:inline-block;margin-top:4px;padding:2px 9px;border-radius:999px;background:#F1E9DA;font-size:.78rem;font-weight:700;color:#2D2521!important}
.vc-cta{flex:none;width:92px;padding:8px 6px;border-radius:12px;background:#2D4E86;color:#fff!important;font:800 .8rem/1.15 "Nunito Sans",sans-serif;text-align:center;box-sizing:border-box}
#judge .jfoot:has(.en-hide){display:none}
html.yg .vc{background:#FBF6EC!important}
.vc-nxu{margin:6px 0 0;text-align:center;font-size:.86rem;opacity:.85}
.vc-who{display:block;margin-top:2px;font-style:normal;font-size:.76rem;font-weight:700;color:#8A5A0A!important}
#vgGoal.vg{width:100%;margin:6px 0 4px;box-sizing:border-box}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('vote cash ok')
