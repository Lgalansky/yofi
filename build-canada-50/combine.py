# Combined Yofi Skill: one app, two looks.
#   ages 18 to 24 (and anyone who hasn't picked yet) -> original dark Yofi look and words  (html.yg)
#   ages 45+                                          -> Fall Fair look and gentler words    (html:not(.yg))
# Logic/HTML come from the Fall Fair build (yofi-ca50.html); the dark look comes from the Skill base styles.
import re
d='/tmp/claude-0/-home-user-yofi/c69be753-0b48-5242-b029-4f4be89f4655/scratchpad/'
base=open(d+'yofi-skill-base.html').read()
s=open(d+'yofi-ca50.html').read()

def split_rules(css):
    out=[]; i=0; n=len(css)
    while i<n:
        j=css.find('{',i)
        if j<0: break
        pre=css[i:j]; depth=1; k=j+1
        while k<n and depth:
            if css[k]=='{': depth+=1
            elif css[k]=='}': depth-=1
            k+=1
        out.append((pre.strip(), css[j+1:k-1])); i=k
    return out
def split_sel(sel):
    parts=[]; depth=0; cur=''
    for ch in sel:
        if ch in '([': depth+=1
        elif ch in ')]': depth-=1
        if ch==',' and depth==0: parts.append(cur); cur=''
        else: cur+=ch
    parts.append(cur); return [p.strip() for p in parts if p.strip()]
def scope_sel(sel, P):
    if re.match(r'^(:root|html)\b', sel): return re.sub(r'^(:root|html)', P, sel, 1)
    if re.match(r'^body\b', sel): return P+' '+sel
    return P+' '+sel
def scope(css, P, kf_suffix, drop=None, glob=None):
    out=[]
    for pre, body in split_rules(css):
        if pre.startswith('@media') or pre.startswith('@supports'):
            out.append(pre+'{'+scope(body,P,kf_suffix,drop,glob)+'}')
        elif re.match(r'@(-webkit-)?keyframes', pre):
            out.append(pre+kf_suffix+'{'+body+'}')
        elif pre.startswith('@'):
            out.append(pre+'{'+body+'}')
        else:
            sels=split_sel(pre)
            if drop and any(drop(x) for x in sels): continue
            if glob and all(glob(x) for x in sels): out.append(pre+'{'+body+'}'); continue
            if kf_suffix:
                body=re.sub(r'(animation(?:-name)?\s*:\s*)([^;}]+)', lambda m: m.group(1)+re.sub(r'\b([a-zA-Z][\w-]*)\b', lambda w: w.group(1)+kf_suffix if w.group(1) in KF else w.group(1), m.group(2)), body)
            out.append(','.join(scope_sel(x,P) for x in sels)+'{'+body+'}')
    return ''.join(out)

css_y=''.join(re.findall(r'<style>(.*?)</style>', base, re.S))
css_f=''.join(re.findall(r'<style>(.*?)</style>', s, re.S))
KF=set(re.findall(r'@(?:-webkit-)?keyframes\s+([\w-]+)', css_y))
ONB=lambda x: bool(re.search(r'#ageGate|\.ag-|\.ob[-\b ]|\.ob\b|\.a18-pill', x))
Y=scope(css_y, 'html.yg', '_y', drop=ONB)
F=scope(css_f, 'html:not(.yg)', '', glob=ONB)
EXTRA = """
html.yg .ca-hero{display:none!important}
html:not(.yg) .hx-in.hxp-low{display:none!important}
#ageGate{z-index:100000}
html.yg .sp-go,html.yg .enh-go,html.yg .shop4 .sp-go,html.yg .ro .enh-go,html.yg #sheet .sp-go,html.yg #coach .enh-go{background:#118A4A!important;box-shadow:0 4px 0 #0A5E32!important}
.fav:not(.me){box-shadow:inset 0 0 0 60px rgba(0,0,0,.22);text-shadow:0 1px 2px rgba(0,0,0,.4)}html.yg .lk-box.mine b{color:#FFFFFF!important}html.yg .lk-box.mine small{color:#FFFFFF!important}html.yg .lk-box.mine{background:linear-gradient(135deg,#D41F7E,#6B2FD6)!important}
html:not(.yg) #avatar.av,html:not(.yg) .av{color:#FFFFFF!important}
html:not(.yg) .catchip{background:rgba(255,255,255,.94)!important;color:#2B2320!important;box-shadow:0 2px 10px rgba(0,0,0,.2)!important}html:not(.yg) .catchip svg{color:#2D4E86!important}
#ageGate .ob-bub button{background:#EADCC6!important;color:#2B2320!important}#ageGate .ob-bub button[aria-pressed="true"]{background:#2D4E86!important;color:#fff!important}
html.yg #ageGate .ob-bub button[aria-pressed="true"]{background:linear-gradient(135deg,#FF2D8E,#7B3CFF)!important}html.yg #ageGate .btn:not(:disabled){background:linear-gradient(135deg,#FF2D8E,#7B3CFF)!important}
"""
# one style block in place of the Fall Fair ones
first=s.index('<style>'); s=re.sub(r'<style>.*?</style>\s*', '', s, flags=re.S)
s=s[:first]+'<style>'+Y+'\n'+F+EXTRA+'</style>\n'+s[first:]

# theme class before first paint: saved bracket decides; no bracket yet -> original look
s=s.replace('<html lang="en" data-theme="light">','<html lang="en" class="yg">',1)
s=s.replace('<body>','<body>\n<script>try{var _b=(JSON.parse(localStorage.getItem("yofi.proto.v1")||"{}")||{}).ageBr;window.__young=!(_b&&_b!=="18 to 24");if(!window.__young){document.documentElement.classList.remove("yg");document.documentElement.setAttribute("data-theme","light")}}catch(e){window.__young=true}</script>',1)

def R(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# younger words for 25 to 44, and keep the theme class in step with the bracket
R("const isYoung = () => S && S.ageBr === '25 to 34';",
  "const isYoung = () => S && (!S.ageBr || S.ageBr === '18 to 24');\nfunction setLook() { const y = isYoung(), r = document.documentElement; r.classList.toggle('yg', y); if (y) r.removeAttribute('data-theme'); else r.setAttribute('data-theme', 'light'); }")
R("S.ageBr = b.dataset.oa; S.likes0 = null; save(); obAge(g);","S.ageBr = b.dataset.oa; S.likes0 = null; save(); setLook(); obAge(g);")
R("S.likes = [...picked]; S.obDone = 1; save();","S.likes = [...picked]; S.obDone = 1; save(); setLook(); youngPass();")
s=s.replace("setTimeout(youngPass, 0);","setTimeout(() => { setLook(); youngPass(); }, 0);",1)

R("const OB_AGES = ['25 to 34',","const OB_AGES = ['18 to 24', '25 to 34',")
R("const OB_PRE = { '25 to 34':","const OB_PRE = { '18 to 24': ['Travel', 'Dogs', 'Dinner parties', 'Beach'], '25 to 34':")
# under 25: Skill categories and their own interest bubbles; 25+: Fall Fair categories and interests
R("${GI_CA[k] || GICON[k] || GICON.star}</svg>`;","${(!window.__young && GI_CA[k]) || GICON[k] || GICON.star}</svg>`;")
R("const OB_INT = [","const OB_INT_O = [")
R("const OB_PRE = { '18 to 24': ['Travel', 'Dogs', 'Dinner parties', 'Beach'],", """const OB_INT_Y = [['Selfies', 3, 'selfie'], ['Bodybuilding', 3, 'fitness'], ['Fashion', 3, 'style'], ['Nights out', 3, 'night'], ['Travel', 2, 'travel'], ['Gym', 2, 'fitness'],
  ['Makeup', 2, 'selfie'], ['Festivals', 2, 'night'], ['Beach', 2, 'travel'], ['Dogs', 2, 'pets'], ['Food', 2, 'food'], ['Sneakers', 1, 'style'], ['Streetwear', 1, 'style'], ['Partying', 1, 'night'],
  ['Running', 1, 'fitness'], ['Road trips', 1, 'travel'], ['Cats', 1, 'pets'], ['Brunch', 1, 'food'], ['Cooking', 1, 'food'], ['Cars', 1, 'any'], ['Music', 1, 'night']];
let OB_INT = window.__young ? OB_INT_Y : OB_INT_O;
const OB_PRE = { '18 to 24': ['Selfies', 'Bodybuilding', 'Fashion', 'Nights out', 'Travel'],""")
a=s.index("const WALL_SHORT = {"); b=s.index("};", a)+2; s=s[:b]+"\napplyNames();"+s[b:]
R("function setLook() { const y = isYoung(), r = document.documentElement;", """// category names follow the look: Skill names for under 25, Fall Fair names for 25+
function applyNames() { const y = !!window.__young, A = applyNames; if (!A.o) A.o = { fc: FC_THEMES.map(t => t[1]), pc: PCATS.map(t => t[1]), ch: { ...CHAL }, ws: { ...WALL_SHORT } };
  const FY = { selfie: 'Best Selfie', style: 'Best Outfit', fitness: 'Best Gym', pets: 'Best Pet', food: 'Best Cooking', travel: 'Best Holiday', night: 'Best Night Out', any: 'Best Anything' };
  const PY = { selfie: 'Selfies', night: 'Night out', travel: 'Holiday', food: 'Cooking', style: 'Outfit', fitness: 'Gym' };
  const CY = { Pets: 'Best Pet', Nature: 'Best Holiday', Wildlife: 'Best Anything', People: 'Best Selfie', Travel: 'Best Holiday', Food: 'Best Cooking', Cities: 'Best Night Out', Action: 'Best Gym' };
  const WY = { selfie: 'Selfie', food: 'Cooking', travel: 'Holiday', night: 'Night out', fitness: 'Gym', style: 'Outfit' };
  FC_THEMES.forEach((t, i) => t[1] = y ? (FY[t[0]] || A.o.fc[i]) : A.o.fc[i]);
  PCATS.forEach((t, i) => t[1] = y && PY[t[0]] ? PY[t[0]] : A.o.pc[i]);
  Object.keys(CHAL).forEach(k => CHAL[k] = y && CY[k] ? CY[k] : A.o.ch[k]);
  Object.keys(WALL_SHORT).forEach(k => WALL_SHORT[k] = y && WY[k] ? WY[k] : A.o.ws[k]); }
function setLook() { const y = isYoung(), r = document.documentElement; window.__young = y; OB_INT = y ? OB_INT_Y : OB_INT_O; applyNames();""")
# photo scores stay in points (stars are only the daily pot points)
for a,b in [("- p.s.total} stars from qualifying","- p.s.total} points from qualifying"),("<small>${gap} star${gap === 1 ? '' : 's'} t","<small>${gap} point${gap === 1 ? '' : 's'} t"),
            ("You’re ${need - bestP.s.total} star${need - bestP.s.total ==","You’re ${need - bestP.s.total} point${need - bestP.s.total =="),("${mn - close.s.total} stars away.","${mn - close.s.total} points away."),
            ("- p.s.total} stars from entering cash compe","- p.s.total} points from entering cash compe"),("Closest to levelling up · <b>${n} star${n === 1 ? '' : 's'}","Closest to levelling up · <b>${n} point${n === 1 ? '' : 's'}")]:
    assert a in s, a; s=s.replace(a,b)
# younger words only once 18 to 24 is chosen; if the words were switched and she then picks 25+, reload so every label resets
R("function youngPass() { if (!isYoung()","const isYoungW = () => S && S.ageBr === '18 to 24';\nfunction youngPass() { if (!isYoungW()")
R("if (!isYoung() || youngQ)","if (!isYoungW() || youngQ)")
R("S.likes = [...picked]; S.obDone = 1; save(); setLook(); youngPass();","S.likes = [...picked]; S.obDone = 1; save(); setLook(); if (!isYoungW() && window.__ywDone) { location.reload(); return; } youngPass();")
R("if (u !== t) n.nodeValue = u;","if (u !== t) { n.nodeValue = u; window.__ywDone = 1; }")
# neutral, 18+
R('<p>Yofi has cash prizes, so you must be the age of majority in your province (<b>19+</b>, or 18+ in AB, MB and QC) to play.</p>','<p>Yofi has cash prizes, so you must be <b>18 or over</b> to play.</p>')
R('I confirm I’m of legal age in my province','I confirm I’m <b>18 or over</b>')
R('<div class="ag-b">19+</div>','<div class="ag-b">18+</div>')
R('<span class="a18-pill" title="Adults only · 19+">19+</span>','<span class="a18-pill" title="Adults only · 18+">18+</span>')
R(' Prizes are paid by Interac e-Transfer.',' Cash prizes are paid straight to your account.')
R('Yofi is for adults of legal age in your province.','Yofi is for adults aged 18 and over.')
R("You must be of legal age in your province. Entries are $1. Prize pots pay at midnight by Interac e-Transfer.","You must be 18 or over. Entries are $1. Prize pots pay at midnight.")
R('help@yofi.ca','help@yofi.app')
for a,b in [('Linda, 54 · Halifax','Linda, 54'),('Carol, 66 · Victoria','Carol, 66'),('Dianne, 58 · Muskoka','Dianne, 58'),('Margaret, 61 · Kelowna','Margaret, 61'),('Susan, 49 · Ottawa','Susan, 49')]: R(a,b)
# gem (dark look) and coin (Fall Fair) icons side by side; CSS shows the right one
gy='<g id="gemPathY"><path d="M7 3h10l5 6.2L12 21 2 9.2z" fill="url(#gemGrad)"/><path d="M2 9.2h20M7 3l5 18M17 3l-5 18M7 3l-2.2 6.2M17 3l2.2 6.2" stroke="#fff" stroke-opacity=".55" stroke-width=".9" fill="none"/></g>'
i=s.index('<g id="gemPath">'); j=s.index('</g>', i)+4; s=s[:j]+gy+s[j:]
s=s.replace('<use href="#gemPath"/>','<use class="gm-c" href="#gemPath"/><use class="gm-g" href="#gemPathY"/>')
s=s.replace('</style>','html.yg .gm-c,html:not(.yg) .gm-g{display:none}\n</style>',1)
s=s.replace("[/🏅/g, '👑'],",r"[/🏅/g, '👑'], [/🟡/g, '💎'], [/\bChampion bounties\b/g, 'King bounties'], [/\bChampions?\b/g, 'King'], [/real members vote/g, 'real judges vote'], [/\breal members\b/g, 'real judges'], [/\bMembers vote\b/g, 'Judges vote'], [/\bmembers are voting\b/g, 'judges are voting'], [/\bVote to earn\b/g, 'Judge to earn'], [/\bVote on (\d+) photos\b/g, 'Judge $1 photos'], [/\bVote on photos\b/g, 'Judge photos'], [/\bCompete for cash\b/g, 'Battle for cash'], [/\bcoins\b/g, 'gems'], [/\bcoin\b/g, 'gem'], [/\bCoins\b/g, 'Gems'],",1)
# Skill save and name
R("const KEY = 'yofi.ca50.v1'","const KEY = 'yofi.proto.v1'")
s=re.sub(r'<title>[^<]*</title>','<title>Yofi - Skill (Preview)</title>',s,1)
open(d+'yofi-preview.html','w').write(s)
print('combined', len(s)//1024, 'KB; css y', len(Y)//1024, 'KB f', len(F)//1024, 'KB')

# ---------- new start: age page -> landing; interests after the first photo is scored ----------
s=open(d+'yofi-preview.html').read()
def R2(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R2("function obAge(g) { const prog = n => `<div class=\"ob-prog\">${[1, 2].map(i => `<i class=\"${i <= n ? 'on' : ''}\"></i>`).join('')}</div>`;",
   "function obAge(g) { const prog = n => '';")
R2("g.querySelector('#obGo1').onclick = () => obLikes(g);",
   "g.querySelector('#obGo1').onclick = () => { S.age18 = 1; S.adult = 1; S.obDone = 1; save(); setLook(); if (!isYoungW() && window.__ywDone) { location.reload(); return; } youngPass(); g.className = ''; setTimeout(() => g.remove(), 300); if (typeof renderGallery === 'function') renderGallery(); paintTop(); };")
# age gate: no 18+ tick page, the age page is the first screen
a=s.index("  if (S.age18 && S.obDone) return; if (S.age18) {"); b=s.index("\n}\nsetTimeout(ageGate, 0);", a)
s=s[:a]+"  if (S.obDone && S.ageBr) return; let g0 = document.getElementById('ageGate'); if (!g0) { g0 = document.createElement('div'); g0.id = 'ageGate'; document.body.appendChild(g0); } g0.className = 'on'; obAge(g0);"+s[b:]
# interests: a callback mode used after the first photo
R2("g.querySelector('#obGo2').onclick = () => { S.likes = [...picked]; S.obDone = 1; save();",
   "g.querySelector('#obGo2').onclick = () => { if (window.__obAfter) { const f = window.__obAfter; window.__obAfter = null; S.likes = [...picked]; save(); obSort(); g.className = ''; setTimeout(() => g.remove(), 300); f(); return; } S.likes = [...picked]; S.obDone = 1; save();")
R2('<button class="link ob-back" id="obB2">Back</button>','${window.__obAfter ? \'\' : \'<button class="link ob-back" id="obB2">Back</button>\'}')
R2("g.querySelector('#obB2').onclick = () => obAge(g);","if (g.querySelector('#obB2')) g.querySelector('#obB2').onclick = () => obAge(g);")
R2("  await sleep(2000); clearInterval(iv);",
   "  await sleep(2000); clearInterval(iv);\n  if (!S.likes) await new Promise(res => { window.__obAfter = res; let g1 = document.getElementById('ageGate'); if (!g1) { g1 = document.createElement('div'); g1.id = 'ageGate'; document.body.appendChild(g1); } g1.className = 'on'; obLikes(g1); });")
s=s.replace('>Start playing · ${picked.size} picked<','>${window.__obAfter ? \'Continue\' : \'Start playing\'} · ${picked.size} picked<',1)
s=s.replace('<h1>What do you love to photograph?</h1>','<h1>${window.__obAfter ? \'Nice photo! What else do you love to photograph?\' : \'What do you love to photograph?\'}</h1>',1)
open(d+'yofi-preview.html','w').write(s); print('start ok')

# ---------- tournament loss: only suggest a new photo, and open the picker without jumping to Touch-ups ----------
s=open(d+'yofi-preview.html').read()
a="<div class=\"tw-b\"><button id=\"twNew\">📷 Try a new photo</button>${lowestOpen(p) ? `<button id=\"twEnh\" data-k=\"${k}\">✨ Touch up ${esc(c.short.toLowerCase())} · ${fixCost(p)} 🟡</button>` : ''}</div>"
assert s.count(a)==1, s.count(a)
s=s.replace(a,"<div class=\"tw-b\"><button id=\"twNew\">📷 Try a new photo</button></div>")
a="if ($('#twNew')) $('#twNew').onclick = () => { closeSheet(); if ($('#flow').classList.contains('on')) closeFlow(); go('studio'); pickPhoto(true); };"
assert s.count(a)==1
s=s.replace(a,"if ($('#twNew')) $('#twNew').onclick = () => { closeSheet(); if ($('#flow').classList.contains('on')) closeFlow(); pickPhoto(true); };")
open(d+'yofi-preview.html','w').write(s); print('tourney ok')
