# Real Money build, step 193 (after rmv189.py): winning the qualifier sends you back to voting; your voting streaks
#  take the photo to its Final (3 steps, 2 in a row = 1 step), then the Final lobby opens.
#  - Win screen: "Qualified!", "Mountain wins 11–9 · Against Desert pause · +50 coins",
#    "Next: 3 voting steps to the Final", button "⚖️ Vote your way to the Final".
#  - Finalist card on the Vote screen: "🏆 Qualified · 1 of 3 steps to the Final" with gold streak dots; when the
#    steps are done the lobby opens, and the card shows "Your Final is waiting" + "Meet your finalists & race".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("try { (S.photos || []).forEach(p => { if (p.fin) p.fr = { s: QS_STEPS, go: 1 }; }); save(); } catch (e) {}", "")
RA("const qsElig = () => pvList().filter(p => p.ql && !p.ql.done && !p.ql.live && !p.tr);", "const qsElig = () => pvList().filter(p => (p.ql && !p.ql.done && !p.ql.live && !p.tr) || (p.fin && !(p.fr && p.fr.go)));")
RA("p.fin = 1; p.cashOK = 1; p.fr = { s: QS_STEPS, go: 1 }; save();", "p.fin = 1; p.cashOK = 1; p.fr = { s: 0 }; save();")
RA('<h2 class="nv-big">You’re in<br>the final!</h2>', '<h2 class="nv-big">Qualified!</h2>')
RA('<button class="btn block nv-go" id="qlvGo">Meet your finalists</button>', '<p class="qw-nx">Next: <b>${QS_STEPS} voting steps</b> to the Final<br><small>Vote 2 in a row with the crowd = 1 step</small></p><button class="btn block nv-go" id="qlvGo">⚖️ Vote your way to the Final</button>')
i = s.index('function qlWon('); j = s.index('$(\'#qlvGo\').onclick = () => qfStart(p);', i)
s = s[:j] + "$('#qlvGo').onclick = () => { popClose(); go('judge'); renderJudge(); };" + s[j + len("$('#qlvGo').onclick = () => qfStart(p);"):]
RA("if (!p.fin) return pc.apply(this, arguments); p.fr = { s: QS_STEPS, go: 1 };", "if (!p.fin) return pc.apply(this, arguments); p.fr = p.fr || { s: 0 }; if (!p.fr.go) return `<div class=\"pv-c fin\" data-pid=\"${p.id}\"><div class=\"pv-t\"><b>${esc(rcName(p))}</b><span class=\"pv-st\">🏆 Qualified</span><em>🟡 +${p.qc || 0}</em></div>${pvStep(p, p.fr.s || 0, 1)}</div>`;")
RA("${Math.min(QS_STEPS, s)} of ${QS_STEPS} steps · 2 in a row = 1 step", "${Math.min(QS_STEPS, s)} of ${QS_STEPS} steps${fin ? ' to the Final' : ' · 2 in a row = 1 step'}")
s = s.replace('</style>', """.qw-nx{margin:0 0 12px;font:700 1.05rem/1.35 Nunito,system-ui;color:#EEF1F8}.qw-nx b{color:#F3D98B}.qw-nx small{font-size:.85rem;color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v190 ok')
