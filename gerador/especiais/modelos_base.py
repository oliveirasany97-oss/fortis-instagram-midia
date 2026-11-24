"""Base dos novos modelos de feed (24/11/2026): mais imagem do Sâny, FORTÍS FLOW, FORTÍS OBRAS e tráfego para o site.
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


