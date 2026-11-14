"""Post fixado do feed do novo perfil oficial @fortismatcon.oficial."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G

CARD = "position:absolute;left:90px;right:90px;border:2px solid rgba(217,181,121,.55);border-radius:26px;background:rgba(14,31,57,.72);padding:26px 40px"
LIN = "display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-bottom:1px solid rgba(217,181,121,.22)"
ROT = "font-size:26px;color:#c4ccda;font-weight:500"
VAL = "font-size:31px;color:#fff;font-weight:700"

def feed():
    w, h = 1080, 1440
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,1.2)}
  <img class="logo" src="{G.A}/logo.png" style="top:90px;width:140px">
  <div class="kicker" style="top:340px;font-size:28px">COMUNICADO</div>
  <div class="titulo" data-max="920" data-fs="98" style="top:388px;line-height:1.04"><div class="branco">ESTE É O NOVO</div><div class="metal">PERFIL OFICIAL</div></div>
  <p class="sub" style="top:620px;left:100px;right:100px;font-size:32px">Nosso perfil anterior, <b>@fortis.solucoesmatcon</b>, foi desativado pelo Instagram. A Fortís segue com a <b>mesma equipe, os mesmos serviços</b> e o mesmo compromisso com a sua loja.</p>
  <div style="{CARD};top:870px">
    <div style="font-size:24px;letter-spacing:6px;color:var(--gold);font-weight:600;margin-bottom:4px">FALE COM A GENTE</div>
    <div style="{LIN}"><span style="{ROT}">WhatsApp</span><span style="{VAL}">(31) 99898-1530</span></div>
    <div style="{LIN}"><span style="{ROT}">Site</span><span style="{VAL}">fortismatcon.com.br</span></div>
    <div style="{LIN};border-bottom:0"><span style="{ROT}">E-mail</span><span style="{VAL}">contato@fortismatcon.com.br</span></div>
  </div>
  <p class="sub" style="top:1220px;left:110px;right:110px;font-size:28px;color:#c4ccda">Siga <b style="color:var(--gold)">@fortismatcon.oficial</b> e acompanhe por aqui.</p>
  <div class="rodape" style="top:1340px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

def story():
    w, h = 1080, 1920
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{G.fundo(w,h,1.2)}
  <img class="logo" src="{G.A}/logo.png" style="top:200px;width:170px">
  <div class="kicker" style="top:500px;font-size:30px">COMUNICADO</div>
  <div class="titulo" data-max="920" data-fs="104" style="top:552px;line-height:1.04"><div class="branco">ESTE É O NOVO</div><div class="metal">PERFIL OFICIAL</div></div>
  <p class="sub" style="top:800px;left:100px;right:100px;font-size:35px">Nosso perfil anterior, <b>@fortis.solucoesmatcon</b>, foi desativado pelo Instagram. Seguimos com a <b>mesma equipe e os mesmos serviços</b>.</p>
  <div style="{CARD};top:1080px;padding:34px 40px">
    <div style="font-size:26px;letter-spacing:6px;color:var(--gold);font-weight:600;margin-bottom:6px">FALE COM A GENTE</div>
    <div style="{LIN};padding:18px 0"><span style="{ROT}">WhatsApp</span><span style="{VAL}">(31) 99898-1530</span></div>
    <div style="{LIN};padding:18px 0"><span style="{ROT}">Site</span><span style="{VAL}">fortismatcon.com.br</span></div>
    <div style="{LIN};padding:18px 0;border-bottom:0"><span style="{ROT}">E-mail</span><span style="{VAL}">contato@fortismatcon.com.br</span></div>
  </div>
  <p class="sub" style="top:1500px;left:110px;right:110px;font-size:32px;color:#c4ccda">Siga <b style="color:var(--gold)">@fortismatcon.oficial</b></p>
  <div class="rodape" style="top:1690px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'especiais')
asyncio.run(G.renderizar([('perfil-oficial-fixado-feed', feed(), (1080, 1440)), ('perfil-oficial-story', story(), (1080, 1920))], saida))
