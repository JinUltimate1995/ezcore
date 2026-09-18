"""Regression contract for the unbranded header and responsive game dock."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).parent
OUT = ROOT / 'verification' / 'game-dock'
OUT.mkdir(parents=True, exist_ok=True)
report = {'states': [], 'errors': []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    page.on('pageerror', lambda e: report['errors'].append(str(e)))
    page.goto('http://127.0.0.1:8770/', wait_until='networkidle')
    page.reload(wait_until='networkidle')
    page.wait_for_function('ready')
    for platform in ['ios', 'android', 'mac', 'windows', 'linux', 'web']:
        page.locator('#tab-' + platform).click()
        page.wait_for_function('ready')
        for orientation in (['portrait', 'landscape'] if platform in ['ios', 'android'] else ['desktop']):
            if orientation == 'landscape':
                page.locator('#rotate-button').click()
            ch = page.frames[1]
            ch.wait_for_timeout(500)
            assert ch.locator('.topbar .brand').count() == 0, 'Remove header brand, not merely hide it'
            assert 'ezcore' not in ch.locator('.topbar').inner_text().lower()
            assert ch.locator('#selection').get_attribute('data-component') == 'game-dock'
            if platform in ['ios', 'android']:
                assert ch.locator('.footer').is_hidden(), 'No keyboard hints on phones in either orientation'
                assert ch.locator('.play-key').count() == 0 or ch.locator('.play-key').is_hidden()
            for i in range(10):
                ch.evaluate('(i) => {state.index=i;positionCases()}', i)
                ch.wait_for_timeout(40)
                m = ch.evaluate('''() => {
                    const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();
                    const dock=r('#selection'), play=r('#play-selected'), options=r('#details-selected'), title=r('#selection h2');
                    return {w:innerWidth,h:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,dock,play,options,title};
                }''')
                assert m['sw'] <= m['w'] and m['sh'] <= m['h']+1, (platform, orientation, i, m)
                for key in ['play', 'options', 'title']:
                    r, d = m[key], m['dock']
                    assert r['left'] >= d['left'] and r['right'] <= d['right']+1 and r['top'] >= d['top'] and r['bottom'] <= d['bottom']+1, (platform, key, m)
                assert m['h']-m['dock']['bottom'] < 80, (platform, 'dock not at bottom', m)
                for key in ['play', 'options']:
                    assert m[key]['height'] >= 44 and m[key]['width'] >= 44, (platform, key, m)
            ch.evaluate('state.index=4;positionCases()')
            ch.wait_for_timeout(600)
            ch.locator('#details-selected').click()
            assert ch.locator('#detail-title').inner_text() == 'Metroid: Zero Mission'
            ch.locator('.close').click()
            ch.locator('#play-selected').click()
            assert ch.locator('#session-title').is_visible()
            ch.locator('.close').click()
            page.locator('#stage').screenshot(path=str(OUT / f'{platform}-{orientation}.png'))
            report['states'].append({'platform':platform,'orientation':orientation,'games_checked':10})
    assert not report['errors'], report['errors']
    browser.close()
(OUT / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
