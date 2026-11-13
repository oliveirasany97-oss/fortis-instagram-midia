"""Comunicado para status do WhatsApp: Instagram da Fortís temporariamente fora do ar."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G

CARD = "position:absolute;left:90px;right:90px;border:2px solid rgba(217,181,121,.55);border-radius:26px;background:rgba(14,31,57,.72);padding:34px 40px"
LIN = "display:flex;justify-content:space-between;align-items:baseline;padding:18px 0;border-bottom:1px solid rgba(217,181,121,.22)"
ROT = "font-size:28px;color:#c4ccda;font-weight:500"
VAL = "font-size:36px;color:#fff;font-weight:700"

def status():
    w, h = 1080, 1920
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,1.03)}
  <img class="logo" src="{G.A}/logo.png" style="top:200px;width:170px">
  <div class="kicker" style="top:500px;font-size:30px">COMUNICADO</div>
  <div class="titulo" data-max="920" data-fs="104" style="top:552px;line-height:1.04"><div class="branco">NOSSO INSTAGRAM</div><div class="metal">ESTÁ FORA DO AR</div></div>
  <p class="sub" style="top:800px;left:100px;right:100px;font-size:36px">O perfil <b>@fortis.solucoesmatcon</b> está temporariamente indisponível. Já estamos resolvendo com o Instagram e voltamos em breve.</p>
  <div style="{CARD};top:1060px">
    <div style="font-size:26px;letter-spacing:6px;color:var(--gold);font-weight:600;margin-bottom:6px">CONTINUE FALANDO COM A FORTÍS</div>
    <div style="{LIN}"><span style="{ROT}">WhatsApp</span><span style="{VAL}">(31) 99898-1530</span></div>
    <div style="{LIN}"><span style="{ROT}">Site</span><span style="{VAL}">fortismatcon.com.br</span></div>
    <div style="{LIN};border-bottom:0"><span style="{ROT}">Instagram</span><span style="{VAL}">@sany.gestao</span></div>
  </div>
  <p class="sub" style="top:1520px;left:110px;right:110px;font-size:28px;color:#c4ccda">Atenção: não responda a perfis que usem o nome da Fortís até o nosso retorno.</p>
  <div class="rodape" style="top:1690px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'especiais')
asyncio.run(G.renderizar([('comunicado-instagram-status', status(), (1080, 1920))], saida))
