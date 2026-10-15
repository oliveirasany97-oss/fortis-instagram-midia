"""Reel 8 — Fila de compras por marca. Uso: python3 montar_reel9.py [voz.mp3 cortes]"""
import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel8')
CARDS={
 'H':gancho('SEU PEDIDO AO<br>FORNECEDOR AINDA SAI<br>DE MEMÓRIA?'),
 'A':cena_tela('PASSO 1','Cada falta da loja<br>cai na fila<br>da <b>marca certa</b>'),
 'B':cena_tela('PASSO 2','Item por item,<br>com a <b>quantidade</b><br>sugerida'),
 'C':cena_tela('PASSO 3','Um toque fecha<br>o <b>pedido</b> com tudo<br>o que faltava'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">NENHUM ITEM</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">ESQUECIDO</div>
   <div class="txt" style="top:800px;font-size:46px">Pedido completo, sem frete extra<br><b>para buscar o que faltou.</b></div>'''),
 'cta':cta_diag('Fila de compras · rupturas · encomendas<br>avarias · painel do dono · rotas'),
}
r=Reel(R,CARDS); ks=['H','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':3.8,'A':4.6,'B':3.8,'C':5.2,'resultado':4.0,'cta':4.6}
r.tela('H','H','H0','H1',150,DUR['H'])
r.tela('A','A','A0','A1',150,DUR['A'])
r.tela('B','B','A1','B1',150,DUR['B'])
r.tela('C','C','B1','C1',150,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel8-fila-por-marca'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
