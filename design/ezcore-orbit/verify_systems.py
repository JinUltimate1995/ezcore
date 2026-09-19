"""Systems: 3D hardware browser + reversible, persisted preview core management."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
OUT=ROOT/'verification'/'systems-redesign'
OUT.mkdir(parents=True, exist_ok=True)
report={'states':[], 'errors':[]}
with sync_playwright() as p:
 b=p.chromium.launch()
 pg=b.new_page(viewport={'width':1440,'height':1100})
 pg.on('pageerror',lambda e:report['errors'].append(str(e)))
 pg.goto('http://127.0.0.1:8770/',wait_until='networkidle')
 pg.reload(wait_until='networkidle');pg.wait_for_function('ready')
 for platform in ['ios','android','mac','windows','linux','web']:
  pg.locator('#tab-'+platform).click();pg.wait_for_function('ready')
  pg.locator('[data-screen="systems"]').click()
  ch=pg.frames[1]
  assert ch.locator('#core-flow').count()==1, 'Systems needs a 3D hardware browser'
  assert ch.locator('.core-card').count()==18
  assert ch.locator('.handheld').count()==0, 'Remove the universal GBA placeholder'
  for orientation in (['portrait','landscape'] if platform in ['ios','android'] else ['desktop']):
   if orientation=='landscape':pg.locator('#rotate-button').click()
   ch.wait_for_timeout(500)
   for core in ch.evaluate('cores.map(c=>c.id)'):
    ch.evaluate('(id)=>selectCore(id)',core);ch.wait_for_timeout(120)
    assert ch.locator('.core-card.selected .hardware-art').count()==1
    m=ch.evaluate('''() => {const r=s=>document.querySelector(s).getBoundingClientRect().toJSON();return {w:innerWidth,h:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,stage:r('#core-flow'),card:r('.core-card.selected'),dock:r('#system-feature'),toggle:r('#core-toggle')}}''')
    assert m['sw']<=m['w'] and m['sh']<=m['h']+1,(platform,orientation,core,m)
    a,d=m['card'],m['stage']
    assert a['top']>=d['top']-1 and a['bottom']<=d['bottom']+1,(platform,core,'card clipping',m)
    assert m['toggle']['bottom']<=m['h'] and m['toggle']['height']>=44,(platform,core,m)
   ch.evaluate("selectCore('advancebit')");ch.wait_for_timeout(800)
   pg.locator('#stage').screenshot(path=str(OUT/f'{platform}-{orientation}.png'))
   report['states'].append({'platform':platform,'orientation':orientation,'cores':18})
 # Actual user actions, cancellation, persistence and no library/save deletion.
 ch=pg.frames[1]
 before=ch.evaluate('JSON.stringify({games:games.map(g=>g.id),saves})')
 ch.locator('#core-toggle').click()
 assert ch.locator('#remove-core-title').is_visible()
 ch.locator('#cancel-remove-core').click()
 assert ch.locator('#core-toggle').inner_text()=='Remove core'
 ch.locator('#core-toggle').click();ch.locator('#confirm-remove-core').click()
 assert ch.locator('#core-toggle').inner_text()=='Add core'
 assert ch.locator('#browse-core').is_disabled()
 assert before==ch.evaluate('JSON.stringify({games:games.map(g=>g.id),saves})')
 pg.reload(wait_until='networkidle');pg.wait_for_function('ready');pg.locator('[data-screen="systems"]').click();ch=pg.frames[1]
 ch.evaluate("selectCore('advancebit')")
 assert ch.locator('#core-toggle').inner_text()=='Add core'
 ch.locator('#core-toggle').click()
 assert ch.locator('#core-toggle').inner_text()=='Remove core'
 ch.locator('#browse-core').click()
 assert ch.locator('#library').is_visible()
 assert ch.locator('.game-case').count()==2
 ch.locator('[data-go="systems"]').click()
 ch.locator('[data-core-scope="available"]').click()
 assert ch.locator('.core-card').count()==1
 ch.locator('#core-toggle').click()
 assert ch.locator('#cores-empty').is_visible()
 ch.locator('[data-core-scope="all"]').click()
 assert ch.locator('.core-card').count()==18
 ch.evaluate("selectCore('advancebit')")
 ch.locator('#core-next').click()
 assert ch.evaluate('state.core')=='gambatte'
 ch.locator('#core-next').press('ArrowRight')
 assert ch.evaluate('state.core')=='nesbyte'
 assert not report['errors'],report['errors']
 b.close()
(OUT/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
