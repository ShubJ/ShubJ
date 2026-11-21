from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = ROOT / "build"


def cut_white_background(im: Image.Image, tol: int = 28) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        q.extend([(0, y), (w - 1, y)])
    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    # flood from the edges only, so white shirts and eye highlights inside the outline survive
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        r, g, b, _ = px[x, y]
        if min(r, g, b) < 255 - tol:
            continue
        mp[x, y] = 0
        if x > 0: q.append((x - 1, y))
        if x < w - 1: q.append((x + 1, y))
        if y > 0: q.append((x, y - 1))
        if y < h - 1: q.append((x, y + 1))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(mask)
    return im


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, size in (("portrait", 360), ("pointing", 400)):
        im = cut_white_background(Image.open(ASSETS / f"{name}.png"))
        im = im.crop(im.getbbox())
        im.thumbnail((size, size), Image.LANCZOS)
        im = im.quantize(colors=200, method=Image.FASTOCTREE, dither=Image.NONE)
        dest = OUT / f"{name}.png"
        im.save(dest, optimize=True)
        print(dest.name, im.size, dest.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
