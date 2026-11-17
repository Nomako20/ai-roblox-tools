"""side-by-side check image: python _strip.py out_name a b c"""
import sys, os
from PIL import Image
o = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
ims = [Image.open(f'{o}/{n}.png').convert('RGBA') for n in sys.argv[2:]]
h = 520
ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
s = Image.new('RGBA', (sum(i.width for i in ims), h), (0, 0, 0, 255))
x = 0
for i in ims:
    s.alpha_composite(i, (x, 0)); x += i.width
s.save(f'{o}/{sys.argv[1]}.png')
