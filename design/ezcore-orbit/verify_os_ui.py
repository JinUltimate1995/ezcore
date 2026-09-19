"""Console collection contract, exercised against the packaged shared app."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width":1280,"height":760})
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8770/ezCORE-Orbit.html', wait_until='networkidle')
    tabs=page.locator('#system-strip button').all_text_contents()
    assert [s.strip() for s in tabs[:3]] == ['Time capsule','Favorites','All systems'], tabs[:3]
    page.locator('[data-collection="vault"]').click()
    assert page.locator('#vault').is_visible()
    assert page.locator('#system-strip').is_visible()
    page.locator('[data-filter="All systems"]').click()
    assert page.locator('#library').is_visible()
    page.locator('[data-library-core="advancebit"]').click()
    assert page.locator('.game-case').count()==2
    page.locator('[data-library-core="gambatte"]').click()
    assert page.locator('#no-games').is_visible(), 'Per-core filter must not show another engine games'
    assert not errors, errors
    print('PASS: ordered persistent collection tabs; real capsule navigation; exact per-core filtering')
    page.locator('[data-filter="All systems"]').click()
    assert page.evaluate('document.documentElement.scrollHeight<=innerHeight'), 'Collection should fit desktop height'
    for width,height in [(1280,760),(860,390),(390,856),(320,700),(768,1024),(1920,1080)]:
        page.set_viewport_size({'width':width,'height':height})
        page.wait_for_timeout(850)
        geometry=page.evaluate('''() => {const nav=document.querySelector('.nav').getBoundingClientRect(), stage=document.querySelector('.flow').getBoundingClientRect(), cover=document.querySelector('.game-case.selected').getBoundingClientRect();return {nav:{x:nav.x,y:nav.y,w:nav.width,h:nav.height},stage:{top:stage.top,bottom:stage.bottom},cover:{top:cover.top,bottom:cover.bottom},width:innerWidth,scroll:document.documentElement.scrollWidth}}''')
        assert geometry['scroll']<=width,(width,height,geometry)
        if width>=700 and width>height:
            assert geometry['nav']['h']>geometry['nav']['w'], ('Expected left OS rail',geometry)
        else:
            assert geometry['nav']['y']<180, ('Portrait command dock belongs at top',geometry)
        assert geometry['cover']['top']>=geometry['stage']['top']-1 and geometry['cover']['bottom']<=geometry['stage']['bottom']+1, geometry
        page.screenshot(path=f'/Users/jinultimate/Projects/Mobile/universal-emulator/design/ezcore-orbit/verification/os-{width}-{height}.png')
    print('PASS: OS rail/dock and selected-cover fit at six aspect ratios')
    b.close()
