"""Verify canonical final build, all 36 platform/screens and live behavior."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).parent
OUT = ROOT / 'verification'
OUT.mkdir(exist_ok=True)
report = {'build':'ezcore-final-01','matrix':[],'checks':[],'errors':[]}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1440,'height':1100}, device_scale_factor=1)
    page.on('pageerror',lambda e: report['errors'].append(str(e)))
    page.goto('http://127.0.0.1:8770/',wait_until='networkidle')
    page.reload(wait_until='networkidle')
    assert page.locator('body').get_attribute('data-brand-build') == report['build']
    page.wait_for_function('typeof frame?.contentWindow?.orbitNavigate === "function"')
    for platform in ['ios','android','mac','windows','linux','web']:
        page.locator(f'#tab-{platform}').click()
        page.wait_for_function('ready && frame.contentWindow.document.body.dataset.brandBuild === "ezcore-final-01"')
        child = page.frames[1]
        for screen in ['library','systems','details','vault','pause','settings']:
            page.locator(f'[data-screen="{screen}"]').click()
            selector = '#overlay .dialog' if screen in ['details','pause'] else '#'+screen
            child.locator(selector).wait_for(state='visible')
            child.wait_for_function('Array.from(document.images).filter(x=>x.getClientRects().length).every(x=>x.complete && x.naturalWidth>0)')
            measurements = child.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,accent:getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(),visibleText:document.body.innerText.length})''')
            assert measurements['scrollWidth'] <= measurements['width'], (platform, screen, measurements)
            assert measurements['accent'].lower() == '#007bff', measurements
            assert measurements['visibleText'] > 100
            report['matrix'].append({'platform':platform,'screen':screen,**measurements})
            if screen == 'library':
                child.wait_for_timeout(500)
                box = child.evaluate('''() => {const a=document.querySelector('.game-case.selected').getBoundingClientRect(),b=document.querySelector('.flow').getBoundingClientRect();return {top:a.top-b.top,bottom:b.bottom-a.bottom}}''')
                assert box['top'] >= -1 and box['bottom'] >= -1, (platform,box)
            page.screenshot(path=str(OUT/f'{platform}-{screen}.png'),full_page=True)
    report['checks'].append('36 platform/screen states; decoded visible images; no horizontal overflow; selected cover inside stage; final blue tokens')
    page.locator('[data-screen="library"]').click()
    child = page.frames[1]
    before=child.locator('#selection h2').inner_text()
    child.locator('.next').click()
    assert child.locator('#selection h2').inner_text()!=before
    child.locator('[data-filter="GBA"]').click()
    assert child.locator('.game-case').count()==2
    child.locator('#grid-view').click()
    assert child.locator('#game-grid').is_visible()
    child.locator('#search').fill('not-a-title')
    assert child.locator('#no-games').is_visible()
    child.locator('#clear-filters').click()
    child.locator('#flow-view').click()
    child.locator('#details-selected').click()
    child.locator('#favorite').click()
    assert child.locator('#favorite').get_attribute('aria-pressed')=='true'
    child.locator('.close').press('Escape')
    assert child.locator('#overlay').is_hidden()
    child.locator('#play-selected').click()
    child.locator('#save-demo').click()
    child.locator('#open-capsule').click()
    assert child.locator('#vault-grid .save-card').count()==4
    report['checks'].append('Cover navigation, system filter, grid, search empty/reset, favorite, Escape, demo save and capsule')
    page.locator('[data-screen="settings"]').click()
    for setting in ['Appearance','Emulation','Controllers','Audio','Library & storage','About ezCORE']:
        child.locator(f'[data-setting="{setting}"]').click()
        assert child.locator('#settings-panel h2').is_visible()
        page.screenshot(path=str(OUT/('settings-'+setting.split()[0].lower()+'.png')),full_page=True)
    child.locator('[data-setting="Appearance"]').click()
    child.locator('[data-toggle="motion"]').click()
    assert child.locator('[data-toggle="motion"]').get_attribute('aria-checked')=='false'
    page.reload(wait_until='networkidle')
    page.wait_for_function('ready && typeof frame.contentWindow.orbitNavigate === "function"')
    child=page.frames[1]
    assert child.locator('body').evaluate('(x)=>x.classList.contains("still")')
    report['checks'].append('All six settings tabs and local preference persistence')
    page.locator('#tab-mac').click()
    page.wait_for_function('ready')
    page.locator('[data-window="minimize"]').click()
    assert page.locator('#restore-card').is_visible()
    page.locator('#restore-button').click()
    assert page.locator('#shell-host').is_visible()
    page.locator('[data-window="maximize"]').click()
    assert page.locator('#stage').evaluate('(x)=>x.classList.contains("expanded")')
    page.locator('#expanded-exit').click()
    page.locator('#shell-button').click()
    assert page.locator('#stage').evaluate('(x)=>x.classList.contains("flat")')
    page.locator('#shell-button').click()
    page.locator('#brand-guide-button').click()
    assert page.locator('#brand-guide').is_visible()
    page.screenshot(path=str(OUT/'brand-identity.png'),full_page=True)
    page.keyboard.press('Escape')
    assert not page.locator('#brand-guide').is_visible()
    report['checks'].append('Minimize/restore, maximize/exit focus, shell mode and brand guide dialog')
    for width in [390,768]:
        page.set_viewport_size({'width':width,'height':900})
        page.locator('#tab-ios').click()
        page.wait_for_function('ready')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=str(OUT/f'responsive-{width}.png'),full_page=True)
    report['checks'].append('390px and 768px responsive wrapper without horizontal overflow')
    # Legacy prefs retain user collections and migrate the old lime accent.
    page.set_viewport_size({'width':1440,'height':1100})
    page.evaluate('localStorage.setItem("orbit-prefs",JSON.stringify({accent:"#c5f477",motion:false}))')
    page.reload(wait_until='networkidle')
    page.wait_for_function('ready')
    assert page.frames[1].evaluate('getComputedStyle(document.documentElement).getPropertyValue("--accent").trim()')=='#007bff'
    report['checks'].append('Legacy lime preference cannot override finalized blue identity')
    assert not report['errors'], report['errors']
    browser.close()
(OUT/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'build':report['build'],'matrix_states':len(report['matrix']),'checks':report['checks'],'errors':report['errors'],'evidence':str(OUT)},indent=2))
