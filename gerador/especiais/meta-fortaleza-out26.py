"""Post especial: meta de outubro batida com a equipe da Fortaleza (Mariana/MG)."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G

FOTO = f"{G.A}/fotos/fortaleza-equipe-meta-out26.jpg"
QUADRO = "position:absolute;border:3px solid var(--gold);border-radius:28px;overflow:hidden;box-shadow:0 0 50px rgba(217,181,121,.28),0 30px 60px rgba(0,0,0,.55)"

def feed():
    w, h = 1080, 1350
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,.86)}
  <img class="logo" src="{G.A}/logo.png" style="top:52px;width:130px">
  <div class="kicker" style="top:250px;font-size:24px">OUTUBRO · MARIANA/MG</div>
  <div class="titulo" data-max="960" data-fs="150" style="top:292px;line-height:1"><div class="metal">META BATIDA!</div></div>
  <p class="sub" style="top:462px;left:90px;right:90px;font-size:34px">Equipe da <b>Fortaleza Materiais de Construção</b></p>
  <div style="{QUADRO};left:50px;top:560px;width:980px;height:441px"><img src="{FOTO}" style="width:100%;height:100%;object-fit:cover"></div>
  <p class="sub" style="top:1040px;left:100px;right:100px;font-size:30px">Parabéns, Geise e todo o time.<br>Meta se bate com <b>rotina, processo e equipe unida</b>.</p>
  <div class="rodape" style="bottom:56px;font-size:21px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

def story():
    w, h = 1080, 1920
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,.84)}
  <img class="logo" src="{G.A}/logo.png" style="top:230px;width:170px">
  <div class="kicker" style="top:520px;font-size:28px">OUTUBRO · MARIANA/MG</div>
  <div class="titulo" data-max="960" data-fs="170" style="top:570px;line-height:1"><div class="metal">META<br>BATIDA!</div></div>
  <div style="{QUADRO};left:50px;top:960px;width:980px;height:441px"><img src="{FOTO}" style="width:100%;height:100%;object-fit:cover"></div>
  <p class="sub" style="top:1450px;left:90px;right:90px;font-size:38px">Parabéns, equipe da<br><b>Fortaleza Materiais de Construção</b></p>
  <div class="rodape" style="top:1640px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

saida = os.path.join(G.RAIZ, 'posts', '2026-10', 'especiais')
asyncio.run(G.renderizar([('meta-fortaleza-out26-feed', feed(), (1080, 1350)), ('meta-fortaleza-out26-story', story(), (1080, 1920))], saida))
