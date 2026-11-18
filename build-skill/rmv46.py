# Real Money build, step 49 (after rmv45.py): qualifier result for returning players.
#  - Coin player without a free pick ready: main button "Keep judging" + coin progress "205 / 250 toward a free Final pick".
#  - Coin player with a free pick ready: "Use your free pick · 10am Pets Final (live now)".
#  - Depositor: "Pick the 10am Pets Final · from $2".
#  - "Through to the 11am Final · picks open at 10am" so it's clear which Final the qualifiers feed.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("<small>The ${cw.toLowerCase()} top 2 qualify.</small>", "<small>The ${cw.toLowerCase()} top 2 qualify · picks open at ${raceName(G.ns - 1)}</small>")
m = re.findall(r'\n    <button class="btn block g2-fin" id="gtFin">.*?</div></div>`\);', s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], "\n    ${g2Act(pay)}</div>`);")
RA("  $('#gtFin').onclick = () => { popClose(); setTimeout(ppOpen, 250); };",
   "  if ($('#gtFin')) $('#gtFin').onclick = () => { popClose(); setTimeout(ppOpen, 250); }; if ($('#gtKeep')) $('#gtKeep').onclick = () => popClose(); if (!$('#gtNo')) { const z = document.createElement('i'); z.id = 'gtNo'; z.hidden = true; $('#coach').appendChild(z); }")
s = s.replace("function fcNotify() {", r"""function g2Act(pay) { const y = isYoungW(), g = ppGame(), nm = `${raceName(g.sl)} ${esc(showName(g.k))} Final`, keep = y ? 'Keep judging' : 'Keep voting', link = `<div style="text-align:center"><button class="link g2-link" id="gtNo">${keep}</button></div>`;
  if (isCash()) return `<button class="btn block g2-fin" id="gtFin">🎀 Pick the ${nm} · from $2</button>${link}`;
  if (fqLeft() && (S.gems || 0) >= FREE_BET_COINS) return `<button class="btn block g2-fin" id="gtFin">🎟️ Use your free pick</button><p class="g2-foot">${nm} · live now · ${FREE_BET_COINS} coins</p>${link}`;
  const gm = Math.floor(S.gems || 0), pct = Math.min(100, Math.round(100 * gm / FREE_BET_COINS));
  return `<div class="g2-prog"><p>${pay ? `<b>+${pay} coins</b> · ` : ''}${gm} / ${FREE_BET_COINS} toward a free Final pick</p><i><i style="width:${pct}%"></i></i>${!fqLeft() ? `<small>Both free picks used this hour · next in ${frMinsLeft()} min</small>` : ''}</div><button class="btn block g2-fin" id="gtKeep">⚖️ ${keep}</button>`; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.g2-prog{background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E8C46A;border-radius:14px;padding:10px 12px;margin:0 0 10px}.g2-prog p{margin:0 0 6px;font-size:.92rem}.g2-prog b{color:#2F6B3F}.g2-prog>i{display:block;height:9px;border-radius:5px;background:#F0E2B8;overflow:hidden}.g2-prog>i>i{display:block;height:100%;background:#E2A21C;border-radius:5px}.g2-prog small{display:block;margin-top:6px;font-size:.78rem;opacity:.8}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v46 ok')
