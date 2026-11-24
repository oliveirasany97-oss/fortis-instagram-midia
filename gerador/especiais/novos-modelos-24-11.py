"""Novos modelos de feed (24/11/2026): mais imagem do Sâny, FORTÍS FLOW, FORTÍS OBRAS e tráfego para o site.
Uso: python3 gerador/especiais/novos-modelos-24-11.py
Saída: posts/2026-11/novos-modelos/
"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

FOTO = f"{A}/sany-notebook.png"
TELA = f"{A}/telas/fila.png"

EXTRA = """
<style>
.foto{position:absolute;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6));-webkit-mask-image:linear-gradient(to bottom,#000 78%,transparent 100%);mask-image:linear-gradient(to bottom,#000 78%,transparent 100%)}
.suave .beam{opacity:.18!important}
.it b,.it span{text-shadow:0 2px 10px #050c19}
.retrato{position:absolute;border-radius:50%;overflow:hidden;border:4px solid #D9B579;
 box-shadow:0 0 0 10px rgba(217,181,121,.12),0 25px 50px rgba(0,0,0,.55);background:radial-gradient(circle at 50% 35%,#1c3a68,#0a1830)}
.retrato img{position:absolute;width:260%;left:-95%;top:-6%}
.balao{position:absolute;border:2px solid rgba(217,181,121,.85);border-radius:28px 28px 28px 6px;
 background:linear-gradient(180deg,rgba(22,44,80,.97),rgba(10,22,42,.97));box-shadow:0 18px 40px rgba(0,0,0,.45)}
.tag{display:inline-block;font-weight:700;letter-spacing:5px;font-size:20px;color:#0E1F39;background:#D9B579;padding:8px 16px;border-radius:8px}
.url{position:absolute;border:2px solid #D9B579;border-radius:18px;background:rgba(217,181,121,.12);
 font-weight:700;color:#fff;text-align:center}
.url b{color:#D9B579}
.celular{position:absolute;border-radius:54px;padding:16px;background:linear-gradient(160deg,#2b3a52,#0b1220);
 box-shadow:0 0 0 2px rgba(217,181,121,.6),0 40px 70px rgba(0,0,0,.65)}
.celular .tela{border-radius:40px;overflow:hidden;height:100%}
.celular img{width:100%;display:block}
.it{display:flex;gap:22px;align-items:flex-start;margin-bottom:34px}
.it .n{flex:none;width:52px;height:52px;border:2px solid #D9B579;border-radius:12px;display:flex;align-items:center;justify-content:center;
 font-family:Osw;font-size:30px;color:#D9B579}
.it b{display:block;font-size:31px;color:#fff;line-height:1.2}
.it span{display:block;font-size:23px;color:#c4ccda;margin-top:6px;line-height:1.35}
.esq{position:absolute;text-align:left}
.esq .titulo{text-align:left}
.esq .titulo div{margin:0}
.kl{font-weight:600;letter-spacing:8px;color:#D9B579;font-size:23px}
</style>"""


def base(corpo, logo_top=60, logo_w=110, cls=''):
    return f'''{EXTRA}<div class="arte {cls}" style="width:{W}px;height:{H}px">{G.fundo(W, H, .80)}
  <img class="logo k" src="{A}/logo.png" style="top:{logo_top}px;width:{logo_w}px">
  {corpo}
  <div class="rodape k" style="bottom:56px;font-size:21px">FORTÍS SOLUÇÕES MATCON</div>
</div>'''


def tl(linhas, fs):
    return "".join(f'<div class="{"metal" if i == len(linhas) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(linhas))


def itens(lst, ini=1):
    return "".join(f'<div class="it k"><div class="n">{i + ini}</div><div><b>{a}</b><span>{b}</span></div></div>' for i, (a, b) in enumerate(lst))


# 1) SÂNY RESPONDE — rosto + pergunta real de lojista + resposta + link do site
sany_responde = base(f'''
  <img class="foto" src="{FOTO}" style="right:-110px;bottom:215px;width:640px">
  <div class="esq" style="left:70px;top:250px;width:600px">
    <div class="kl k">O LOJISTA PERGUNTOU</div>
  </div>
  <div class="balao k" style="left:70px;top:310px;width:560px;padding:30px 34px">
    <div style="font-size:31px;font-weight:600;line-height:1.35">“Para organizar minhas compras, eu preciso <b style="color:#D9B579">trocar de ERP</b>?”</div>
  </div>
  <div class="esq" style="left:70px;top:560px;width:470px">
    <div class="kl k" style="margin-bottom:18px">SÂNY RESPONDE</div>
    <div class="titulo k" data-max="560" data-fs="96" style="position:static;line-height:1.02">{tl(["NÃO", "PRECISA."], 96)}</div>
    <p class="k" style="margin-top:28px;font-size:26px;line-height:1.45;color:#e9edf5">O ERP cuida do <b style="color:#D9B579">produto e da nota</b>. O FORTÍS FLOW cuida das <b style="color:#D9B579">pessoas, pedidos e prazos</b>. Um completa o outro.</p>
  </div>
  <div class="url k" style="left:70px;right:70px;bottom:120px;padding:22px 20px;font-size:30px">Veja como funciona: <b>fortismatcon.com.br/fortis-flow</b></div>
''')

# 2) FLOW NA PRÁTICA — tela real do app no celular
flow_pratica = base(f'''
  <div class="esq" style="left:70px;top:230px;width:560px">
    <div class="tag k">FORTÍS FLOW NA PRÁTICA</div>
    <div class="titulo k" data-max="540" data-fs="84" style="position:static;margin-top:30px;line-height:1.04">{tl(["O PEDIDO", "QUE SE PERDIA", "NO WHATSAPP"], 84)}</div>
    <div style="margin-top:46px">{itens([
        ("Vendedor pede no app", "Item, quantidade e cliente, no mesmo lugar."),
        ("Comprador vê a fila", "Nada some no meio da conversa."),
        ("Dono acompanha", "Quem pediu, quem comprou e quando."),
    ])}</div>
  </div>
  <div class="celular" style="right:62px;top:220px;width:390px;height:880px"><div class="tela"><img src="{TELA}"></div></div>
  <div class="url k" style="left:70px;right:70px;bottom:120px;padding:22px 20px;font-size:30px">Conheça o Flow: <b>fortismatcon.com.br/fortis-flow</b></div>
''')

# 3) FORTÍS OBRAS — Sâny em destaque + recursos
obras = base(f'''
  <div class="retrato" style="right:70px;top:230px;width:300px;height:300px"><img src="{FOTO}"></div>
  <div class="esq" style="left:70px;top:240px;width:580px">
    <div class="tag k">FORTÍS OBRAS</div>
    <div class="titulo k" data-max="580" data-fs="90" style="position:static;margin-top:30px;line-height:1.04">{tl(["A OBRA QUE", "ESTÁ ESFRIANDO"], 90)}</div>
  </div>
  <p class="k" style="position:absolute;left:70px;right:70px;top:600px;font-size:30px;line-height:1.45;color:#e9edf5">Obra boa é a que <b style="color:#D9B579">ainda não comprou tudo</b>. O FORTÍS OBRAS mostra quais estão parando de comprar na sua loja, antes de o cliente ir para o concorrente.</p>
  <div style="position:absolute;left:70px;right:70px;top:800px">{itens([
      ("Painel de obras quentes", "A venda de agora aparece primeiro."),
      ("Aviso de obra parada", "Hora certa de ligar para o cliente."),
      ("Profissionais parceiros", "Pontos e ranking de quem traz obra."),
  ])}</div>
  <div class="url k" style="left:70px;right:70px;bottom:120px;padding:22px 20px;font-size:30px">Quer ver na sua loja? <b>Chame no direct.</b></div>
''', cls="suave")

# 4) FERRAMENTA GRÁTIS NO SITE — tráfego para fortismatcon.com.br/ferramentas
ferramenta = base(f'''
  <img class="foto" src="{FOTO}" style="left:-50px;bottom:215px;width:560px">
  <div class="esq" style="left:70px;top:230px;width:940px">
    <div class="tag k">GRÁTIS NO SITE DA FORTÍS</div>
    <div class="titulo k" data-max="940" data-fs="92" style="position:static;margin-top:30px;line-height:1.04">{tl(["O CLIENTE PERGUNTOU", "QUANTO LEVAR?"], 92)}</div>
  </div>
  <div class="esq" style="left:520px;top:600px;width:500px">
    <div class="kl k" style="margin-bottom:26px">CALCULADORAS</div>
    {itens([("Telhado", "Telha, cumeeira e fixação."), ("Tinta", "Litros por parede e demão."), ("Piso e reboco", "Metragem com a perda certa.")])}
  </div>
  <div class="url k" style="left:70px;right:70px;bottom:120px;padding:22px 20px;font-size:30px">Use agora: <b>fortismatcon.com.br/ferramentas</b></div>
''')

if __name__ == '__main__':
    saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'novos-modelos')
    asyncio.run(renderizar([
        ('modelo-1-sany-responde', sany_responde, (W, H)),
        ('modelo-2-flow-na-pratica', flow_pratica, (W, H)),
        ('modelo-3-fortis-obras', obras, (W, H)),
        ('modelo-4-ferramenta-no-site', ferramenta, (W, H)),
    ], saida))
