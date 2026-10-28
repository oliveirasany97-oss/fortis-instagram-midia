"""Reels 20 a 23 (personagem). Uso: python3 montar_20a23.py N [voz.mp3 cortes]
Fecham com o card do diagnóstico gratuito pelo link da bio (não mais "chame no direct")."""
import os, sys
from kitpers import ReelP, duracoes, AQUI
from reelkit import base


def cta_bio(lista):
    return base(f'''<div class="big metal" style="top:600px;font-size:96px;line-height:1.05">DIAGNÓSTICO<br>GRATUITO</div>
   <div class="txt" style="top:840px;font-size:40px">{lista}</div>
   <div class="big branco" style="top:1010px;font-size:64px;line-height:1.1">QUER ISSO NA<br>SUA LOJA?</div>
   <div class="top" style="top:1200px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:58px;color:var(--gold);letter-spacing:1px">LINK NA BIO</span></span></div>
   <div class="rodape" style="top:1420px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''', logo_top=230)


def k(t): return f'<div class="k" style="top:230px">{t}</div>'
def t1(t, top=290, fs=84, cls='branco'): return f'<div class="t {cls}" style="top:{top}px;font-size:{fs}px">{t}</div>'
def s(t, top=540): return f'<div class="s" style="top:{top}px">{t}</div>'

REELS = {
 20: ('estoque-parado', {
   'H': t1('QUANTO DINHEIRO<br>ESTÁ PARADO NA<br>PRATELEIRA?', 250, 88, 'metal'),
   'A': k('90 DIAS SEM GIRO') + t1('NÃO É ESTOQUE.<br>É CAIXA PRESO.', 290, 90, 'metal'),
   'B': k('TODA SEMANA') + t1('PUXE A LISTA<br>DOS ITENS<br>SEM VENDA', 290, 90, 'metal'),
   'C': k('FAÇA UMA AÇÃO COM ELES') + t1('PONTA DE GÔNDOLA<br>KIT COM ITEM DE GIRO<br>CONDIÇÃO PARA O PEDREIRO', 290, 62, 'metal'),
   'R': k('ANTES DE COMPRAR, OLHE O PARADO') + t1('ESTOQUE QUE GIRA', 290, 74) + t1('PAGA AS<br>CONTAS', 380, 110, 'metal'),
 }, ['r20H', 'r20A', 'r20B', 'r20C', 'r20H']),
 22: ('exposicao-que-vende', {
   'H': t1('O CLIENTE ENTRA<br>NA SUA LOJA<br>E VÊ O QUÊ?', 250, 88, 'metal'),
   'A': k('PRODUTO ESCONDIDO NÃO VENDE') + t1('PONTA DE GÔNDOLA<br>E ENTRADA', 290, 84, 'metal') + s('os lugares <b>mais vistos</b> da loja', 500),
   'B': k('COLOQUE ALI') + t1('MAIOR MARGEM<br>E LANÇAMENTOS', 290, 88, 'metal') + s('com <b>preço claro</b>', 500),
   'C': k('A CADA 15 DIAS') + t1('TROQUE A<br>EXPOSIÇÃO', 290, 110, 'metal'),
   'R': t1('LOJA BEM EXPOSTA', 270, 74) + t1('VENDE SEM<br>PRECISAR OFERECER', 360, 86, 'metal'),
 }, ['r22H', 'r22A', 'r22B', 'r22C', 'r22H']),
}

n = int(sys.argv[1]); slug, OV, IMGS = REELS[n]
R = os.path.join(AQUI, f'reel{n}')
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz, DUR = duracoes(ks, {'H': 3.8, 'A': 5.0, 'B': 4.2, 'C': 5.0, 'R': 4.6, 'cta': 4.0}, sys.argv[1:])
r = ReelP(R, OV, {'cta': cta_bio('Gestão · vendas · equipe<br>compras · FORTÍS FLOW')})
for i, kk in enumerate(['H', 'A', 'B', 'C', 'R']):
    r.foto(kk, IMGS[i] + '.png', DUR[kk], zoom_in=(i % 2 == 0), pan=(1 if i == 1 else 0))
r.card('cta', DUR['cta'])
saida = os.path.join(R, f'reel{n}-{slug}' + ('-narrado' if voz else '') + '.mp4')
print(n, DUR, r.final(ks, saida, voz))
