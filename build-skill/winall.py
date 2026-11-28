# Skill preview: every game win pauses on the celebration pop before the result screen.
#  The shared result screens (jackpot, head-to-head, friend, Quick Sprint, Showdown, Sprint,
#  Crowd Championship, card steals) used to clear any open pop, so some wins went straight to
#  the result list. Now a win always opens the winner pop first (confetti, your photo, the prize
#  counting up). Cash/coin prizes use "Collect" (the money flies into the balance); stars and
#  cards use "See result". Only one pop per win: if the game already fired its own winner pop,
#  that one is kept and nothing is doubled.
# usage: python3 build-skill/winall.py in.html out.html
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()

JS = r'''
// ---- a win always pauses on the celebration pop ----
let WA_AT = 0; const _winPopWA = winPop;
winPop = function (amt, cur, label, o) { const c = $('#coach'), mine = c && c.querySelector('.wpbox[data-wa]');
  if (mine) { mine.dataset.cur = cur; mine.dataset.amt = amt; mine.dataset.lbl = label; return; } // our pop is up: its Collect pays this
  WA_AT = Date.now(); return _winPopWA.apply(this, arguments); };
function waShow(o) { // { title, big, label, src, amt, cur }
  const c = $('#coach'); if (!c || Date.now() - WA_AT < 4000 || c.querySelector('.wpbox')) return; WA_AT = Date.now();
  const isCash = o.cur === 'cash', ic = o.cur ? (isCash ? '<span class="wp-bill">$</span>' : gemIcon('wp-ci')) : '';
  c.innerHTML = `<div class="crbox wpbox" data-wa="1" role="dialog" aria-modal="true" aria-labelledby="wpT">
    <div class="cr-rays wp-rays" aria-hidden="true"></div>
    ${[...Array(26)].map((_, i) => `<i class="wp-cf" style="left:${(i * 37) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A', '#F59E0B'][i % 5]};animation-delay:${(i * .09).toFixed(2)}s;animation-duration:${(2.1 + (i % 5) * .3).toFixed(2)}s"></i>`).join('')}
    ${o.src ? `<div class="wp-photo"><img src="${o.src}" alt="Your photo"><span class="wp-badge">🏆</span></div>` : '<div class="wp-trophy" aria-hidden="true">🏆</div>'}
    <h2 id="wpT">${esc(o.title || 'You won!')}</h2>
    <p class="wp-amt ${isCash ? 'cash' : ''}"><span id="wpN">${o.big}</span>${ic}</p>
    ${o.label ? `<p class="wp-lbl">${esc(o.label)}</p>` : ''}
    <button class="bt-cta" id="wpGo">${o.cur ? (isCash ? 'Collect my cash' : 'Collect my coins') : 'See result'}</button></div>`;
  c.classList.add('on', 'cr');
  let done = false; const box = c.querySelector('.wpbox');
  const close = () => { if (done) return; done = true; const a = +box.dataset.amt || o.amt, cu = box.dataset.cur || o.cur; c.classList.remove('on', 'cr'); c.innerHTML = '';
    if (a && cu) setTimeout(() => { try { cu === 'cash' ? cashExplosion(a, { small: 1 }) : gemExplosion(a, { small: 1 }); } catch (e) {} }, 80); };
  $('#wpGo').onclick = close; c.onclick = e => { if (e.target === c) close(); }; }
const waPrize = b => { const t = String(b || '').replace(/<[^>]+>/g, '').trim(), m = t.match(/\$\s?([\d,.]+)/), g = t.match(/([\d,]+)\s*🟡/);
  return m ? { amt: parseFloat(m[1].replace(/,/g, '')), cur: 'cash' } : g ? { amt: parseInt(g[1].replace(/,/g, '')), cur: 'gems' } : {}; };
const waSrc = () => (document.querySelector('#sheetBody .gr-w.pj-me img, #sheetBody .pj-me img, #sheetBody .gpl-r.me img, #sheetBody .gr-w img') || {}).src;
// list games and steals
const _gsResultSheetWA = gsResultSheet;
gsResultSheet = function (o) { const c = $('#coach'), keep = c && c.classList.contains('on') && c.querySelector('.wpbox') ? [...c.childNodes] : null; // a winner pop already up stays up
  const r = _gsResultSheetWA.apply(this, arguments); if (keep) { keep.forEach(n => c.appendChild(n)); c.classList.add('on', 'cr'); }
  if (o && o.won) { const pz = waPrize(o.box && o.box.b), big = String(o.box && o.box.b || '').replace(/<[^>]+>/g, '');
    setTimeout(() => waShow({ title: String(o.head || 'You won!').replace(/<[^>]+>/g, ''), big: pz.cur ? (pz.cur === 'cash' ? money(pz.amt) : '+' + pz.amt.toLocaleString()) : o.ic === '🃏' ? '🃏 ' + String(o.box.k || 'Now yours') : big, cur: pz.cur, amt: pz.amt, label: o.ic === '🃏' ? `${big} · ${String(o.box.s || '').replace(/<[^>]+>/g, '')}` : `${String(o.nm).replace(/<[^>]+>/g, '')} · ${String(o.box.s || '').replace(/<[^>]+>/g, '')}`, src: o.ic === '🃏' ? (document.querySelector('#sheetBody .pj-them img') || {}).src : waSrc() }), 350); }
  return r; };
// jackpot, head-to-head and friend results
const _gsResultWA = gsResult;
gsResult = function () { const before = document.querySelector('#sheetBody .pj.gs.gr'); const r = _gsResultWA.apply(this, arguments);
  const w = document.querySelector('#sheetBody .pj.gs.gr.won'); if (w && w !== before && !w.dataset.wa) { w.dataset.wa = 1;
    const b = w.querySelector('.gr-box b'), sm = w.querySelector('.gr-box span'), nm = (w.querySelector('.pj-t') || {}).textContent || '';
    const pz = waPrize(b && b.textContent), txt = (b && b.textContent || '').trim();
    setTimeout(() => waShow({ title: 'You won!', big: /⭐/.test(txt) ? txt : pz.cur === 'cash' ? money(pz.amt) : txt, cur: /⭐/.test(txt) ? null : pz.cur, amt: pz.amt, label: `${nm.replace(/^\S+\s/, '')}${sm && sm.textContent ? ' · ' + sm.textContent : ''}`, src: (w.querySelector('.pj-me img') || {}).src }), 350); }
  return r; };
'''
anchor = "  shownGems = S.gems;\n})();\n})();"
assert s.count(anchor) == 1
s = s.replace(anchor, JS + anchor)
open(p, 'w', encoding='utf-8').write(s); print('winall ok')
