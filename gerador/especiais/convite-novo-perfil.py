"""Convite para seguir o @fortismatcon.oficial — para @sany.gestao e status do WhatsApp."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G
A = G.A
PILL = 'display:inline-block;border:3px solid var(--gold);border-radius:60px;padding:22px 54px;font-weight:700;color:var(--gold);background:rgba(14,31,57,.8)'
def tit(l):
    return "".join(f'<div class="{"metal" if i == len(l) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(l))
def corpo(fs, sub, pill, small):
    return f'''<div class="kicker" style="position:static;font-size:28px">NOVO PERFIL OFICIAL</div>
    <div class="titulo" data-max="900" data-fs="{fs}" style="position:static;margin-top:34px;line-height:1.05">{tit(["A FORTÍS ESTÁ", "DE CASA NOVA"])}</div>
    <p class="sub" style="position:static;margin:44px 100px 0;font-size:{sub}px">Notícias do mercado, dicas técnicas e gestão de loja de <b>material de construção</b>, todos os dias.</p>
    <div style="text-align:center;margin-top:64px"><span style="{PILL};font-size:{pill}px">@fortismatcon.oficial</span></div>
    <p class="cta" style="position:static;margin-top:44px;font-size:{small}px;padding:0 80px">Siga no Instagram e acompanhe.</p>'''
story = f'''<div class="arte" style="width:1080px;height:1920px">{G.fundo(1080,1920,.93)}
  <img class="logo" src="{A}/logo.png" style="top:270px;width:190px">
  <div style="position:absolute;top:590px;left:0;right:0;bottom:560px;display:flex;flex-direction:column;justify-content:center">{corpo(112,40,50,34)}</div>
  <div class="rodape" style="bottom:400px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div></div>'''
feed = f'''<div class="arte" style="width:1080px;height:1440px">{G.fundo(1080,1440,.8)}
  <img class="logo" src="{A}/logo.png" style="top:80px;width:170px">
  <div style="position:absolute;top:340px;left:0;right:0;bottom:170px;display:flex;flex-direction:column;justify-content:center">{corpo(112,36,48,32)}</div>
  <div class="rodape" style="bottom:70px;font-size:21px">FORTÍS SOLUÇÕES MATCON</div></div>'''
asyncio.run(G.renderizar([("convite-story-status", story, (1080,1920)), ("convite-feed", feed, (1080,1440))], os.path.join(G.RAIZ,'posts','2026-11','destaques')))
