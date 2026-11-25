# Builds Yofi - Skill 2 (index.html on the skill-2 branch) from app.src.html.
# Photos come from the SEED photos in the Skill app on main (git show main:index.html).
# Usage (repo root, on skill-2): python3 build-skill2/build.py
import re, json, subprocess, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'build-skill2' / 'app.src.html').read_text(encoding='utf-8')
main = subprocess.run(['git', 'show', 'main:index.html'], cwd=root, capture_output=True, text=True, check=True).stdout
seed = json.loads(re.search(r'const SEED = (\[.*?\]);', main, re.S).group(1))
photos = {x['id']: x['src'] for x in seed if x.get('src')}
(root / 'index.html').write_text(src.replace('__PHOTOS__', json.dumps(photos)), encoding='utf-8')
print('built', len(photos), 'photos')
