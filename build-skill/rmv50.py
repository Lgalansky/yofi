# Real Money build, step 53 (after rmv49.py): coin players' qualifier result never offers the Final.
# With 250+ coins it shows an info line ("You have enough for a free Final pick · it's in your coins") and Keep judging.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
m = re.findall(r"  if \(fqLeft\(\) && \(S\.gems \|\| 0\) >= FREE_BET_COINS\) return `<button class=\"btn block g2-fin\" id=\"gtFin\">🎟️ Use your free pick</button>.*?\n", s); assert len(m) == 1, len(m)
s = s.replace(m[0], "  if (fqLeft() && (S.gems || 0) >= FREE_BET_COINS) return `<div class=\"g2-prog ready\"><p>${pay ? `<b>+${pay} coins</b> · ` : ''}${Math.floor(S.gems)} coins</p><p>🎟️ You have enough for a free Final pick · it’s in your coins</p></div><button class=\"btn block g2-fin\" id=\"gtKeep\">⚖️ ${keep}</button>`;\n")
s = s.replace('</style>', ".g2-prog.ready{background:#E6F0DF;box-shadow:inset 0 0 0 1.5px #2F6B3F}.g2-prog.ready p+p{margin:0;font-weight:700;color:#2F6B3F}\n</style>", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v50 ok')
