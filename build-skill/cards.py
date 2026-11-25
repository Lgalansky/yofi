# Photo cards (Skill). Every photo is a card that shows its five scores and a tier frame
# (Bronze <60, Silver 60+, Gold 70+ = can enter challenges, Hall of Fame 85+).
# - Upload: "Your card is printed!" reveal, +50 coins, then the usual score / touch-up screen.
# - Voting: your cards win votes in the background and pay coins by tier (+3 / +5 / +8), with a banner;
#   capped at 20 wins a day. A strip on the Vote screen shows today's wins and coins.
# - "Touch-ups" tab is renamed "My photos" and opens with a "My cards" row; touch-ups raise the card's
#   stats and a tier-up reveal plays when a card reaches Silver, Gold or Hall of Fame.
# - Fix: the overall score could freeze mid count-up (showed 16 while every part was 53-80).
# Usage: python3 build-skill/cards.py [in.html] [out.html]  (defaults to index.html in place)
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if 'function cardTier(' in s: sys.exit('cards already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)

# 1. score count-up: remember the real target so a second animation can't freeze on a half-way number
rep("if (big) { const to2 = +big.textContent, f2 = from == null ? 0 : from,",
    "if (big) { const to2 = +(big.dataset.to || (big.dataset.to = big.textContent)), f2 = from == null ? 0 : from,")

# 2. tab name
rep('<button id="segStudio" aria-pressed="false">', '<button id="segStudio" aria-pressed="false" data-cards="1">')
s = s.replace('<span>Touch-ups</span></button>', '<span>My photos</span></button>', 1)

JS = r'''
/* ---------- photo cards ---------- */
const CARD_BASE = 3, CARD_T = [{ n: 'Bronze', at: 0, x: 1, c: 'br' }, { n: 'Silver', at: 60, x: 2, c: 'si' }, { n: 'Gold', at: 70, x: 3, c: 'go' }, { n: 'Hall of Fame', at: 85, x: 4, c: 'hf' }];
CARD_T.forEach(t => { t.pay = CARD_BASE * t.x; });
const CARD_CAP = 10, CARD_PRINT = 50, PRINT_DAY = 3;
CFG.MAX_PHOTOS = Math.max(CFG.MAX_PHOTOS, 12);
function cardTier(v) { let k = 0; CARD_T.forEach((t, i) => { if (v >= t.at) k = i; }); return k; }
function cwDay() { const d = todayKey(); if (!S.cw || S.cw.d !== d) S.cw = { d, n: 0, c: 0, by: {}, pr: 0 }; return S.cw; }
function cardHTML(p, o = {}) {
  const k = cardTier(p.s.total), t = CARD_T[k], nx = CARD_T[k + 1], w = cwDay().by[p.id] || 0;
  const stats = C.map(c => `<div class="pc-st${o.hi === c.k ? ' up' : ''}"><span>${esc(c.short)}</span><i><u style="width:${p.s[c.k]}%"></u></i><b>${p.s[c.k]}${o.hi === c.k ? ' ▲' : ''}</b></div>`).join('');
  return `<div class="pcard ${t.c}${o.mini ? ' mini' : ''}"><div class="pc-h"><span>${t.n} ×${t.x}</span><b>${p.s.total}</b></div><img src="${p.src}" alt="">
    ${o.mini ? `<small class="pc-w">${w ? `${w} win${w === 1 ? '' : 's'} · +${w * t.pay} today` : nx ? `${nx.at - p.s.total} to ${nx.n}` : 'Top tier'}</small>` : `${p.cat ? `<p class="pc-c">${esc(pcatName(p.cat))}</p>` : ''}${stats}`}</div>`;
}
function cardPop({ p, title, amt, text, cta, act, later, lact, hi }) {
  const c = $('#coach'); if (!c) { act && act(); return; }
  c.innerHTML = `<div class="crbox pcpop" role="dialog" aria-modal="true" aria-labelledby="pcT">
    ${[...Array(18)].map((_, i) => `<i class="wp-cf" style="left:${(i * 41) % 100}%;background:${['#FFC93C', '#FF6B6B', '#5B8DEF', '#3CCB8A'][i % 4]};animation-delay:${(i * .1).toFixed(2)}s"></i>`).join('')}
    <div class="pc-wrap">${cardHTML(p, { hi })}</div><h2 id="pcT">${title}</h2>${amt ? `<p class="wp-amt"><span>+${amt}</span>${gemIcon('wp-ci')}</p>` : ''}<p class="pc-tx">${text}</p>
    <button class="bt-cta" id="pcGo">${cta}</button>${later ? `<button class="bt-no" id="pcLater">${later}</button>` : ''}</div>`;
  c.classList.add('on', 'cr');
  const close = f => { c.classList.remove('on', 'cr'); c.innerHTML = ''; if (f) f(); };
  $('#pcGo').onclick = () => close(act); if ($('#pcLater')) $('#pcLater').onclick = () => close(lact);
  c.onclick = e => { if (e.target === c) close(lact || act); };
}
// a new photo is printed as a card first, then goes on to its score and touch-ups as before
const _showResultC = showResult;
showResult = function (p, o = {}) {
  if (!o.fresh || p.carded || !p.s) return _showResultC.apply(this, arguments);
  p.carded = 1; p.tierSeen = cardTier(p.s.total); const D0 = cwDay(), bonus = (D0.pr || 0) < PRINT_DAY ? CARD_PRINT : 0; D0.pr = (D0.pr || 0) + 1; S.gems += bonus; save();
  const t = CARD_T[p.tierSeen], args = arguments, self = this;
  cardPop({ p, title: 'Your card is printed!', amt: bonus,
    text: `It’s a <b>${t.n}</b> card: <b>×${t.x}</b> coins on every vote it wins (+${t.pay} a win). Touch it up to reach ${CARD_T[Math.min(2, p.tierSeen + 1)].n} for <b>×${CARD_T[Math.min(2, p.tierSeen + 1)].x}</b>.${bonus ? '' : ` You’ve had today’s ${PRINT_DAY} print bonuses, but it still earns.`}`,
    cta: 'See its scores', act: () => { paintGems(); _showResultC.apply(self, args); },
    later: 'Vote and watch it earn', lact: () => { paintGems(); try { closeFlow(); } catch (e) {} openApp && openApp(); go('judge'); renderJudge(); } });
};
// cards earn while you vote
function cardVoteTick() {
  const D = cwDay(), cards = S.photos.filter(x => x.s && !photoLock(x) && (D.by[x.id] || 0) < CARD_CAP);
  if (!cards.length || Math.random() > .4) return;
  const p = cards[Math.floor(Math.random() * cards.length)], win = Math.random() < Math.max(.25, Math.min(.85, (p.s.total - 35) / 50));
  if (!win) return;
  const t = CARD_T[cardTier(p.s.total)]; D.n++; D.c += t.pay; D.by[p.id] = (D.by[p.id] || 0) + 1; S.gems += t.pay; save();
  const b = document.createElement('div'); b.className = 'pc-ban'; b.setAttribute('role', 'status');
  b.innerHTML = `<img src="${p.src}" alt=""><span><b>Your card won a vote · ${t.x > 1 ? `×${t.x} ` : ''}+${t.pay}</b>${gemIcon('')}<small>${t.n} card · ${D.by[p.id]} of ${CARD_CAP} paid wins today</small></span>`;
  document.body.appendChild(b); setTimeout(() => b.classList.add('on'), 20); setTimeout(() => { b.classList.remove('on'); setTimeout(() => b.remove(), 400); }, 2600);
  setTimeout(paintGems, 300); paintCardStrip();
}
function paintCardStrip() {
  const j = $('#judge'); if (!j || !S.photos.length) return; let el = j.querySelector('.pc-strip');
  if (!el) { el = document.createElement('button'); el.className = 'pc-strip'; j.appendChild(el); el.onclick = () => go('studio'); }
  const D = cwDay(), best = S.photos.slice().sort((a, b) => (D.by[b.id] || 0) - (D.by[a.id] || 0) || b.s.total - a.s.total)[0];
  el.innerHTML = `<img src="${best.src}" alt=""><span><b>Your cards · ${D.n} win${D.n === 1 ? '' : 's'} today</b><small>+${D.c} coins earned · each card pays up to ${CARD_CAP} wins a day · more cards, more coins</small></span><em>My photos ›</em>`;
}
const _voteC = vote;
vote = async function () { const n0 = S.votes; const r = await _voteC.apply(this, arguments); if (S.votes > n0) cardVoteTick(); return r; };
const _renderJudgeC = renderJudge;
renderJudge = function () { const r = _renderJudgeC.apply(this, arguments); try { paintCardStrip(); } catch (e) {} return r; };
// My photos: a row of your cards above the touch-up screen, and a tier-up reveal after a touch-up
const _renderStudioC = renderStudio;
renderStudio = function () {
  const r = _renderStudioC.apply(this, arguments);
  try {
    const st = $('#studio'), p = cur(); if (!st || !p || !p.s || !S.photos.length || st.querySelector('.enh0')) return r;
    const k = cardTier(p.s.total), nx = CARD_T[k + 1], D = cwDay();
    // My photos has two views: Touch up (this photo) and My cards (pick a card or print a new one)
    const seg = v => `<div class="pc-seg" role="tablist"><button role="tab" data-pcv="touch" aria-selected="${v === 'touch'}">Touch up</button><button role="tab" data-pcv="cards" aria-selected="${v === 'cards'}">My cards<em>${S.photos.length}</em></button></div>`;
    if (S.pcView === 'cards') {
      st.classList.remove('tallp');
      st.innerHTML = `${seg('cards')}<div class="pc-cards"><div class="pc-rh"><small>${D.n ? `<b>+${D.c} coins</b> from vote wins today` : 'Your cards earn coins while you vote'}</small></div>
        <div class="pc-grid">${S.photos.map(x => `<button class="pc-pick${x.id === p.id ? ' on' : ''}" data-pcp="${x.id}" aria-label="Touch up card scoring ${x.s.total}">${cardHTML(x, { mini: 1 })}</button>`).join('')}
        ${S.photos.length < CFG.MAX_PHOTOS ? `<button class="pc-new" id="pcNew"><b>+</b><span>New card</span><small>Upload a photo${(cwDay().pr || 0) < PRINT_DAY ? ` · +${CARD_PRINT} coins` : ''}</small></button>` : ''}</div>
        <p class="pc-next">Tap a card to touch it up. Tiers multiply the coins each vote win pays: Bronze ×1 · Silver ×2 · Gold ×3 · Hall of Fame ×4. Each card pays up to ${CARD_CAP} wins a day, so more cards earn more.</p></div>`;
      st.querySelectorAll('[data-pcp]').forEach(b => b.onclick = () => { S.cur = b.dataset.pcp; S.pcView = 'touch'; save(); renderStudio(); st.scrollTop = 0; });
      if ($('#pcNew')) $('#pcNew').onclick = () => pickPhoto(true);
    } else {
      const h = st.querySelector('.tot-h'); if (h) { const bt = h.querySelector('.sd-btns'); if (bt) bt.remove(); h.insertAdjacentHTML('beforeend', seg('touch')); }
    }
    st.querySelectorAll('[data-pcv]').forEach(b => b.onclick = () => { S.pcView = b.dataset.pcv; save(); renderStudio(); st.scrollTop = 0; });
    if (S.pcView === 'cards') return r;
    { const sc = st.querySelector('.scr2'); if (sc) sc.insertAdjacentHTML('beforeend', `<p class="pc-tag ${CARD_T[k].c}"><strong>${CARD_T[k].n} card ×${CARD_T[k].x}</strong> · +${CARD_T[k].pay} coins a vote win${nx ? ` · ${nx.at - p.s.total} to ${nx.n} ×${nx.x}` : ''}</p>`); }
    if (p.tierSeen == null) { p.tierSeen = k; save(); }
    else if (k > p.tierSeen) { p.tierSeen = k; save(); const t = CARD_T[k];
      const show = (n = 0) => { const c = $('#coach'); if (c && (c.classList.contains('on') || $('#flow').classList.contains('on'))) { if (n < 20) setTimeout(() => show(n + 1), 700); return; }
        cardPop({ p, title: k === 3 ? 'Hall of Fame!' : `${t.n} card!`, text: k === 3 ? `Your photo scored <b>${p.s.total}</b>. It earns ×${t.x} (+${t.pay}) on every vote it wins. Ready to print your next card?` : `Your card levelled up. It now earns <b>×${t.x}</b>: <b>+${t.pay} coins</b> for every vote it wins${k === 2 ? ' and can <b>enter challenges</b>' : ''}.`,
          cta: k === 3 ? 'Print another card' : k === 2 ? 'Enter a challenge' : 'Keep touching it up', act: () => { if (k === 3) pickPhoto(true); else if (k === 2) { try { openComps(p); } catch (e) {} } },
          later: k === 3 ? 'Keep it racing' : k === 2 ? 'Not now' : '', lact: () => {} }); };
      setTimeout(show, SCORE_ANIM_MS + 200); }
  } catch (e) {}
  return r;
};
'''
rep("  shownGems = S.gems;\n})();\n})();", JS + "  shownGems = S.gems;\n})();\n})();")

CSS = r'''
.pcard{position:relative;background:#fff;border-radius:16px;padding:9px;box-shadow:0 0 0 4px #C9A27A,0 14px 26px -12px rgba(0,0,0,.45);text-align:left;color:#2A211C}
.pcard.si{box-shadow:0 0 0 4px #AEB7C4,0 14px 26px -12px rgba(0,0,0,.45)}.pcard.go{box-shadow:0 0 0 4px #F3C447,0 0 22px rgba(243,196,71,.6),0 14px 26px -12px rgba(0,0,0,.45)}.pcard.hf{box-shadow:0 0 0 4px #F3C447,0 0 0 8px #2D4E86,0 0 26px rgba(243,196,71,.7)}
.pc-h span{color:#7A5A12!important;display:inline!important}.pc-h{display:flex;justify-content:space-between;align-items:center;font:800 .72rem system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#7A5A12;margin-bottom:6px}.pc-h b{font-size:1rem;letter-spacing:0;color:#2A211C}
.pcard img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:10px;display:block}
.pc-c{margin:6px 0 4px!important;font:800 .8rem system-ui,sans-serif!important;color:#2D4E86!important}
.pc-st{display:grid;grid-template-columns:76px 1fr 38px;gap:6px;align-items:center;font-size:.72rem;margin:3px 0;color:#463933}.pc-st i{height:6px;border-radius:3px;background:#EEE5D2;overflow:hidden}.pc-st u{display:block;height:100%;background:#2D4E86}.pc-st b{text-align:right}
.pc-st.up{background:#FFF3D0;border-radius:6px;padding:1px 4px;margin:3px -4px}.pc-st.up u{background:#E9A514}
.pcpop .pc-wrap{width:200px;margin:6px auto 0;transform:rotate(-3deg);animation:wppop .55s cubic-bezier(.2,1.5,.4,1) both;position:relative;z-index:2}
.pcpop{position:relative;overflow:hidden;text-align:center}.pcpop > :not(.wp-cf){position:relative;z-index:2}.pcpop h2{margin-top:18px!important}
.pc-tx{margin:6px 0 14px!important;font-size:.95rem!important;line-height:1.4}
.pcard.mini{padding:6px;border-radius:12px}.pcard.mini .pc-h{font-size:.6rem;margin-bottom:4px}.pcard.mini .pc-h b{font-size:.82rem}.pcard.mini img{border-radius:8px}
.pc-w{display:block;margin-top:4px;font:700 .66rem system-ui,sans-serif;color:#6B5B4A;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pc-seg{display:flex;gap:4px;margin:10px auto 2px;padding:4px;border-radius:999px;background:rgba(0,0,0,.06);width:max-content;max-width:100%}
html.yg .pc-seg{background:rgba(255,255,255,.08)}
.pc-seg button{border:0;background:none;color:inherit;font:800 .95rem system-ui,sans-serif;padding:9px 18px;border-radius:999px;display:flex;gap:6px;align-items:center}
.pc-seg button[aria-selected="true"]{background:#2D4E86;color:#fff}html.yg .pc-seg button[aria-selected="true"]{background:#fff;color:#1A1030}
.pc-seg em{font-style:normal;font-size:.72rem;min-width:20px;padding:1px 6px;border-radius:999px;background:#F3C447;color:#2A1600}
#studio>.pc-seg{margin-top:14px}
.pc-cards{padding:4px 2px 30px}.pc-cards .pc-rh{justify-content:center;margin:10px 0 14px}
.pc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.pc-grid .pc-pick{flex:none;opacity:1}
.pc-new{border:2px dashed rgba(0,0,0,.25);border-radius:16px;background:none;color:inherit;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:14px;font:inherit;min-height:200px}
html.yg .pc-new{border-color:rgba(255,255,255,.3)}
.pc-new b{font-size:2.2rem;line-height:1}.pc-new span{font-weight:800}.pc-new small{font-size:.76rem;opacity:.75;text-align:center}.pc-rh{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin:0 2px 10px}.pc-rh h2{margin:0;font-size:1.35rem}.pc-rh small{font-size:.78rem;opacity:.75}
.pc-list{display:flex;gap:14px;overflow-x:auto;padding:6px 6px 10px;scrollbar-width:none}.pc-list::-webkit-scrollbar{display:none}
.pc-pick{flex:0 0 104px;border:0;background:none;padding:0;border-radius:14px;opacity:.8}.pc-pick.on{opacity:1;transform:translateY(-3px)}.pc-pick.on .pcard{outline:3px solid #2D4E86;outline-offset:5px}
.pc-hero{outline:4px solid #C9A27A;outline-offset:-4px}.pc-hero.si{outline-color:#AEB7C4}.pc-hero.go{outline-color:#F3C447}.pc-hero.hf{outline-color:#F3C447;box-shadow:0 0 0 4px #2D4E86}
.pc-tag{margin:8px 0 0!important;padding:6px 10px;border-radius:10px;background:#F6EBD6;font-size:.82rem!important;line-height:1.3;color:#463933}.pc-tag strong{font:800 .82rem system-ui,sans-serif!important;color:#7A4A00}.pc-tag.si{background:#E8ECF2}.pc-tag.go,.pc-tag.hf{background:#FFF0C2}html.yg .pc-tag{background:rgba(255,255,255,.08);color:#EADBFF}html.yg .pc-tag strong{color:#FFD86B}
.pc-next{margin:2px 2px 0;font-size:.88rem;line-height:1.4}
.pc-ban{position:fixed;left:50%;top:12px;z-index:60;transform:translate(-50%,-140%);width:min(92vw,420px);display:flex;gap:10px;align-items:center;padding:9px 12px;border-radius:16px;background:#2A211C;color:#fff;box-shadow:0 12px 28px -10px rgba(0,0,0,.6);transition:transform .35s cubic-bezier(.2,1.2,.4,1)}
.pc-ban.on{transform:translate(-50%,0)}.pc-ban img{width:40px;height:50px;object-fit:cover;border-radius:7px;box-shadow:0 0 0 2px #F3C447}.pc-ban b{color:#FFD86B;margin-right:4px}.pc-ban svg{width:16px;height:16px;vertical-align:-3px}.pc-ban small{display:block;opacity:.8;font-size:.76rem}
.pc-strip{display:flex;gap:10px;align-items:center;width:100%;margin:14px 0 4px;padding:9px 12px;border-radius:16px;border:1.5px solid rgba(0,0,0,.12);background:rgba(255,255,255,.7);text-align:left;color:inherit;font:inherit}
html.yg .pc-strip{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.16)}
.pc-strip img{width:40px;height:50px;object-fit:cover;border-radius:7px;box-shadow:0 0 0 2px #F3C447}.pc-strip b{display:block;font-size:.92rem}.pc-strip small{font-size:.78rem;opacity:.75}.pc-strip em{margin-left:auto;font-style:normal;font-weight:800;font-size:.8rem;white-space:nowrap}
@media (prefers-reduced-motion:reduce){.pcpop .pc-wrap{animation:none}.pc-ban{transition:none}}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('cards ok')
