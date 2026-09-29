from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(r'C:\PRODENTIM\prodentim-bridge')
url = (root / 'index.html').as_uri()
out = root / 'tools' / '_shots'
out.mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [('mobile', 375, 667), ('desktop', 1280, 900)]:
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('requestfailed', lambda r: errs.append('FAILED ' + r.url))
        pg.goto(url, wait_until='networkidle')
        pg.screenshot(path=str(out / f'{name}_fold.png'))
        pg.screenshot(path=str(out / f'{name}_full.png'), full_page=True)
        box = pg.evaluate("""() => {
            const r = document.getElementById('cta-principal').getBoundingClientRect();
            return {top: Math.round(r.top), bottom: Math.round(r.bottom)};
        }""")
        print(name, 'primary CTA rect at scroll 0:', box)
        # sticky bar visible after scrolling past hero
        pg.evaluate('window.scrollTo(0, 900)')
        pg.wait_for_timeout(500)
        on = pg.evaluate("document.getElementById('stickyBar').classList.contains('on')")
        print(name, 'sticky_on=', on, 'errors=', errs)
        pg.close()
    b.close()
print('done')
