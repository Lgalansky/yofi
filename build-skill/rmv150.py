# Real Money build, step 153 (after rmv149.py): judge 3 rounds → earn your photo entry.
#  - Round bar: "Round 2 of 3 · earn your photo entry" (or "🎟️ Entry ticket ready").
#  - Every 3rd completed round: "🎟️ You qualified!" with an entry ticket; the main button is
#    "📷 Enter your photo · free" (contest screen if you have a photo, otherwise upload first). Judging more is optional.
#  - Contests: the free daily needs an entry ticket ("🔒 Judge 3 rounds"); the ⚡ Quick contest can be entered with a
#    ticket instead of $1. Cash $2 entries don't need a ticket. The contest screen shows your tickets / progress.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("'Finish it for your free Match Race' : 'Call the crowd · 10 pairs'",
   "'Finish it for your free Match Race' : (S.entT || 0) > 0 ? '🎟️ Entry ticket ready · enter your photo' : `Round ${(S.vrq || 0) + 1} of 3 · earn your photo entry`")
RA("const head = ok >= 9 ?", "S.vrq = (S.vrq || 0) + 1; const qual = S.vrq >= 3; if (qual) { S.vrq = 0; S.entT = (S.entT || 0) + 1; } save();\n  const head = qual ? '🎟️ You qualified!' : ok >= 9 ?")
RA('<button class="btn block db-go" id="vrNext">⚖️ Next round</button>',
   '${qual ? `<div class="vrq">🎟️ <b>Entry ticket earned</b><br>Enter your photo in today’s contest, free. The crowd decides, prizes in real cash.</div><button class="btn block db-go cashb" id="vrEnter">📷 Enter your photo · free</button>` : `<p class="vrq-p">Round ${S.vrq} of 3 done · <b>${3 - S.vrq} more</b> to earn a free photo entry</p>`}<button class="btn block db-go ${qual ? \'quiet\' : \'\'}" id="vrNext">⚖️ ${qual ? \'Keep judging\' : \'Next round\'}</button>')
RA("$('#vrNext').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} };",
   "$('#vrNext').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} };\n  if ($('#vrEnter')) $('#vrEnter').onclick = () => { popClose(); const P = (S.photos || []).filter(x => x.framed && !x.starter); setTimeout(() => P.length ? ctOpen(photoShow(P[0]), P[0].id) : finPick(), 200); };")
# contests
RA('<p class="ct-m">🤝', '<p class="ct-tk ${(S.entT || 0) ? \'ok\' : \'\'}">${(S.entT || 0) ? `🎟️ You have <b>${S.entT} entry ticket${S.entT > 1 ? \'s\' : \'\'}</b>` : `🔒 Free entries need a ticket · judge <b>${3 - (S.vrq || 0)} more round${3 - (S.vrq || 0) === 1 ? \'\' : \'s\'}</b> to earn one`}</p><p class="ct-m">🤝')
RA("'<button class=\"btn db-go\" id=\"ctF\">Enter free</button>'", "((S.entT || 0) ? '<button class=\"btn db-go\" id=\"ctF\">Enter · 🎟️</button>' : '<button class=\"btn db-go quiet\" id=\"ctLock\">🔒 Judge</button>')")
RA("'<button class=\"btn db-go cashb\" id=\"ctQ\">Enter · $1</button>'", "('<button class=\"btn db-go cashb\" id=\"ctQ\">' + ((S.entT || 0) ? 'Enter · 🎟️' : 'Enter · $1') + '</button>')")
RA("if ($('#ctF')) $('#ctF').onclick = () => enter('f');",
   "if ($('#ctF')) $('#ctF').onclick = () => { if (!(S.entT > 0)) return; S.entT--; save(); enter('f'); };\n    if ($('#ctLock')) $('#ctLock').onclick = () => { popClose(); go('judge'); renderJudge(); };")
RA("if ($('#ctQ')) $('#ctQ').onclick = () => needAge(", "if ($('#ctQ') && S.entT > 0) $('#ctQ').onclick = () => { S.entT--; save(); enter('q'); };\n    else if ($('#ctQ')) $('#ctQ').onclick = () => needAge(")
RA('<div><b>🎟️ Free daily</b>', '<div><b>🎟️ Free daily · entry ticket</b>')
s = s.replace('</style>', """.vrq{margin:0 0 8px;padding:12px;border-radius:14px;background:#F1F6EC;box-shadow:inset 0 0 0 2px #2F6B3F;color:#22502F;font-size:.88rem;line-height:1.45;animation:cdPop .5s ease-out both}.vrq b{color:#14213D;font-size:1rem}
.vrq-p{margin:0 0 6px;font-size:.88rem;color:#14213D}
.ct-tk{margin:-2px 0 6px;padding:7px 10px;border-radius:10px;background:#F3EEE5;font:700 .84rem Nunito,system-ui;color:#5B4A3F;text-align:left}.ct-tk.ok{background:#F1F6EC;color:#22502F;box-shadow:inset 0 0 0 1.5px #2F6B3F}.ct-tk b{color:#14213D}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v150 ok')
