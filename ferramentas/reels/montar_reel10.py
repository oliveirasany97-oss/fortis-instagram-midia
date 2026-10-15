"""Reel 10 — Pedido de preço por link. Uso: python3 montar_reel9.py [voz.mp3 cortes]"""
import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel10')
CARDS={
 'H':gancho('SEU COMPRADOR<br>AINDA LIGA PARA<br>PEDIR PREÇO?'),
 'A':cena_tela('PASSO 1','O fornecedor recebe<br>um <b>link</b> e preenche<br>os preços no celular'),
 'B':cena_tela('PASSO 2','O FLOW compara<br>e mostra quem tem<br>o <b>melhor preço</b>'),
 'C':cena_tela('PASSO 3','Um toque aplica<br>o <b>menor preço</b><br>de cada item'),
 'resultado':base('''<div class="passo" style="top:380px">NESTE EXEMPLO</div>
   <div class="big branco" style="top:450px;font-size:64px;line-height:1.1">MESMA COMPRA</div>
   <div class="big" style="top:570px;font-size:58px;color:#9fb0c9;text-decoration:line-through">R$ 1.700,00</div>
   <div class="big metal" style="top:670px;font-size:150px">R$ 1.510,00</div>
   <div class="txt" style="top:900px;font-size:46px"><b>R$ 190 a menos</b> em um único pedido,<br>sem uma ligação sequer.</div>
   <div class="txt" style="top:1110px;font-size:38px;color:#c4ccda">Agora imagine isso em todas<br>as compras do mês.</div>'''),
 'cta':cta_diag('Pedido de preço por link · fila de compras<br>rupturas · avarias · painel do dono'),
}
r=Reel(R,CARDS); ks=['H','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':3.8,'A':5.6,'B':4.4,'C':4.6,'resultado':4.6,'cta':4.6}
r.tela('H','H','H0','H1',150,DUR['H'])
r.tela('A','A','A0','A1',0,DUR['A'])
r.tela('B','B','B0','B1',450,DUR['B'])
r.tela('C','C','B1','B2',450,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel10-pedido-de-preco'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
