import os, sys
from reelkit import *
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel2')
CARDS={
 'hook':base('''<div class="big metal" style="top:640px;font-size:112px;line-height:1.05">QUANTO CUSTA<br>CONTRATAR A<br>PESSOA ERRADA?</div>
   <div class="txt" style="top:1080px;font-size:44px">Currículo bonito não mostra<br>como a pessoa <b>atende no balcão.</b></div>''',logo_top=250),
 'A':cena_tela('PASSO 1','Crie a vaga e<br>divulgue <b>um link</b><br>no WhatsApp'),
 'B':cena_tela('PASSO 2','O candidato responde<br>pelo celular em<br><b>8 minutos</b>'),
 'C':cena_tela('PASSO 3','O FLOW dá a nota<br>e mostra <b>quem</b><br><b>priorizar</b>'),
 'D':cena_tela('PASSO 4','Perfil comportamental<br>e <b>roteiro de entrevista</b><br>prontos'),
 'resultado':base('''<div class="passo" style="top:420px">O RESULTADO</div>
   <div class="big branco" style="top:500px;font-size:84px;line-height:1.08">VOCÊ SÓ ENTREVISTA</div>
   <div class="big metal" style="top:610px;font-size:118px;line-height:1.05">QUEM TEM<br>PERFIL</div>
   <div class="txt" style="top:920px;font-size:46px">Menos tempo lendo currículo.<br><b>Mais acerto na contratação.</b></div>
   <div class="txt" style="top:1110px;font-size:34px;color:#c4ccda">O FLOW apoia — a decisão final<br>continua sendo sua.</div>'''),
 'cta':cta('RH com perfil comportamental<br>cotação por link · fila de compras · metas'),
}
r=Reel(R,CARDS)
voz=sys.argv[1] if len(sys.argv)>1 else None
if voz:
    CORTES=[float(x) for x in sys.argv[2].split(',')]; ks=['hook','A','B','C','D','resultado','cta']
    DUR={k:(CORTES[i+1] if i+1<len(CORTES) else dur(voz)+1.4)-CORTES[i] for i,k in enumerate(ks)}
else:
    DUR={'hook':3.4,'A':4.2,'B':11.0,'C':5.2,'D':7.6,'resultado':4.0,'cta':4.4}
r.card('hook',DUR['hook'])
r.tela('A','A','A0','A1',300,DUR['A'])
r.tela('B','B','B0','B1',0,DUR['B'])
r.tela('C','C','C0','D0',300,DUR['C'])
r.tela('D','D','D0','D1',100,DUR['D'])
r.card('resultado',DUR['resultado']); r.card('cta',DUR['cta'])
saida=os.path.join(R,'reel2-rh-perfil-comportamental'+('-narrado' if voz else '')+'.mp4')
print(DUR, r.final(['hook','A','B','C','D','resultado','cta'],saida,voz))
