"""Render hardware in isolation so carousel transforms cannot corrupt the visual audit."""
from pathlib import Path
import hashlib, urllib.request
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch()
 pg=b.new_page(viewport={'width':1200,'height':1050})
 pg.goto('http://127.0.0.1:8770/ezCORE-Orbit.html',wait_until='networkidle')
 art=pg.evaluate('cores.map(c=>({id:c.id,svg:hardwareArt(c.id)}))')
 assert len(art)==18
 assert len(set(a['svg'] for a in art))==18
 pg.set_content('<style>body{margin:0;background:#0a0a0a;color:#dde6f4;font:12px sans-serif;display:grid;grid-template-columns:repeat(6,200px)}section{padding:14px;border:1px solid #dde6f422}svg{width:170px;height:190px;display:block}p{margin:8px 0}</style>'+''.join('<section>'+a['svg']+'<p>'+a['id']+'</p></section>' for a in art))
 assert pg.locator('svg.hardware-art').count()==18
 assert pg.evaluate('Array.from(document.querySelectorAll("svg")).every(s=>s.getAttribute("viewBox")==="0 0 320 240" && s.getAttribute("aria-label") && s.getBBox().width>0)')
 pg.screenshot(path=str(ROOT/'verification/systems-redesign/hardware-contact.png'),full_page=True)
 b.close()
data=urllib.request.urlopen('http://127.0.0.1:8770/').read()
assert data==(ROOT/'index.html').read_bytes()
print('PASS: 18 labeled hardware SVGs render; canonical served bytes match '+hashlib.sha256(data).hexdigest())
