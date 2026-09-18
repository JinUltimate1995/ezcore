from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':1100})
 pg.goto('http://127.0.0.1:8770/',wait_until='networkidle');pg.wait_for_function('ready')
 for platform in ['ios','android','mac','windows','linux','web']:
  pg.locator('#tab-'+platform).click();pg.wait_for_function('ready')
  for step in range(3 if platform in ['ios','android'] else 2):
   ch=pg.frames[1]
   if step==1:
    ch.evaluate('window.rotationSentinel=42')
    if platform in ['ios','android']:pg.locator('#rotate-button').click()
    else:pg.locator('#expand-button').click()
   elif step==2:pg.locator('#rotate-button').click()
   pg.wait_for_timeout(300)
   geo=pg.evaluate('''() => {const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();return {shell:r('.platform-shell'),glass:r('.phone-glass')||null,frame:r('.native-frame')}}'''.replace("glass:r('.phone-glass')||null,",''))
   s,f=geo['shell'],geo['frame']
   assert f['right']<=s['right']+1 and f['bottom']<=s['bottom']+1,(platform,step,geo)
   assert abs(f['width']-(s['width']-(26 if platform in ['ios','android'] else 2)*(s['width']/(882 if step==1 else 416) if platform in ['ios','android'] else 1)))<3,(platform,step,geo)
   if step==1 and platform in ['ios','android']:
    assert s['width']>s['height'],geo
    assert ch.evaluate('rotationSentinel')==42
    assert ch.evaluate('parseInt(getComputedStyle(document.body).getPropertyValue("--safe-left"))')>=32
   if step==1 and platform not in ['ios','android']:pg.locator('#expanded-exit').click()
 print('PASS: six shells fit iframe; phones rotate real shell and retain frame; safe areas reach child')
 b.close()
