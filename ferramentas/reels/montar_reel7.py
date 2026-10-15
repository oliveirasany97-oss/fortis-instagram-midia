"""Reel 7 — Encomenda de cliente. Uso: python3 montar_reel9.py [voz.mp3 cortes]"""
import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel7')
CARDS={
 'H':gancho('ENCOMENDA DE CLIENTE<br>AINDA FICA NO<br>CADERNO DO BALCÃO?'),
 'A':cena_tela('PASSO 1','Cliente, obra<br>e produto <b>registrados</b><br>na hora da venda'),
 'B':cena_tela('PASSO 2','Valor e prazo<br>combinados: vai direto<br>para a <b>fila de compras</b>'),
 'C':cena_tela('PASSO 3','O gestor acompanha<br>cada encomenda<br>até a <b>entrega</b>'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">NENHUM CLIENTE</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">ESQUECIDO</div>
   <div class="txt" style="top:800px;font-size:46px">Prazo cumprido é cliente<br><b>que volta a comprar.</b></div>'''),
 'cta':cta_diag('Encomendas · rupturas · fila de compras<br>avarias · painel do dono · rotas'),
}
r=Reel(R,CARDS); ks=['H','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':3.8,'A':5.2,'B':5.2,'C':4.6,'resultado':4.0,'cta':4.6}
r.tela('H','H','H0','H1',150,DUR['H'])
r.tela('A','A','A0','A1',150,DUR['A'])
r.tela('B','B','A1','B1',150,DUR['B'])
r.tela('C','C','B1','C1',150,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel7-encomenda-cliente'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
