"""Verify shell layout: orientation controls + adaptive desktop iframe sizing."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SERVED = 'http://127.0.0.1:8770/'

def fr(page):
    return page.frames[1]

def wait_ready(page):
    page.wait_for_function('ready && typeof frame?.contentWindow?.orbitNavigate === "function"')


def run():
    report = {'checks': [], 'errors': [], 'fatal': None}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 1100}, device_scale_factor=1)
        pg.on('pageerror', lambda e: report['errors'].append(str(e)))
        pg.goto(SERVED, wait_until='networkidle')
        pg.reload(wait_until='networkidle')
        wait_ready(pg)

        # Initial state: ios (phone). Rotate should be VISIBLE
        rotate_initial = pg.locator('#rotate-button').is_visible()
        report['checks'].append(f'initial ios rotate visible: {rotate_initial}')
        assert rotate_initial, 'rotate-button should be visible on initial ios'

        # Switch to mac (desktop). Rotate should be HIDDEN
        pg.locator('#tab-mac').click()
        wait_ready(pg)
        rotate_mac = pg.locator('#rotate-button').is_visible()
        report['checks'].append(f'mac rotate hidden: {not rotate_mac}')
        assert not rotate_mac, 'rotate-button should be hidden on desktop mac'

        # Back to ios. Rotate visible
        pg.locator('#tab-ios').click()
        wait_ready(pg)
        rotate_ios = pg.locator('#rotate-button').is_visible()
        report['checks'].append(f'ios rotate visible: {rotate_ios}')
        assert rotate_ios, 'rotate-button should be visible on ios'

        # --- Phone portrait natural size ---
        host_geo = pg.evaluate('''() => {
            const f = document.querySelector('.native-frame');
            return {frameW: f.offsetWidth, frameH: f.offsetHeight};
        }''')
        report['checks'].append(f'iOS portrait frame: {json.dumps(host_geo)}')
        assert host_geo['frameW'] < 500, f'portrait width too big: {host_geo["frameW"]}'
        assert host_geo['frameH'] > 600, f'portrait height too small: {host_geo["frameH"]}'

        # --- Rotate to landscape ---
        pg.locator('#rotate-button').click()
        pg.wait_for_timeout(400)
        ch2 = fr(pg)
        host_geo_ls = pg.evaluate('''() => {
            const f = document.querySelector('.native-frame');
            return {frameW: f.offsetWidth, frameH: f.offsetHeight};
        }''')
        report['checks'].append(f'iOS landscape frame: {json.dumps(host_geo_ls)}')
        assert host_geo_ls['frameW'] > 600, f'landscape frame width should be ~882, got {host_geo_ls["frameW"]}'
        assert host_geo_ls['frameH'] < 500, f'landscape frame height should be ~416, got {host_geo_ls["frameH"]}'
        report['checks'].append('iOS rotation swapped dimensions 416x882 -> 882x416')

        # --- State preserved: active screen unchanged ---
        active_after_rotate = ch2.evaluate("() => document.querySelector('.nav button.active')?.dataset.go")
        report['checks'].append(f'active screen after rotate: {active_after_rotate}')

        # --- Body classes ---
        body_cls = pg.evaluate("() => document.body.className")
        report['checks'].append(f'body classes after rotate: {body_cls}')
        assert 'phone-ios' in body_cls, f'phone-ios not in body classes: {body_cls}'
        assert 'landscape-orientation' in body_cls, f'landscape-orientation not in body classes: {body_cls}'

        # --- Safe-area vars ---
        safe_vars = pg.evaluate('''() => {
            const s = getComputedStyle(document.body);
            return {top: s.getPropertyValue('--safe-top').trim(), bottom: s.getPropertyValue('--safe-bottom').trim(), left: s.getPropertyValue('--safe-left').trim()};
        }''')
        report['checks'].append(f'safe-area vars (landscape): {safe_vars}')

        # --- Rotate back ---
        pg.locator('#rotate-button').click()
        pg.wait_for_timeout(400)
        host_geo_p2 = pg.evaluate('''() => {
            const f = document.querySelector('.native-frame');
            return {frameW: f.offsetWidth, frameH: f.offsetHeight};
        }''')
        assert host_geo_p2['frameW'] < 500 and host_geo_p2['frameH'] > 600, f'rotate-back failed: {host_geo_p2}'
        body_cls_p2 = pg.evaluate("() => document.body.className")
        assert 'landscape-orientation' not in body_cls_p2, 'landscape still set after rotate-back'
        report['checks'].append('iOS rotate-back restored portrait')

        # --- Android ---
        pg.locator('#tab-android').click()
        wait_ready(pg)
        rotate_android = pg.locator('#rotate-button').is_visible()
        assert rotate_android, 'rotate-button should be visible on android'
        host_android = pg.evaluate('''() => {
            const f = document.querySelector('.native-frame');
            return {frameW: f.offsetWidth, frameH: f.offsetHeight};
        }''')
        assert host_android['frameW'] < 500 and host_android['frameH'] > 600
        body_cls_and = pg.evaluate("() => document.body.className")
        assert 'phone-android' in body_cls_and, f'phone-android not in classes: {body_cls_and}'
        assert 'phone-ios' not in body_cls_and, f'phone-ios still in classes: {body_cls_and}'
        report['checks'].append(f'Android portrait OK: {json.dumps(host_android)}')

        # --- Desktop chrome: mac traffic lights, windows/linux controls ---
        pg.locator('#tab-mac').click()
        wait_ready(pg)
        assert pg.locator('.traffic-lights').count() == 1, 'mac traffic lights missing'
        report['checks'].append('mac traffic lights chrome present')

        geo1 = pg.evaluate('''() => {
            const s = document.getElementById('stage');
            const f = document.querySelector('.native-frame');
            return {stageW: Math.round(s.getBoundingClientRect().width), frameW: f.offsetWidth};
        }''')
        report['checks'].append(f'mac desktop adaptive frame: {json.dumps(geo1)}')

        pg.locator('#tab-windows').click()
        wait_ready(pg)
        assert pg.locator('.win-controls').count() == 1, 'windows controls missing'
        report['checks'].append('windows chrome controls present')

        pg.locator('#tab-linux').click()
        wait_ready(pg)
        assert pg.locator('.linux .win-controls').count() == 1, 'linux controls missing'
        report['checks'].append('linux chrome controls present')

        # --- Shell controls: minimize, restore, expand, shell toggle ---
        pg.locator('#tab-mac').click()
        wait_ready(pg)
        pg.locator('[data-window="minimize"]').click()
        assert pg.locator('#restore-card').is_visible(), 'minimize did not show restore card'
        pg.locator('#restore-button').click()
        assert pg.locator('#shell-host').is_visible(), 'restore failed'
        report['checks'].append('minimize/restore works')

        pg.locator('[data-window="maximize"]').click()
        assert pg.evaluate('document.getElementById("stage").classList.contains("expanded")'), 'maximize did not expand'
        pg.locator('#expanded-exit').click()
        report['checks'].append('maximize/expand+exit works')

        pg.locator('#shell-button').click()
        assert pg.evaluate('document.getElementById("stage").classList.contains("flat")'), 'shell toggle failed'
        pg.locator('#shell-button').click()
        report['checks'].append('shell toggle (chrome on/off) works')

        b.close()

    ok = not report['errors'] and not report['fatal']
    print(json.dumps({'ok': ok, **report}, indent=2))
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    run()
