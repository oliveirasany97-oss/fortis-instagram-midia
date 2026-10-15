"""Reel 11 — O preço real do desconto (personagem). Uso: python3 montar_reel11.py [voz.mp3 cortes]"""
import os, sys
from kitpers import ReelP, duracoes, cta_diag, AQUI
R = os.path.join(AQUI, 'reel11')
OV = {
 'H': '''<div class="t metal" style="top:250px;font-size:96px">10% DE DESCONTO<br>PARECE POUCO</div>
   <div class="s" style="top:500px">Sabe quanto você precisa<br><b>vender a mais</b> para compensar?</div>''',
 'A': '''<div class="k" style="top:230px">COM MARGEM DE 30%</div>
   <div class="t branco" style="top:290px;font-size:84px">5% DE DESCONTO</div>
   <div class="t metal" style="top:400px;font-size:104px">= VENDER 20%<br>A MAIS</div>''',
 'B': '''<div class="k" style="top:230px">COM MARGEM DE 30%</div>
   <div class="t branco" style="top:290px;font-size:84px">10% DE DESCONTO</div>
   <div class="t metal" style="top:400px;font-size:104px">= VENDER 50%<br>A MAIS</div>''',
 'C': '''<div class="k" style="top:230px">COM MARGEM DE 30%</div>
   <div class="t branco" style="top:290px;font-size:84px">15% DE DESCONTO</div>
   <div class="t metal" style="top:400px;font-size:104px">= VENDER<br>O DOBRO</div>''',
 'R': '''<div class="k" style="top:230px">ANTES DE DAR DESCONTO, FAÇA A CONTA</div>
   <div class="t metal" style="top:290px;font-size:100px">DESCONTO SAI<br>DIRETO DO<br>SEU LUCRO</div>''',
}
CARDS = {'cta': cta_diag('Gestão · negociação · equipe<br>compras · FORTÍS FLOW')}
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz, DUR = duracoes(ks, {'H': 4.6, 'A': 5.4, 'B': 4.2, 'C': 4.8, 'R': 4.6, 'cta': 4.4}, sys.argv)
r = ReelP(R, OV, CARDS)
r.foto('H', 'c1.png', DUR['H'])
r.foto('A', 'c2.png', DUR['A'], pan=1)
r.foto('B', 'c3.png', DUR['B'], zoom_in=False)
r.foto('C', 'c4.png', DUR['C'])
r.foto('R', 'c5.png', DUR['R'], zoom_in=False)
r.card('cta', DUR['cta'])
saida = os.path.join(R, 'reel11-preco-real-do-desconto' + ('-narrado' if voz else '') + '.mp4')
print(DUR, r.final(ks, saida, voz))
