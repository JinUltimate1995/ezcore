from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1280,'height':760})
 page.goto('http://127.0.0.1:8770/ezCORE-Orbit.html',wait_until='networkidle')
 page.wait_for_timeout(1200)
 print(page.evaluate('''() => {let c=document.querySelector('.selected'),i=c.querySelector('img');return {image:[i.naturalWidth,i.naturalHeight,i.getBoundingClientRect().toJSON()],cover:c.getBoundingClientRect().toJSON(),height:document.documentElement.scrollHeight}}'''))
 page.screenshot(path=str(Path(__file__).parent/'verification/os-initial.png'))
 b.close()
