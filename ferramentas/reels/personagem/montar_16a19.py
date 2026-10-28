"""Reels 16 a 19 (personagem). Uso: python3 montar_16a19.py N [voz.mp3 cortes]
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
 16: ('venda-adicional-no-caixa', {
   'H': t1('SEU CLIENTE<br>COMPROU TINTA.', 250, 100, 'metal') + s('E saiu sem o rolo?', 500),
   'A': k('TODA VENDA TEM UM ITEM QUE FALTA') + t1('TINTA PEDE', 290, 74) + t1('ROLO, FITA<br>E LIXA', 380, 104, 'metal'),
   'B': k('TODA VENDA TEM UM ITEM QUE FALTA') + t1('CANO PEDE', 290, 74) + t1('COLA E<br>CONEXÃO', 380, 104, 'metal'),
   'C': k('A PERGUNTA DO CAIXA') + t1('"JÁ TEM TUDO PARA<br>TERMINAR O SERVIÇO?"', 300, 78, 'metal'),
   'R': t1('UM ITEM A MAIS', 270, 80) + t1('POR VENDA', 360, 110, 'metal') + s('muda o <b>faturamento do mês</b>.', 520),
 }, ['r16H', 'r16A', 'r16B', 'r16C', 'r16H']),
 17: ('preco-errado-na-gondola', {
   'H': t1('O PREÇO DA PRATELEIRA<br>BATE COM O DO CAIXA?', 250, 80, 'metal'),
   'A': k('ETIQUETA MOSTRA MENOS') + t1('DAR O DESCONTO', 290, 84, 'metal') + s('ou perder a <b>confiança do cliente</b>', 420),
   'B': k('ETIQUETA MOSTRA MAIS') + t1('O CLIENTE<br>NEM LEVA', 290, 104, 'metal'),
   'C': k('TODA SEGUNDA-FEIRA') + t1('CONFIRA AS ETIQUETAS<br>DOS ITENS REAJUSTADOS', 290, 72, 'metal'),
   'R': t1('PREÇO CERTO NA GÔNDOLA', 270, 70) + t1('É MARGEM<br>PROTEGIDA', 360, 104, 'metal'),
 }, ['r17H', 'r17A', 'r17B', 'r17C', 'r17H']),
 18: ('inventario-rotativo', {
   'H': t1('VOCÊ FECHA A LOJA<br>PARA CONTAR<br>O ESTOQUE?', 250, 88, 'metal'),
   'A': k('INVENTÁRIO UMA VEZ POR ANO') + t1('CHEGA<br>TARDE', 290, 110, 'metal') + s('a diferença <b>já virou prejuízo</b>', 560),
   'B': k('FAÇA O ROTATIVO') + t1('20 ITENS<br>POR SEMANA', 290, 110, 'metal') + s('começando pelos de <b>maior giro e valor</b>', 560),
   'C': k('ACHOU DIFERENÇA? INVESTIGUE NA HORA') + t1('ENTRADA SEM NOTA<br>VENDA SEM BAIXA<br>AVARIA SEM REGISTRO', 290, 66, 'metal'),
   'R': t1('ESTOQUE CONFERIDO', 270, 74) + t1('É ESTOQUE<br>CONFIÁVEL', 360, 104, 'metal'),
 }, ['r18H', 'r18A', 'r18B', 'r18C', 'r18H']),
 19: ('comissao-que-premia-margem', {
   'H': t1('SEU VENDEDOR<br>GANHA MAIS QUANDO<br>DÁ DESCONTO?', 250, 84, 'metal'),
   'A': k('COMISSÃO SÓ SOBRE VOLUME') + t1('QUEM PAGA<br>É A MARGEM', 290, 104, 'metal'),
   'B': k('COLOQUE A MARGEM NA REGRA') + t1('COMISSÃO MAIOR<br>PARA MARGEM<br>SAUDÁVEL', 290, 84, 'metal'),
   'C': k('O RESULTADO') + t1('O VENDEDOR<br>DEFENDE O PREÇO', 290, 90, 'metal') + s('junto com você', 520),
   'R': t1('COMISSÃO CERTA', 270, 80) + t1('ALINHA A EQUIPE<br>AO LUCRO', 360, 96, 'metal'),
 }, ['r19H', 'r19A', 'r19B', 'r19C', 'r19H']),
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
