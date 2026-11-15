# Fall Fair colour clean-up across every CSS rule (and inline style strings)
import re, colorsys
def lum(h):
    h=h.lstrip('#'); h=''.join(c*2 for c in h) if len(h)==3 else h
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]; hh,l,s=colorsys.rgb_to_hls(r,g,b); return hh*360,l,s
def isblue(h): hd,l,s=lum(h); return 200<=hd<=235 and s>.3 and l<.5
def isdarksat(h): hd,l,s=lum(h); return s>.28 and l<.42
def isdark(h): hd,l,s=lum(h); return l<.32
HEX=r'#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b'
def fix_rule(sel, body):
    decl=body
    bg=re.search(r'background(?:-color|-image)?\s*:([^;]*)', decl)
    if bg:
        v=bg.group(1)
        hs=re.findall(HEX, v)
        # gradients that end up half ribbon-blue, half muddy grey/brown -> solid ribbon blue
        if 'gradient' in v and any(isblue(h) for h in hs) and any(not isblue(h) for h in hs if lum(h)[1]<.6):
            decl=decl.replace(bg.group(0), 'background:#2D4E86'+(' !important' if '!important' in v else '')); v='#2D4E86'; hs=['#2D4E86']
        # glow gradients that mix a very dark warm stop with a pale one (left over from the dark theme) -> warm light fill
        if 'gradient' in v and hs and any(lum(h)[1]<.4 and not isblue(h) for h in hs) and any(lum(h)[1]>.85 for h in hs):
            decl=decl.replace(bg.group(0), 'background:#FFF8EA'+(' !important' if '!important' in v else '')); v='#FFF8EA'; hs=['#FFF8EA']
        # translucent dark washes that were white glass on the old dark theme -> soft white
        def wash(m):
            r,g,b,a=int(m.group(1)),int(m.group(2)),int(m.group(3)),float(m.group(4))
            return 'rgba(255,255,255,.72)' if (r+g+b)/3<110 and a<=.6 else m.group(0)
        nv=re.sub(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', wash, v)
        if nv!=v and 'gradient' not in v: decl=decl.replace(v, nv); v=nv
        # dark coloured fill with dark text -> white text
        if hs and all(isdarksat(h) or isdark(h) for h in hs if lum(h)[1]<.5) and any(isdarksat(h) for h in hs) and not any(lum(h)[1]>.7 for h in hs):
            col=re.search(r'(?<![-\w])color\s*:\s*(#[0-9A-Fa-f]{3,6})', decl)
            if col and lum(col.group(1))[1]<.55: decl=decl.replace(col.group(0), 'color:#FFFFFF')
            elif not col and 'svg' not in sel and '::' not in sel: decl=decl.rstrip(';')+';color:#FFFFFF'
            return decl
        light_bg = hs and all(lum(h)[1]>.75 for h in hs)
    else: light_bg = False
    # hairline outlines so pale they vanish on cream -> visible kraft line
    def line(m):
        hd,l,sa=lum(m.group(2)); return m.group(1)+('#CDBB98' if l>.86 and l<.97 else m.group(2))
    decl=re.sub(r'(inset\s+0\s+0\s+0\s+[\d.]+px\s+)(#[0-9A-Fa-f]{6})', line, decl)
    col=re.search(r'(?<![-\w])color\s*:\s*(#[0-9A-Fa-f]{3,6})', decl)
    if col:
        hd,l,sa=lum(col.group(1))
        if 30<=hd<=55 and sa>.55 and l>.45: decl=decl.replace(col.group(0), 'color:#94650C')   # gold text on cream -> deep gold
        elif light_bg and l>.72: decl=decl.replace(col.group(0), 'color:#2B2320')              # pale text on pale fill -> ink
    return decl
def cssfix(s):
    def style(m):
        css=m.group(1)
        css=re.sub(r'([^{}]+)\{([^{}]*)\}', lambda r: r.group(1)+'{'+fix_rule(r.group(1), r.group(2))+'}', css)
        return '<style>'+css+'</style>'
    s=re.sub(r'<style>(.*?)</style>', style, s, flags=re.S)
    return s
