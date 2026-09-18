"""Consolidated shell/screen geometry and screenshot evidence."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).parent
OUT=ROOT/'verification'/'os-matrix'
OUT.mkdir(exist_ok=True)
report={'states':[],'errors':[],'failures':[]}
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':1100})
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.goto('http://127.0.0.1:8770/',wait_until='networkidle')
 page.reload(wait_until='networkidle')
 page.wait_for_function('ready')
 for platform in ['ios','android','mac','windows','linux','web']:
  page.locator('#tab-'+platform).click()
  page.wait_for_function('ready')
  for orientation in (['portrait','landscape'] if platform in ['ios','android'] else ['desktop']):
   if orientation=='landscape':
    if page.locator('#rotate-button').is_hidden():
     report.setdefault('skipped',[]).append(platform+'-landscape: rotate control not landed yet')
     continue
    page.locator('#rotate-button').click()
    page.wait_for_timeout(700)
   for screen in ['library','systems','details','vault','pause','settings']:
    page.locator('[data-screen="'+screen+'"]').click()
    ch=page.frames[1]
    target='#overlay .dialog' if screen in ['details','pause'] else '#'+screen
    ch.locator(target).wait_for(state='visible')
    ch.wait_for_timeout(850)
    ch.wait_for_function('Array.from(document.images).filter(x=>x.getClientRects().length).every(x=>x.complete&&x.naturalWidth>0)')
    m=ch.evaluate('''() => {const r=s=>{const e=document.querySelector(s);return e&&!e.hidden?e.getBoundingClientRect().toJSON():null};return {w:innerWidth,h:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,cover:r('.selected'),stage:r('.flow'),play:r('#play-selected'),dialog:r('#overlay .dialog'),header:r('.screen:not([hidden]) .screen-header'),nav:r('.nav')}}''')
    key=f'{platform}-{orientation}-{screen}'
    failures=[]
    if m['sw']>m['w']:failures.append('horizontal overflow')
    if screen=='library':
     a,c=m['cover'],m['stage']
     if a['top']<c['top']-1 or a['bottom']>c['bottom']+1:failures.append('cover clipped')
     if m['play']['bottom']>m['h']+1:failures.append('play below viewport')
    if m['dialog'] and (m['dialog']['bottom']>m['h']+1 or m['dialog']['top']<0):failures.append('dialog outside viewport')
    report['states'].append({'id':key,**m})
    report['failures'] += [{'id':key,'issues':failures}] if failures else []
    page.locator('#stage').screenshot(path=str(OUT/(key+'.png')))
    if screen=='library':page.screenshot(path=str(OUT/(key+'-full.png')),full_page=True)
 b.close()
for platform in ['ios','android','mac','windows','linux','web']:
 files=[OUT/(s['id']+'.png') for s in report['states'] if s['id'].startswith(platform+'-')]
 board=Image.new('RGB',(1200,330*((len(files)+2)//3)),'#eef1f6')
 draw=ImageDraw.Draw(board)
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGB');im.thumbnail((390,295))
  x=(i%3)*400;y=(i//3)*330
  board.paste(im,(x+(390-im.width)//2,y+25));draw.text((x+8,y+5),f.stem,fill='#10151c')
 board.save(OUT/(platform+'-contact.jpg'))
(OUT/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'states':len(report['states']),'errors':report['errors'],'failures':report['failures'],'evidence':str(OUT)},indent=2))
raise SystemExit(bool(report['errors'] or report['failures']))
