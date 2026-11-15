"""Destaques do @fortismatcon.oficial — capas + stories de abertura (15/11/2026)."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G
A = G.A
W, H = 1080, 1920
G.ICONES["obra"] = '<path d="M8 54h48M14 54V26l18-14 18 14v28"/><path d="M26 54V38h12v16"/><path d="M4 30l28-22 28 22"/>'
G.ICONES["lupa"] = '<circle cx="28" cy="28" r="16"/><path d="M40 40l14 14"/><path d="M21 29l5 5 9-10"/>'
G.ICONES["lampada"] = '<path d="M22 40c-6-4-9-10-9-16a19 19 0 0 1 38 0c0 6-3 12-9 16v6H22z"/><path d="M24 52h16M27 58h10"/>'

def tit(l):
    return "".join(f'<div class="{"metal" if i == len(l) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(l))

def capa(ic):
    return f'''<div class="arte" style="width:{W}px;height:{H}px">
  <div class="glow" style="width:700px;height:700px;left:190px;top:610px;background:rgba(217,181,121,.16)"></div>
  <div class="card" style="position:absolute;left:290px;top:710px;width:500px;height:500px;border-radius:50%;border-width:8px;display:flex;align-items:center;justify-content:center">{G.icone(ic, 250)}</div></div>'''

def story(kicker, titulo, sub, cta, fs=100):
    return f'''<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W, H, .93)}
  <img class="logo" src="{A}/logo.png" style="top:270px;width:170px">
  <div style="position:absolute;top:560px;left:0;right:0;bottom:560px;display:flex;flex-direction:column;justify-content:center">
    <div class="kicker" style="position:static;font-size:28px">{G.e(kicker)}</div>
    <div class="titulo" data-max="900" data-fs="{fs}" style="position:static;margin-top:34px;line-height:1.05">{tit(titulo)}</div>
    <p class="sub" style="position:static;margin:44px 100px 0;font-size:40px">{sub}</p>
    <p class="cta" style="position:static;margin-top:54px;font-size:34px;padding:0 80px">{cta}</p>
  </div>
  <div class="rodape" style="bottom:430px;font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
  <div class="handle" style="bottom:385px;font-size:24px">@fortismatcon.oficial</div></div>'''

itens = [(f"capa-{n}", capa(ic), (W, H)) for n, ic in [("comece-aqui", "seta_acao"), ("mercado", "grafico"), ("dicas", "lampada"), ("flow", "app"), ("obras", "obra"), ("diagnostico", "lupa")]]
itens += [
 ("comece-1", story("COMECE AQUI", ["GESTÃO PARA LOJAS", "DE MATERIAL DE CONSTRUÇÃO"], "A Fortís trabalha <b>só com o varejo MATCON</b>: compras, equipe e números organizados, de loja em loja, lado a lado com o dono.", "Seja bem-vindo.", 84), (W, H)),
 ("comece-2", story("O QUE VOCÊ ENCONTRA AQUI", ["CONTEÚDO PARA", "QUEM VIVE O BALCÃO"], "<b>12h:</b> notícias do mercado de material de construção.<br><b>18h:</b> dicas técnicas de produto.<br><b>No feed:</b> gestão de loja na prática.", "Tudo com fonte e sem enrolação.", 92), (W, H)),
 ("comece-3", story("FALE COM A GENTE", ["SUA LOJA TEM", "UMA DÚVIDA?"], "Mande uma mensagem aqui no <b>direct</b> ou no WhatsApp <b>(31) 99898-1530</b>.", "Quem responde conhece loja por dentro.", 100), (W, H)),
 ("diagnostico-1", story("DIAGNÓSTICO SEM CUSTO", ["15 MINUTOS", "SOBRE A SUA LOJA"], "Uma conversa rápida, <b>por vídeo ou na loja</b>, para enxergar onde estão os gargalos de compras, equipe e margem.", "WhatsApp <b>(31) 99898-1530</b>", 104), (W, H)),
]
asyncio.run(G.renderizar(itens, os.path.join(G.RAIZ, 'posts', '2026-11', 'destaques')))
