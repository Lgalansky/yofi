# landing page, part 2: how it works, reviews carousel, quick answers, closing CTA, footer
import base64, re
d='/tmp/claude-0/-home-user-yofi/c69be753-0b48-5242-b029-4f4be89f4655/scratchpad/'
s=open(d+'yofi-ca50.html').read()
U=lambda k:'data:image/jpeg;base64,'+base64.b64encode(open(d+'landimg/'+k+'.jpg','rb').read()).decode()
IMG={k:U(k) for k in ['garden','baking','seasons','pets','home','family','win2']}
ic=lambda p:f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
PHOTO='<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="15.5" cy="9" r="1.8"/><path d="M3.5 18l6-6 4.5 4.5 2.5-2.5 4 4"/>'
SPARK='<path d="M10 3l1.6 4.4L16 9l-4.4 1.6L10 15l-1.6-4.4L4 9l4.4-1.6z"/><path d="M18 14l.8 2.2L21 17l-2.2.8L18 20l-.8-2.2L15 17l2.2-.8z"/>'
TROPHY='<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4v1.5A3.5 3.5 0 0 0 7.5 11M17 6h3v1.5a3.5 3.5 0 0 1-3.5 3.5"/><path d="M12 14v4M8 21h8M9.5 18h5"/>'
steps=''.join(f'<div class="cs-st"><span class="cs-ic">{ic(p)}</span><span><b>{t}</b><small>{x}</small></span></div>' for p,t,x in [(PHOTO,'Choose your photo','Get your first AI score free.'),(SPARK,'Make it shine','Enhance your photo for competitions.'),(TROPHY,'Compete for cash','Enter competitions and aim for a prize.')])
REV=[('garden','I won $120 with a photo of my tulips. I check in every morning with my coffee.','Linda, 54 · Halifax'),
     ('baking','My strawberry cake took the Baking blue ribbon. The grandkids think I’m famous.','Margaret, 61 · Kelowna'),
     ('seasons','Fall colours at the cottage won me $85. It’s the nicest part of my day.','Dianne, 58 · Muskoka'),
     ('pets','I joined for fun with photos of Max. Now half my book club plays.','Carol, 66 · Victoria'),
     ('home','I love seeing other people’s gardens and kitchens. Voting is so relaxing.','Susan, 49 · Ottawa')]
revs=''.join(f'<figure class="cs-rv"><img src="{IMG[k]}" alt=""><figcaption><q>{q}</q><small>{w}</small></figcaption></figure>' for k,q,w in REV)
FAQ=[('Can I use photos from my phone?','Yes. Any photo in your phone’s gallery works. We help you crop it to fit, and your first score is free.'),
     ('How are winners chosen?','Members vote. Two photos are shown side by side and people tap their favourite. The photo with the most votes wins.'),
     ('How do entries and cash prizes work?','Each entry is $1 and most of it goes into that day’s prize pot. Collect 5 stars in a category by midnight to share the pot. Prizes are paid by Interac e-Transfer.'),
     ('Is it safe to play?','Yofi is for adults of legal age in your province. Your photos are only shown for voting, and you can delete them any time.')]
faq=''.join(f'<details class="cs-q"><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q,a in FAQ)
MORE=f'''<div class="cs"><h2>From camera roll to cash</h2><div class="cs-steps">{steps}</div></div>
        <div class="cs"><h2>A little everyday joy</h2><div class="cs-car" id="csCar">{revs}</div><div class="cs-dots" id="csDots">{''.join('<i></i>' for _ in REV)}</div></div>
        <div class="cs"><h2>A few quick answers</h2>{faq}</div>
        <div class="cs-end"><h2>Your next favourite photo is already on your phone.</h2><button class="btn block ca-any" onclick="window.__preCat=null;document.getElementById(\'file\').click()">{ic(PHOTO)}Choose your photo</button><p>Your first photo score is free.</p></div>
        <footer class="cs-ft"><span class="wm">Yofi</span><nav><button onclick="csInfo(\'help\')">Help</button><span>·</span><button onclick="csInfo(\'terms\')">Terms</button><span>·</span><button onclick="csInfo(\'privacy\')">Privacy</button></nav></footer>
'''
a='</div>\n      <img class="hxp-img"'; assert s.count(a)==1; s=s.replace(a, MORE+a,1)
# winners: four, swipe sideways
WIN=[('pets','$250','@pawprincess'),('win2','$200','@catlover22'),('garden','$120','@linda.blooms'),('baking','$95','@nana_bakes')]
i=s.index('<div class="ca-wg">'); j=s.index('</div></div></div>', i)
s=s[:i]+'<div class="ca-wg">'+''.join(f'<div><img src="{IMG[k]}" alt=""><b>{m}</b><span>{h}</span></div>' for k,m,h in WIN)+s[j+len('</div>'):]
JS=r"""
// landing: review dots follow the swipe; Help / Terms / Privacy open a short note
function csInfo(k) { const T = { help: ['Help', 'Questions about your account, entries or prizes? Email help@yofi.ca and a real person replies within a day.'], terms: ['Terms', 'You must be of legal age in your province. Entries are $1. Prize pots pay at midnight by Interac e-Transfer. Full terms will be published before launch.'], privacy: ['Privacy', 'Your photos are only shown for voting. We never sell your data, and you can delete your photos and account at any time.'] }[k];
  openSheet(`<div class="cwn"><h2>${T[0]}</h2><p class="sub">${T[1]}</p><button class="btn block" data-shclose>OK</button></div>`); }
window.csInfo = csInfo;
setTimeout(() => { const c = document.getElementById('csCar'), d = document.getElementById('csDots'); if (!c || !d) return;
  const paint = () => { const n = Math.round(c.scrollLeft / (c.firstElementChild.offsetWidth + 12)); [...d.children].forEach((x, i) => x.className = i === n ? 'on' : ''); };
  c.addEventListener('scroll', () => requestAnimationFrame(paint), { passive: true }); paint();
  [...d.children].forEach((x, i) => x.onclick = () => c.scrollTo({ left: i * (c.firstElementChild.offsetWidth + 12), behavior: 'smooth' })); }, 0);
"""
s=s.replace("function fcNotify() {", JS+"function fcNotify() {",1)
CSS=""":root,:root[data-theme="light"],:root[data-theme="dark"]{--violet:#24406F!important;--pink:#2D4E86!important;--gem:#2D4E86!important;--gold:#B8862A!important}
.gembig b{background:none!important;-webkit-text-fill-color:#2D4E86!important;color:#2D4E86!important}.gembig span{color:#2B2320!important}.gembig{box-shadow:0 20px 50px -12px rgba(43,35,32,.45),inset 0 0 0 2px #E4D6C1!important}
.hp-d i{background:#FFFFFF!important;box-shadow:inset 0 0 0 2px #2D4E86!important}.hp-d i.on{background:#D9A441!important;box-shadow:inset 0 0 0 2px #94650C!important}.stopc.crb.hp.zero0{opacity:1!important;box-shadow:inset 0 0 0 1.5px #C9B590!important}
.stk-steps>i:not(.on):not(.m){background:#D9C6A5!important}.stk-steps>i.m:not(.on):not(.m10){background:#FFFFFF!important;box-shadow:inset 0 0 0 2px #C99A3B!important}
.dsk-dy>i:not(.on){background:#FFFFFF!important;box-shadow:inset 0 0 0 2px #B9A47E!important}#judge .d>i:not(.on){background:#D9C6A5!important}#judge .d>i.on{background:#2F6B3F!important}
.lk-box.mine b,.lk-box.mine small{color:#FFFFFF!important}.lk-box.mine b{color:#FFD873!important}
.lgs-jp small{color:#2F6B3F!important}.lgs-hd em{color:#7A6650!important}.f2-chg{color:#2D4E86!important}
.tsh-tix{background:#2F6B3F!important;color:#FFFFFF!important}.tsh-tix b{color:#FFFFFF!important}.tp-stub span{color:#5A3E00!important}
.wr.l .wr-h{color:#9E2F2A!important;text-shadow:none!important}.ch-rar.r-common{background:#6F6258!important;color:#fff!important}.ch-rar.r-epic{background:#9E2F2A!important;color:#fff!important}
.fixbtn .gpill,.fixbtn.quiet .gpill{background:#FFFFFF!important;color:#2D4E86!important;box-shadow:none!important}.gpill.need{color:#9E2F2A!important}
.bar.low span:first-child,.bar.low span.v{color:#2B2320!important}.bar.low{background:#EEF2F9!important}.kg2-pot.gbz small{color:#2D4E86!important}
.ca-wg{display:flex!important;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -22px;padding:0 22px 6px;scrollbar-width:none}.ca-wg::-webkit-scrollbar{display:none}.ca-wg>div{flex:0 0 44%;scroll-snap-align:start}
.cs{margin-top:26px;padding-top:22px;border-top:1px solid #E4D6C1;text-align:left}.cs h2{margin:0 0 14px;text-align:center;font:900 1.65rem/1.15 Fraunces,Georgia,serif;color:#2B2320}
.cs-st{display:flex;align-items:center;gap:16px;padding:14px 4px;border-top:1px solid #EADCC6}.cs-st:first-child{border-top:0}.cs-ic svg{width:40px;height:40px;color:#2D4E86;display:block}.cs-st b{display:block;font:800 1.2rem Fraunces,Georgia,serif;color:#2B2320}.cs-st small{font-size:.98rem;color:#5F534A}
.cs-car{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -22px;padding:2px 22px 8px;scrollbar-width:none}.cs-car::-webkit-scrollbar{display:none}
.cs-rv{flex:0 0 86%;scroll-snap-align:center;margin:0;display:flex;gap:14px;align-items:center;padding:12px;border-radius:18px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}
.cs-rv img{flex:0 0 42%;width:42%;aspect-ratio:1.1;object-fit:cover;border-radius:12px}.cs-rv q{display:block;font:800 1.02rem/1.3 Fraunces,Georgia,serif;color:#2B2320;quotes:"“" "”"}.cs-rv small{display:block;margin-top:8px;color:#6F6258;font-size:.9rem}
.cs-dots{display:flex;justify-content:center;gap:8px;margin-top:8px}.cs-dots i{width:8px;height:8px;border-radius:50%;background:#E4D6C1;cursor:pointer}.cs-dots i.on{background:#2D4E86;width:22px;border-radius:9px}
.cs-q{margin:0 0 10px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}.cs-q summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 16px;font:800 1.02rem Fraunces,Georgia,serif;color:#2B2320;cursor:pointer}.cs-q summary::-webkit-details-marker{display:none}
.cs-q summary i{position:relative;flex:none;width:16px;height:16px}.cs-q summary i::before,.cs-q summary i::after{content:"";position:absolute;left:0;top:7px;width:16px;height:2.5px;border-radius:2px;background:#2D4E86}.cs-q summary i::after{transform:rotate(90deg);transition:transform .2s}.cs-q[open] summary i::after{transform:rotate(0)}
.cs-q p{margin:0!important;padding:0 16px 14px;text-align:left;font-size:.98rem!important;color:#5F534A!important}
.ca-any svg{width:26px!important;height:26px!important;flex:none}.ca-wg,.cs-car{margin:0!important;padding-left:0!important;padding-right:0!important}.cs-rv{scroll-snap-align:start!important}.cs-end{margin-top:22px;padding:22px 18px;border-radius:20px;background:#E3EAF5;text-align:center}.cs-end h2{margin:0 0 14px;font:900 1.55rem/1.15 Fraunces,Georgia,serif;color:#2B2320}.cs-end p{margin:10px 0 0!important}
.cs-ft{margin:22px 0 4px;text-align:center}.cs-ft .wm{font-size:1.6rem}.cs-ft nav{display:flex;justify-content:center;gap:10px;margin-top:4px;color:#6F6258}.cs-ft button{border:0;background:none;font:600 .98rem "Nunito Sans",sans-serif;color:#5F534A;cursor:pointer;padding:4px}
@media (prefers-reduced-motion:reduce){.cs-q summary i::after{transition:none}}
"""
s=s.replace("</style>\n</head>", CSS+"</style>\n</head>",1)
open(d+'yofi-ca50.html','w').write(s); print('more ok')

# ---------- tickets sheet: with no tickets, explain how to earn one instead of listing tournaments ----------
s=open(d+'yofi-ca50.html').read()
a="function useTickets() {\n  const n = S.cashTix || 0, SL = tSlots().filter(t => !t.gem).slice(0, 4);"
assert s.count(a)==1
s=s.replace(a, a+r"""
  if (!n) { const c = Math.min(S.combo || 0, 10);
    openSheet(`<div class="ug ut0"><h2>Free entries</h2><p class="sub">You don’t have a free entry yet. Each one enters a <b>$1 tournament</b> free.</p>
      <div class="ut0-how"><span class="ut0-i">🧰</span><div><b>Pick the winner 10 times in a row</b><small>On the Vote page. The big chest opens and gives you free entries.</small></div></div>
      <div class="ut0-bar"><i style="width:${c * 10}%"></i></div><p class="ut0-n">${c} of 10 in a row</p>
      <button class="btn block" id="ut0Go">Keep voting</button><button class="link ug-buy" id="utAll">See tournaments</button></div>`);
    $('#ut0Go').onclick = () => { closeSheet(); go('judge'); }; $('#utAll').onclick = () => { closeSheet(); openComps(null); }; return; }""",1)
s=s.replace("</style>\n</head>",""".ug-r em.claim{background:#2F6B3F!important;color:#FFFFFF!important}
.ut0-how{display:flex;gap:14px;align-items:center;margin:14px 0 12px;padding:14px;border-radius:16px;background:#fff;box-shadow:inset 0 0 0 1.5px #CDBB98}.ut0-i{font-size:2rem}.ut0-how b{display:block;font:800 1.05rem Fraunces,Georgia,serif;color:#2B2320}.ut0-how small{color:#5F534A;font-size:.92rem}
.ut0-bar{height:10px;border-radius:9px;background:#EADCC6;overflow:hidden}.ut0-bar i{display:block;height:100%;background:#D9A441;border-radius:9px}.ut0-n{margin:6px 0 16px;font-weight:700;color:#5F534A;text-align:center}
</style>
</head>""",1)
open(d+'yofi-ca50.html','w').write(s); print('tix ok')
