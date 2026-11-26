# Método das artes (Condutrix e Negócio Pronto)

Gera as artes em 1080x1350 (4:5), sem faixas brancas, com os logos e fontes oficiais.

Requisitos: Python 3, Pillow e cairosvg (`python3 -m pip install pillow cairosvg`).

Gerar: `python3 metodo/build.py saida` (ou só algumas: `python3 metodo/build.py saida cdx_10 np_16`).

Publicar o dia:
1. Converter para JPEG q95 e salvar em `AAAA-MM-DD/<empresa>-<hora>.jpg`.
2. `git add AAAA-MM-DD && git commit -m "Artes de AAAA-MM-DD" && git push origin main`
3. Mandar ao conector o link `https://raw.githubusercontent.com/Condutrix/redes/main/AAAA-MM-DD/<arquivo>.jpg` com `ajustar_imagem` falso.
