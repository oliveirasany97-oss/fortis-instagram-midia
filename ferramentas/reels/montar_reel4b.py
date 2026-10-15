import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel4')
import shutil
CARDS={
 'hookold':base('''<div class="big metal" style="top:620px;font-size:100px;line-height:1.06">SEU VENDEDOR SABE<br>QUANTO FALTA PARA<br>BATER A META?</div>
   <div class="txt" style="top:1060px;font-size:44px">Ou ele só descobre<br><b>no fim do mês?</b></div>''',logo_top=240),
 'H':base(f'''<div class="big metal" style="top:205px;font-size:76px;line-height:1.04">SEU VENDEDOR SABE<br>QUANTO FALTA PARA<br>BATER A META?</div>
   <div class="moldura" style="left:{PX-6}px;top:{PY-6}px;width:{PW+12}px;height:{PH+12}px"></div>
   <div class="top" style="top:{PY+PH+34}px;font-weight:600;letter-spacing:8px;color:var(--gold);font-size:22px">FORTÍS FLOW · TELA REAL · DADOS FICTÍCIOS</div>'''),
 'A':cena_tela('PASSO 1','O vendedor vê a meta<br>e <b>quanto falta</b><br>todo dia'),
 'B':cena_tela('PASSO 2','Lança a venda<br>do dia em<br><b>segundos</b>'),
 'C':cena_tela('PASSO 3','A meta diária<br>se <b>recalcula</b><br>sozinha'),
 'D':cena_tela('PASSO 4','Evolução diária e<br><b>projeção</b> de<br>fechamento do mês'),
 'E':cena_tela('PASSO 5','O dono vê quem<br>está <b>no ritmo</b><br>e quem precisa de atenção'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:80px;line-height:1.08">A META DEIXA DE SER</div>
   <div class="big metal" style="top:610px;font-size:112px;line-height:1.05">SURPRESA NO<br>FIM DO MÊS</div>
   <div class="txt" style="top:920px;font-size:46px">Cada vendedor sabe, todo dia,<br><b>quanto precisa vender.</b></div>'''),
 'cta':cta_diag('Metas · rupturas · fila de compras<br>cotação por link · RH'),
}
r=Reel(R,CARDS)
ks=['H','A','B','C','D','E','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':3.6,'A':4.6,'B':4.4,'C':3.6,'D':3.6,'E':3.6,'resultado':4.0,'cta':4.6}
r.tela('H','H','D0','D1',150,DUR['H'],fade=False)
r.tela('A','A','A0','A1',150,DUR['A'])
r.tela('B','B','A1','Bs',1000,DUR['B'])
r.tela('C','C','Bs','B1',600,DUR['C'])
r.tela('D','D','B1','C1',150,DUR['D'])
r.tela('E','E','D0','D1',150,DUR['E'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel4-modelo-novo-gancho'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
