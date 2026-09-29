import re
from pathlib import Path
root = Path(r'C:\PRODENTIM\prodentim-bridge')
s = (root / 'index.html').read_text(encoding='utf-8')
print('chars', len(s))
print('hoplink count', s.count('hop.clickbank.net'))
print('cta ids', re.findall(r'id="(cta[^"]*)"', s))
refs = re.findall(r'(?:src|href)="(assets/[^"]+)"', s)
print('asset refs', set(refs))
for a in sorted(set(refs)) + ['privacy.html']:
    p = root / a
    print(' ', a, p.exists(), p.stat().st_size if p.exists() else '-')
# tag balance sanity
for t in ['section', 'details', 'ul', 'ol', 'div', 'a']:
    o = len(re.findall(r'<%s\b' % t, s))
    c = len(re.findall(r'</%s>' % t, s))
    print(f'{t}: open={o} close={c} {"OK" if o == c else "MISMATCH"}')
