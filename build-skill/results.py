# Skill preview: every cash game's result uses one screen, matching the game screen.
#   1. icon + name, and "Pet · final result"
#   2. headline: "You won!" / "@rival won", with the vote score
#   3. a prize box: what you won (green), or what you lost (neutral) with one tip
#   4. the VS picture: rival left, you right, a WINNER tag, votes under each, the vote bar
#   5. one big green button (Play again / Rematch · $1) and one small link (Back to voting)
# Covers jackpot challenges, head-to-head and friend challenges. Also: your stars today show
# big and gold on the Compete jackpot photos.
# usage: python3 build-skill/results.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- one result screen for every cash game ----
function gsResult() { const sb = $('#sheetBody'); if (!sb) return;
  const jp = sb.querySelector('#lb .pr3'), kg = sb.querySelector('.kg2 .kg2-fin') && sb.querySelector('.kg2#du, .kg2#fb');
  const root = jp || kg; if (!root || root.dataset.gsr) return; root.dataset.gsr = 1;
  const T = e => e ? e.textContent.replace(/\s+/g, ' ').trim() : '';
  let o;
  if (jp) { const figs = jp.querySelectorAll('.pr3-vs figure'), me = figs[0], th = figs[1], won = jp.classList.contains('w');
    const g = (T(jp.querySelector('.pr3-s')).match(/\+(\d+)\s*⭐/) || [])[1], share = T(jp.querySelector('.pr3-pool p'));
    const btn = jp.querySelector('#lbRev') || jp.querySelector('#lbMore') || jp.querySelector('#lbNew'), tip = jp.querySelector('#lbTip');
    o = { ic: '💰', nm: `${T(jp.querySelector('.pr3-k'))} jackpot`, won, them: T(th.querySelector('figcaption')), mv: parseInt(T(me.querySelector('strong'))) || 0, tv: parseInt(T(th.querySelector('strong'))) || 0,
      mi: (me.querySelector('img') || {}).src, ti: (th.querySelector('img') || {}).src,
      box: won ? { k: 'You won', b: `+${g || 1} ⭐`, s: share.replace(/^\d+ stars? · /, 'Your share now: ').replace('you’re in · ', '') } : { k: 'You lost', b: isCash() ? money(LG_FEE).replace('.00', '') : LG_COIN + ' 🟡', s: 'Stars you won today stay yours' },
      btn, tipBtn: tip, rib: T(jp.querySelector('.pr3-s')) };
  } else { const id = kg.id, mine = kg.querySelector('.kg2-ph.me'), won = mine && mine.classList.contains('won'), who = kg.querySelector('.kg2-who .king'), nx = kg.querySelector('.kg2-next');
    o = { ic: id === 'fb' ? '🤝' : '⚔️', nm: id === 'fb' ? 'Friend challenge' : 'Head-to-head', cat: T(kg.querySelector('.kg2-cat')), won,
      them: (T(who.querySelector('small')).startsWith('@') ? T(who.querySelector('small')) : T(who.querySelector('b'))), mv: parseInt(T(kg.querySelector('#duMn, #fbM'))) || 0, tv: parseInt(T(kg.querySelector('#duRn, #fbT'))) || 0,
      mi: (kg.querySelector('.kg2-ph.me img') || {}).src, ti: (kg.querySelector('.kg2-ph.king img') || {}).src,
      box: won ? { k: 'You won', b: T(nx && nx.querySelector('b')), s: 'Added to your cash' } : { k: 'You lost', b: T(nx && nx.querySelector('b')), s: 'Touch up your photo to win more votes' },
      btn: kg.querySelector('#duAgain, #fbMore') };
    if (o.btn && id === 'fb' && !/\$/.test(o.btn.textContent)) o.btn.textContent = 'Rematch';
  }
  const mg = Math.abs(o.mv - o.tv), N = o.mv + o.tv || 1, pm = Math.round(o.mv / N * 100), cat = o.cat ? o.cat.charAt(0) + o.cat.slice(1).toLowerCase() : '';
  const fig = (src, nm, v, w, me) => `<figure class="${me ? 'pj-me' : 'pj-them'} ${w ? 'gr-w' : 'gr-l'}"><span class="pj-ph"><img src="${src || ''}" alt="">${w ? '<i class="gr-tag">🏆 WINNER</i>' : ''}</span><figcaption>${esc(nm)}<small>${v} vote${v === 1 ? '' : 's'}</small></figcaption></figure>`;
  const wrap = document.createElement('div'); wrap.className = `pj gs gr ${o.won ? 'won' : 'lost'}`;
  wrap.innerHTML = `${o.won ? '<div class="wr-cf" aria-hidden="true">' + [...Array(14)].map((_, i) => `<i style="left:${(i * 37) % 95}%;animation-delay:${(i * .11).toFixed(2)}s"></i>`).join('') + '</div>' : ''}
    <div class="pj-top"><span class="pj-t">${o.ic} ${esc(o.nm)}</span><button class="pj-x" data-shclose aria-label="Close">✕</button></div><p class="gs-what">${cat ? esc(cat) + ' · ' : ''}Final result</p>
    <h2 class="gr-h">${o.won ? 'You won!' : `${esc(o.them)} won`}<small>${mg ? `by ${mg} vote${mg === 1 ? '' : 's'}` : 'a tie'} · ${o.mv}–${o.tv}</small></h2>
    <div class="pj-pot gr-box ${o.won ? '' : 'neu'}"><small class="gs-pl">${o.box.k}</small><b>${esc(o.box.b)}</b><span>${esc(o.box.s)}</span></div>
    <div class="pj-vs">${fig(o.ti, o.them, o.tv, !o.won)}<span class="pj-x2">VS</span>${fig(o.mi, 'You', o.mv, o.won, 1)}</div>
    <div class="gr-bar"><i style="width:${100 - pm}%">${100 - pm}%</i><i style="width:${pm}%">${pm}%</i></div>
    <div class="gr-acts"></div><button class="link pj-how" data-shclose>${$('#panes').dataset.at === 'judge' ? 'Back to voting' : 'Back to Compete'}</button>`;
  const acts = wrap.querySelector('.gr-acts');
  if (o.btn) { o.btn.className = 'btn block pj-go'; o.btn.querySelectorAll('svg').forEach(x => x.remove()); acts.appendChild(o.btn); }
  if (!o.won && o.tipBtn) { const t = document.createElement('button'); t.className = 'link gr-tip'; t.textContent = '✨ Touch up your photo first'; t.onclick = () => o.tipBtn.click(); wrap.querySelector('.gr-box').appendChild(t); }
  if (jp && o.btn) { const k = CATS8.find(x => crownName(x) === T(jp.querySelector('.pr3-k'))), fee = isCash() ? '$' + LG_FEE : LG_COIN + ' 🟡';
    o.btn.textContent = `${o.won ? 'Play again' : 'Rematch'} · ${fee}`; o.btn.onclick = () => { closeSheet(); setTimeout(() => lgCat(k), 280); }; }
  const host = jp ? jp.closest('.kg2') : kg; host.innerHTML = ''; host.appendChild(wrap);
  sb.querySelectorAll('.to-cash').forEach(x => x.remove());
}
new MutationObserver(() => { try { gsResult(); } catch (e) {} }).observe($('#sheetBody'), { childList: true, subtree: true });
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
CSS = '''
/* result screen */
.gr{position:relative}
.gr-h{margin:10px 0 8px;text-align:center;font:900 2rem/1.05 Fraunces,serif;color:#1F3157}.gr.won .gr-h{color:#1E6B3E}.gr-h small{display:block;margin-top:4px;font:800 .85rem "Nunito Sans";color:#4E433C}
.gr-box.neu{background:#FBF5EA;box-shadow:inset 0 0 0 2px #E2D5BE}.gr-box.neu b{color:#4E433C;font-size:1.9rem}.gr-box.neu .gs-pl{color:#8A7E72}.gr-box.neu span{color:#4E433C}
.gr.won .gr-box{animation:grPop .6s cubic-bezier(.2,1.5,.4,1) both}@keyframes grPop{0%{transform:scale(.6);opacity:0}100%{transform:none;opacity:1}}
.gr-tip{display:block;margin:6px auto 0;font:800 .82rem "Nunito Sans"}
.gr .pj-ph{position:relative}.gr-tag{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);white-space:nowrap;font:900 .7rem "Nunito Sans";font-style:normal;padding:3px 9px;border-radius:99px;background:linear-gradient(180deg,#F3D27A,#E0A82E);color:#3A2600;box-shadow:0 2px 6px rgba(0,0,0,.35)}
.gr figure.gr-l .pj-ph img{filter:grayscale(.45) brightness(.92)}.gr figure.gr-w .pj-ph{box-shadow:0 0 0 3px #E0A82E,0 0 18px rgba(224,168,46,.55)!important}
.gr figcaption small{font:800 .8rem "Nunito Sans"!important;color:#1F3157!important}
.gr-bar{display:flex;height:22px;border-radius:99px;overflow:hidden;margin:2px 0 14px;font:900 .72rem/22px "Nunito Sans";color:#fff}.gr-bar i{font-style:normal;text-align:center;min-width:34px}.gr-bar i:first-child{background:#9E8A6A}.gr-bar i:last-child{background:#2D4E86}
.gr .gr-acts .btn{margin:0}
/* your stars today, big and gold on Compete jackpot photos */
html body .c3-st{top:40px!important;right:auto!important;left:8px!important;font:900 1.05rem Fraunces,serif!important;padding:4px 12px!important;box-shadow:0 0 0 2px rgba(255,255,255,.85),0 0 16px rgba(243,210,122,.9)!important;animation:c3Glow 2.2s ease-in-out infinite;white-space:nowrap}
.c3-st small{font:800 .66rem "Nunito Sans";margin-left:3px;text-transform:uppercase;letter-spacing:.04em}
@keyframes c3Glow{0%,100%{box-shadow:0 0 0 2px rgba(255,255,255,.85),0 0 10px rgba(243,210,122,.6)}50%{box-shadow:0 0 0 2px rgba(255,255,255,.95),0 0 22px rgba(243,210,122,1)}}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
# the badge reads "★ 5 today"
a = "${y ? `<span class=\"c3-st\">★ ${y}</span>` : ''}"
assert s.count(a) == 1, 'star badge'
s = s.replace(a, "${y ? `<span class=\"c3-st\">★ ${y}<small>today</small></span>` : ''}")
open(p, 'w', encoding='utf-8').write(s); print('results ok')
