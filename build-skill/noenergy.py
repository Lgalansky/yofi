# No energy (Skill preview). Votes were already unlimited (energy() always returns full);
# this removes what was left on screen: the energy bar under the photos, the energy button, the energy sheets,
# "+N energy" in chest toasts and "+N energy" extras in tournament results.
# Usage: python3 build-skill/noenergy.py [in.html] [out.html]
import sys
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
if '/* no energy */' in s: sys.exit('no energy already applied')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)
rep("toast(`⚡ +${rar.e} energy`);", "")
rep("const en = e.fin === 1 ? 25 : e.fin <= 10 ? 10 : 0; e.xtra = { ticket: false, en };", "const en = 0; e.xtra = { ticket: false, en };")
rep("function outOfEnergy(reason) {", "function outOfEnergy(reason) { return;")
CSS = '''
/* no energy */
#judge .jfoot,#judge .vstrip,.vs-en,.jf-en,#enPlus,#enBuy,.en-plus,.tot-x.en,.ug.enq,.t-energy{display:none!important}
'''
i = s.rindex('</style>'); s = s[:i] + CSS + s[i:]
open(p, 'w', encoding='utf-8').write(s); print('no energy ok')
