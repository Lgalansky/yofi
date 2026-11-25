# Pets sample photos (Skill preview): replaces the six tiny Pets thumbnails in SEED with the owner's own
# dog photos from build-skill/samples/pets/<id>.jpg (600 x 800, the 3:4 upright shape uploads use).
# Photos with people in them were left out; the collar tag (name and phone number) on "Stare-down" is blurred.
# Usage: python3 build-skill/samples.py [in.html] [out.html]
import sys, re, json, base64, pathlib
src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'; p = sys.argv[2] if len(sys.argv) > 2 else src
s = open(src, encoding='utf-8').read()
d = pathlib.Path(__file__).resolve().parent / 'samples' / 'pets'
m = re.search(r'const SEED = (\[.*?\]);', s, re.S); seed = json.loads(m.group(1))
TITLES = {'shades': 'Sunbather', 'kitten': 'Puppy eyes'}
n = 0
for x in seed:
    f = d / (x['id'] + '.jpg')
    if x['cat'] == 'Pets' and f.exists():
        x['src'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read_bytes()).decode()
        if x['id'] in TITLES: x['title'] = TITLES[x['id']]
        n += 1
s = s[:m.start(1)] + json.dumps(seed, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
open(p, 'w', encoding='utf-8').write(s); print('samples ok', n)
