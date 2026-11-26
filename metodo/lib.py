import os
import io
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features

S = 2  # escala de trabalho (renderiza em 2160x2700 e reduz para 1080x1350)
W, H = 1080, 1350
BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = {"open": os.path.join(BASE, "fonts", "OpenSans.ttf"), "noto": os.path.join(BASE, "fonts", "NotoSans.ttf")}
LOGOS = os.path.join(BASE, "logos") + "/"
_cache = {}


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def font(fam, size, weight=400):
    key = (fam, size, weight)
    if key not in _cache:
        f = ImageFont.truetype(FONTS[fam], int(size * S), layout_engine=ImageFont.Layout.RAQM)
        f.set_variation_by_axes([weight, 100])
        _cache[key] = f
    return _cache[key]


def canvas(bg):
    return Image.new("RGBA", (W * S, H * S), hexc(bg) if isinstance(bg, str) else bg)


def svg_layer(inner):
    """Camada vetorial do tamanho da arte. Coordenadas em px da arte final (1080x1350)."""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*S}" height="{H*S}" viewBox="0 0 {W} {H}">{inner}</svg>'
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    return Image.open(io.BytesIO(png)).convert("RGBA")


def add_svg(img, inner):
    img.alpha_composite(svg_layer(inner))


def icon(img, paths, x, y, size, color, stroke=2.0):
    """Ícone de traço (viewBox 24) desenhado em (x,y) com lado size (px da arte)."""
    inner = (f'<g transform="translate({x},{y}) scale({size/24})" fill="none" stroke="{color}" '
             f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{paths}</g>')
    add_svg(img, inner)


def shadow(img, box, radius, color=(41, 13, 61, 40), blur=28, offset=(0, 14)):
    x0, y0, x1, y1 = box
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([(x0 + offset[0]) * S, (y0 + offset[1]) * S, (x1 + offset[0]) * S, (y1 + offset[1]) * S],
                        radius=radius * S, fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(blur * S))
    img.alpha_composite(lay)


def rrect(img, box, radius, fill, outline=None, width=0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([v * S for v in box], radius=radius * S, fill=fill, outline=outline, width=int(width * S))


def text_w(txt, f):
    return f.getlength(txt) / S


def draw_text(img, xy, txt, f, fill, anchor="ls"):
    d = ImageDraw.Draw(img)
    d.text((xy[0] * S, xy[1] * S), txt, font=f, fill=fill, anchor=anchor)


def grad_text(img, xy, txt, f, c1, c2, anchor="ls"):
    """Texto com degradê horizontal c1->c2."""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).text((xy[0] * S, xy[1] * S), txt, font=f, fill=255, anchor=anchor)
    bb = mask.getbbox()
    if not bb:
        return
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    w = max(1, bb[2] - bb[0])
    a, b = hexc(c1), hexc(c2)
    strip = Image.new("RGBA", (w, 1))
    for i in range(w):
        t = i / (w - 1 if w > 1 else 1)
        strip.putpixel((i, 0), tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(4)))
    strip = strip.resize((w, bb[3] - bb[1]))
    g.paste(strip, (bb[0], bb[1]))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(g, (0, 0), mask)
    img.alpha_composite(out)


def rich_line(img, x, y, segs, f, align="left", center_x=None):
    """segs: lista de (texto, cor) ou (texto, ('grad', c1, c2)). y = linha de base."""
    total = sum(text_w(t, f) for t, _ in segs)
    if align == "center":
        x = center_x - total / 2
    for t, c in segs:
        if isinstance(c, tuple) and c and c[0] == "grad":
            grad_text(img, (x, y), t, f, c[1], c[2])
        else:
            draw_text(img, (x, y), t, f, hexc(c) if isinstance(c, str) else c)
        x += text_w(t, f)
    return total


def wrap(txt, f, maxw):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def paragraph(img, x, y, txt, f, color, maxw, lh, align="left", center_x=None):
    for i, ln in enumerate(wrap(txt, f, maxw)):
        if align == "center":
            draw_text(img, (center_x, y + i * lh), ln, f, hexc(color), anchor="ms")
        else:
            draw_text(img, (x, y + i * lh), ln, f, hexc(color))
    return y + (len(wrap(txt, f, maxw)) - 1) * lh


def logo(img, name, x, y, width=None, height=None, anchor="lt", alpha=1.0):
    lg = Image.open(LOGOS + name).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    if width:
        h = width * lg.height / lg.width
        w = width
    else:
        w = height * lg.width / lg.height
        h = height
    lg = lg.resize((round(w * S), round(h * S)), Image.LANCZOS)
    if alpha < 1:
        a = lg.getchannel("A").point(lambda v: int(v * alpha))
        lg.putalpha(a)
    px, py = x, y
    if anchor[0] == "m":
        px = x - w / 2
    elif anchor[0] == "r":
        px = x - w
    if anchor[1] == "m":
        py = y - h / 2
    elif anchor[1] == "b":
        py = y - h
    img.alpha_composite(lg, (round(px * S), round(py * S)))
    return w, h


def save(img, path):
    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    out.save(path, "PNG", optimize=True)
    return path


ICONS = {
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 13h5"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M7 16v-4M12 16V8M17 16v-7"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="M8 14h2M14 14h2M8 18h2"/>',
    "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    "users": '<circle cx="9" cy="7" r="4"/><path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/><path d="M21 21v-2a4 4 0 0 0-3-3.85"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "arrowup": '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
}
