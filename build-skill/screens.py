# Skill preview: Rematch and Quick Sprint screens redone to the user's mock-ups.
#  Rematch (cash jackpot rematch):
#   - big "REMATCH?" + "The Pet blue ribbon is still in play."
#   - both photos with a "Score 84" pill, names under; tap your photo ("Change" chip) to swap photos
#   - "<weakest part> made the difference"
#   - "Choose your entry" chips $1 / $2 / $5 with the stars a win earns (doubled for a rematch)
#   - one gold "Touch up <part>" row (coins), green "Rematch for $2", "Win to earn 4 stars"
#     (max 2 actions: "Choose another photo" moved onto your photo; the X closes)
#  Quick Sprint: illustrated rival / you avatars in round frames with the eye % in a red / navy pill
#   (your profile photo is used for "You" when you have one). Art: assets/av_rival.jpg, av_you.jpg.
# usage: python3 build-skill/screens.py in.html out.html
import sys, base64, os
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
b64 = lambda f: 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(A, f), 'rb').read()).decode()

JS = "const AV_RIVAL = '" + b64('av_rival.jpg') + "', AV_YOU = '" + b64('av_you.jpg') + "';\n" + r'''
// ---- Rematch screen ----
const _revengePrepSC = revengePrep;
revengePrep = function (c, k, h, pid) { if (c || !isCash()) return _revengePrepSC.apply(this, arguments);
  const pool = S.photos.filter(p => fitsTheme(p, k) && p.s.total >= CFG.QUALIFY && !p.heldBy).sort((a, b) => b.s.total - a.s.total);
  const p = S.photos.find(x => x.id === pid) || pool[0]; if (!p) { addCatPhoto(k); return; }
  const weak = C.reduce((a, x) => (p.s[x.k] < p.s[a.k] ? x : a)), their = (lgS().pl.find(x => x.h === h) || {}).sc, tsc = their ? their[k] : Math.min(97, p.s.total + 5), canE = !photoLock(p) && lowestOpen(p);
  const st = LG_STAKES.includes(LG_FEE) ? LG_FEE : 2, again = () => revengePrep(c, k, h, p.id), G = gemIcon('');
  openSheet(`<div class="rm2">
    <h1 class="rm2-h">REMATCH?</h1><p class="rm2-s">The ${esc(crownName(k))} blue ribbon is still in play.</p>
    <div class="rm2-vs"><figure class="th"><span class="rm2-ph"><span class="wr-cr">${CRW}</span><img src="${lgPhoto(h, k)}" alt=""><i>Score ${tsc}</i></span><figcaption>@${esc(h)}</figcaption></figure><span class="rm2-x2">VS</span>
      <figure class="me"><button class="rm2-ph" id="rmSwap" aria-label="Choose another photo"><img src="${p.src}" alt=""><i>Score ${p.s.total}</i>${pool.length > 1 ? '<b class="rm2-chg">Change</b>' : ''}</button><figcaption>You</figcaption></figure></div>
    <div class="rv-sw rm2-sw" id="rvList" hidden>${pool.map(x => `<button data-rvp="${x.id}" aria-pressed="${x.id === p.id}"><img src="${x.src}" alt=""><i>${x.s.total}</i></button>`).join('')}</div>
    <h3 class="rm2-why">${esc(weak.name)} made the difference</h3>
    <div class="rm2-card"><div class="rm2-ct"><b>Choose your entry</b><span>USD</span></div>
      <div class="rm2-st">${LG_STAKES.map(v => `<button data-rst="${v}" aria-pressed="${v === st}"><b>$${v}</b><small>★ ${v * 2} stars</small></button>`).join('')}</div></div>
    ${canE ? `<button class="rm2-tu" id="rvEnh"><span class="rm2-ti">✨</span><span><b>Touch up ${esc(weak.name.toLowerCase())}</b><small>Strengthen your photo first</small></span><em>${fixCost(p) ? fixCost(p) + ' ' + G : 'Free'}</em></button>` : ''}
    <button class="btn block rm2-go" id="rvGo">Rematch for $${st}</button><p class="rm2-win">Win to earn <b>${st * 2} stars</b> · double for a rematch</p></div>`, { full: true, cover: true });
  document.querySelectorAll('#sheetBody [data-shclose]').forEach(b => b.onclick = () => closeSheet());
  document.querySelectorAll('#sheetBody [data-rst]').forEach(b => b.onclick = () => { S.lgStake = +b.dataset.rst; LG_FEE = S.lgStake; save(); again(); });
  $('#rmSwap').onclick = () => { if (pool.length > 1) $('#rvList').hidden = !$('#rvList').hidden; };
  document.querySelectorAll('#sheetBody [data-rvp]').forEach(b => b.onclick = () => revengePrep(c, k, h, b.dataset.rvp));
  if ($('#rvEnh')) $('#rvEnh').onclick = () => { window.__pickRet = { label: 'Back to rematch', go: () => { closeFlow(); again(); } }; closeSheet(); startEnhance(p, weak.k); };
  $('#rvGo').onclick = () => lgPay(() => lgFight(k, h, lgHold(k).h === h, true, p.id)); };
// ---- Quick Sprint: avatars instead of rings ----
const _qsSheetSC = qsSheet;
qsSheet = function () { const r = _qsSheetSC.apply(this, arguments);
  try { const box = document.querySelector('#sheetBody .pj-vs'); if (box) { const av = (side, img, cls) => { const f = box.querySelector(side); if (!f) return; const ph = f.querySelector('.pj-ph'); if (!ph) return; const lab = (ph.querySelector('b') || {}).textContent || '?';
      ph.outerHTML = `<span class="qs-av ${cls}"><img src="${img}" alt=""><i>${esc(lab)}</i></span>`; };
    av('.pj-them', AV_RIVAL, 'rv'); av('.pj-me', (S.user && S.user.pic) || AV_YOU, 'me'); box.classList.add('qs-avs'); } } catch (e) {}
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* Rematch */
.rm2{position:relative;padding:6px 4px 20px;text-align:center}
html body #sheetBody .rm2-x{position:absolute;right:0;top:0;width:36px;height:36px;border:0;background:none;font:900 1.3rem "Nunito Sans";color:#2D2521;cursor:pointer}
.rm2-h{margin:10px 0 0;font:900 3rem/1 Fraunces,serif;color:#2D2521;letter-spacing:.01em;text-shadow:0 3px 0 rgba(45,37,33,.15)}
.rm2-s{margin:8px 0 16px;font:700 1.02rem "Nunito Sans";color:#2D2521}
.rm2-vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:0}.rm2-vs figure{margin:0}
.rm2-ph{position:relative;display:block;width:100%;padding:0;border:0;background:none;cursor:pointer}
.rm2-ph img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:22px}
.th .rm2-ph img{box-shadow:0 0 0 5px #F3C24A}.me .rm2-ph img{box-shadow:0 0 0 5px #2D4E86}
.rm2-ph>i{position:absolute;left:10px;bottom:10px;padding:5px 12px;border-radius:99px;background:#1F3157;color:#fff;font:800 .95rem "Nunito Sans";font-style:normal;box-shadow:0 0 0 2px #fff}
.rm2-ph .wr-cr{position:absolute;left:50%;top:-14px;transform:translateX(-50%);z-index:1}
.rm2-chg{position:absolute;right:10px;top:10px;padding:4px 10px;border-radius:99px;background:rgba(255,253,249,.92);color:#1F3157;font:800 .72rem "Nunito Sans"}
.rm2-x2{position:relative;z-index:2;width:58px;height:58px;margin:0 -14px;border-radius:50%;background:#2D4E86;color:#fff;font:900 1.25rem/58px Fraunces,serif;box-shadow:0 0 0 5px #F7F0E4}
.rm2-vs figcaption{margin-top:8px;font:800 1rem "Nunito Sans";color:#2D2521}
.rm2-sw{margin-top:10px}
html body #sheetBody .rm2-why{margin:22px 0 14px!important;font:900 1.35rem Fraunces,serif;color:#2D2521}
.rm2-card{padding:14px;border-radius:20px;background:#FFFDF9;box-shadow:inset 0 0 0 2px #F3C24A;text-align:left}
.rm2-ct{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.rm2-ct b{font:900 1.35rem Fraunces,serif;color:#2D2521}.rm2-ct span{padding:4px 12px;border-radius:99px;background:#F1E6D2;font:800 .78rem "Nunito Sans";color:#4E433C}
.rm2-st{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
html body #sheetBody .rm2-st button{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;padding:14px 4px;border:0;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #E2D5BE;cursor:pointer;font-family:inherit}
.rm2-st button b{font:900 1.9rem/1 Fraunces,serif;color:#2D2521}.rm2-st button small{font:800 .85rem "Nunito Sans";color:#2D2521;white-space:nowrap}
html body #sheetBody .rm2-st button[aria-pressed="true"]{background:#E9F7EE;box-shadow:inset 0 0 0 3px #2E9A5C}
.rm2-st button[aria-pressed="true"]::after{content:"✓";position:absolute;right:-6px;top:-6px;width:24px;height:24px;border-radius:50%;background:#2E9A5C;color:#fff;font:900 .8rem/24px "Nunito Sans";box-shadow:0 0 0 2px #fff}
html body #sheetBody .rm2-tu{display:flex;align-items:center;gap:12px;width:100%;margin-top:12px;padding:12px 14px;border:0;border-radius:18px;background:#FFF6DD;box-shadow:inset 0 0 0 1.5px #E8C771;text-align:left;font-family:inherit;cursor:pointer}
.rm2-ti{font-size:1.6rem}.rm2-tu>span:nth-child(2){flex:1}.rm2-tu b{display:block;font:900 1.05rem "Nunito Sans";color:#2D2521}.rm2-tu small{font:700 .82rem "Nunito Sans";color:#4E433C}.rm2-tu em{display:flex;align-items:center;gap:4px;font:900 1.05rem "Nunito Sans";font-style:normal;color:#3A2600}
html body #sheetBody .rm2-go{margin-top:16px;min-height:58px;background:linear-gradient(180deg,#2E9A5C,#1E7A44)!important;color:#fff!important;font:900 1.4rem Fraunces,serif!important;box-shadow:0 10px 20px -10px rgba(33,120,74,.8)!important}
.rm2-win{margin:8px 0 0;font:700 .95rem "Nunito Sans";color:#2D2521}.rm2-win b{color:#1E6B3E}
/* Quick Sprint avatars */
html body #sheetBody .qs-avs{align-items:center!important}html body #sheetBody .qs-avs figure{background:none!important;box-shadow:none!important;padding:0!important}
html body #sheetBody .qs-av{position:relative;display:block;width:100%;max-width:170px;height:auto!important;min-height:0!important;margin:0 auto 22px;aspect-ratio:1!important;overflow:visible!important;padding:0!important;background:none!important;border:0!important;box-shadow:none!important;border-radius:0!important}
html body #sheetBody .qs-av img{display:block;width:100%!important;height:100%!important;max-width:none!important;aspect-ratio:1!important;border-radius:50%!important;object-fit:cover!important;margin:0!important}
.qs-av.rv img{box-shadow:0 0 0 4px #A83A2A,0 10px 22px -10px rgba(0,0,0,.5)}.qs-av.me img{box-shadow:0 0 0 4px #1F3157,0 10px 22px -10px rgba(0,0,0,.5)}
.qs-av i{position:absolute;left:50%;bottom:-18px;transform:translateX(-50%);min-width:84px;padding:4px 14px;border-radius:99px;font:900 1.4rem/1.2 Fraunces,serif;font-style:normal;color:#fff;text-align:center;box-shadow:0 0 0 3px #F7F0E4}
.qs-av.rv i{background:#A83A2A}.qs-av.me i{background:#1F3157}
html body #sheetBody .qs-avs figcaption{margin-top:6px}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('screens ok')
