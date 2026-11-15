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
s=s.replace("[/🏅/g, '👑'],",r"[/🏅/g, '👑'], [/🟡/g, '💎'], [/\bChampion bounties\b/g, 'King bounties'], [/\bCategory champion\b/g, 'Category King'], [/\b(Beat|Challenge|beat|challenge) the Champion\b/g, '$1 the King'], [/\bThe Champion\b/g, 'The King'], [/\bA Champion challenge\b/g, 'A King challenge'], [/real members vote/g, 'real judges vote'], [/\breal members\b/g, 'real judges'], [/\bMembers vote\b/g, 'Judges vote'], [/\bmembers are voting\b/g, 'judges are voting'], [/\bVote to earn\b/g, 'Judge to earn'], [/\bVote on (\d+) photos\b/g, 'Judge $1 photos'], [/\bVote on photos\b/g, 'Judge photos'], [/\bCompete for cash\b/g, 'Battle for cash'], [/\bcoins\b/g, 'gems'], [/\bcoin\b/g, 'gem'], [/\bCoins\b/g, 'Gems'],",1)
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

# ---------- after a lost tournament: Touch-ups opens on a "New photo" screen; once the new photo is ready, offer the next tournament ----------
s=open(d+'yofi-preview.html').read()
def R3(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R3('<div class="tw-b"><button id="twNew">📷 Try a new photo</button></div>','<div class="tw-b"><button id="twNew" data-k="${k}">📷 Try a new photo</button></div>')
R3("if ($('#twNew')) $('#twNew').onclick = () => { closeSheet(); if ($('#flow').classList.contains('on')) closeFlow(); pickPhoto(true); };",
   "if ($('#twNew')) $('#twNew').onclick = () => { const k = $('#twNew').dataset.k; S.retryT = { fee: T.fee || 1, at: Date.now() }; save(); closeSheet(); if ($('#flow').classList.contains('on')) closeFlow(); newPhotoStart(k); };")
NP = r"""
// "Try a new photo" after a lost tournament: a calm start screen in Touch-ups
function newPhotoStart(k) {
  const c = C.find(x => x.k === k), nm = c ? c.name.toLowerCase() : '';
  const TIP = { light: 'Look for a photo taken in soft daylight, near a window or outdoors.', comp: 'Pick one where the subject fills the frame and isn’t cut off.', colour: 'Bright, natural colours do best. Avoid dull or very dark shots.', subject: 'Faces and moments with feeling win votes. Pick one that tells a story.', tech: 'Choose a sharp photo that isn’t blurry or grainy.' };
  const ks = CATS8.slice();
  openSheet(`<div class="np"><span class="np-ic">📷</span><h2>Try a new photo</h2>
    ${nm ? `<p class="np-why">You lost on <b>${esc(nm)}</b>. ${TIP[k] || ''}</p>` : '<p class="np-why">A fresh photo gives you a fresh chance.</p>'}
    <p class="np-l">Pick a category</p><div class="np-g">${ks.map(x => `<button data-npk="${x}">${gi(x)}<span>${esc(crownName(x))}</span></button>`).join('')}</div>
    <button class="btn block np-go" id="npGo">Choose a photo</button><div style="text-align:center"><button class="link" data-shclose>Not now</button></div></div>`, { full: true, cover: true });
  document.querySelectorAll('#sheetBody [data-npk]').forEach(b => b.onclick = () => { window.__preCat = b.dataset.npk; closeSheet(); pickPhoto(true); });
  $('#npGo').onclick = () => { window.__preCat = null; closeSheet(); pickPhoto(true); }; }
// once a photo added after the loss reaches the goal, Touch-ups offers the next tournament
function retryBar() { const st = $('#studio'); if (!st) return; const old = st.querySelector('.np-back'); if (old) old.remove();
  const R0 = S.retryT, p = cur && cur(); if (!R0 || !p || !(p.at > R0.at) || p.s.total < CFG.QUALIFY) return;
  const b = document.createElement('button'); b.className = 'btn block np-back'; b.innerHTML = `🏆 Enter the next tournament with this photo`;
  b.onclick = () => retryEnter(p);
  st.insertBefore(b, st.firstChild); }
setInterval(retryBar, 1000);
function retryEnter(p) { const R0 = S.retryT; S.retryT = null; save(); const b = document.querySelector('.np-back'); if (b) b.remove(); tTier((R0 && R0.fee) || 1); S.tour = null; save(); window.__tSel = p.id; if ($('#flow').classList.contains('on')) closeFlow(); openTourney(); }
"""
R3("function whyLostHTML(T) {", NP+"function whyLostHTML(T) {")
R3("function showCompReady(p, goal) {\n  if (p) { p.readyShown = true; save(); }", "function showCompReady(p, goal) {\n  if (p) { p.readyShown = true; save(); }\n  if (S.retryT && p && p.at > S.retryT.at && p.s.total >= CFG.QUALIFY) { celebrate({ src: p.src, score: p.s.total, title: 'Ready for the next tournament!', text: `Your new photo hit <b>${p.s.total}</b>. Take it back into a tournament and try again.`, cta: '🏆 Enter the next tournament', onCta: () => retryEnter(p), later: 'Later' }); return; }")
s=s.replace('</style>',"""#sheetBody .np{text-align:center;padding:6px 2px}.np-ic{font-size:2.6rem}.np h2{margin:6px 0 6px}.np-why{margin:0 0 16px}.np-l{margin:0 0 8px;font-weight:800;text-align:left}
.np-g{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 16px}.np-g button{display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 4px;border-radius:14px;border:0;font:700 .82rem/1.2 inherit;cursor:pointer}.np-g svg{width:26px;height:26px}
html:not(.yg) .np-g button{background:#fff;color:#2B2320;box-shadow:inset 0 0 0 1.5px #CDBB98}html:not(.yg) .np-g svg{color:#9E2F2A}html:not(.yg) .np-why b{color:#2D4E86}
html.yg .np-g button{background:#241640;color:#fff;box-shadow:inset 0 0 0 1.5px #4A2F78}html.yg .np-g svg{color:#FF4FB0}html.yg .np-why{color:#D8C8F5}html.yg .np-why b{color:#FFC93C}
.np-back{margin:4px 0 10px!important}
</style>""",1)
open(d+'yofi-preview.html','w').write(s); print('newphoto ok')

# ---------- tickets: earned by voting (every 25 votes), shown in a header pill; energy removed; 10 in a row is a loot box again ----------
import re as _re
s=open(d+'yofi-preview.html').read()
def R4(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# unlimited voting
# (energy back) R4("function paintEnergy() {", "function paintEnergy() {}\nf
# (energy back) R4("function energy() {", "function energy() { S.en = EN_MAX
# count votes toward a ticket
R4("  S.votes++; S.since++;", "  S.votes++; S.tixV = (S.tixV || 0) + 1; if (S.tixV >= TIX_EVERY) { S.tixV = 0; S.cashTix = (S.cashTix || 0) + 1; setTimeout(() => { paintTix(); ticketPop(); }, 1600); } S.since++;")
# energy bar -> ticket bar
# (energy back) a=s.index('`<div class="jf-en"><div class="en-top"><span cla
# (energy back) s=s[:a]+'`<button class="jf-en tkp" id="tkpBar" aria-label="
# 10th step: loot box again
R4("i === 9 ? `<u class=\"tkb\">🎟️</u><span class=\"tkl\">FREE $1</span>${(S.cashTix || 0) ? `<em class=\"chtx\">${S.cashTix}</em>` : ''}` : ''","i === 9 ? '<u>🧰</u>×10' : ''")
R4("${i === 9 ? 'data-chtix role=\"button\" aria-label=\"Big chest at 10 in a row. See your tickets\"' : ''}","")
# chest: coins, and a bonus ticket only in epic or legendary chests; no energy
R4("const want = rar.k === 'rare' ? 2 : 1,","const want = (rar.k === 'epic' || rar.k === 'legend') ? 1 : 0,")
# (energy back) R4("<div class=\"ch-it\" style=\"animation-delay:.45s\"><b>+
# (energy back) R4("toast(`⚡ +${rar.e} energy`);","")
# lucky boxes: coins instead of energy
# (energy back) R4("{ w: .3, k: 'e', n: 5 }","{ w: .3, k: 'g', n: 10 * LM }"
# free entries panel: progress is votes now
s=s.replace("if (!n) { const c = Math.min(S.combo || 0, 10);","if (!n) { const c = S.tixV || 0;")
s=_re.sub(r'<span class="ut0-i">🧰</span><div><b>Pick the winner 10 times in a row</b><small>On the (Vote|Judge) page\. The big chest opens and gives you free entries\.</small></div>',
          lambda m: f'<span class="ut0-i">🎟️</span><div><b>Every {{TIX_EVERY}} votes = 1 free entry</b><small>Keep going on the {m.group(1)} page. A big chest at 10 in a row can hold a bonus entry too.</small></div>'.replace('{TIX_EVERY}','${TIX_EVERY}'), s)
s=s.replace('<div class="ut0-bar"><i style="width:${c * 10}%"></i></div><p class="ut0-n">${c} of 10 in a row</p>','<div class="ut0-bar"><i style="width:${c / TIX_EVERY * 100}%"></i></div><p class="ut0-n">${c} of ${TIX_EVERY} votes</p>')
# header ticket pill
R4('<button class="wplus" id="walletPlus" aria-label="Add funds">+</button>','<button class="wb tixp" id="tixPill" aria-label="Free tournament entries"><span class="tx-ic">🎟️</span><b id="tixNum">0</b><small id="tixProg" class="tx-pr">0/25</small><svg class="tx-ring" viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="15.5"/><circle class="f" cx="18" cy="18" r="15.5"/></svg></button><button class="wplus" id="walletPlus" aria-label="Add funds">+</button>')
JS = r"""
function paintTix() { const b = document.getElementById('tixPill'); if (!b || !S) return; const n = S.cashTix || 0, v = S.tixV || 0;
  b.classList.toggle('has', n > 0); document.getElementById('tixNum').textContent = n;
  b.style.setProperty('--p', 0); const pr = document.getElementById('tixProg'); if (pr) pr.textContent = `${v}/${TIX_EVERY}`;
  b.setAttribute('aria-label', n ? `${n} free tournament entr${n === 1 ? 'y' : 'ies'}` : `${v} of ${TIX_EVERY} votes to your next free entry`); }
setInterval(paintTix, 800);
document.addEventListener('click', e => { if (e.target.closest('#tixPill') || e.target.closest('#tkpBar')) useTickets(); });
"""
R4("function fcNotify() {", JS+"function fcNotify() {")
R4("const STK = [3, 5, 10];","const STK = [3, 5, 10]; const TIX_EVERY = 25;")
s=s.replace('</style>',"""html .wallet{display:flex!important;gap:6px}html .wallet .wb.cash,html .wallet .wb.gems{flex:1 1 0;min-width:0}html .wallet .wplus{flex:none}
.wb.tixp{flex:none;display:flex;align-items:center;justify-content:center;gap:4px;min-width:62px;padding:0 10px!important;border:0;cursor:pointer;border-radius:16px;background-repeat:no-repeat!important;background-position:8px calc(100% - 5px)!important;background-size:calc((100% - 16px) * var(--p, 0)) 3px!important}
.tixp .tx-ic{font-size:1.15rem;line-height:1}.wb.tixp{min-width:0!important;padding:0 7px!important;gap:3px!important}.tixp b{font-size:.95rem!important}.tixp .tx-ic{font-size:1rem!important}.tixp .tx-pr{font-size:.66rem!important;padding-left:4px!important}html .wallet .wb.cash small,html .wallet .wb.gems small{display:none!important}.tixp .tx-pr{font-size:.72rem;font-weight:800;opacity:.75;padding-left:5px;margin-left:2px;border-left:1.5px solid currentColor}.tixp b{font-weight:900;font-size:1.05rem}.tixp .tx-ring{display:none}
html:not(.yg) .wb.tixp{background-color:#F7F1E7!important;background-image:linear-gradient(#D9A441,#D9A441)!important;box-shadow:inset 0 0 0 1.5px #CDBB98;color:#2B2320}html:not(.yg) .tixp .tx-ring circle{stroke:#EADCC6}html:not(.yg) .tixp .tx-ring .f{stroke:#D9A441}html:not(.yg) .wb.tixp.has{background-color:#FFF3D1!important;box-shadow:inset 0 0 0 2px #D9A441}
html.yg .wb.tixp{background-color:#1E1236!important;background-image:linear-gradient(#FFC93C,#FFC93C)!important;box-shadow:inset 0 0 0 1.5px #3A2760;color:#fff}html.yg .tixp .tx-ring circle{stroke:#33204F}html.yg .tixp .tx-ring .f{stroke:#FFC93C}html.yg .wb.tixp.has{box-shadow:inset 0 0 0 2px #FFC93C}
.jf-en.tkp{display:block;width:100%;border:0;background:none;padding:0;text-align:left;cursor:pointer;font:inherit;color:inherit}.tkp-l{display:block;margin:2px 0 0 30px;font-size:.78rem;opacity:.8}
# (energy back) .t-energy,#enPlus{display:none!important}
</style>""",1)
open(d+'yofi-preview.html','w').write(s); print('tickets ok')

# ---------- energy is gone: remove what players would still see ----------
s=open(d+'yofi-preview.html').read()
# (energy back) s=s.replace(".enfly{",".enfly{display:none!important;",1) if
# (energy back) s=s.replace("</style>",".enfly{display:none!important}\n</st
# a="<b>${gemIcon('')}100 <i>+</i> ⚡50</b><small>Coins to enhance it · energy to vote and earn more</small>"
# assert s.count(a)==1; s=s.replace(a,"<b>${gemIcon('')}100</b><small>Coins to enhance your photo</small>")
# a=" + tile('⚡', CASH_EN[i], 'Free energy', 'en')"
# assert s.count(a)==1; s=s.replace(a,"")
open(d+'yofi-preview.html','w').write(s); print('energy text ok')

# ---------- batch: loot boxes at 3/6/10, chest surprise, 50 votes per ticket, interests before the picker, wording, clubs, packs, layout ----------
s=open(d+'yofi-preview.html').read()
def R5(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# loot boxes at 3, 6 and 10 in a row
R5("const STK = [3, 5, 10];","const STK = [3, 6, 10];")
R5("const streakX = c => c >= 10 ? 10 : c >= 5 ? 5 : c >= 3 ? 3 : 1;","const streakX = c => c >= 10 ? 10 : c >= 6 ? 6 : c >= 3 ? 3 : 1;")
R5("({ 3: 3, 5: 5, 10: 10 })[S.combo]","({ 3: 3, 6: 5, 10: 10 })[S.combo]")
R5("${[2, 4, 9].includes(i) ? 'm m' + (i + 1) : ''}","${[2, 5, 9].includes(i) ? 'm m' + (i === 5 ? 5 : i + 1) : ''}")
R5("i === 4 ? '<u>🎁</u>×5' :","i === 5 ? '<u>🎁</u>×6' :")
# chest: no ticket; surprise = double coins on the next 10 votes
R5("const want = (rar.k === 'epic' || rar.k === 'legend') ? 1 : 0,","const want = 0,")
R5("const tk = chestTix(rar);","const tk = chestTix(rar); S.boostN = 10;")
R5("${tk ? `<div class=\"ch-it\" style=\"animation-delay:.7s\">","<div class=\"ch-it\" style=\"animation-delay:.45s\"><b>2×</b><small>coins on your next 10 votes</small></div>${tk ? `<div class=\"ch-it\" style=\"animation-delay:.7s\">")
R5("S.gems += earn; meterAdd(earn);","if (S.boostN > 0) { S.boostN--; earn *= 2; } S.gems += earn; meterAdd(earn);")
# 50 votes per free entry
# tickets: 25 votes
# interests come before the photo picker (first photo only)
R5("  if (!S.likes) await new Promise(res => { window.__obAfter = res;","  if (false) await new Promise(res => { window.__obAfter = res;")
s=s.replace("document.getElementById('file').click()","yWL()")
R5("$('#file').value = ''; $('#file').click();","$('#file').value = ''; yWL();",3)
R5("Nice photo! What else do you love to photograph?","Before you pick a photo: what do you love to photograph?")
YW = r"""
// first photo: ask interests, then open the phone's photo picker
window.yWL = function () { const f = document.getElementById('file'); if (S.likes || !S.obDone) { f.click(); return; }
  window.__obAfter = () => f.click(); let g1 = document.getElementById('ageGate'); if (!g1) { g1 = document.createElement('div'); g1.id = 'ageGate'; document.body.appendChild(g1); } g1.className = 'on'; obLikes(g1); };
document.addEventListener('click', e => { const l = e.target.closest('label[for="file"]'); if (l && S.obDone && !S.likes) { e.preventDefault(); yWL(); } }, true);
// the + on the coins pill opens the shop
document.addEventListener('click', e => { if (e.target.closest('#gemPill .gplus') || e.target.closest('#walletPlus')) { e.preventDefault(); e.stopPropagation(); openStore(); } }, true);
// 25+: prizes, not pots
const OLD_W = [[/\bprize pots\b/g, 'prizes'], [/\bprize pot\b/g, 'prize'], [/\bPots\b/g, 'Prizes'], [/\bpots\b/g, 'prizes'], [/\bPot\b/g, 'Prize'], [/\bpot\b/g, 'prize'], [/\bPOT\b/g, 'PRIZE']];
function oldPass() { if (isYoungW() || !document.body) return;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => { const p = n.parentElement; return !p || p.closest('script,style,textarea,input') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
  let n; while ((n = w.nextNode())) { const t = n.nodeValue; if (!t || !/pot/i.test(t)) continue; let u = t; for (const [a, b] of OLD_W) u = u.replace(a, b); if (u !== t) n.nodeValue = u; } }
let oldQ = 0; new MutationObserver(() => { if (isYoungW() || oldQ) return; oldQ = requestAnimationFrame(() => { oldQ = 0; oldPass(); }); }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
setTimeout(oldPass, 0);
"""
R5("function fcNotify() {", YW+"function fcNotify() {")
# new players start with no old clubs
R5("g.querySelector('#obGo1').onclick = () => { S.age18 = 1;","g.querySelector('#obGo1').onclick = () => { S.crews = []; S.crewCur = null; S.age18 = 1;")
# club names and members follow the look
R5("const CREW_POOL = ['mike', 'james', 'sophie', 'dan', 'priya', 'olly', 'chloe', 'sam', 'ella', 'tom'];","const CREW_POOL = ['mike', 'james', 'sophie', 'dan', 'priya', 'olly', 'chloe', 'sam', 'ella', 'tom'], CREW_POOL_Y = CREW_POOL.slice(), CREW_POOL_O = ['margaret', 'susan', 'dave', 'carol', 'linda.b', 'pete', 'jean', 'barb', 'gord', 'helen'];")
R5("const CREW_SUGG = ['Friday lads', 'The pet squad', 'Gym rats', 'Family'];","const CREW_SUGG = ['Friday lads', 'The pet squad', 'Gym rats', 'Family'], CREW_SUGG_Y = ['Friday lads', 'The pet squad', 'Gym rats', 'Uni crew'], CREW_SUGG_O = ['Garden club', 'Book club', 'Family', 'Walking group'];")
R5("newCrew(S.user && S.user.h ? `${S.user.h}’s friends` : 'My friends')","newCrew(S.user && S.user.h ? `${S.user.h}’s ${window.__young ? 'friends' : 'club'}` : (window.__young ? 'My friends' : 'My club'))")
R5("function setLook() { const y = isYoung(), r = document.documentElement; window.__young = y;","function setLook() { const y = isYoung(), r = document.documentElement; window.__young = y; try { CREW_SUGG.splice(0, CREW_SUGG.length, ...(y ? CREW_SUGG_Y : CREW_SUGG_O)); CREW_POOL.splice(0, CREW_POOL.length, ...(y ? CREW_POOL_Y : CREW_POOL_O)); } catch (e) {}")
# buying cash gives only a small coin bonus
R5("quickPack(5, 1000, 'Welcome offer')","quickPack(5, 25, 'Welcome offer')")
R5("quickPack(5, 500, '$5 pack',","quickPack(5, 10, '$5 pack',")
R5("quickPack(5, 500, 'Rematch top-up',","quickPack(5, 10, 'Rematch top-up',")
s=s.replace("coins = w ? 1000 : 500;","coins = w ? 25 : 10;")
# score area: Expression -> Wow factor
R5("name: 'Expression', short: 'Expression', verb: 'Improve Expression'","name: 'Wow factor', short: 'Wow factor', verb: 'Improve Wow factor'")
R5("{ k: 'expr', name: 'Expression',","{ k: 'expr', name: 'Wow factor',")
# 25+: Tournaments, not Shows (keep "Best in Show")
s=re.sub(r'\bShows\b','Tournaments',s)
s=s.replace('</style>',"""html.yg #judge .stk-steps,html:not(.yg) #judge .stk-steps{grid-template-columns:1fr 1fr 46px 1fr 1fr 46px 1fr 1fr 1fr 52px!important}
html .stk-steps i.m10{animation:none!important}html .stk-steps i.m10 u{font-size:1.3rem!important}
html.yg .stk-steps i.m10:not(.on){background:#241640!important;box-shadow:inset 0 0 0 1.5px #FFC93C!important;color:#fff!important}html.yg .stk-steps i.m10.on{background:#FFC93C!important;color:#2A1600!important;box-shadow:none!important}
html:not(.yg) .stk-steps i.m10:not(.on){background:#fff!important;box-shadow:inset 0 0 0 2px #C99A3B!important;color:#2B2320!important}html:not(.yg) .stk-steps i.m10.on{background:#D9A441!important;color:#2B2320!important;box-shadow:none!important}
html .nxu{max-width:100%!important;overflow:hidden}html .nxu .d{min-width:0;overflow:hidden;gap:3px!important;flex-shrink:1}html .nxu .d i{flex:0 0 auto;width:7px!important;height:7px!important}
</style>""",1)
open(d+'yofi-preview.html','w').write(s); print('batch ok')

# ---------- upload confirmation: say it worked and where the photo is ----------
s=open(d+'yofi-preview.html').read()
a="function showResult(p, o = {}) {"
assert s.count(a)==1
# profile photo from the selfie pop-up: confirm it was saved and where
a2="$('#picGo').onclick = () => { close(); pickProfilePic(() => { toast('Looking good! Now challenge your friend.');"
assert s.count(a2)==1
s=s.replace(a2,"$('#picGo').onclick = () => { close(); pickProfilePic(() => { picDone();")
UP = r"""
function picDone() { const old = document.getElementById('upOk'); if (old) old.remove();
  const b = document.createElement('div'); b.id = 'upOk'; b.className = 'up-ok'; b.setAttribute('role', 'status');
  b.innerHTML = `<img src="${S.user.pic}" alt=""><span><b>✓ Profile photo saved</b><small>It’s your picture at the top right, and friends see it on every challenge</small></span><button aria-label="Dismiss">✕</button>`;
  document.body.appendChild(b); requestAnimationFrame(() => b.classList.add('on'));
  const bye = () => { b.classList.remove('on'); setTimeout(() => b.remove(), 300); }; b.querySelector('button').onclick = bye; setTimeout(bye, 5000); }
function upDone(p) { const old = document.getElementById('upOk'); if (old) old.remove();
  const k = p.cat || 'any', nm = crownName(k), y = !!window.__young;
  const b = document.createElement('div'); b.id = 'upOk'; b.className = 'up-ok'; b.setAttribute('role', 'status');
  b.innerHTML = `<img src="${p.src}" alt=""><span><b>✓ Photo uploaded</b><small>Saved in <b>${esc(nm)}</b> · find it in ${y ? 'Studio' : 'Touch-ups'} under Switch</small></span><button aria-label="Dismiss">✕</button>`;
  document.body.appendChild(b); requestAnimationFrame(() => b.classList.add('on'));
  const bye = () => { b.classList.remove('on'); setTimeout(() => b.remove(), 300); }; b.querySelector('button').onclick = bye; setTimeout(bye, 6000); }
"""
s=s.replace("function fcNotify() {", UP+"function fcNotify() {",1)
s=s.replace('</style>',""".up-ok{position:fixed;left:12px;right:12px;top:calc(env(safe-area-inset-top,0px) + 12px);z-index:99998;display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:16px;transform:translateY(-130%);transition:transform .3s ease;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.up-ok.on{transform:none}.up-ok img{width:44px;height:44px;border-radius:10px;object-fit:cover;flex:none}.up-ok span{flex:1;min-width:0;display:flex;flex-direction:column}.up-ok small{font-size:.85rem}.up-ok button{border:0;background:none;font-size:1rem;cursor:pointer;color:inherit;opacity:.7}
html:not(.yg) .up-ok{background:#2F6B3F;color:#fff}html.yg .up-ok{background:#118A4A;color:#fff}
</style>""",1)
open(d+'yofi-preview.html','w').write(s); print('upload ok')


# ---------- energy is paid from the Cash balance ----------
s=open(d+'yofi-preview.html').read()
def R6(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R6("const EN_PACKS = [{ en: 50, usd: 1.99, gems: 150 }, { en: 150, usd: 4.99, gems: 400, tag: 'Popular' }, { en: 500, usd: 14.99, gems: 1200, tag: 'Best value' }];",
   "const EN_PACKS = [{ en: 50, usd: 1, gems: 150 }, { en: 150, usd: 2, gems: 400, tag: 'Popular' }, { en: 500, usd: 5, gems: 1200, tag: 'Best value' }];")
R6("close(); checkout(`${k.en} energy`, k.usd, () => { S.paidCash = true; addEnergy(k.en); }); });","close(); enCash(k, () => addEnergy(k.en)); });")
R6("buy: () => checkout(`${EN_PACKS[1].en} energy`, EN_PACKS[1].usd, () => { S.paidCash = true; addEnergy(EN_PACKS[1].en); if (onBuy) setTimeout(onBuy, 1500); }),",
   "buy: () => enCash(EN_PACKS[1], () => { addEnergy(EN_PACKS[1].en); if (onBuy) setTimeout(onBuy, 1500); }),")
R6("function bindEnPacks(root, close) {", r"""function enCash(k, then) { const c = S.cash || 0;
  if (c < k.usd) { openStore(`${k.en} energy costs ${money(k.usd)} from your cash. You have ${money(c)}. Add cash first.`); setTimeout(() => { const t = [...document.querySelectorAll('#sheetBody button')].find(b => /^\s*\S*\s*Cash\s*$/.test(b.textContent)); if (t) t.click(); }, 50); return; }
  S.cash = +(c - k.usd).toFixed(2); save(); paintWallet(); toast(`⚡ +${k.en} energy · ${money(k.usd)} from your cash`); then(); }
function bindEnPacks(root, close) {""")
s=s.replace("`Buy $${k.usd}`, `data-enusd=\"${i}\"`","`Pay $${k.usd} cash`, `data-enusd=\"${i}\"`")
s=s.replace('<button class="sb" data-enusd="${i}">Buy $${k.usd}</button>','<button class="sb" data-enusd="${i}">Pay $${k.usd} cash</button>')
open(d+'yofi-preview.html','w').write(s); print('energy cash ok')
s=open(d+'yofi-preview.html').read()
a='<button class="enh-go" id="roBuy">Buy · $${(+cfg.usd).toFixed(2)}</button>'
assert s.count(a)==1
s=s.replace(a,'<button class="enh-go" id="roBuy">${kind === \'energy\' ? `Pay $${cfg.usd} from cash` : `Buy · $${(+cfg.usd).toFixed(2)}`}</button>')
open(d+'yofi-preview.html','w').write(s)

# ---------- energy in the wallet: one pack, 50 energy for $1 from cash ----------
s=open(d+'yofi-preview.html').read()
def R7(a,b):
    global s; assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
R7("const EN_PACKS = [{ en: 50, usd: 1, gems: 150 }, { en: 150, usd: 2, gems: 400, tag: 'Popular' }, { en: 500, usd: 5, gems: 1200, tag: 'Best value' }];",
   "const EN_PACKS = [{ en: 50, usd: 1, gems: 150 }, { en: 150, usd: 2, gems: 400, tag: 'Popular' }, { en: 500, usd: 5, gems: 1200, tag: 'Best value' }]; const EN_SHOW = 3;")
s=s.replace("EN_PACKS.map((k, i) => card(","EN_PACKS.slice(0, EN_SHOW).map((k, i) => card(",1)
s=s.replace("${EN_PACKS.map((k, i) => `<div class=\"srow\">","${EN_PACKS.slice(0, EN_SHOW).map((k, i) => `<div class=\"srow\">",1)
R7('<button class="wb tixp" id="tixPill"','<button class="wb enpl" id="enPill" aria-label="Energy. Tap to buy 50 energy for $1"><span>⚡</span><b id="enNum">0</b></button><button class="wb tixp" id="tixPill"')
EW = r"""
function paintEnPill() { const b = document.getElementById('enNum'); if (b && S) b.textContent = energy(); }
setInterval(paintEnPill, 800);
function enQuick() { const e = energy(), c = S.cash || 0;
  openSheet(`<div class="ug enq"><h2>⚡ Energy</h2><p class="sub">You have <b>${e} energy</b>. Each vote uses 1, and it refills +5 an hour for free.</p>
    <div class="enq-c"><span class="enq-i">⚡</span><div><b>50 energy</b><small>Paid from your cash · you have ${money(c)}</small></div></div>
    <button class="btn block" id="enqGo">Pay $1 from cash</button><div style="text-align:center"><button class="link" data-shclose>Not now</button></div></div>`);
  $('#enqGo').onclick = () => { closeSheet(); enCash(EN_PACKS[0], () => { addEnergy(EN_PACKS[0].en); paintEnPill(); }); }; }
document.addEventListener('click', e => { if (e.target.closest('#enPill')) { e.preventDefault(); enQuick(); } });
"""
R7("function fcNotify() {", EW+"function fcNotify() {")
s=s.replace('</style>',""".wb.enpl{flex:none;display:flex;align-items:center;justify-content:center;gap:2px;padding:0 8px!important;border:0;border-radius:16px;cursor:pointer;font:inherit}.enpl span{font-size:.95rem}.enpl b{font-weight:900;font-size:.95rem}
html:not(.yg) .wb.enpl{background:#F7F1E7;box-shadow:inset 0 0 0 1.5px #CDBB98;color:#2B2320}html.yg .wb.enpl{background:#1E1236;box-shadow:inset 0 0 0 1.5px #3A2760;color:#fff}
html .wallet .wb.cash b,html .wallet .wb.gems b{font-size:1rem!important}html .wallet{gap:5px!important}html .wallet .wb.cash,html .wallet .wb.gems{padding-left:8px!important;padding-right:8px!important}
.enq-c{display:flex;gap:14px;align-items:center;margin:14px 0;padding:14px;border-radius:16px}.enq-i{font-size:2rem}.enq-c b{display:block;font-size:1.1rem}
html:not(.yg) .enq-c{background:#fff;box-shadow:inset 0 0 0 1.5px #CDBB98}html.yg .enq-c{background:#1E1236;box-shadow:inset 0 0 0 1.5px #3A2760}
</style>""",1)
open(d+'yofi-preview.html','w').write(s); print('energy wallet ok')
s=open(d+'yofi-preview.html').read()
s=s.replace('</style>',"""html #shell > .wallet{display:flex!important;gap:5px!important}html #shell > .wallet #wCash,html #shell > .wallet #gemPill{flex:1 1 0!important;min-width:0!important;width:auto!important}
html #shell > .wallet #enPill,html #shell > .wallet #tixPill{flex:0 0 auto!important;width:auto!important;min-width:0!important}html #shell > .wallet #walletPlus{display:none!important}
html #shell > .wallet #enPill>span{display:inline!important;min-width:0!important}
</style>""",1)
open(d+'yofi-preview.html','w').write(s)
s=open(d+'yofi-preview.html').read()
s=s.replace('</style>',"""html #shell > .wallet .wb{padding:0 6px!important;gap:4px!important}html #shell > .wallet .wb b{font-size:.9rem!important;letter-spacing:-.01em}html #shell > .wallet .wb svg{width:18px!important;height:18px!important}
html #shell > .wallet #gemPill .gplus{position:static!important;flex:none;width:20px!important;height:20px!important;margin-left:2px}html #shell > .wallet #gemPill .gplus svg{width:10px!important;height:10px!important}
html #shell > .wallet #tixPill .tx-pr{font-size:.62rem!important}
</style>""",1)
open(d+'yofi-preview.html','w').write(s)
# ---------- shop: cash packs only (they include coins and energy); no Energy / Coins tabs ----------
s=open(d+'yofi-preview.html').read()
a="  SHOPTAB = tab || SHOPTAB;\n  const T = SHOPTAB;"
assert s.count(a)==1
s=s.replace(a,"  SHOPTAB = 'cash';\n  const T = SHOPTAB;")
s=s.replace('</style>','#sheetBody .sp-tabs{display:none!important}\n</style>',1)
open(d+'yofi-preview.html','w').write(s)
# ---------- $5 cash pack ----------
s=open(d+'yofi-preview.html').read()
a="const CASH_EN = [50, 150, 400];"; assert s.count(a)==1; s=s.replace(a,"const CASH_EN = [25, 50, 150, 400];")
a="const PACKS = [\n  { t: 'Starter',"; assert s.count(a)==1
s=s.replace(a,"const PACKS = [\n  { t: 'Try it', sub: 'A small top-up to play.', cash: 5, bonus: 0, gems: 10, free: 10, cls: '' },\n  { t: 'Starter',")
open(d+'yofi-preview.html','w').write(s)
s=open(d+'yofi-preview.html').read()
a="PACKS.map((k, i) => card(i === 2 ? 'Best value' : '',"; assert s.count(a)==1
s=s.replace(a,"PACKS.map((k, i) => card(i === 3 ? 'Best value' : i === 2 ? 'Popular' : '',")
open(d+'yofi-preview.html','w').write(s)
