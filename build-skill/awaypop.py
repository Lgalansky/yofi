# Skill preview: the "while you were away" pop when a card was stolen (user request).
#  Shows the stolen photo with a 🦝 badge, "Leo stole Milo!", "While you were away, Leo won Milo 5–4. You keep the
#  coins it already earned." (plus any coins collected), then how to protect: "🛡 You have 1 shield: put it on Cleo so
#  it can't happen again" or "🛡 Win shields from ✨ special tiles to stop steals".
#  Two actions: green "Win Milo back · $1" (the win-back Photo Duel) and a link: "🛡 Shield Cleo" when you have a
#  shield and an unprotected photo, otherwise "Back to voting".
# Usage: python3 build-skill/awaypop.py in.html out.html  (run after steal2.py)
import sys
src = sys.argv[1]; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src).read()
JS = r'''
// ---- coming back after a steal ----
(() => { const _ap = awayPop;
  awayPop = function () { const N = S.awayNews;
    if (!N || N.shown || !N.st || !S.user || $('#panes').dataset.at !== 'judge' || $('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || $('#flow').classList.contains('on')) return _ap.apply(this, arguments);
    N.shown = 1; save(); const coins = Math.floor(S.vgJar || 0); if (coins) { try { jarCollect(); } catch (e) {} }
    const st = N.st, who = rvName(st.h), p = S.photos.find(x => x.id === st.pid), t = riskable().filter(x => !x.shield).sort((a, b) => b.s.total - a.s.total)[0], n = S.shields || 0;
    const prot = n && t ? `🛡 You have ${n} shield${n === 1 ? '' : 's'}: put one on <b>${esc(alName(t))}</b> so it can’t happen again.` : '🛡 Win shields from ✨ special tiles while you vote to stop steals.';
    celebrate({ src: st.src, score: '🦝', title: `${who} stole ${st.nm}!`,
      text: `While you were away, <b>${esc(who)}</b> won ${esc(st.nm)} ${esc(st.score)}. You keep the coins it already earned${coins ? `, and your photos earned <b>+${coins} 🟡</b>` : ''}.<br><br><span class="aw-prot">${prot}</span>`,
      cta: `Win ${st.nm} back · $1`, onCta: () => { if (p && p.heldBy) stealSheet({ back: p.id }); },
      later: n && t ? `🛡 Shield ${alName(t)}` : 'Back to voting', onLater: () => { if (n && t && window.__shPut) window.__shPut(t); } });
    setTimeout(() => { const b = document.querySelector('#coach.on #crGo, #coach.on .bt-cta'); if (b) b.classList.add('aw-cash'); }, 30); };
})();
'''
a = "  shownGems = S.gems;\n})();\n})();"
assert s.count(a) == 1
i = s.index(a); s = s[:i] + JS + s[i:]
CSS = r'''
html body #coach .aw-cash{background:linear-gradient(180deg,#3E9A55,#2F7A3F)!important;color:#fff!important}
html body #coach .aw-prot{display:inline-block;padding:8px 12px;border-radius:12px;background:#EEF2FA;color:#24406F;font-weight:700}
'''
i = s.rfind('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w').write(s); print('awaypop ok')
