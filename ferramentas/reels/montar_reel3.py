import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel3')
CARDS={
 'hook':base('''<div class="big metal" style="top:620px;font-size:104px;line-height:1.06">QUANTAS VENDAS<br>SUA LOJA PERDEU<br>HOJE?</div>
   <div class="txt" style="top:1060px;font-size:44px">O cliente pediu, não tinha…<br>e <b>ninguém anotou.</b></div>''',logo_top=240),
 'A':cena_tela('PASSO 1','O vendedor registra<br>a <b>ruptura</b> no balcão<br>em segundos'),
 'B':cena_tela('PASSO 2','O item cai sozinho<br>na <b>fila de compra</b><br>da marca'),
 'C':cena_tela('PASSO 3','O dono acompanha<br>tudo no <b>painel</b>'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">NENHUMA FALTA</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">FICA<br>ESQUECIDA</div>
   <div class="txt" style="top:920px;font-size:46px">O que falta no balcão<br><b>vira pedido de compra.</b></div>
   <div class="txt" style="top:1110px;font-size:36px;color:#c4ccda">Menos venda perdida.<br>Mais controle para o dono.</div>'''),
 'cta':cta('Rupturas · fila de compras · cotação por link<br>RH com perfil comportamental · metas'),
}
r=Reel(R,CARDS)
ks=['hook','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'hook':3.6,'A':9.0,'B':6.0,'C':4.6,'resultado':4.0,'cta':4.4}
r.card('hook',DUR['hook'])
r.tela('A','A','A0','A1',100,DUR['A'])
r.tela('B','B','C0','C1',300,DUR['B'])
r.tela('C','C','D0','D1',200,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel3-ruptura-fila'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
