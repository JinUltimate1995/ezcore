"""Package the interface study with embedded, validated cover images."""
import base64
import concurrent.futures
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent
source = (ROOT / 'orbit-app.source.html').read_text()
assets = re.findall(r"art\('([^']+)','([^']+)'\)", source)

def fetch(pair):
    repo, name = pair
    url = 'https://raw.githubusercontent.com/libretro-thumbnails/' + repo + '/master/Named_Boxarts/' + urllib.parse.quote(name) + '.png'
    data = urllib.request.urlopen(url, timeout=60).read()
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError(f'Not a PNG: {name}')
    return pair, 'data:image/png;base64,' + base64.b64encode(data).decode(), len(data)

results = list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch, assets))
for (repo, name), data, size in results:
    source = source.replace(f"art('{repo}','{name}')", '"' + data + '"')
    print(f'Validated {name}: {size:,} bytes')
output = ROOT / 'ezCORE-Orbit.html'
output.write_text(source)
print(f'Packaged {len(results)} covers: {output} ({output.stat().st_size:,} bytes)')
