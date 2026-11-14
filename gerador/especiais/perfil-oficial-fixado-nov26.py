"""Post fixado do feed do novo perfil oficial @fortismatcon.oficial."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G

CARD = "position:absolute;left:90px;right:90px;border:2px solid rgba(217,181,121,.55);border-radius:26px;background:rgba(14,31,57,.72);padding:26px 40px"
LIN = "display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-bottom:1px solid rgba(217,181,121,.22)"
ROT = "font-size:26px;color:#c4ccda;font-weight:500"
VAL = "font-size:31px;color:#fff;font-weight:700"

def feed():
    w, h = 1080, 1350
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,1.2)}
  <img class="logo" src="{G.A}/logo.png" style="top:70px;width:130px">
  <div class="kicker" style="top:300px;font-size:28px">COMUNICADO</div>
  <div class="titulo" data-max="920" data-fs="96" style="top:345px;line-height:1.04"><div class="branco">ESTE É O NOVO</div><div class="metal">PERFIL OFICIAL</div></div>
  <p class="sub" style="top:570px;left:100px;right:100px;font-size:32px">Nosso perfil anterior, <b>@fortis.solucoesmatcon</b>, foi desativado pelo Instagram. A Fortís segue com a <b>mesma equipe, os mesmos serviços</b> e o mesmo compromisso com a sua loja.</p>
  <div style="{CARD};top:810px">
    <div style="font-size:24px;letter-spacing:6px;color:var(--gold);font-weight:600;margin-bottom:4px">FALE COM A GENTE</div>
    <div style="{LIN}"><span style="{ROT}">WhatsApp</span><span style="{VAL}">(31) 99898-1530</span></div>
    <div style="{LIN}"><span style="{ROT}">Site</span><span style="{VAL}">fortismatcon.com.br</span></div>
    <div style="{LIN};border-bottom:0"><span style="{ROT}">E-mail</span><span style="{VAL}">contato@fortismatcon.com.br</span></div>
  </div>
  <p class="sub" style="top:1150px;left:110px;right:110px;font-size:27px;color:#c4ccda">Siga <b style="color:var(--gold)">@fortismatcon.oficial</b> e acompanhe por aqui.</p>
  <div class="rodape" style="top:1260px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'especiais')
asyncio.run(G.renderizar([('perfil-oficial-fixado-feed', feed(), (1080, 1350))], saida))
