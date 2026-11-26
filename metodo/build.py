import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "saida"
import os
os.makedirs(OUT, exist_ok=True)

# Condutrix
RP, V, RD, LI, LC = "#290D3D", "#6D21FD", "#5F22D8", "#A67EF4", "#F6F2FD"
# Negócio Pronto
AZ, MA, CL, LA = "#2745F4", "#131B3A", "#E8EDFC", "#C8D2FF"
M = 88  # margem


def footer_cdx(img, y=1262, dark=RP):
    draw_text(img, (M, y), "Condutrix", font("open", 26, 700), hexc(dark))
    x = M + text_w("Condutrix ", font("open", 26, 700))
    draw_text(img, (x, y), "Negócio Inteligente", font("open", 26, 400), hexc(dark))
    draw_text(img, (W - M, y), "condutrix.com.br", font("open", 26, 600), hexc(V), anchor="rs")


# ---------------- Condutrix 10h ----------------
def cdx_10():
    img = canvas(LC)
    add_svg(img, f'''
      <defs>
        <radialGradient id="g1" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stop-color="{V}" stop-opacity="0.30"/>
          <stop offset="1" stop-color="{V}" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <circle cx="930" cy="250" r="430" fill="url(#g1)"/>
      <circle cx="930" cy="250" r="250" fill="none" stroke="{LI}" stroke-opacity="0.35" stroke-width="2"/>
      <circle cx="930" cy="250" r="340" fill="none" stroke="{LI}" stroke-opacity="0.22" stroke-width="2"/>
      <circle cx="930" cy="250" r="430" fill="none" stroke="{LI}" stroke-opacity="0.12" stroke-width="2"/>
      <circle cx="1105" cy="350" r="9" fill="{V}"/>
      <circle cx="700" cy="85" r="6" fill="{LI}"/>
    ''')
    logo(img, "cdx-h-cor.png", M, M, width=300)
    # selo
    f = font("open", 24, 700)
    tw = text_w("AUTOMAÇÃO COM IA", f)
    rrect(img, (M, 268, M + tw + 56, 318), 25, hexc("#FFFFFF"))
    add_svg(img, f'<circle cx="{M+26}" cy="293" r="7" fill="{V}"/>')
    draw_text(img, (M + 42, 302), "AUTOMAÇÃO COM IA", f, hexc(RD))
    # título
    ft = font("open", 96, 800)
    y = 450
    rich_line(img, M, y, [("Sua rotina", RP)], ft)
    rich_line(img, M, y + 108, [("no automático,", ("grad", V, RD))], ft)
    rich_line(img, M, y + 216, [("seu tempo", RP)], ft)
    rich_line(img, M, y + 324, [("de volta.", RP)], ft)
    paragraph(img, M, y + 400, "A IA cuida do repetitivo. Você cuida do que faz a empresa crescer.",
              font("open", 34, 400), "#4A3560", 800, 48)
    # cartão com o interruptor
    box = (M, 975, W - M, 1185)
    shadow(img, box, 36)
    rrect(img, box, 36, hexc("#FFFFFF"))
    draw_text(img, (M + 48, 1048), "Modo automático", font("open", 34, 700), hexc(RP))
    draw_text(img, (M + 48, 1090), "Ligado para as tarefas do dia a dia", font("open", 26, 400), hexc("#6B5A80"))
    # toggle
    tx, ty = W - M - 48 - 150, 1020
    add_svg(img, f'''
      <defs><linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{RD}"/></linearGradient></defs>
      <rect x="{tx}" y="{ty}" width="150" height="80" rx="40" fill="url(#tg)"/>
      <circle cx="{tx+110}" cy="{ty+40}" r="31" fill="#FFFFFF"/>
    ''')
    icon(img, ICONS["check"], tx + 96, ty + 26, 28, RD, 3)
    # chips
    cx = M + 48
    for t in ["Atendimento", "Relatórios", "Agenda", "Lembretes"]:
        fc = font("open", 22, 600)
        w = text_w(t, fc) + 64
        rrect(img, (cx, 1118, cx + w, 1160), 21, hexc(LC))
        icon(img, ICONS["check"], cx + 14, 1128, 22, V, 3)
        draw_text(img, (cx + 44, 1147), t, fc, hexc(RD))
        cx += w + 12
    footer_cdx(img)
    return save(img, f"{OUT}/condutrix-10h.png")


# ---------------- Condutrix 16h ----------------
def cdx_16():
    img = canvas("#FFFFFF")
    add_svg(img, f'''
      <defs><radialGradient id="g1" cx="0.5" cy="0.5" r="0.5">
        <stop offset="0" stop-color="{LI}" stop-opacity="0.28"/><stop offset="1" stop-color="{LI}" stop-opacity="0"/></radialGradient></defs>
      <circle cx="80" cy="200" r="360" fill="url(#g1)"/>
    ''')
    logo(img, "cdx-ab-cor.png", W - M, M, height=58, anchor="rt")
    grad_text(img, (M - 10, 395), "5", font("open", 300, 800), V, RD)
    fx = M + 205
    ft = font("open", 60, 800)
    draw_text(img, (fx, 250), "tarefas para", ft, hexc(RP))
    draw_text(img, (fx, 322), "tirar das", ft, hexc(RP))
    grad_text(img, (fx, 394), "suas mãos", ft, V, RD)
    items = [("chat", "Responder dúvidas frequentes"), ("chart", "Montar relatórios"),
             ("calendar", "Organizar a agenda"), ("sheet", "Lançar dados em planilhas"),
             ("bell", "Enviar lembretes a clientes")]
    y0, hh, gap = 470, 116, 22
    for i, (ic, t) in enumerate(items):
        y = y0 + i * (hh + gap)
        rrect(img, (M, y, W - M, y + hh), 30, hexc(LC))
        add_svg(img, f'''<defs><linearGradient id="ig{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{RD}"/></linearGradient></defs>
          <rect x="{M+22}" y="{y+22}" width="72" height="72" rx="20" fill="url(#ig{i})"/>''')
        icon(img, ICONS[ic], M + 40, y + 40, 36, "#FFFFFF", 2.2)
        draw_text(img, (M + 122, y + hh / 2 + 12), t, font("open", 34, 600), hexc(RP))
        draw_text(img, (W - M - 34, y + hh / 2 + 12), f"0{i+1}", font("open", 32, 800), hexc(LI), anchor="rs")
    # pergunta
    draw_text(img, (M, 1208), "Qual delas mais toma o seu tempo hoje?", font("open", 32, 700), hexc(V))
    add_svg(img, f'<rect x="{M}" y="1236" width="{W-2*M}" height="2" fill="{LC}"/>')
    footer_cdx(img, 1290)
    return save(img, f"{OUT}/condutrix-16h.png")


# ---------------- Condutrix 20h ----------------
def cdx_20():
    img = canvas(LC)
    cx, cy, r = 540, 470, 210
    circ = 2 * 3.14159265 * r
    ticks = "".join(
        f'<circle cx="{cx + (r+72)*__import__("math").cos(a*3.14159265/30)}" cy="{cy + (r+72)*__import__("math").sin(a*3.14159265/30)}" r="{5 if a%5==0 else 2.5}" fill="{LI}" fill-opacity="{0.9 if a%5==0 else 0.5}"/>'
        for a in range(60))
    add_svg(img, f'''
      <defs>
        <linearGradient id="ag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{RD}"/></linearGradient>
        <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{V}" stop-opacity="0.18"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>
      </defs>
      <circle cx="{cx}" cy="{cy}" r="{r+170}" fill="url(#glow)"/>
      {ticks}
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E7DDFB" stroke-width="44"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#ag)" stroke-width="44" stroke-linecap="round"
              stroke-dasharray="{circ*0.68} {circ}" transform="rotate(-90 {cx} {cy})"/>
    ''')
    icon(img, ICONS["repeat"], cx - 75, cy - 75, 150, RD, 2)
    ft = font("open", 74, 800)
    rich_line(img, 0, 860, [("Quanto do seu dia", RP)], ft, align="center", center_x=540)
    rich_line(img, 0, 948, [("foi para tarefas", RP)], ft, align="center", center_x=540)
    rich_line(img, 0, 1036, [("que ", RP), ("se repetem?", ("grad", V, RD))], ft, align="center", center_x=540)
    paragraph(img, 0, 1112, "Seu tempo vale mais no que só você pode fazer.", font("open", 34, 400), "#4A3560",
              860, 48, align="center", center_x=540)
    logo(img, "cdx-h-cor.png", 540, 1205, width=270, anchor="mt")
    return save(img, f"{OUT}/condutrix-20h.png")


# ---------------- Negócio Pronto 10h ----------------
def np_10():
    img = canvas(MA)
    add_svg(img, f'''
      <defs><radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{AZ}" stop-opacity="0.45"/><stop offset="1" stop-color="{AZ}" stop-opacity="0"/></radialGradient>
      <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="2" fill="#FFFFFF" fill-opacity="0.07"/></pattern></defs>
      <rect width="1080" height="1350" fill="url(#dots)"/>
      <circle cx="1000" cy="180" r="420" fill="url(#g)"/>
    ''')
    logo(img, "np-n-azul.png", W - M, 250, height=230, anchor="rm", alpha=0.22)
    logo(img, "np-h-escuro.png", M, M, width=360)
    ft = font("noto", 104, 800)
    y = 400
    draw_text(img, (M, y), "Empreender", ft, hexc("#FFFFFF"))
    draw_text(img, (M, y + 118), "sem começar", ft, hexc("#FFFFFF"))
    grad_text(img, (M, y + 236), "do zero.", ft, "#5C78FF", AZ)
    paragraph(img, M, y + 320, "Um negócio pronto já chega estruturado para você começar a operar.",
              font("noto", 34, 400), LA, 820, 48)
    # painel
    box = (M, 860, W - M, 1170)
    rrect(img, box, 36, hexc("#1C2754"))
    rrect(img, box, 36, None, outline=hexc("#2C3A72"), width=2)
    draw_text(img, (M + 44, 920), "JÁ CHEGA COM", font("noto", 24, 700), hexc("#8EA0FF"))
    items = ["Marca e logo", "Site", "Redes sociais", "Anúncios"]
    for i, t in enumerate(items):
        col, row = i % 2, i // 2
        x = M + 44 + col * 430
        yy = 975 + row * 100
        add_svg(img, f'<circle cx="{x+26}" cy="{yy+26}" r="26" fill="{AZ}"/>')
        icon(img, ICONS["check"], x + 12, yy + 12, 28, "#FFFFFF", 3)
        draw_text(img, (x + 70, yy + 38), t, font("noto", 34, 600), hexc("#FFFFFF"))
    draw_text(img, (M, 1268), "Foque no que importa: vender e crescer.", font("noto", 30, 600), hexc("#FFFFFF"))
    add_svg(img, f'<circle cx="{W-M-32}" cy="1257" r="32" fill="{AZ}"/>')
    icon(img, ICONS["arrow"], W - M - 50, 1239, 36, "#FFFFFF", 2.6)
    return save(img, f"{OUT}/negocio-pronto-10h.png")


# ---------------- Negócio Pronto 16h ----------------
def np_16():
    img = canvas(CL)
    add_svg(img, f'''<defs><radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{LA}" stop-opacity="0.9"/><stop offset="1" stop-color="{LA}" stop-opacity="0"/></radialGradient></defs>
      <circle cx="1020" cy="120" r="380" fill="url(#g)"/>''')
    logo(img, "np-h-cor.png", M, M, width=340)
    f = font("noto", 24, 800)
    tw = text_w("DICA DO DIA", f)
    rrect(img, (M, 205, M + tw + 48, 253), 24, hexc(AZ))
    draw_text(img, (M + 24, 238), "DICA DO DIA", f, hexc("#FFFFFF"))
    ft = font("noto", 76, 800)
    draw_text(img, (M, 352), "Antes de escolher", ft, hexc(MA))
    draw_text(img, (M, 438), "seu negócio,", ft, hexc(MA))
    grad_text(img, (M, 524), "responda:", ft, AZ, "#5C78FF")
    qs = [("clock", "Quanto tempo vou dedicar?"), ("heart", "Combina com o que eu gosto de fazer?"),
          ("users", "Quem é o meu cliente?")]
    y0, hh, gap = 600, 150, 26
    for i, (ic, q) in enumerate(qs):
        y = y0 + i * (hh + gap)
        box = (M, y, W - M, y + hh)
        shadow(img, box, 32, color=(19, 27, 58, 30), blur=22, offset=(0, 10))
        rrect(img, box, 32, hexc("#FFFFFF"))
        draw_text(img, (M + 40, y + hh / 2 + 22), f"0{i+1}", font("noto", 60, 800), hexc(AZ))
        add_svg(img, f'<rect x="{M+150}" y="{y+36}" width="2" height="{hh-72}" fill="{CL}"/>')
        fq = font("noto", 36, 700)
        lines = wrap(q, fq, 560)
        lh = 46
        ty = y + hh / 2 + 13 - (len(lines) - 1) * lh / 2
        for j, ln in enumerate(lines):
            draw_text(img, (M + 184, ty + j * lh), ln, fq, hexc(MA))
        add_svg(img, f'<circle cx="{W-M-62}" cy="{y+hh/2}" r="34" fill="{CL}"/>')
        icon(img, ICONS[ic], W - M - 80, y + hh / 2 - 18, 36, AZ, 2.2)
    draw_text(img, (M, 1252), "Essas respostas mostram o caminho certo.", font("noto", 32, 600), hexc(MA))
    logo(img, "np-n-azul.png", W - M, 1265, height=58, anchor="rb")
    return save(img, f"{OUT}/negocio-pronto-16h.png")


# ---------------- Negócio Pronto 20h ----------------
def np_20():
    img = canvas("#FFFFFF")
    # painel ilustrado
    px0, py0, px1, py1 = M, M, W - M, 640
    add_svg(img, f'''
      <defs>
        <linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CL}"/><stop offset="1" stop-color="{LA}"/></linearGradient>
        <linearGradient id="ar" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{AZ}"/><stop offset="1" stop-color="#5C78FF"/></linearGradient>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.5"/></pattern>
        <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="{MA}" flood-opacity="0.18"/></filter>
      </defs>
      <rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" rx="44" fill="url(#pg)"/>
      <rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" rx="44" fill="url(#grid)"/>
      <g transform="rotate(-6 360 380)" filter="url(#sh)">
        <path d="M200 200 H460 L540 280 V560 H200 Z" fill="#FFFFFF"/>
        <path d="M460 200 V280 H540 Z" fill="#C8D2FF"/>
        <rect x="240" y="250" width="160" height="16" rx="8" fill="{MA}"/>
        <rect x="240" y="300" width="250" height="10" rx="5" fill="#C9D1EE"/>
        <rect x="240" y="330" width="210" height="10" rx="5" fill="#C9D1EE"/>
        <rect x="240" y="385" width="26" height="26" rx="7" fill="{AZ}"/>
        <rect x="282" y="393" width="170" height="10" rx="5" fill="#C9D1EE"/>
        <rect x="240" y="435" width="26" height="26" rx="7" fill="{AZ}"/>
        <rect x="282" y="443" width="140" height="10" rx="5" fill="#C9D1EE"/>
        <rect x="240" y="485" width="26" height="26" rx="7" fill="none" stroke="{AZ}" stroke-width="3"/>
        <rect x="282" y="493" width="180" height="10" rx="5" fill="#C9D1EE"/>
      </g>
      <path d="M470 470 C 600 470, 700 400, 800 230" fill="none" stroke="url(#ar)" stroke-width="22" stroke-linecap="round"/>
      <path d="M752 226 L812 196 L824 262" fill="none" stroke="#5C78FF" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
    ''')
    # checks brancos nos quadradinhos (rotacionados junto do papel, aproximação leve)
    ft = font("noto", 86, 800)
    y = 790
    draw_text(img, (M, y), "O plano de ter o", ft, hexc(MA))
    draw_text(img, (M, y + 100), "seu negócio pode", ft, hexc(MA))
    grad_text(img, (M, y + 200), "sair do papel.", ft, AZ, "#5C78FF")
    paragraph(img, M, y + 282, "Com um negócio pronto, você foca em fazer acontecer.", font("noto", 34, 400),
              "#3B4566", 860, 48)
    add_svg(img, f'<rect x="{M}" y="1192" width="{W-2*M}" height="2" fill="{CL}"/>')
    logo(img, "np-h-cor.png", M, 1236, width=300, anchor="lm")
    draw_text(img, (W - M, 1248), "negociopronto.com.br", font("noto", 28, 700), hexc(AZ), anchor="rs")
    return save(img, f"{OUT}/negocio-pronto-20h.png")


if __name__ == "__main__":
    which = sys.argv[2:] or ["cdx_10", "cdx_16", "cdx_20", "np_10", "np_16", "np_20"]
    for n in which:
        print(globals()[n]())
