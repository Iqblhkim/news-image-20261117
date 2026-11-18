# Generates entry.png (offline, one-time). main.py just copies the result.
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
BG = (14, 18, 28)
INK = (240, 240, 235)
MUTED = (150, 160, 175)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
f = lambda p, s: ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# header
d.rectangle([0, 0, W, 112], fill=(24, 30, 46))
d.text((32, 14), "TUESDAY 17 NOVEMBER 2026", font=f(B, 22), fill=(255, 196, 70))
d.text((32, 46), "THE WORLD IN ONE FRAME", font=f(S, 44), fill=INK)
d.rectangle([0, 112, W, 116], fill=(255, 196, 70))

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

# icons -------------------------------------------------------------
def ic_plane(x, y, c):
    d.polygon([(x-30,y+6),(x+34,y-6),(x-30,y-18),(x-18,y-6)], fill=c)
    d.polygon([(x-10,y-6),(x+6,y-30),(x+14,y-30),(x+8,y-6)], fill=c)
    d.polygon([(x-10,y-6),(x+6,y+18),(x+14,y+18),(x+8,y-6)], fill=c)
def ic_fire(x, y, c):
    d.polygon([(x,y-34),(x+22,y+4),(x+14,y+30),(x-14,y+30),(x-22,y+4),(x-8,y-8)], fill=c)
    d.polygon([(x,y-6),(x+11,y+14),(x+6,y+28),(x-6,y+28),(x-11,y+14)], fill=(255,225,120))
def ic_bridge(x, y, c):
    d.rectangle([x-36,y+6,x+36,y+12], fill=c)
    d.arc([x-36,y-26,x+36,y+34], 180, 360, fill=c, width=5)
    for k in range(-30,31,10): d.line([x+k,y+6,x+k,y-8+abs(k)//3*0 + (abs(k)//4)], fill=c, width=2)
    d.line([x-18,y+12,x-4,y+30], fill=(255,120,60), width=4)  # damage
    d.line([x+4,y+12,x+18,y+30], fill=(255,120,60), width=4)
def ic_crate(x, y, c):
    d.rectangle([x-28,y-22,x+28,y+22], outline=c, width=5)
    d.line([x-28,y-4,x+28,y-4], fill=c, width=4); d.line([x,y-22,x,y+22], fill=c, width=4)
    d.line([x-34,y+30,x+34,y-34], fill=(255,90,90), width=5)  # blocked
def ic_power(x, y, c):
    d.arc([x-26,y-24,x+26,y+28], -50, 230, fill=c, width=7)
    d.line([x,y-34,x,y-4], fill=c, width=7)
def ic_tv(x, y, c):
    d.rounded_rectangle([x-34,y-24,x+34,y+18], 6, outline=c, width=5)
    d.line([x-14,y+28,x+14,y+28], fill=c, width=5)
    d.line([x-18,y-12,x+18,y+8], fill=(255,90,90), width=6); d.line([x-18,y+8,x+18,y-12], fill=(255,90,90), width=6)
def ic_ballot(x, y, c):
    d.rectangle([x-30,y-4,x+30,y+28], outline=c, width=5)
    d.rectangle([x-12,y-6,x+12,y-1], fill=c)
    d.polygon([(x-14,y-34),(x+14,y-34),(x+14,y-12),(x-14,y-12)], fill=(240,240,235))
    d.line([x-8,y-22,x-2,y-16], fill=(30,30,30), width=3); d.line([x-2,y-16,x+9,y-30], fill=(30,30,30), width=3)
def ic_server(x, y, c):
    for k in range(3):
        yy = y-28+k*20
        d.rounded_rectangle([x-30,yy,x+30,yy+15], 3, outline=c, width=4)
        d.ellipse([x+16,yy+5,x+22,yy+11], fill=c)
    d.ellipse([x-6,y+34,x+6,y+46], fill=(120,220,140))
def ic_globe(x, y, c):
    d.ellipse([x-30,y-30,x+30,y+30], outline=c, width=5)
    d.ellipse([x-13,y-30,x+13,y+30], outline=c, width=3)
    d.line([x-30,y,x+30,y], fill=c, width=3)

tiles = [
 ("ASIA",     ic_plane,  (90,170,255),  "Trump lands in Manila", "ASEAN summit, then a Trump–Xi–Putin summit Thursday"),
 ("IRAN WAR", ic_fire,   (255,110,70),  "Iran targets US radar in Bahrain", "Ships ablaze in the Strait of Hormuz"),
 ("UKRAINE",  ic_bridge, (255,205,80),  "Ukraine’s largest drone strike", "Russia says Crimea bridge hit, 2,000+ drones downed"),
 ("GAZA",     ic_crate,  (240,240,235), "Ceasefire aid falls short", "Food and medicine deliveries shrinking"),
 ("OUTAGES",  ic_power,  (190,130,255), "Chase, Zelle, United outages", "After record US ground stop, Microsoft outage"),
 ("TURKEY",   ic_tv,     (255,120,140), "Opposition TV seized", "Sözcü TV taken off air, trustee installed"),
 ("ISRAEL",   ic_ballot, (110,220,190), "Election-meddling claims", "Opposition: Netanyahu must go"),
 ("CLIMATE",  ic_server, (120,220,140), "COP31 meets in Antalya", "US data centers emit as much CO₂ as Denmark"),
]

M, GAP = 24, 16
top = 134
tw = (W - 2*M - GAP) // 2
th = (H - top - 56 - 3*GAP) // 4
for i, (tag, icon, col, head, sub) in enumerate(tiles):
    cx = M + (i % 2) * (tw + GAP)
    cy = top + (i // 2) * (th + GAP)
    d.rounded_rectangle([cx, cy, cx+tw, cy+th], 14, fill=(26, 33, 50))
    d.rounded_rectangle([cx, cy, cx+8, cy+th], 4, fill=col)
    # icon plate
    px, py = cx + 70, cy + th//2
    d.ellipse([px-48, py-48, px+48, py+48], fill=(14,18,28))
    icon(px, py, col)
    tx = cx + 134
    maxw = tw - 134 - 14
    d.text((tx, cy+16), tag, font=f(B, 17), fill=col)
    y = cy + 42
    hf = f(B, 27)
    for ln in wrap(head, hf, maxw):
        d.text((tx, y), ln, font=hf, fill=INK); y += 34
    sf = f(R, 19)
    y += 2
    for ln in wrap(sub, sf, maxw):
        d.text((tx, y), ln, font=sf, fill=MUTED); y += 25

d.rectangle([0, H-44, W, H], fill=(24,30,46))
d.text((32, H-33), "World headlines of 17 Nov 2026: conflict, crisis, and a planet running hot", font=f(R, 16), fill=MUTED)
img.save("entry.png", optimize=True)
print(img.size)
