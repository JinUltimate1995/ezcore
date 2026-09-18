"""Package the shared app and all platform shells with approved brand assets.

Run: python3 build_brand.py
Uses cached validated covers; no network required. Web fonts remain external.
"""
import base64
import re
from pathlib import Path
ROOT = Path(__file__).parent
BUILD = 'ezcore-final-01'

def embed_assets(source):
    def embed(match):
        path = ROOT / match.group(0)
        data = path.read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), path
        return 'data:image/png;base64,' + base64.b64encode(data).decode()
    return re.sub(r'assets/[a-zA-Z0-9_/-]+\.png', embed, source)

app = (ROOT / 'orbit-app.source.html').read_text()
for marker, filename in [('/* __SYSTEMS_CSS__ */', 'systems.css'),
                         ('/* __HARDWARE_ART_JS__ */', 'hardware-art.js'),
                         ('/* __SYSTEMS_JS__ */', 'systems.js')]:
    assert marker in app, f'Missing source marker: {marker}'
    app = app.replace(marker, (ROOT / filename).read_text())
assert BUILD in app, 'Shared app must carry final brand marker'
images = list(re.finditer(r"art\('[^']+','[^']+'\)", app))
assert len(images) == 10, 'Unexpected sample cover inventory'
for i, match in reversed(list(enumerate(images))):
    data = (ROOT / 'assets' / 'covers' / f'{i:02}.png').read_bytes()
    assert data.startswith(b'\x89PNG\r\n\x1a\n')
    value = '"data:image/png;base64,' + base64.b64encode(data).decode() + '"'
    app = app[:match.start()] + value + app[match.end():]
app = embed_assets(app)
wrapper = embed_assets((ROOT / 'platforms.source.html').read_text())
assert BUILD in wrapper
wrapper = wrapper.replace('__ORBIT_APP_BASE64__', base64.b64encode(app.encode()).decode())
assert '__ORBIT_APP_BASE64__' not in wrapper
for name, content in [('ezCORE-Orbit.html',app),('ezCORE-Platforms.html',wrapper),('index.html',wrapper)]:
    (ROOT / name).write_text(content)
    print(f'{name}: {len(content.encode()):,} bytes; {BUILD}')
print('Canonical URL: http://127.0.0.1:8770/ ; all brand and cover artwork embedded.')
