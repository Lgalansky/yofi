import re, colorsys
d='/tmp/claude-0/-home-user-yofi/c69be753-0b48-5242-b029-4f4be89f4655/scratchpad/'
s=open(d+'yofi-ca50.html').read()
def R(a,b,n=None):
    global s; c=s.count(a); assert c>=1 and (n is None or c==n),(a[:90],c); s=s.replace(a,b)

# ---------- Fall Fair palette: lavender -> cream/kraft, plum ink -> warm ink, pink/violet -> ribbon blue, bright green -> prize green ----------
def hx(h,l,sat):
    r,g,b=colorsys.hls_to_rgb(h/360,l,sat); return int(r*255+.5),int(g*255+.5),int(b*255+.5)
def ff(r,g,b):
    h,l,sat=colorsys.rgb_to_hls(r/255,g/255,b/255); hd=h*360
    if (r,g,b) in {(0x2A,0x16,0x00),(0x3A,0x1E,0x00)}: return None
    if 240<=hd<=352 or sat<.10:
        if l>=.78: return hx(38, l, .50 if sat>.05 else .32)
        if l<=.32: return hx(18, max(l,.13), .16)
        if sat>.42: return hx(218, .36, .50) if hd>=300 or hd<250 else hx(218, .29, .52)
        return hx(25, l, .10)
    if 140<=hd<=175 and sat>.45 and .3<l<.72: return hx(140, .30, .40)
    if 180<=hd<240 and sat>.35:
        if l>.9: return hx(38, .95, .45)
        if l>.78: return hx(218, .93, .45)
        if l<.3: return hx(18, max(l,.13), .16)
        return hx(218, .36, .50)
    return None
def hexsub(m):
    pre,h6=m.group(1),m.group(2)
    if len(h6)==3: r,g,b=[int(c*2,16) for c in h6]
    else: r,g,b=int(h6[0:2],16),int(h6[2:4],16),int(h6[4:6],16)
    f=ff(r,g,b); return m.group(0) if not f else pre+'#%02X%02X%02X'%f
def rgbasub(m):
    r,g,b=int(m.group(1)),int(m.group(2)),int(m.group(3)); f=ff(r,g,b)
    if not f: return m.group(0)
    a=m.group(4); return f'rgba({f[0]},{f[1]},{f[2]}{"," + a if a is not None else ""})'
s=re.sub(r'([:\s,(])#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})(?![0-9A-Za-z_-])', hexsub, s)
s=re.sub(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', rgbasub, s)

# ---------- type: Fraunces + Nunito Sans ----------
R('family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800','family=Fraunces:opsz,wght@9..144,600;9..144,800;9..144,900',1)
R('family=Figtree:wght@400;500;600;700','family=Nunito+Sans:wght@400;600;700;800',1)
s=s.replace('"Bricolage Grotesque"','"Fraunces"').replace("'Bricolage Grotesque'","'Fraunces'").replace('Figtree,','"Nunito Sans",').replace("Figtree","Nunito Sans")

# ---------- name and words ----------
pass  # brand stays Yofi
s=s.replace('👑','🏅').replace('💎','🪙')
s=re.sub(r"(?<=[ >`'\"])crown(s?)\b(?![\w(=:])", lambda m:'blue ribbon'+m.group(1), s)
s=re.sub(r"(?<=[ >`'\"])Crown(s?)\b(?![\w(=:])", lambda m:'Blue ribbon'+m.group(1), s)
s=re.sub(r"(?<=[\d}] )points?\b", lambda m:'star'+('s' if m.group(0).endswith('s') else ''), s)
s=re.sub(r"(?<=<b>)(\d+|\$\{[^}]+\}) points?\b", lambda m:m.group(0).replace('points','stars').replace('point','star'), s)
s=re.sub(r"(?<=[ >`'\"🏆])Points\b", 'Stars', s)
s=re.sub(r"(?<=[\d}] )gems?\b", lambda m:'coin'+('s' if m.group(0).endswith('s') else ''), s)
s=re.sub(r"\b(more|your|my|free|the|bonus|of|in|for|earn|Earn|with|Get|Use|use|spend|got) gems\b", lambda m:m.group(1)+' coins', s)
s=re.sub(r"(?<=[ >`'\"])Gems\b(?![\w(])", 'Coins', s)
s=re.sub(r"(?<=[ >`'\"])[Gg]em challenge", lambda m:('C' if m.group(0)[0]=='G' else 'c')+'oin challenge', s)
for a,b in [('>Studio<','>Touch-ups<'),('>Tournaments<','>Shows<'),('Start a friends group','Start a club'),('New friends group','New club'),('Create a friends group','Create a club'),
            ('friends group','club'),('Friends group','Club'),('Friends pot','Club pot'),('friends pot','club pot'),('friends blue ribbon','club blue ribbon'),('Friends blue ribbon','Club blue ribbon'),
            ('aria-selected="${fr}">Friends','aria-selected="${fr}">Clubs'),('data-ydt="friends" aria-selected="${tab === \'friends\'}">Friends','data-ydt="friends" aria-selected="${tab === \'friends\'}">Clubs'),
            ('Friends challenge','Club challenge')]:
    s=s.replace(a,b)
s=re.sub(r"(?<=[ >`'\"✨])Enhance\b(?![\w(])", 'Touch up', s)
s=re.sub(r"(?<=[ >`'\"])Tournaments\b(?![\w(])", 'Shows', s)

# categories: names that match her interests
for a,b in [("'Best Family'","'Best Family Moments'"),("'Best Home & Decor'","'Best Home & Handmade'"),("'Best Garden'","'Best Garden & Flowers'"),("'Best Baking & Cooking'","'Best Kitchen & Table'"),("'Best Travel'","'Best Travel & Cottage'")]:
    R(a,b,1)

# rosette replaces the crown graphic, a star replaces the gem
import math
pet=''.join(f'<circle cx="{24+15*math.cos(i*math.pi/7):.1f}" cy="{22+15*math.sin(i*math.pi/7):.1f}" r="6.2"/>' for i in range(14))
ROS=f'<svg class="crw-ic" viewBox="0 0 48 58" aria-hidden="true"><path d="M16 30 9 56l8-5 4 6 5-22z" fill="#9E2F2A"/><path d="M32 30l7 26-8-5-4 6-5-22z" fill="#7C2420"/><g fill="#2D4E86">{pet}</g><circle cx="24" cy="22" r="14" fill="#3D62A3"/><circle cx="24" cy="22" r="9" fill="#F4E7CC"/><circle cx="24" cy="22" r="9" fill="none" stroke="#C99A3B" stroke-width="1.5"/></svg>'
i=s.index("const CRW = '"); j=s.index("';", i)
s=s[:i]+"const CRW = '"+ROS+s[j:]
a=s.index('<g id="gemPath">'); b=s.index('</g>', a)+4
s=s[:a]+'<g id="gemPath"><circle cx="12" cy="12" r="9.5" fill="#E0A82E" stroke="#A8761A" stroke-width="1.2"/><circle cx="12" cy="12" r="6.3" fill="none" stroke="#F6D67A" stroke-width="1.4"/><path d="M12 8.2v7.6" stroke="#A8761A" stroke-width="1.8" stroke-linecap="round"/></g>'+s[b:]

# ---------- sign-up: age bracket, interest bubbles, her categories ----------
OB = r"""
const OB_AGES = ['25 to 34', '35 to 44', '45 to 54', '55 to 64', '65 and over'];
const OB_INT = [['Gardening', 3, 'fitness'], ['Grandkids', 3, 'selfie'], ['Baking', 2, 'food'], ['Travel', 3, 'travel'], ['Dogs', 2, 'pets'], ['Flowers', 2, 'fitness'], ['Cottage life', 2, 'travel'], ['Birds', 1, 'night'],
  ['Fall colours', 2, 'night'], ['Family', 2, 'selfie'], ['Quilting & crafts', 1, 'style'], ['Cats', 1, 'pets'], ['Home decor', 2, 'style'], ['Sunsets', 1, 'night'], ['Dinner parties', 1, 'food'], ['Winter scenes', 1, 'night'],
  ['Golf', 1, 'night'], ['Beach', 1, 'travel'], ['Weddings', 1, 'selfie'], ['Fishing', 1, 'night'], ['Vintage finds', 1, 'style']];
const OB_PRE = { '25 to 34': ['Travel', 'Dogs', 'Dinner parties', 'Home decor'], '35 to 44': ['Family', 'Travel', 'Baking', 'Dogs'], '45 to 54': ['Gardening', 'Family', 'Travel', 'Cottage life', 'Baking'], '55 to 64': ['Gardening', 'Grandkids', 'Travel', 'Flowers', 'Baking'], '65 and over': ['Grandkids', 'Gardening', 'Birds', 'Quilting & crafts'] };
function obRank() { const r = {}; (S.likes || []).forEach(n => { const x = OB_INT.find(i => i[0] === n); if (x) r[x[2]] = (r[x[2]] || 0) + 1; }); return r; }
function obSort() { if (!S.likes) return; const r = obRank(), o = ['selfie', 'style', 'fitness', 'pets', 'food', 'travel', 'night', 'any'];
  CATS8.sort((a, b) => (a === 'any') - (b === 'any') || (r[b] || 0) - (r[a] || 0) || o.indexOf(a) - o.indexOf(b)); }
function obAge(g) { const prog = n => `<div class="ob-prog">${[1, 2].map(i => `<i class="${i <= n ? 'on' : ''}"></i>`).join('')}</div>`;
  g.innerHTML = `<div class="ag-in ob">${prog(1)}<h1>Which age group are you in?</h1><p>We use this to suggest challenges you’ll enjoy. We never show it to other members.</p>
    <div class="ob-ages">${OB_AGES.map(a => `<button type="button" data-oa="${a}" aria-pressed="${a === S.ageBr}">${a}</button>`).join('')}</div><button class="btn block" id="obGo1" ${S.ageBr ? '' : 'disabled'}>Continue</button></div>`;
  g.querySelectorAll('[data-oa]').forEach(b => b.onclick = () => { S.ageBr = b.dataset.oa; S.likes0 = null; save(); obAge(g); });
  g.querySelector('#obGo1').onclick = () => obLikes(g); }
function obLikes(g, picked) { picked = picked || new Set(S.likes0 || OB_PRE[S.ageBr] || []);
  const draw = () => { g.innerHTML = `<div class="ag-in ob"><div class="ob-prog"><i class="on"></i><i class="on"></i></div><h1>What do you love to photograph?</h1><p>We’ve suggested a few for ${esc(S.ageBr || 'you')}. Tap to change.</p>
      <div class="ob-bub">${OB_INT.map(([n, z]) => `<button type="button" class="s${z}" data-ol="${esc(n)}" aria-pressed="${picked.has(n)}">${esc(n)}</button>`).join('')}</div>
      <button class="btn block" id="obGo2" ${picked.size ? '' : 'disabled'}>Start playing · ${picked.size} picked</button><button class="link ob-back" id="obB2">Back</button></div>`;
    g.querySelectorAll('[data-ol]').forEach(b => b.onclick = () => { const n = b.dataset.ol; picked.has(n) ? picked.delete(n) : picked.add(n); S.likes0 = [...picked]; draw(); });
    g.querySelector('#obB2').onclick = () => obAge(g);
    g.querySelector('#obGo2').onclick = () => { S.likes = [...picked]; S.obDone = 1; save(); obSort(); g.className = ''; setTimeout(() => g.remove(), 300); if (typeof renderGallery === 'function') renderGallery(); paintTop(); }; };
  draw(); }
function obDone(g) { obSort(); const r = obRank(), top = CATS8.filter(k => k !== 'any' && r[k]).slice(0, 5).concat('any'), L = lgS();
  const why = k => k === 'any' ? 'Open to every photo' : 'Because you picked ' + (S.likes || []).filter(n => (OB_INT.find(i => i[0] === n) || [])[2] === k).map(n => n.toLowerCase()).join(', ');
  g.innerHTML = `<div class="ag-in ob"><div class="ob-prog"><i class="on"></i><i class="on"></i><i class="on"></i></div><h1>Your challenges</h1><p>Picked from what you love. You can change them any time in your account.</p>
    <div class="ob-cats">${top.map(k => `<div><span class="ob-ic">${gi(k)}</span><span><b>${esc(crownName(k))}</b><small>${esc(why(k))}</small></span><em>${money(L.jp[k] || 0)}</em></div>`).join('')}</div>
    <button class="btn block" id="obGo3">Start playing</button></div>`;
  g.querySelector('#obGo3').onclick = () => { S.obDone = 1; save(); g.className = ''; setTimeout(() => g.remove(), 300); if (typeof renderGallery === 'function') renderGallery(); paintTop(); }; }
"""
R("// Yofi is adults only: confirm 18+ once, before anything else\nfunction ageGate() {\n  if (S.age18) return;",
  OB+"// Yofi is adults only: confirm age once, then age bracket and interests\nfunction ageGate() {\n  if (S.likes) { try { obSort(); if ($('#panes').dataset.at === 'gallery') renderGallery(); } catch (e) {} }\n  if (S.age18 && S.obDone) return; if (S.age18) { let g0 = document.getElementById('ageGate'); if (!g0) { g0 = document.createElement('div'); g0.id = 'ageGate'; document.body.appendChild(g0); } g0.className = 'on'; obAge(g0); return; }",1)
R("go.onclick = () => { if (!ok.checked) return; S.age18 = 1; S.adult = 1; save(); g.className = ''; setTimeout(() => g.remove(), 300); };",
  "go.onclick = () => { if (!ok.checked) return; S.age18 = 1; S.adult = 1; save(); obAge(g); };",1)
R("const CATS8 = ['selfie', 'style', 'fitness', 'pets', 'food', 'travel', 'night', 'any'];", "const CATS8 = ['selfie', 'style', 'fitness', 'pets', 'food', 'travel', 'night', 'any'];",1)

R("const CHAL = { Pets: 'Best Pet', Nature: 'Best Holiday', Wildlife: 'Best Anything', People: 'Best Selfie', Travel: 'Best Holiday', Food: 'Best Cooking', Cities: 'Best Night Out', Action: 'Best Gym' };",
  "const CHAL = { Pets: 'Best Pet', Nature: 'Best Nature & Seasons', Wildlife: 'Best Nature & Seasons', People: 'Best Family Moments', Travel: 'Best Travel & Cottage', Food: 'Best Kitchen & Table', Cities: 'Best Travel & Cottage', Action: 'Best Garden & Flowers' };",1)
s=s.replace("any: 'Anything', pets: 'Pet', selfie: 'Selfie', food: 'Cooking', travel: 'Holiday', night: 'Night out', fitness: 'Gym', style: 'Outfit' };","any: 'Anything', pets: 'Pet', selfie: 'Family', food: 'Kitchen', travel: 'Travel', night: 'Nature', fitness: 'Garden', style: 'Home' };")
CSS2 = """.btn,.bt-cta,.lgs-go,.kg2-go,.wr-go,.fcn-go,.bf-go,.dw-go,.lt-go,#crGo,#agGo,.ca-go,.obgo{background:#2D4E86!important;background-image:none!important;color:#fff!important;box-shadow:0 6px 16px rgba(45,78,134,.25)!important}
.wr-go.rev{background:#9E2F2A!important}.btn:disabled,#agGo:disabled{background:#A9B6CC!important;box-shadow:none!important}
.bt-sw button[aria-selected="true"],.yd-sw button[aria-selected="true"]{background:#2D4E86!important;background-image:none!important;color:#fff!important}
.seg button{font-size:.72rem!important;white-space:nowrap}#shell > .seg button[aria-pressed="true"],.seg button[aria-pressed="true"],.seg #segGallery[aria-pressed="true"],.seg #segStudio[aria-pressed="true"],.seg #segJudge[aria-pressed="true"]{background:#E3EAF5!important;background-image:none!important;color:#2D4E86!important;box-shadow:none!important}
.cr-crown{display:none!important}
.wr-pot{background:#fff!important;background-image:none!important;box-shadow:inset 0 0 0 2px #E4D6C1!important}.wr-pot small,.wr-pot p,.wr-pot span,.wr-pot strong,.wr-pot em{color:#5F534A!important}.wr-pot>b{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F!important}
"""

CSS = """.wm{font-family:Fraunces,Georgia,serif!important;font-weight:900!important;background:none!important;-webkit-text-fill-color:#9E2F2A!important;color:#9E2F2A!important;letter-spacing:-.02em!important}
.wm{font-size:1.7rem;white-space:nowrap}.ag-in .wm,.ca-hero .wm{font-size:2.6rem}
body{background:#FBF7F0}.crbox h2,.wr-h{font-family:Fraunces,Georgia,serif!important;letter-spacing:0!important}
.ca-hero{background:linear-gradient(180deg,#F6EBDA,#FBF7F0)!important}.ca-hero h1{color:#2B2320!important}.ca-hero p{color:#5F534A!important}.ca-cats span{background:#fff!important;box-shadow:inset 0 0 0 1.5px #E4D6C1!important;color:#3B2F28!important}.ca-q{color:#3B2F28!important}.ca-in{color:#2D4E86!important}
#ageGate{background:linear-gradient(180deg,#F6EBDA,#FBF7F0)!important;color:#2B2320!important;align-items:flex-start!important}
.ag-b{color:#2D4E86!important;box-shadow:inset 0 0 0 4px #2D4E86!important}.ag-in p{color:#5F534A!important}.ag-in p b,.ag-in h1{color:#2B2320!important}.ag-tk{background:#fff!important;box-shadow:inset 0 0 0 1.5px #E4D6C1!important;color:#2B2320}.ag-tk b{color:#2B2320!important}.ag-bx{box-shadow:inset 0 0 0 2px #2D4E86!important}.ag-tk input:checked+.ag-bx{background:#2D4E86!important}
.ob{padding-top:8px}.ob h1{font-size:1.7rem!important;text-align:left}.ob p{text-align:left}.ob-prog{display:flex;gap:6px;margin:0 0 18px}.ob-prog i{flex:1;height:6px;border-radius:9px;background:#EADCC6}.ob-prog i.on{background:#2D4E86}
.ob-ages{display:grid;gap:10px;margin:0 0 18px}.ob-ages button{font:800 1.08rem/1 "Nunito Sans",sans-serif;text-align:left;padding:17px 18px;border-radius:16px;border:0;background:#fff;color:#2B2320;box-shadow:inset 0 0 0 1.5px #E4D6C1;cursor:pointer;display:flex;justify-content:space-between}
.ob-ages button[aria-pressed="true"]{box-shadow:inset 0 0 0 2.5px #2D4E86;background:#EEF2F9}.ob-ages button[aria-pressed="true"]::after{content:"✓";color:#2D4E86}
.ob-bub{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;margin:4px 0 18px}.ob-bub button{border:0;border-radius:50%;display:grid;place-items:center;text-align:center;padding:6px;font:800 .8rem/1.15 "Nunito Sans",sans-serif;background:#F1E7D8;color:#2B2320;cursor:pointer;transition:transform .18s ease}
.ob-bub .s1{width:70px;height:70px}.ob-bub .s2{width:84px;height:84px;font-size:.86rem}.ob-bub .s3{width:100px;height:100px;font-size:.92rem}.ob-bub button[aria-pressed="true"]{background:#2D4E86;color:#fff;transform:scale(1.05)}
.ob-back{display:block;margin:12px auto 0;color:#5F534A!important}
.ob-cats{display:grid;gap:9px;margin:0 0 18px;text-align:left}.ob-cats>div{display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #E4D6C1}
.ob-ic svg{width:26px;height:26px;color:#9E2F2A;display:block}.ob-cats span:nth-child(2){flex:1;display:flex;flex-direction:column}.ob-cats b{font-size:1rem;color:#2B2320}.ob-cats small{font-size:.78rem;color:#6F6258}.ob-cats em{font:800 1.05rem Fraunces,serif;font-style:normal;color:#2F6B3F}
#ageGate .btn:disabled{opacity:.4}
"""
s=s.replace("</style>\n</head>", CSS+CSS2+"</style>\n</head>",1)
s=s.replace('<title>Rosette - Canada 50+ (Preview)</title>','<title>Rosette - Canada 50+ (Preview)</title>')
open(d+'yofi-ca50.html','w').write(s); print('ok')

import sys; sys.path.insert(0, d); from words import words
from cssfix import cssfix
s=open(d+'yofi-ca50.html').read(); s=words(s); s=cssfix(s); open(d+'yofi-ca50.html','w').write(s)
# ---------- age bracket 1 (25 to 34) keeps the original, younger feature names ----------
s=open(d+'yofi-ca50.html').read()
orig=open(d+'yofi-skill-base.html').read()
i=orig.index("const CRW = '"); j=orig.index("';", i); CRW_Y=orig[i+len("const CRW = '"):j].replace('<svg class="crw-ic"','<svg data-y="1" class="crw-ic"')
YJS = r"""
// Age bracket 1 (25 to 34) sees the younger names: Battle, Crown, Points, Gems, Friends, Studio, Tournaments, Judge
const CRW_Y = '__CRW__';
const YOUNG_W = [[/Today’s photo challenges/g, 'Battle for the crown'], [/\bHead-to-head\b/g, 'Crown battle'], [/\bBlue ribbons held\b/g, 'Crowns held'], [/\bBlue ribbon holder\b/g, 'Crown holder'],
  [/\bBlue ribbons\b/g, 'Crowns'], [/\bblue ribbons\b/g, 'crowns'], [/\bBlue ribbon\b/g, 'Crown'], [/\bblue ribbon\b/g, 'crown'], [/\bStars\b/g, 'Points'], [/\bstars\b/g, 'points'], [/\bstar\b/g, 'point'], [/\bCoins\b/g, 'Gems'], [/\bcoins\b/g, 'gems'], [/🪙/g, '💎'], [/🏅/g, '👑'],
  [/\bClubs\b/g, 'Friends'], [/\bClub pot\b/g, 'Friends pot'], [/\bclub pot\b/g, 'friends pot'], [/\bClub\b/g, 'Friends group'], [/\bclub\b/g, 'friends group'], [/\bTouch-ups\b/g, 'Studio'], [/\bTouch up\b/g, 'Enhance'], [/\btouch up\b/g, 'enhance'],
  [/\bShows\b/g, 'Tournaments'], [/^Vote$/, 'Judge'], [/^Compete$/, 'Battle'], [/\bCHALLENGE\b/g, 'BATTLE'], [/\bChallenges\b/g, 'Battles'], [/\bchallenges\b/g, 'battles'], [/\bChallenge\b/g, 'Battle'], [/\bchallenge\b/g, 'battle'], [/^Enter · /, 'Battle · ']];
const isYoung = () => S && S.ageBr === '25 to 34';
function youngPass() { if (!isYoung() || !document.body) return;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => { const p = n.parentElement; return !p || p.closest('script,style,textarea,input,.wm') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
  let n; while ((n = w.nextNode())) { const t = n.nodeValue; if (!t || !t.trim()) continue; let u = t; for (const [a, b] of YOUNG_W) { if (a.source.startsWith('^')) { if (a.test(u.trim())) u = u.replace(u.trim(), u.trim().replace(a, b)); } else u = u.replace(a, b); } if (u !== t) n.nodeValue = u; }
  document.querySelectorAll('svg.crw-ic:not([data-y])').forEach(el => { el.outerHTML = CRW_Y; }); }
let youngQ = 0; new MutationObserver(() => { if (!isYoung() || youngQ) return; youngQ = requestAnimationFrame(() => { youngQ = 0; youngPass(); }); }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
setTimeout(youngPass, 0);
""".replace('__CRW__', CRW_Y)
s=s.replace("function fcNotify() {", YJS+"function fcNotify() {",1)
open(d+'yofi-ca50.html','w').write(s); print('young ok')
