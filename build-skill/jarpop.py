# Skill preview: the coin jar receipt. One tap still collects (coins fly into the balance at once);
#  then a receipt pop shows what each photo earned since your last collect:
#   - "+56 🟡 collected · since 2h 40m ago"
#   - Your photos: thumb, name, tier, +coins
#   - Cards you stole (gold, every one you own, even at +0): "won from Maya +14" and "Stolen cards earned you +14 extra"
#     (no stolen cards yet: a gold teaser "Steal a card · it earns for you too")
#   - Taken from you (red): "Emma has it · missed about +12"
#  One button: "Win Tidepool back" / "Steal a card · free try" (navy, free), plus "Done".
#  Only when you tap the jar yourself (the "While you were away" pop has its own summary).
# usage: python3 build-skill/jarpop.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- coin jar receipt ----
const jpRate = p => GAL.BASE * galMult(p.s.total) * Math.max(.5, 1 + (p.s.total - 55) / 15);
const jpSnap = () => { S.jarSnap = {}; S.photos.forEach(p => { S.jarSnap[p.id] = p.gl || 0; }); S.jarLastC = Date.now(); };
if (!S.jarSnap) { jpSnap(); save(); }
let JP_TAP = 0;
document.addEventListener('click', e => { if (e.target.closest('#vgGoal')) JP_TAP = Date.now(); }, true);
const _jarCollectJP = jarCollect;
jarCollect = function () { const n = S.vgJar || 0, snap = S.jarSnap || {}, since = Date.now() - (S.jarLastC || Date.now()), tap = Date.now() - JP_TAP < 1500;
  const r = _jarCollectJP.apply(this, arguments); if (!n) return r;
  // what each photo earned since the last collect, scaled to what was collected
  const earn = S.photos.filter(p => p.s && !p.heldBy).map(p => ({ p, d: Math.max(0, (p.gl || 0) - (snap[p.id] || 0)) })).filter(x => x.d > 0);
  let tot = earn.reduce((a, x) => a + x.d, 0);
  if (!tot) { jarHung().forEach(p => earn.push({ p, d: jpRate(p) })); tot = earn.reduce((a, x) => a + x.d, 0); }
  let left = n; earn.sort((a, b) => b.d - a.d).forEach((x, i) => { x.c = i === earn.length - 1 ? left : Math.round(n * x.d / (tot || 1)); left -= x.c; });
  const hrs = Math.min(JAR_HRS, Math.max(.25, since / 36e5)), held = S.photos.filter(p => p.heldBy).map(p => ({ p, miss: Math.round(jpRate(p) * hrs) }));
  jpSnap(); save();
  const shown = earn.filter(x => x.c > 0); S.photos.filter(p => p.card && p.s && !p.heldBy && !shown.some(x => x.p === p)).forEach(p => shown.push({ p, c: 0 })); // every stolen card you own is listed
  if (tap) setTimeout(() => { try { jpShow(n, shown, held, since); } catch (e) {} }, 1100);
  return r; };
function jpShow(n, earn, held, since) { const co = $('#coach'); if (!co || co.classList.contains('on')) return;
  const per = p => galMult(p.s.total) * GAL.BASE, picks = x => x.c > 0 ? Math.max(1, Math.round(x.c / per(x.p))) : 0;
  const mine = earn.filter(x => !x.p.card), won = earn.filter(x => x.p.card), wonT = won.reduce((a, x) => a + x.c, 0), allPk = earn.reduce((a, x) => a + picks(x), 0), rc = typeof rivalCards === 'function' ? rivalCards() : [];
  const ago = since < 36e5 ? `${Math.max(1, Math.round(since / 6e4))} min` : (Math.round(since % 36e5 / 6e4) ? `${Math.floor(since / 36e5)}h ${Math.round(since % 36e5 / 6e4)}m` : `${Math.floor(since / 36e5)}h`);
  const tier = p => { const t = galTier(p.s.total); return `<i class="jp-t t-${t ? t.toLowerCase() : 'none'}">${t ? `${t === 'Gold' ? '🥇' : t === 'Diamond' ? '💎' : '🏆'} ${t}` : 'No tier'}</i>`; };
  let k = 0; const row = (x, sub, cls = '') => `<div class="jp-r ${cls}" style="animation-delay:${(.35 + k++ * .18).toFixed(2)}s"><img src="${x.p.src}" alt=""><span><b>${esc(alName(x.p))}</b><small>${sub}</small></span><em data-jc="${x.c}" data-jd="${(.35 + (k - 1) * .18).toFixed(2)}">+0</em></div>`;
  const pk = x => `${per(x.p)} 🟡 a vote`;
  const h = held[0], lt = stlLeft(), go = h ? { t: `Win ${alName(h.p)} back`, fn: () => stealSheet({ back: h.p.id }) } : rc.length ? { t: lt ? `Steal a card · ${lt} free tr${lt === 1 ? 'y' : 'ies'} left` : 'Steal a card · new tries tomorrow', fn: () => stealSheet({}) } : null;
  co.innerHTML = `<div class="crbox jpbox" role="dialog" aria-modal="true" aria-labelledby="jpT"><div class="cr-rays wp-rays" aria-hidden="true"></div>
    ${[...Array(18)].map((_, i) => `<i class="wp-cf" style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B'][i % 5]};animation-delay:${(i * .09).toFixed(2)}s"></i>`).join('')}
    <span class="jp-pay">💰 Payday</span>
    <h2 id="jpT"><span>+<b id="jpN">0</b></span> ${gemIcon('jp-ci')}</h2>
    <p class="jp-sub">🗳 Voters picked your photos in the last <b>${ago}</b></p>
    <div class="jp-list">
      ${mine.length ? `<h3>📸 Your photos earned</h3>${mine.map(x => row(x, `${tier(x.p)}${pk(x)}`)).join('')}` : ''}
      <h3 class="g">🃏 Stolen cards · bonus</h3>${won.length ? won.map(x => row(x, `${tier(x.p)}${pk(x)} · from ${esc(rvName(x.p.card.from))}`, 'won')).join('') + (wonT ? `<p class="jp-note" style="animation-delay:${(.45 + k * .18).toFixed(2)}s">🎉 Stealing earned you <b>+${wonT}</b> extra</p>` : '')
        : `<div class="jp-r won tease" data-jst="1" style="animation-delay:${(.35 + k++ * .18).toFixed(2)}s"><span class="jp-fan">${rc.slice(0, 2).map(x => `<img src="${x.src}" alt="">`).join('')}</span><span><b>Steal a card</b><small>It earns coins for you too</small></span><em>?</em></div>`}
      ${held.length ? `<h3 class="r">😤 Taken from you</h3>${held.map(x => `<div class="jp-r lost" style="animation-delay:${(.35 + k++ * .18).toFixed(2)}s"><img src="${x.p.src}" alt=""><span><b>${esc(alName(x.p))}</b><small>${esc(rvName(x.p.heldBy))} is earning from it now</small></span><em><small>missed</small>~${x.miss}</em></div>`).join('')}` : ''}
    </div>
    ${go ? `<button class="bt-cta jp-go" id="jpGo">${esc(go.t)}</button>` : ''}<button class="bt-no" id="jpNo">${go ? 'Done' : 'Nice! Back to voting'}</button></div>`;
  co.classList.add('on', 'cr');
  const close = () => { co.classList.remove('on', 'cr'); co.innerHTML = ''; };
  if ($('#jpGo')) $('#jpGo').onclick = () => { close(); go.fn(); };
  $('#jpNo').onclick = close; co.onclick = e => { if (e.target === co) close(); };
  co.querySelectorAll('[data-jst]').forEach(r => r.onclick = () => { close(); stealSheet({}); });
  const count = (el, to, ms, delay, pre) => { const t0 = performance.now() + delay * 1000; const tick = t => { if (!el.isConnected) return; const q = Math.max(0, Math.min(1, (t - t0) / ms)); el.textContent = pre + Math.round(to * (1 - Math.pow(1 - q, 3))); if (q < 1) requestAnimationFrame(tick); else if (pre) { el.classList.add('pop'); } }; requestAnimationFrame(tick); };
  count($('#jpN'), n, 1100, .1, '');
  co.querySelectorAll('[data-jc]').forEach(e => count(e, +e.dataset.jc, 600, +e.dataset.jd + .2, '+')); }
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* coin jar receipt */
html body #coach .jpbox{position:relative;overflow:hidden}
.jp-pay{display:inline-block;align-self:center;margin-top:2px;padding:4px 14px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;font:900 .78rem "Nunito Sans";letter-spacing:.08em;text-transform:uppercase;box-shadow:0 4px 10px -6px rgba(160,110,10,.8);animation:jpBounce .6s cubic-bezier(.3,1.6,.5,1) both}
.jp-sub b{color:#2D4E86}
.jp-r,.jp-note{animation:jpIn .45s cubic-bezier(.2,1.2,.4,1) both}
@keyframes jpIn{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:none}}
@keyframes jpBounce{from{transform:scale(.3)}to{transform:none}}
.jp-r em.pop{animation:jpPop .35s ease-out}@keyframes jpPop{50%{transform:scale(1.35)}}
html body #coach .jpbox .wp-drop,html body #coach .jpbox .wp-cf{z-index:0!important;opacity:.55}html body #coach .jpbox>*:not(.wp-drop):not(.wp-cf):not(.cr-rays){position:relative;z-index:2}
html body #coach .jpbox{max-height:86vh;display:flex;flex-direction:column;text-align:center}
.jpbox h2{display:flex;align-items:center;justify-content:center;gap:6px;margin:4px 0 0;font:900 2.6rem/1 Fraunces,serif;color:#2D4E86}.jpbox .jp-ci{width:34px;height:34px}
.jp-sub{margin:4px 0 10px;font:700 .85rem "Nunito Sans";color:#4E433C}
.jp-list{overflow-y:auto;text-align:left;margin:0 -4px;padding:0 4px}
.jp-list h3{margin:10px 0 6px;font:900 .74rem "Nunito Sans";letter-spacing:.07em;text-transform:uppercase;color:#4E433C}.jp-list h3.g{color:#8A5A0A}.jp-list h3.r{color:#A3372A}
.jp-r{display:flex;align-items:center;gap:10px;padding:7px 10px 7px 7px;margin-bottom:6px;border-radius:14px;background:#FFFDF9;box-shadow:inset 0 0 0 1.5px #E2D5BE}
.jp-r img{width:40px;height:48px;border-radius:8px;object-fit:cover;flex:none}
.jp-r>span{flex:1;min-width:0}.jp-r b{display:block;font:900 .98rem Fraunces,serif;color:#2D2521;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.jp-r small{display:flex;align-items:center;gap:5px;font:700 .74rem "Nunito Sans";color:#4E433C;white-space:nowrap}
.jp-r em{flex:none;font:900 1.05rem "Nunito Sans";font-style:normal;color:#2D4E86}
.jp-r.won{background:#FFF3D6;box-shadow:inset 0 0 0 2px #E0A82E}.jp-r.won em{color:#8A5A0A}.jp-r.won img{box-shadow:0 0 0 2px #E0A82E}
.jp-r.lost{background:#FBECE8;box-shadow:inset 0 0 0 1.5px #E7B8AE}.jp-r.lost img{filter:grayscale(.7)}.jp-r.lost em{color:#A3372A;text-align:right;line-height:1.1}.jp-r.lost em small{display:block;font:800 .62rem "Nunito Sans";text-transform:uppercase;letter-spacing:.05em}
.jp-r.tease{cursor:pointer}.jp-fan{position:relative;width:44px;height:48px;flex:none!important}.jp-fan img{position:absolute;width:30px;height:40px}.jp-fan img:first-child{left:0;top:4px;transform:rotate(-10deg)}.jp-fan img:nth-child(2){right:0;top:0;transform:rotate(8deg)}
.jp-x{font-style:normal;font:900 .7rem "Nunito Sans";padding:1px 6px;border-radius:99px;background:#1F3157;color:#fff}.jp-t.t-none{background:#EFE6D6;color:#4E433C}
.jp-t{font-style:normal;font:900 .62rem "Nunito Sans";padding:1px 6px;border-radius:99px;background:#F3D27A;color:#3A2600}.jp-t.t-diamond{background:#CFE0F5;color:#1F3157}.jp-t.t-platinum{background:#E3E6EA;color:#2E3440}
.jp-note{margin:0 2px 4px;font:800 .8rem "Nunito Sans";color:#8A5A0A}.jp-note.r{color:#A3372A}
html body #coach .jpbox .jp-go{background:#2D4E86!important;color:#fff!important;margin-top:12px}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('jarpop ok')
