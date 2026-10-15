import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel6')
def gancho(linhas):
    return base(f'''<div class="big metal" style="top:205px;font-size:76px;line-height:1.04">{linhas}</div>
   <div class="moldura" style="left:{PX-6}px;top:{PY-6}px;width:{PW+12}px;height:{PH+12}px"></div>
   <div class="top" style="top:{PY+PH+34}px;font-weight:600;letter-spacing:8px;color:var(--gold);font-size:22px">FORTÍS FLOW · TELA REAL · DADOS FICTÍCIOS</div>''')
CARDS={
 'H':gancho('VOCÊ SABE O QUE<br>ACONTECE NA LOJA<br>QUANDO NÃO ESTÁ LÁ?'),
 'A':cena_tela('PASSO 1','Tudo o que entrou,<br>o que está <b>pendente</b><br>e o que foi resolvido'),
 'B':cena_tela('PASSO 2','Quanto a loja comprou<br>e quanto <b>perdeu</b><br>com avarias'),
 'C':cena_tela('PASSO 3','O que mais falta<br>e <b>quem</b> mais<br>registra na equipe'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">A LOJA INTEIRA</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">EM UMA TELA</div>
   <div class="txt" style="top:800px;font-size:46px">Decida com números,<br><b>de qualquer lugar.</b></div>'''),
 'cta':cta_diag('Painel do dono · rupturas · fila de compras<br>metas · rotas · RH'),
}
r=Reel(R,CARDS)
ks=['H','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':3.8,'A':4.4,'B':4.0,'C':4.2,'resultado':4.0,'cta':4.6}
r.tela('H','H','H0','H1',150,DUR['H'])
r.tela('A','A','A0','A1',150,DUR['A'])
r.tela('B','B','A1','B1',150,DUR['B'])
r.tela('C','C','B1','C1',150,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel6-painel-proprietario'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
