import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel5')
def gancho(linhas):
    return base(f'''<div class="big metal" style="top:205px;font-size:76px;line-height:1.04">{linhas}</div>
   <div class="moldura" style="left:{PX-6}px;top:{PY-6}px;width:{PW+12}px;height:{PH+12}px"></div>
   <div class="top" style="top:{PY+PH+34}px;font-weight:600;letter-spacing:8px;color:var(--gold);font-size:22px">FORTÍS FLOW · TELA REAL · DADOS FICTÍCIOS</div>''')
CARDS={
 'H':gancho('SUAS ENTREGAS AINDA<br>SÃO COMBINADAS<br>NO PAPEL?'),
 'A':cena_tela('PASSO 1','Monte a rota do dia<br>com as <b>entregas</b><br>de cada cliente'),
 'B':cena_tela('PASSO 2','Tudo no <b>calendário</b>:<br>a equipe sabe o que<br>sai e quando'),
 'C':cena_tela('PASSO 3','Entregou? Um toque<br>e a rota fica<br><b>concluída</b>'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">NENHUMA ENTREGA</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">ESQUECIDA</div>
   <div class="txt" style="top:800px;font-size:46px">Expedição organizada<br><b>é cliente que volta a comprar.</b></div>'''),
 'cta':cta_diag('Rotas · rupturas · fila de compras<br>metas · cotação por link · RH'),
}
r=Reel(R,CARDS)
ks=['H','A','B','C','resultado','cta']
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'H':4.2,'A':7.4,'B':3.8,'C':4.0,'resultado':4.0,'cta':4.6}
r.tela('H','H','H0','H1',150,DUR['H'])
r.tela('A','A','A0','A1',880,DUR['A'])
r.tela('B','B','B0','B1',300,DUR['B'])
r.tela('C','C','C0','C1',1000,DUR['C'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel5-rota-entrega'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(ks,saida,voz))
