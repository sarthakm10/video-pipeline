# Contact sheet: last step of every slide, 3 per row, for quick visual checks.
import sys, os, glob
from PIL import Image
m = sys.argv[1]; d = f"work/{m}"
last = {}
for p in sorted(glob.glob(f"{d}/s*_*.png")):
    s = os.path.basename(p)[:3]; last[s] = p
ims = [Image.open(p).resize((960, 540)) for p in last.values()]
cols = 2; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 960, rows * 540), "white")
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 960, (i // cols) * 540))
sheet.save(f"{d}/sheet.png"); print(len(ims), sheet.size)
