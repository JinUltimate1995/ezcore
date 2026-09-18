"""Check computed core transforms, independently reconstructing the layout contract."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
report={'viewports':[], 'errors':[], 'matrix_checks':0}
with sync_playwright() as p:
 b=p.chromium.launch()
 pg=b.new_page()
 pg.on('pageerror',lambda e:report['errors'].append(str(e)))
 pg.goto('http://127.0.0.1:8770/ezCORE-Orbit.html',wait_until='networkidle')
 # Disable interpolation for exact endpoint geometry; does not alter layout rules.
 pg.evaluate("prefs.motion=false;applyPrefs();go('systems')")
 ids=pg.evaluate('cores.map(c=>c.id)')
 for w,h in [(320,700),(390,844),(768,1024),(860,390),(1440,900),(1920,1080)]:
  pg.set_viewport_size({'width':w,'height':h})
  pg.wait_for_timeout(100)
  for selected in ids:
   pg.evaluate('(id)=>selectCore(id)',selected)
   result=pg.evaluate('''() => {
    const stage=document.querySelector('#core-flow'), cards=[...stage.querySelectorAll('.core-card')];
    const selected=cards.findIndex(e=>e.classList.contains('selected'));
    const step=Math.min(cards[0].offsetWidth*.91,stage.clientWidth*.43);
    let checks=0, maxError=0; const failures=[];
    cards.forEach((e,i)=>{
     const d=i-selected,a=Math.abs(d),style=getComputedStyle(e);
     const actual=new DOMMatrix(style.transform);
     const width=parseFloat(style.width),height=parseFloat(style.height);
     const expected=new DOMMatrix().translate(-width/2,-height/2,0)
       .translate(d*step,0,a?-80-(a-1)*50:10).rotate(0,d===0?0:d>0?-24:24,0);
     const av=actual.toFloat64Array(),ev=expected.toFloat64Array();
     for(let k=0;k<16;k++){const error=Math.abs(av[k]-ev[k]);maxError=Math.max(maxError,error);if(error>.02)failures.push({id:e.dataset.core,k,actual:av[k],expected:ev[k]});}
     if(Number(style.zIndex)!==20-a)failures.push({id:e.dataset.core,error:'incorrect depth ordering'});
     checks++;
    });
    const r=cards[selected].getBoundingClientRect(),s=stage.getBoundingClientRect();
    if(r.left<s.left-1||r.right>s.right+1||r.top<s.top-1||r.bottom>s.bottom+1)failures.push({error:'selected card outside stage',card:r.toJSON(),stage:s.toJSON()});
    if(Math.abs((r.left+r.right)/2-(s.left+s.right)/2)>1)failures.push({error:'selected card not centered'});
    return {checks,maxError,failures};
   }''')
   assert not result['failures'],(w,h,selected,result)
   report['matrix_checks']+=result['checks']
  report['viewports'].append({'width':w,'height':h,'selections':len(ids)})
 # Also check real animated navigation settles at the same endpoint.
 pg.evaluate("prefs.motion=true;applyPrefs();selectCore('mgba')")
 pg.wait_for_timeout(800)
 pg.locator('#core-next').click()
 pg.wait_for_timeout(850)
 assert pg.evaluate("state.core==='gambatte' && document.querySelector('.core-card.selected').dataset.core==='gambatte'")
 assert pg.evaluate("Math.abs(new DOMMatrix(getComputedStyle(document.querySelector('.core-card.selected')).transform).m43-10)<.02")
 assert not report['errors'],report['errors']
 b.close()
(ROOT/'verification/systems-redesign/transforms-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
print('PASS: computed matrices match positioning contract; selected cards contained and centered; animated endpoint verified')
