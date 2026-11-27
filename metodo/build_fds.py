"""Artes de sexta 27/11 (16h e 20h), sábado 28/11 e domingo 29/11 de 2026.
Uso: python3 metodo/build_fds.py saida [funcao ...]
"""
import os
import sys
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "saida"
os.makedirs(OUT, exist_ok=True)

# Condutrix
RP, V, RD, LI, LC = "#290D3D", "#6D21FD", "#5F22D8", "#A67EF4", "#F6F2FD"
TXC = "#4A3560"
# Negócio Pronto
AZ, MA, CL, LA, AZ2 = "#2745F4", "#131B3A", "#E8EDFC", "#C8D2FF", "#5C78FF"
TXN = "#3B4566"
M = 88

ICONS.update({
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "wallet": '<path d="M20 7H5a2 2 0 0 1 0-4h13v4"/><path d="M3 5v14a2 2 0 0 0 2 2h15V7"/><path d="M16 14h.01"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "play": '<path d="M6 4l14 8-14 8z"/>',
    "bot": '<rect x="3" y="8" width="18" height="12" rx="3"/><path d="M12 8V4"/><circle cx="12" cy="3" r="1"/><path d="M9 14h.01M15 14h.01"/>',
    "cpu": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "trend": '<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
})


# ---------- utilidades ----------
def footer_cdx(img, y=1262, dark=RP):
    f1, f2 = font("open", 26, 700), font("open", 26, 400)
    draw_text(img, (M, y), "Condutrix", f1, hexc(dark))
    draw_text(img, (M + text_w("Condutrix ", f1), y), "Negócio Inteligente", f2, hexc(dark))
    draw_text(img, (W - M, y), "condutrix.com.br", font("open", 26, 600), hexc(V), anchor="rs")


def footer_np(img, y=1236, dark=False):
    add_svg(img, f'<rect x="{M}" y="{y-44}" width="{W-2*M}" height="2" fill="{"#26315E" if dark else CL}"/>')
    logo(img, "np-h-escuro.png" if dark else "np-h-cor.png", M, y, width=300, anchor="lm")
    draw_text(img, (W - M, y + 12), "negociopronto.com.br", font("noto", 28, 700),
              hexc("#8EA0FF" if dark else AZ), anchor="rs")


def chip(img, x, y, txt, fam, bg, fg, dot=None, size=24, h=50):
    f = font(fam, size, 700 if fam == "open" else 800)
    pad = 28
    extra = 22 if dot else 0
    tw = text_w(txt, f)
    rrect(img, (x, y, x + tw + 2 * pad + extra, y + h), h / 2, hexc(bg))
    if dot:
        add_svg(img, f'<circle cx="{x+pad+4}" cy="{y+h/2}" r="7" fill="{dot}"/>')
    draw_text(img, (x + pad + extra, y + h / 2 + size * 0.36), txt, f, hexc(fg))
    return x + tw + 2 * pad + extra


def grad_box(img, box, r, c1, c2, gid):
    x0, y0, x1, y1 = box
    add_svg(img, f'''<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
      <rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="{r}" fill="url(#{gid})"/>''')


def icon_tile(img, ic, x, y, s, c1, c2, gid, ic_color="#FFFFFF", r=None, stroke=2.2):
    grad_box(img, (x, y, x + s, y + s), r if r is not None else s * 0.28, c1, c2, gid)
    k = s * 0.5
    icon(img, ICONS[ic], x + (s - k) / 2, y + (s - k) / 2, k, ic_color, stroke)


def lines_block(img, x, y, lines, f, lh, align="left", cx=540):
    """lines: lista de segs para rich_line."""
    for i, segs in enumerate(lines):
        rich_line(img, x, y + i * lh, segs, f, align=align, center_x=cx)
    return y + (len(lines) - 1) * lh


def text_lines_centered(img, txt, f, color, maxw, y, lh):
    ls = wrap(txt, f, maxw)
    for i, ln in enumerate(ls):
        draw_text(img, (540, y + i * lh), ln, f, hexc(color), anchor="ms")
    return y + (len(ls) - 1) * lh


def glow(cx, cy, r, color, op, gid):
    return (f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>')


# =================== CONDUTRIX ===================

# Sexta 16h: mito ou verdade
def c27_16():
    img = canvas("#FFFFFF")
    add_svg(img, glow(980, 140, 420, LI, 0.30, "g1") + glow(60, 1250, 380, V, 0.10, "g2"))
    logo(img, "cdx-h-cor.png", M, M, width=290)
    chip(img, M, 236, "MITO OU VERDADE?", "open", LC, RD, dot=V)
    ft = font("open", 84, 800)
    lines_block(img, M, 420, [[("Automação é só", RP)], [("para empresa", RP)], [("grande?", ("grad", V, RD))]], ft, 96)
    # dois botões
    y = 668
    bw = (W - 2 * M - 28) / 2
    b1 = (M, y, M + bw, y + 150)
    rrect(img, b1, 34, hexc(LC))
    rrect(img, b1, 34, None, outline=hexc("#E3D8FA"), width=2)
    add_svg(img, f'<circle cx="{M+70}" cy="{y+75}" r="30" fill="#FFFFFF"/>')
    icon(img, ICONS["x"], M + 54, y + 59, 32, "#B9A6DE", 3)
    draw_text(img, (M + 122, y + 92), "Verdade", font("open", 42, 700), hexc("#B9A6DE"))
    b2 = (M + bw + 28, y, W - M, y + 150)
    shadow(img, b2, 34, color=(95, 34, 216, 70), blur=26, offset=(0, 16))
    grad_box(img, b2, 34, V, RD, "bg2")
    add_svg(img, f'<circle cx="{b2[0]+70}" cy="{y+75}" r="30" fill="#FFFFFF"/>')
    icon(img, ICONS["check"], b2[0] + 54, y + 59, 32, RD, 3.4)
    draw_text(img, (b2[0] + 122, y + 92), "Mito", font("open", 42, 800), hexc("#FFFFFF"))
    paragraph(img, M, 920, "A automação funciona para negócios de todos os tamanhos e começa pelas tarefas do dia a dia.",
              font("open", 36, 400), TXC, 880, 52)
    box = (M, 1050, W - M, 1190)
    rrect(img, box, 30, hexc(LC))
    add_svg(img, f'<rect x="{M}" y="1050" width="10" height="140" rx="5" fill="{V}"/>')
    icon(img, ICONS["repeat"], M + 44, 1092, 54, V, 2.2)
    fb = font("open", 32, 700)
    draw_text(img, (M + 128, 1110), "Se uma tarefa se repete,", fb, hexc(RP))
    draw_text(img, (M + 128, 1154), "ela pode ser automatizada.", fb, hexc(V))
    footer_cdx(img, 1270)
    return img


# Sexta 20h: trabalhar mais x crescer mais
def c27_20():
    img = canvas(LC)
    # gráfico: barras de horas x linha de crescimento
    x0, base = 150, 600
    bars = ""
    hs = [150, 210, 260, 300, 330]
    for i, h in enumerate(hs):
        bx = x0 + i * 120
        bars += f'<rect x="{bx}" y="{base-h}" width="70" height="{h}" rx="16" fill="#E4D9FA"/>'
    pts = [(x0 + 35 + i * 120, base - v) for i, v in enumerate([120, 150, 200, 290, 420])]
    path = "M" + " L".join(f"{a} {b}" for a, b in pts)
    add_svg(img, glow(540, 380, 470, V, 0.14, "g1") + f'''
      <defs><linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{LI}"/><stop offset="1" stop-color="{V}"/></linearGradient></defs>
      <rect x="{M}" y="{M}" width="{W-2*M}" height="600" rx="44" fill="#FFFFFF"/>
      {bars}
      <path d="{path}" fill="none" stroke="url(#ln)" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="22" fill="{V}"/>
      <circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="9" fill="#FFFFFF"/>
      <rect x="{x0-20}" y="{base}" width="640" height="3" rx="1.5" fill="#E4D9FA"/>
    ''')
    draw_text(img, (M + 52, 168), "Horas x crescimento", font("open", 26, 700), hexc(RD))
    add_svg(img, f'<rect x="{x0}" y="640" width="26" height="14" rx="7" fill="#E4D9FA"/><rect x="{x0+330}" y="640" width="26" height="14" rx="7" fill="{V}"/>')
    draw_text(img, (x0 + 40, 655), "Horas", font("open", 22, 600), hexc("#8A7AA6"))
    draw_text(img, (x0 + 370, 655), "Crescimento", font("open", 22, 600), hexc(RD))
    ft = font("open", 74, 800)
    lines_block(img, M, 808, [[("Trabalhar mais não é", RP)], [("o mesmo que ", RP), ("crescer", ("grad", V, RD))],
                               [("mais.", ("grad", V, RD))]], ft, 86)
    paragraph(img, M, 1066, "Crescer é colocar o seu tempo no que realmente move o negócio.",
              font("open", 34, 400), TXC, 860, 48)
    chip(img, M, 1162, "Bom fim de semana", "open", "#FFFFFF", RD, dot=V, size=24, h=50)
    footer_cdx(img, 1282)
    return img


# Sábado 10h: 3 passos
def c28_10():
    img = canvas("#FFFFFF")
    add_svg(img, glow(1000, 120, 380, LI, 0.30, "g1"))
    logo(img, "cdx-ab-cor.png", W - M, M, height=58, anchor="rt")
    chip(img, M, M, "PASSO A PASSO", "open", LC, RD, dot=V)
    ft = font("open", 78, 800)
    lines_block(img, M, 300, [[("Como começar a", RP)], [("automatizar em", RP)], [("3 passos", ("grad", V, RD))]], ft, 90)
    steps = [("list", "Liste", "as tarefas que você repete toda semana."),
             ("target", "Escolha", "a que mais toma o seu tempo."),
             ("zap", "Deixe a IA fazer", "e acompanhe o resultado.")]
    y0, hh, gap = 545, 162, 24
    # linha guia
    add_svg(img, f'<rect x="{M+57}" y="{y0+60}" width="4" height="{2*(hh+gap)}" rx="2" fill="#E4D9FA"/>')
    for i, (ic, b, t) in enumerate(steps):
        y = y0 + i * (hh + gap)
        box = (M + 140, y, W - M, y + hh)
        shadow(img, box, 30, color=(41, 13, 61, 28), blur=22, offset=(0, 10))
        rrect(img, box, 30, hexc(LC))
        add_svg(img, f'<circle cx="{M+59}" cy="{y+hh/2}" r="46" fill="#FFFFFF" stroke="#E4D9FA" stroke-width="3"/>')
        grad_text(img, (M + 59, y + hh / 2 + 18), str(i + 1), font("open", 50, 800), V, RD, anchor="ms")
        icon_tile(img, ic, M + 172, y + 37, 88, V, RD, f"t{i}")
        draw_text(img, (M + 290, y + 68), b, font("open", 36, 800), hexc(RP))
        paragraph(img, M + 290, y + 112, t, font("open", 28, 400), TXC, 520, 38)
    draw_text(img, (M, 1166), "Uma tarefa de cada vez já muda a rotina.", font("open", 32, 700), hexc(V))
    add_svg(img, f'<rect x="{M}" y="1206" width="{W-2*M}" height="2" fill="{LC}"/>')
    footer_cdx(img, 1270)
    return img


# Sábado 16h: atendimento
def c28_16():
    img = canvas(LC)
    add_svg(img, glow(540, 470, 520, V, 0.12, "g1"))
    logo(img, "cdx-h-cor.png", M, M, width=290)
    # janela de chat
    box = (M, 210, W - M, 740)
    shadow(img, box, 44, color=(41, 13, 61, 40), blur=34, offset=(0, 18))
    rrect(img, box, 44, hexc("#FFFFFF"))
    add_svg(img, f'<rect x="{M}" y="210" width="{W-2*M}" height="104" rx="44" fill="{LC}" fill-opacity="0.6"/>'
                 f'<rect x="{M}" y="270" width="{W-2*M}" height="44" fill="#FFFFFF"/>')
    icon_tile(img, "bot", M + 36, 226, 72, V, RD, "av", r=36)
    draw_text(img, (M + 128, 258), "Atendimento", font("open", 28, 700), hexc(RP))
    add_svg(img, f'<circle cx="{M+136}" cy="282" r="7" fill="#22C55E"/>')
    draw_text(img, (M + 152, 292), "online agora", font("open", 22, 400), hexc("#6B5A80"))
    # bolha cliente
    fq = font("open", 30, 400)
    q = "Oi, qual é o prazo de entrega?"
    qw = text_w(q, fq) + 64
    rrect(img, (W - M - 36 - qw, 350, W - M - 36, 430), 30, hexc(LC))
    draw_text(img, (W - M - 36 - qw + 32, 401), q, fq, hexc(RP))
    draw_text(img, (W - M - 36, 462), "Cliente  09:41", font("open", 20, 400), hexc("#9A8BB5"), anchor="rs")
    # resposta
    grad_box(img, (M + 36, 490, M + 36 + 690, 646), 30, V, RD, "rb")
    fa = font("open", 30, 400)
    draw_text(img, (M + 68, 552), "Oi! O prazo é de 2 dias úteis.", fa, hexc("#FFFFFF"))
    draw_text(img, (M + 68, 600), "Posso ajudar em algo mais?", fa, hexc("#FFFFFF"))
    icon(img, ICONS["zap"], M + 36, 664, 24, V, 2.4)
    draw_text(img, (M + 68, 684), "Respondido em 3 segundos", font("open", 22, 600), hexc(V))
    ft = font("open", 80, 800)
    lines_block(img, M, 900, [[("Cliente bem atendido", RP)], [("não espera.", ("grad", V, RD))]], ft, 92)
    paragraph(img, M, 1070, "A IA responde as perguntas frequentes na hora, e sua equipe fica livre para os casos que pedem atenção.",
              font("open", 33, 400), TXC, 880, 47)
    footer_cdx(img, 1282)
    return img


# Sábado 20h: descanso
def c28_20():
    img = canvas(LC)
    cx, cy = 540, 440
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{LI}" fill-opacity="{o}"/>' for x, y, r, o in
                    [(250, 210, 5, .8), (830, 180, 6, .9), (900, 420, 4, .6), (190, 520, 4, .6), (760, 650, 5, .7), (300, 690, 3, .5), (640, 150, 3, .6)])
    add_svg(img, glow(cx, cy, 420, V, 0.18, "g1") + f'''
      <defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{RD}"/></linearGradient>
      <mask id="cres"><rect width="1080" height="1350" fill="#fff"/><circle cx="{cx+95}" cy="{cy-75}" r="170" fill="#000"/></mask></defs>
      <circle cx="{cx}" cy="{cy}" r="290" fill="none" stroke="{LI}" stroke-opacity="0.25" stroke-width="2"/>
      <circle cx="{cx}" cy="{cy}" r="360" fill="none" stroke="{LI}" stroke-opacity="0.14" stroke-width="2"/>
      <circle cx="{cx}" cy="{cy}" r="210" fill="url(#mg)"/><circle cx="{cx+95}" cy="{cy-75}" r="170" fill="{LC}"/>
      {stars}
    ''')
    # cartão de status
    box = (240, 720, 840, 820)
    shadow(img, box, 50, color=(41, 13, 61, 45), blur=26, offset=(0, 12))
    rrect(img, box, 50, hexc("#FFFFFF"))
    draw_text(img, (300, 784), "Rotina no automático", font("open", 30, 700), hexc(RP))
    add_svg(img, f'''<defs><linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{RD}"/></linearGradient></defs>
      <rect x="{840-60-96}" y="746" width="96" height="48" rx="24" fill="url(#tg)"/><circle cx="{840-60-24}" cy="770" r="18" fill="#FFFFFF"/>''')
    ft = font("open", 80, 800)
    lines_block(img, 0, 940, [[("Fim de semana é", RP)], [("para ", RP), ("descansar.", ("grad", V, RD))]], ft, 94,
                align="center")
    text_lines_centered(img, "A rotina pode seguir no automático enquanto você recarrega.", font("open", 34, 400), TXC, 800, 1100, 48)
    logo(img, "cdx-h-cor.png", 540, 1215, width=250, anchor="mt")
    return img


# Domingo 10h: assinatura
def c29_10():
    img = canvas("#FFFFFF")
    add_svg(img, glow(960, 180, 440, LI, 0.32, "g1") + glow(80, 900, 300, V, 0.08, "g2"))
    logo(img, "cdx-h-cor.png", M, M, width=290)
    chip(img, M, 236, "ASSINATURA CONDUTRIX", "open", LC, RD, dot=V)
    ft = font("open", 92, 800)
    lines_block(img, M, 420, [[("Automação", RP)], [("sem projeto", RP)], [("gigante.", ("grad", V, RD))]], ft, 104)
    paragraph(img, M, 722, "Você assina e a gente coloca a rotina do seu negócio para rodar com IA.",
              font("open", 34, 400), TXC, 860, 48)
    items = [("calendar", "Rotina organizada"), ("zap", "Menos trabalho manual"), ("clock", "Mais tempo para decidir")]
    y0, hh, gap = 858, 98, 16
    for i, (ic, t) in enumerate(items):
        y = y0 + i * (hh + gap)
        rrect(img, (M, y, W - M, y + hh), 28, hexc(LC))
        icon_tile(img, ic, M + 18, y + 15, 68, V, RD, f"i{i}")
        draw_text(img, (M + 116, y + hh / 2 + 12), t, font("open", 34, 600), hexc(RP))
        add_svg(img, f'<circle cx="{W-M-52}" cy="{y+hh/2}" r="24" fill="#FFFFFF"/>')
        icon(img, ICONS["check"], W - M - 66, y + hh / 2 - 14, 28, V, 3)
    footer_cdx(img, 1270)
    return img


# Domingo 16h: antes e depois
def c29_16():
    img = canvas(LC)
    logo(img, "cdx-h-cor.png", M, M, width=290)
    ft = font("open", 78, 800)
    lines_block(img, M, 300, [[("Antes e depois", RP)], [("da ", RP), ("automação", ("grad", V, RD))]], ft, 90)
    cw = (W - 2 * M - 24) / 2
    y0, y1 = 440, 1150
    a = (M, y0, M + cw, y1)
    b = (M + cw + 24, y0, W - M, y1)
    rrect(img, a, 40, hexc("#FFFFFF"))
    shadow(img, b, 40, color=(95, 34, 216, 70), blur=30, offset=(0, 16))
    grad_box(img, b, 40, V, RD, "dp")
    draw_text(img, (a[0] + 40, y0 + 80), "ANTES", font("open", 28, 800), hexc("#9A8BB5"))
    draw_text(img, (b[0] + 40, y0 + 80), "DEPOIS", font("open", 28, 800), hexc("#FFFFFF"))
    antes = ["Copiar dados à mão", "Responder a mesma pergunta várias vezes", "Lembrar de tudo de cabeça"]
    depois = ["Dados lançados sozinhos", "Respostas na hora", "Lembretes automáticos"]
    fi = font("open", 31, 600)
    for i in range(3):
        y = y0 + 140 + i * 190
        add_svg(img, f'<circle cx="{a[0]+66}" cy="{y+26}" r="26" fill="{LC}"/>')
        icon(img, ICONS["x"], a[0] + 52, y + 12, 28, "#B9A6DE", 3)
        paragraph(img, a[0] + 40, y + 102, antes[i], fi, "#6B5A80", cw - 80, 42)
        add_svg(img, f'<circle cx="{b[0]+66}" cy="{y+26}" r="26" fill="#FFFFFF"/>')
        icon(img, ICONS["check"], b[0] + 52, y + 12, 28, RD, 3.2)
        paragraph(img, b[0] + 40, y + 102, depois[i], fi, "#FFFFFF", cw - 80, 42)
        if i < 2:
            add_svg(img, f'<rect x="{a[0]+40}" y="{y+164}" width="{cw-80}" height="2" fill="{LC}"/>'
                         f'<rect x="{b[0]+40}" y="{y+164}" width="{cw-80}" height="2" fill="#FFFFFF" fill-opacity="0.18"/>')
    footer_cdx(img, 1262)
    return img


# Domingo 20h: qual tarefa sai da lista
def c29_20():
    img = canvas("#FFFFFF")
    add_svg(img, glow(540, 420, 520, LI, 0.26, "g1"))
    logo(img, "cdx-ab-cor.png", 540, M, height=62, anchor="mt")
    # lista
    box = (170, 220, 910, 690)
    shadow(img, box, 40, color=(41, 13, 61, 40), blur=30, offset=(0, 16))
    rrect(img, box, 40, hexc("#FFFFFF"))
    draw_text(img, (220, 296), "Lista da segunda", font("open", 30, 800), hexc(RP))
    chip(img, 660, 258, "SEMANA NOVA", "open", LC, RD, size=18, h=40)
    tasks = [("Responder as mesmas perguntas", True), ("Lançar pedidos na planilha", True),
             ("Reunião com a equipe", False), ("Visitar um cliente", False)]
    for i, (t, done) in enumerate(tasks):
        y = 350 + i * 82
        if done:
            grad_box(img, (220, y, 262, y + 42), 12, V, RD, f"cb{i}")
            icon(img, ICONS["check"], 227, y + 7, 28, "#FFFFFF", 3.2)
            f = font("open", 29, 400)
            draw_text(img, (290, y + 32), t, f, hexc("#A89BC0"))
            add_svg(img, f'<rect x="290" y="{y+21}" width="{text_w(t, f)}" height="3" rx="1.5" fill="{V}"/>')
        else:
            rrect(img, (220, y, 262, y + 42), 12, None, outline=hexc("#D6C8F6"), width=3)
            draw_text(img, (290, y + 32), t, font("open", 29, 600), hexc(RP))
    ft = font("open", 78, 800)
    lines_block(img, 0, 850, [[("Qual tarefa sai da", RP)], [("sua lista ", RP), ("na segunda?", ("grad", V, RD))]], ft, 92,
                align="center")
    text_lines_centered(img, "Semana nova pede uma rotina mais leve. Conta pra gente nos comentários.",
                        font("open", 33, 400), TXC, 820, 1010, 47)
    footer_cdx(img, 1270)
    return img


# =================== NEGÓCIO PRONTO ===================

# Sexta 16h: da ideia ao negócio funcionando
def n27_16():
    img = canvas(CL)
    add_svg(img, glow(1020, 120, 380, LA, 0.9, "g1"))
    logo(img, "np-h-cor.png", M, M, width=320)
    ft = font("noto", 80, 800)
    lines_block(img, M, 330, [[("Da ideia ao seu", MA)], [("negócio ", MA), ("funcionando", ("grad", AZ, AZ2))]], ft, 92)
    steps = [("search", "Escolha", "o negócio que combina com você."),
             ("box", "Receba", "tudo estruturado e pronto para usar."),
             ("play", "Comece", "a operar e foque em vender.")]
    y0, hh, gap = 470, 190, 30
    add_svg(img, f'<path d="M{M+60} {y0+95} V{y0+2*(hh+gap)+95}" stroke="{AZ}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>')
    for i, (ic, b, t) in enumerate(steps):
        y = y0 + i * (hh + gap)
        add_svg(img, f'<circle cx="{M+60}" cy="{y+95}" r="60" fill="{AZ}"/>')
        icon(img, ICONS[ic], M + 36, y + 71, 48, "#FFFFFF", 2.4)
        box = (M + 156, y, W - M, y + hh)
        shadow(img, box, 32, color=(19, 27, 58, 30), blur=22, offset=(0, 10))
        rrect(img, box, 32, hexc("#FFFFFF"))
        draw_text(img, (M + 196, y + 70), f"PASSO {i+1}", font("noto", 22, 800), hexc(AZ))
        draw_text(img, (M + 196, y + 122), b, font("noto", 40, 800), hexc(MA))
        draw_text(img, (M + 196, y + 164), t, font("noto", 28, 400), hexc(TXN))
    draw_text(img, (M, 1166), "O primeiro passo é seu.", font("noto", 36, 800), hexc(AZ))
    footer_np(img, 1266)
    return img


# Sexta 20h: decisão
def n27_20():
    img = canvas(MA)
    add_svg(img, f'''<defs><pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="2" fill="#FFFFFF" fill-opacity="0.06"/></pattern></defs>
      <rect width="1080" height="1350" fill="url(#dots)"/>''' + glow(540, 1350, 640, AZ, 0.45, "g1"))
    logo(img, "np-n-azul.png", W - 40, 1150, height=460, anchor="rb", alpha=0.12)
    logo(img, "np-h-escuro.png", M, M, width=340)
    ft = font("noto", 108, 800)
    lines_block(img, M, 520, [[("Todo negócio", "#FFFFFF")], [("começou com", "#FFFFFF")], [("uma decisão.", "#FFFFFF")]], ft, 126)
    add_svg(img, f'<rect x="{M}" y="850" width="120" height="8" rx="4" fill="{AZ}"/>')
    grad_text(img, (M, 990), "Qual vai ser a sua?", font("noto", 72, 800), "#8EA0FF", AZ2)
    footer_np(img, 1236, dark=True)
    return img


# Sábado 10h: checklist
def n28_10():
    img = canvas("#FFFFFF")
    add_svg(img, glow(1000, 140, 380, LA, 0.8, "g1"))
    logo(img, "np-h-cor.png", M, M, width=320)
    chip(img, M, 206, "CHECKLIST", "noto", AZ, "#FFFFFF", size=24, h=50)
    ft = font("noto", 80, 800)
    lines_block(img, M, 360, [[("Antes de empreender,", MA)], [("organize isto:", ("grad", AZ, AZ2))]], ft, 92)
    items = [("target", "Seu objetivo", True), ("wallet", "Suas finanças pessoais", True),
             ("clock", "Seu tempo", False), ("users", "O seu mercado", False)]
    y0, hh, gap = 470, 128, 20
    for i, (ic, t, done) in enumerate(items):
        y = y0 + i * (hh + gap)
        box = (M, y, W - M, y + hh)
        rrect(img, box, 30, hexc(CL))
        if done:
            rrect(img, (M + 36, y + 36, M + 92, y + 92), 16, hexc(AZ))
            icon(img, ICONS["check"], M + 46, y + 46, 36, "#FFFFFF", 3.2)
        else:
            rrect(img, (M + 36, y + 36, M + 92, y + 92), 16, hexc("#FFFFFF"), outline=hexc(LA), width=3)
        draw_text(img, (M + 126, y + hh / 2 + 14), t, font("noto", 38, 700), hexc(MA))
        add_svg(img, f'<circle cx="{W-M-64}" cy="{y+hh/2}" r="38" fill="#FFFFFF"/>')
        icon(img, ICONS[ic], W - M - 84, y + hh / 2 - 20, 40, AZ, 2.2)
    draw_text(img, (M, 1140), "Quantos itens você já marcou?", font("noto", 34, 800), hexc(AZ))
    footer_np(img, 1266)
    return img


# Sábado 16h: do zero x negócio pronto
def n28_16():
    img = canvas(CL)
    logo(img, "np-h-cor.png", M, M, width=320)
    ft = font("noto", 84, 800)
    lines_block(img, M, 320, [[("Do zero ou", MA)], [("negócio pronto?", ("grad", AZ, AZ2))]], ft, 96)
    cw = (W - 2 * M - 24) / 2
    y0, y1 = 470, 1150
    a = (M, y0, M + cw, y1)
    b = (M + cw + 24, y0, W - M, y1)
    rrect(img, a, 40, hexc("#FFFFFF"))
    shadow(img, b, 40, color=(39, 69, 244, 70), blur=30, offset=(0, 16))
    rrect(img, b, 40, hexc(AZ))
    draw_text(img, (a[0] + 40, y0 + 80), "DO ZERO", font("noto", 28, 800), hexc("#8A93B2"))
    draw_text(img, (b[0] + 40, y0 + 80), "NEGÓCIO PRONTO", font("noto", 28, 800), hexc("#FFFFFF"))
    zero = ["Criar a marca", "Montar site e redes", "Descobrir tudo sozinho"]
    pronto = ["Marca, site e redes prontos", "Estrutura já configurada", "Começa pelo que gera venda"]
    fi = font("noto", 31, 600)
    for i in range(3):
        y = y0 + 140 + i * 186
        add_svg(img, f'<circle cx="{a[0]+66}" cy="{y+26}" r="26" fill="{CL}"/>')
        icon(img, ICONS["x"], a[0] + 52, y + 12, 28, "#9AA6CF", 3)
        paragraph(img, a[0] + 40, y + 102, zero[i], fi, "#5A6385", cw - 80, 42)
        add_svg(img, f'<circle cx="{b[0]+66}" cy="{y+26}" r="26" fill="#FFFFFF"/>')
        icon(img, ICONS["check"], b[0] + 52, y + 12, 28, AZ, 3.2)
        paragraph(img, b[0] + 40, y + 102, pronto[i], fi, "#FFFFFF", cw - 80, 42)
        if i < 2:
            add_svg(img, f'<rect x="{a[0]+40}" y="{y+160}" width="{cw-80}" height="2" fill="{CL}"/>'
                         f'<rect x="{b[0]+40}" y="{y+160}" width="{cw-80}" height="2" fill="#FFFFFF" fill-opacity="0.22"/>')
    footer_np(img, 1266)
    return img


# Sábado 20h: planejar o próximo passo
def n28_20():
    img = canvas("#FFFFFF")
    # calendário
    box = (M, M, W - M, 620)
    add_svg(img, f'''<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CL}"/><stop offset="1" stop-color="{LA}"/></linearGradient>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.5"/></pattern></defs>
      <rect x="{M}" y="{M}" width="{W-2*M}" height="{620-M}" rx="44" fill="url(#pg)"/>
      <rect x="{M}" y="{M}" width="{W-2*M}" height="{620-M}" rx="44" fill="url(#grid)"/>''')
    cb = (230, 170, 850, 560)
    shadow(img, cb, 36, color=(19, 27, 58, 40), blur=26, offset=(0, 14))
    rrect(img, cb, 36, hexc("#FFFFFF"))
    rrect(img, (230, 170, 850, 270), 36, hexc(MA))
    add_svg(img, f'<rect x="230" y="236" width="620" height="34" fill="{MA}"/>')
    draw_text(img, (270, 236), "Próximo passo", font("noto", 32, 800), hexc("#FFFFFF"))
    icon(img, ICONS["calendar"], 778, 196, 44, "#8EA0FF", 2.2)
    days = ["S", "T", "Q", "Q", "S", "S", "D"]
    for i, d in enumerate(days):
        x = 284 + i * 86
        if i == 5:
            add_svg(img, f'<circle cx="{x}" cy="330" r="34" fill="{AZ}"/>')
            draw_text(img, (x, 341), d, font("noto", 28, 800), hexc("#FFFFFF"), anchor="ms")
        else:
            draw_text(img, (x, 341), d, font("noto", 28, 700), hexc("#9AA6CF"), anchor="ms")
    rows = [("edit", "Pensar no negócio que quero ter", True), ("target", "Definir o primeiro objetivo", False)]
    for j, (ic, t, hi) in enumerate(rows):
        y = 400 + j * 76
        rrect(img, (270, y, 810, y + 60), 18, hexc(CL if hi else "#F5F7FE"))
        icon(img, ICONS[ic], 290, y + 15, 30, AZ, 2.2)
        draw_text(img, (338, y + 41), t, font("noto", 25, 700 if hi else 500), hexc(MA if hi else "#6A7396"))
    ft = font("noto", 80, 800)
    y = 780
    lines_block(img, M, y, [[("Sábado também é", MA)], [("dia de planejar o", MA)], [("próximo passo.", ("grad", AZ, AZ2))]], ft, 94)
    paragraph(img, M, y + 290, "Separe um momento hoje para pensar no negócio que você quer ter.", font("noto", 33, 400),
              TXN, 880, 46)
    footer_np(img, 1266)
    return img


# Domingo 10h: nasce com tecnologia
def n29_10():
    img = canvas(MA)
    # circuitos
    circ = ""
    for k, (x, y, dx, dy) in enumerate([(700, 140, 240, 0), (760, 220, 200, 120), (640, 330, 300, 0), (820, 420, 120, -80)]):
        circ += f'<path d="M{x} {y} h{dx*0.6} l{dx*0.2} {dy*0.3}" fill="none" stroke="{AZ}" stroke-opacity="0.5" stroke-width="3"/>'
        circ += f'<circle cx="{x}" cy="{y}" r="7" fill="{AZ2}"/>'
    add_svg(img, f'''<defs><pattern id="grid" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="#FFFFFF" stroke-opacity="0.04" stroke-width="1.5"/></pattern></defs>
      <rect width="1080" height="1350" fill="url(#grid)"/>''' + glow(900, 260, 460, AZ, 0.5, "g1"))
    icon_tile(img, "cpu", 780, 190, 200, AZ, AZ2, "cp", r=48, stroke=1.6)
    logo(img, "np-h-escuro.png", M, M, width=340)
    ft = font("noto", 96, 800)
    lines_block(img, M, 520, [[("Seu negócio", "#FFFFFF")], [("nasce com", "#FFFFFF")], [("tecnologia.", ("grad", "#8EA0FF", AZ2))]], ft, 112)
    paragraph(img, M, 840, "O Negócio Pronto faz parte do grupo Condutrix, que trabalha com automação e inteligência artificial.",
              font("noto", 34, 400), LA, 880, 48)
    box = (M, 990, W - M, 1150)
    rrect(img, box, 34, hexc("#1C2754"))
    rrect(img, box, 34, None, outline=hexc("#2C3A72"), width=2)
    draw_text(img, (M + 44, 1080), "UM NEGÓCIO DO GRUPO", font("noto", 24, 800), hexc("#8EA0FF"))
    logo(img, "cdx-h-branca.png", W - M - 44, 1070, width=300, anchor="rm")
    footer_np(img, 1262, dark=True)
    return img


# Domingo 16h: 3 erros
def n29_16():
    img = canvas(CL)
    add_svg(img, glow(1020, 120, 380, LA, 0.9, "g1"))
    logo(img, "np-h-cor.png", M, M, width=320)
    grad_text(img, (M - 8, 470), "3", font("noto", 300, 800), AZ, AZ2)
    fx = M + 200
    ft = font("noto", 64, 800)
    draw_text(img, (fx, 318), "erros de quem", ft, hexc(MA))
    draw_text(img, (fx, 394), "está", ft, hexc(MA))
    grad_text(img, (fx + text_w("está ", ft), 394), "começando", ft, AZ, AZ2)
    errs = [("Começar sem planejar", "Sem plano, cada decisão vira um chute."),
            ("Querer fazer tudo sozinho", "Estrutura pronta divide o peso."),
            ("Desistir antes de testar", "Dê tempo para ver o que funciona.")]
    y0, hh, gap = 520, 176, 24
    for i, (t, s) in enumerate(errs):
        y = y0 + i * (hh + gap)
        box = (M, y, W - M, y + hh)
        shadow(img, box, 32, color=(19, 27, 58, 30), blur=22, offset=(0, 10))
        rrect(img, box, 32, hexc("#FFFFFF"))
        add_svg(img, f'<circle cx="{M+80}" cy="{y+hh/2}" r="44" fill="{CL}"/>')
        icon(img, ICONS["x"], M + 58, y + hh / 2 - 22, 44, AZ, 3)
        draw_text(img, (M + 158, y + 80), t, font("noto", 38, 800), hexc(MA))
        draw_text(img, (M + 158, y + 126), s, font("noto", 27, 400), hexc(TXN))
        draw_text(img, (W - M - 36, y + 80), f"0{i+1}", font("noto", 30, 800), hexc(LA), anchor="rs")
    draw_text(img, (M, 1160), "Qual desses você quer evitar?", font("noto", 34, 800), hexc(AZ))
    footer_np(img, 1266)
    return img


# Domingo 20h: semana que vem
def n29_20():
    img = canvas("#FFFFFF")
    add_svg(img, glow(540, 330, 520, LA, 0.75, "g1"))
    logo(img, "np-n-azul.png", 540, M, height=80, anchor="mt")
    # faixa da semana
    days = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
    bw, gap = 108, 14
    x0 = (W - (7 * bw + 6 * gap)) / 2
    y = 260
    for i, d in enumerate(days):
        x = x0 + i * (bw + gap)
        if i == 0:
            shadow(img, (x, y - 20, x + bw, y + 220), 30, color=(39, 69, 244, 80), blur=22, offset=(0, 12))
            grad_box(img, (x, y - 20, x + bw, y + 220), 30, AZ, AZ2, "sg")
            draw_text(img, (x + bw / 2, y + 50), d, font("noto", 26, 800), hexc("#FFFFFF"), anchor="ms")
            icon(img, ICONS["flag"], x + bw / 2 - 24, y + 100, 48, "#FFFFFF", 2.4)
        else:
            rrect(img, (x, y, x + bw, y + 200), 28, hexc(CL))
            draw_text(img, (x + bw / 2, y + 50), d, font("noto", 24, 700), hexc("#8A93B2"), anchor="ms")
            add_svg(img, f'<rect x="{x+28}" y="{y+110}" width="{bw-56}" height="8" rx="4" fill="{LA}"/>'
                         f'<rect x="{x+28}" y="{y+136}" width="{(bw-56)*0.6}" height="8" rx="4" fill="{LA}"/>')
    draw_text(img, (x0 + bw / 2, y + 290), "o começo", font("noto", 26, 800), hexc(AZ), anchor="ms")
    add_svg(img, f'<path d="M{x0+bw/2} {y+234} v18" stroke="{AZ}" stroke-width="4" stroke-linecap="round"/>')
    ft = font("noto", 82, 800)
    lines_block(img, 0, 760, [[("A semana que vem", MA)], [("pode ser o começo", MA)], [("do seu negócio.", ("grad", AZ, AZ2))]], ft, 96,
                align="center")
    text_lines_centered(img, "Comece a semana com um plano.", font("noto", 36, 600), TXN, 860, 1066, 50)
    footer_np(img, 1266)
    return img


JOBS = {
    "2026-11-27": [("condutrix-16h", c27_16), ("condutrix-20h", c27_20), ("negocio-pronto-16h", n27_16), ("negocio-pronto-20h", n27_20)],
    "2026-11-28": [("condutrix-10h", c28_10), ("condutrix-16h", c28_16), ("condutrix-20h", c28_20),
                   ("negocio-pronto-10h", n28_10), ("negocio-pronto-16h", n28_16), ("negocio-pronto-20h", n28_20)],
    "2026-11-29": [("condutrix-10h", c29_10), ("condutrix-16h", c29_16), ("condutrix-20h", c29_20),
                   ("negocio-pronto-10h", n29_10), ("negocio-pronto-16h", n29_16), ("negocio-pronto-20h", n29_20)],
}

if __name__ == "__main__":
    only = set(sys.argv[2:])
    for day, jobs in JOBS.items():
        os.makedirs(f"{OUT}/{day}", exist_ok=True)
        for name, fn in jobs:
            if only and fn.__name__ not in only:
                continue
            img = fn()
            out = img.convert("RGB").resize((W, H), Image.LANCZOS)
            path = f"{OUT}/{day}/{name}.jpg"
            out.save(path, "JPEG", quality=95, subsampling=0, optimize=True)
            print(path)
