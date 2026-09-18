"""Extract approved raster artwork without redrawing the supplied identity."""
from pathlib import Path
from PIL import Image
import shutil
ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
SOURCE = Path('/Users/jinultimate/Library/Application Support/Hermes/composer-images/6AA8EC9E-15CB-496D-8F13-5E447470E553_ed39b3.png')
shutil.copy2(SOURCE, ASSETS / 'ezcore-reference.png')
im = Image.open(SOURCE).convert('RGB')
# Full-resolution silver symbol and custom wordmark from the large black icon.
# Background removal follows luminance/chroma, retaining the blue slash.
def transparent(crop):
    out = crop.convert('RGBA')
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r,g,b,_ = px[x,y]
            strength = max(min(r,g,b), b-r)
            a = round(max(0,min(1,(strength-38)/48))*255)
            px[x,y] = (r,g,b,a)
    return out
symbol = transparent(im.crop((173,250,598,437)))
wordmark = transparent(im.crop((191,466,566,534)))
lockup = Image.new('RGBA',(660,110))
lockup.alpha_composite(symbol.resize((225,99),Image.Resampling.LANCZOS),(0,5))
lockup.alpha_composite(wordmark.resize((413,75),Image.Resampling.LANCZOS),(247,18))
lockup.save(ASSETS / 'ezcore-lockup-light.png')
symbol.save(ASSETS / 'ezcore-symbol-light.png')
# Remove the near-white board so the original primary lockup sits cleanly on silver.
dark = im.crop((801,247,1503,357)).convert('RGBA')
for y in range(dark.height):
    for x in range(dark.width):
        r,g,b,_ = dark.getpixel((x,y))
        strength = max(255-min(r,g,b), b-r)
        alpha = round(max(0,min(1,(strength-32)/60))*255)
        dark.putpixel((x,y),(r,g,b,alpha))
dark.save(ASSETS / 'ezcore-lockup-dark.png')
for name,box in [('dark',(44,756,161,870)),('silver',(182,755,300,870)),('blue',(319,755,437,870))]:
    icon = im.crop(box).convert('RGBA')
    # Remove only outside the rounded app tile via a rounded alpha mask.
    from PIL import ImageDraw
    mask = Image.new('L',icon.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,icon.width-1,icon.height-1),radius=28,fill=255)
    icon.putalpha(mask)
    icon.save(ASSETS / f'ezcore-icon-{name}.png')
# Large approved primary app icon for the brand reference panel.
im.crop((117,114,647,614)).save(ASSETS / 'ezcore-app-icon.png')
print('Extracted 8 approved brand assets from supplied image.')
