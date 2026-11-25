"""Kit de identidade das redes — FORTÍS SOLUÇÕES MATCON.

Gera fotos de perfil e capas no padrão oficial (logo oficial, azul #0E1F39, dourado #D9B579).
Uso: python3 especiais/kit-redes.py  ->  posts/kit-redes/*.png
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from gerador import CSS_BASE, A  # mesma identidade das artes do Instagram

SAIDA = os.path.join(os.path.dirname(AQUI), "posts", "kit-redes")
os.makedirs(SAIDA, exist_ok=True)

CSS = CSS_BASE + """
.sany{position:absolute;bottom:0;filter:drop-shadow(0 0 40px rgba(217,181,121,.22)) drop-shadow(0 20px 30px rgba(0,0,0,.6))}
.bloco{position:absolute;display:flex;align-items:center}
.bloco .col{display:flex;flex-direction:column;align-items:flex-start}
.k{font-weight:600;color:var(--gold);text-transform:uppercase}
.t{font-family:Osw;font-weight:700;text-transform:uppercase;line-height:1.05}
.s{font-weight:500;color:#e9edf5}
.s b{color:var(--gold);font-weight:700}
.site{font-weight:700;color:var(--gold)}
.linha{height:2px;background:linear-gradient(90deg,var(--gold),transparent)}
.ring{position:absolute;border-radius:50%;border:2px solid rgba(217,181,121,.55)}
"""

def beams(w, h, e=1.0):
    return f"""
  <div class="glow" style="width:{int(700*e)}px;height:{int(260*e)}px;left:{int(-200*e)}px;top:{int(h*.70)}px;background:rgba(217,181,121,.20)"></div>
  <div class="glow" style="width:{int(640*e)}px;height:{int(240*e)}px;right:{int(-220*e)}px;top:{int(h*.05)}px;background:rgba(217,181,121,.15)"></div>
  <div class="beam" style="width:{int(w*.55)}px;left:{int(-w*.05)}px;top:{int(h*.86)}px;transform:rotate(-8deg)"></div>
  <div class="beam" style="width:{int(w*.42)}px;left:{int(-w*.03)}px;top:{int(h*.92)}px;transform:rotate(-5deg);opacity:.5"></div>
  <div class="beam" style="width:{int(w*.40)}px;left:{int(w*.68)}px;top:{int(h*.30)}px;transform:rotate(-20deg);opacity:.5"></div>
  <div class="beam" style="width:{int(w*.30)}px;left:{int(w*.74)}px;top:{int(h*.38)}px;transform:rotate(-20deg);opacity:.28"></div>"""

def doc(w, h, corpo):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="arte" style="width:{w}px;height:{h}px">{corpo}</div></body></html>"""

def texto(esc, largura_titulo):
    # esc = escala base de fonte
    return f"""<div class="col" style="max-width:{largura_titulo+60}px">
      <div class="k" style="font-size:{int(15*esc)}px;letter-spacing:{int(5*esc)}px">Consultoria e tecnologia · Lojas MATCON</div>
      <div class="linha" style="width:{int(220*esc)}px;margin:{int(12*esc)}px 0 {int(14*esc)}px"></div>
      <div class="t metal" style="font-size:{int(46*esc)}px;width:{largura_titulo}px">Gestão e performance para lojas de material de construção</div>
      <div class="s" style="font-size:{int(17*esc)}px;margin-top:{int(16*esc)}px">Consultoria <b>·</b> FORTÍS FLOW <b>·</b> FORTÍS OBRAS <b>·</b> Academia Fortís</div>
      <div class="site" style="font-size:{int(18*esc)}px;margin-top:{int(12*esc)}px;letter-spacing:{int(2*esc)}px">fortismatcon.com.br</div>
    </div>"""

def perfil_marca():
    w = h = 1080
    corpo = f"""{beams(w, h, 1.2)}
  <div class="ring" style="width:1000px;height:1000px;left:40px;top:40px;border-color:rgba(217,181,121,.35)"></div>
  <img src="{A}/logo.png" class="logo" style="top:205px;height:670px">"""
    return "perfil-marca.png", w, h, doc(w, h, corpo)

def perfil_sany():
    w = h = 1080
    corpo = f"""{beams(w, h, 1.2)}
  <img src="{A}/emblema.png" class="ghost" style="left:-60px;top:60px;height:960px;opacity:.10">
  <img src="{A}/personagem/sany-uniforme.png" class="sany" style="left:40px;width:1000px">"""
    return "perfil-linkedin-sany.png", w, h, doc(w, h, corpo)

def capa(nome, w, h, safe, esc, sany=None, logo_h=None, tit_w=None):
    sx, sy, sw, shh = safe
    logo_h = logo_h or int(shh * .80)
    tit_w = tit_w or int(sw * .55)
    s_html = ""
    if sany:
        sl, sh = sany
        s_html = f'<img src="{A}/personagem/sany-uniforme.png" class="sany" style="left:{sl}px;height:{sh}px">'
    corpo = f"""{beams(w, h, max(1, w/1600))}
  <img src="{A}/emblema.png" class="ghost" style="right:{int(w*.02)}px;top:{int(-h*.1)}px;height:{int(h*1.2)}px">
  <div class="bloco" style="left:{sx}px;top:{sy}px;height:{shh}px;gap:{int(40*esc)}px">
    <img src="{A}/logo.png" style="height:{logo_h}px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6)) drop-shadow(0 0 22px rgba(217,181,121,.25))">
    <div class="linha" style="width:2px;height:{int(logo_h*.8)}px;background:linear-gradient(180deg,transparent,var(--gold),transparent)"></div>
    {texto(esc, tit_w)}
  </div>{s_html}"""
    return nome, w, h, doc(w, h, corpo)

PECAS = [
    perfil_marca(),
    perfil_sany(),
    # Facebook: 1640x624, celular corta as laterais -> conteúdo no centro
    capa("capa-facebook.png", 1640, 624, (230, 122, 900, 380), 1.35, sany=(1150, 560), tit_w=520),
    # LinkedIn (perfil pessoal): 1584x396, foto de perfil cobre o canto inferior esquerdo
    capa("capa-linkedin.png", 1584, 396, (500, 58, 1020, 280), 1.15, tit_w=640),
    # YouTube: 2560x1440, área segura central 1546x423
    capa("capa-youtube.png", 2560, 1440, (507, 509, 1546, 423), 1.6, tit_w=900),
    # Pinterest: 1920x1080
    capa("capa-pinterest.png", 1920, 1080, (170, 290, 1050, 500), 1.6, sany=(1240, 900), tit_w=620),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nome, w, h, html in PECAS:
            pg = await b.new_page(viewport={"width": w, "height": h})
            arq = os.path.join(SAIDA, nome.replace(".png", ".html"))
            open(arq, "w").write(html)
            await pg.goto("file://" + arq)
            await pg.wait_for_timeout(800)
            await pg.screenshot(path=os.path.join(SAIDA, nome))
            os.remove(arq)
            await pg.close()
            print("ok", nome, w, h)
        await b.close()

asyncio.run(main())
