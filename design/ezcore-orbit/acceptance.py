"""Final acceptance for the finalized-brand canonical build (no edits after this)."""
import json, urllib.request
from playwright.sync_api import sync_playwright

served = urllib.request.urlopen('http://127.0.0.1:8770/index.html').read()
disk = open('/Users/jinultimate/Projects/Mobile/universal-emulator/design/ezcore-orbit/index.html','rb').read()
assert served == disk, 'served index.html differs from final build'

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1440,'height':1100})
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto('http://127.0.0.1:8770/', wait_until='networkidle')
    pg.reload(wait_until='networkidle')  # hard reload of the canonical URL

    checks = {}
    checks['wrapper_marker'] = pg.locator('body').get_attribute('data-brand-build') == 'ezcore-final-01'
    pg.wait_for_function('ready && typeof frame.contentWindow.orbitNavigate === "function"')
    ch = pg.frames[1]
    checks['app_marker'] = ch.locator('body').evaluate('x => x.dataset.brandBuild') == 'ezcore-final-01'
    checks['logo_in_masthead'] = pg.locator('.brand-lockup').count() == 1 and pg.locator('.brand-lockup').evaluate('x => x.naturalWidth > 0')
    checks['app_logo'] = ch.locator('.brand img').evaluate('x => x.complete && x.naturalWidth > 0')
    checks['accent_blue'] = ch.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--accent").trim().toLowerCase()') == '#007bff'
    checks['no_lime'] = ch.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--accent").trim().toLowerCase()') != '#c5f477'
    checks['tagline'] = 'Emulation shouldn’t be hard.' in pg.locator('h1').first.inner_text()
    ch.wait_for_function('Array.from(document.images).filter(x=>x.getClientRects().length).every(x=>x.complete && x.naturalWidth>0)')
    checks['artwork_decoded'] = True
    before = ch.locator('#selection h2').inner_text()
    ch.locator('#flow').click(position={'x': 40, 'y': 40})
    pg.keyboard.press('ArrowRight')
    ch.wait_for_timeout(700)
    checks['interaction'] = ch.locator('#selection h2').inner_text() != before
    checks['console_errors'] = errors
    b.close()
    ok = all(v for k, v in checks.items() if k != 'console_errors') and not checks['console_errors']
    print(json.dumps({'served_bytes_match': True, 'checks': checks, 'accepted': ok}, indent=2))
    raise SystemExit(0 if ok else 1)
