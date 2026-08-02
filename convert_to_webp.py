from PIL import Image
import sys

files = [
    'og-mortgage.png',
    'og-loan.png',
    'og-default.png',
]

for f in files:
    try:
        im = Image.open(f)
        webp = f.rsplit('.',1)[0] + '.webp'
        im.save(webp, 'WEBP', quality=85, method=6)
        print('WROTE', webp)
    except Exception as e:
        print('SKIP', f, '->', e, file=sys.stderr)
