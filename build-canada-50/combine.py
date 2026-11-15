# Combined Yofi Skill: one app, two looks.
#   ages 25 to 44 (and anyone who hasn't picked yet) -> original dark Yofi look and words  (html.yg)
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
"""
# one style block in place of the Fall Fair ones
first=s.index('<style>'); s=re.sub(r'<style>.*?</style>\s*', '', s, flags=re.S)
s=s[:first]+'<style>'+Y+'\n'+F+EXTRA+'</style>\n'+s[first:]

# theme class before first paint: saved bracket decides; no bracket yet -> original look
s=s.replace('<html lang="en" data-theme="light">','<html lang="en" class="yg">',1)
s=s.replace('<body>','<body>\n<script>try{var _b=(JSON.parse(localStorage.getItem("yofi.proto.v1")||"{}")||{}).ageBr;if(_b&&_b!=="25 to 34"&&_b!=="35 to 44"){document.documentElement.classList.remove("yg");document.documentElement.setAttribute("data-theme","light")}}catch(e){}</script>',1)

def R(a,b,n=1):
    global s; assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# younger words for 25 to 44, and keep the theme class in step with the bracket
R("const isYoung = () => S && S.ageBr === '25 to 34';",
  "const isYoung = () => S && (!S.ageBr || S.ageBr === '25 to 34' || S.ageBr === '35 to 44');\nfunction setLook() { const y = isYoung(), r = document.documentElement; r.classList.toggle('yg', y); if (y) r.removeAttribute('data-theme'); else r.setAttribute('data-theme', 'light'); }")
R("S.ageBr = b.dataset.oa; S.likes0 = null; save(); obAge(g);","S.ageBr = b.dataset.oa; S.likes0 = null; save(); setLook(); obAge(g);")
R("S.likes = [...picked]; S.obDone = 1; save();","S.likes = [...picked]; S.obDone = 1; save(); setLook(); youngPass();")
s=s.replace("setTimeout(youngPass, 0);","setTimeout(() => { setLook(); youngPass(); }, 0);",1)

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
s=s.replace("[/🏅/g, '👑'],","[/🏅/g, '👑'], [/🟡/g, '💎'],",1)
# Skill save and name
R("const KEY = 'yofi.ca50.v1'","const KEY = 'yofi.proto.v1'")
s=re.sub(r'<title>[^<]*</title>','<title>Yofi - Skill (Preview)</title>',s,1)
open(d+'yofi-preview.html','w').write(s)
print('combined', len(s)//1024, 'KB; css y', len(Y)//1024, 'KB f', len(F)//1024, 'KB')
