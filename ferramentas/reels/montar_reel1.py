import asyncio, os, json, subprocess, sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','gerador'))
import gerador as G
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'reel1'); C=os.path.join(R,'cenas')
W,H=1080,1920; PX,PY,PW,PH=150,570,780,910   # janela da tela do app
def sh(c): subprocess.run(c,shell=True,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
CSS="""
.top{position:absolute;left:0;right:0;text-align:center}
.leg{position:absolute;left:70px;right:70px;top:275px;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase;font-size:60px;line-height:1.12;letter-spacing:.5px}
.leg b{color:var(--gold)}
.passo{position:absolute;left:0;right:0;top:215px;text-align:center;font-weight:700;letter-spacing:8px;color:var(--gold);font-size:26px}
.moldura{position:absolute;border-radius:34px;border:3px solid rgba(217,181,121,.9);box-shadow:0 0 40px rgba(217,181,121,.25),0 30px 60px rgba(0,0,0,.6)}
.big{position:absolute;left:0;right:0;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase}
.txt{position:absolute;left:90px;right:90px;text-align:center;font-weight:500;color:#e9edf5;line-height:1.4}
.txt b{color:var(--gold)}
.preco{display:inline-block;border:2px solid var(--gold);border-radius:22px;padding:22px 46px;background:rgba(10,22,42,.85)}
"""
def base(corpo,logo_top=None):
    lg=f'<img class="logo" src="{G.A}/logo.png" style="top:{logo_top}px;width:260px">' if logo_top is not None else ''
    return f'<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W,H,.80)}{lg}{corpo}</div>'
def cena_tela(passo,leg):
    return base(f'<div class="passo">{passo}</div><div class="leg">{leg}</div><div class="moldura" style="left:{PX-6}px;top:{PY-6}px;width:{PW+12}px;height:{PH+12}px"></div>'
                f'<div class="top" style="top:{PY+PH+34}px;font-weight:600;letter-spacing:8px;color:var(--gold);font-size:22px">FORTÍS FLOW · TELA REAL · DADOS FICTÍCIOS</div>')
CARDS={
 'hook':base(f'''<div class="big metal" style="top:640px;font-size:118px;line-height:1.05">SEU COMPRADOR<br>AINDA LIGA<br>PARA COTAR?</div>
   <div class="txt" style="top:1080px;font-size:44px">Liga para um, espera o outro,<br>anota em papel… e compra<br><b>sem saber se foi o melhor preço.</b></div>''',logo_top=250),
 'resultado':base(f'''<div class="passo" style="top:380px">NESTE EXEMPLO</div>
   <div class="big branco" style="top:450px;font-size:64px;line-height:1.1">MESMA COMPRA</div>
   <div class="big" style="top:570px;font-size:58px;color:#9fb0c9;text-decoration:line-through">R$ 1.823,00</div>
   <div class="big metal" style="top:670px;font-size:150px">R$ 1.633,00</div>
   <div class="txt" style="top:900px;font-size:46px"><b>R$ 190 a menos</b> em um único pedido,<br>sem uma ligação sequer.</div>
   <div class="txt" style="top:1110px;font-size:38px;color:#c4ccda">Agora imagina isso em todas<br>as compras do mês.</div>'''),
 'cta':base(f'''<div class="big metal" style="top:610px;font-size:120px">FORTÍS FLOW</div>
   <div class="txt" style="top:780px;font-size:40px">Cotação por link · fila de compras · rupturas<br>metas · rotas · RH com perfil comportamental</div>
   <div class="top" style="top:950px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:96px;color:var(--gold)">R$ 649,90</span><span style="font-size:40px;font-weight:600;color:#e9edf5">/mês</span></span></div>
   <div class="txt" style="top:1160px;font-size:42px">Quer ver funcionando na sua loja?<br><b>Chame no direct.</b></div>
   <div class="rodape" style="top:1330px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''',logo_top=230),
 'A':cena_tela('PASSO 1','O fornecedor recebe<br>um <b>link</b> e preenche<br>os preços no celular'),
 'B':cena_tela('PASSO 2','O FLOW compara<br>e mostra quem tem<br>o <b>melhor preço</b>'),
 'C':cena_tela('PASSO 3','Um toque aplica<br>o <b>menor preço</b><br>de cada item'),
}
async def render():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':H})
        for k,corpo in CARDS.items():
            f=os.path.join(C,k+'.html'); open(f,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{G.CSS_BASE}{CSS}</style></head><body>{corpo}</body></html>')
            await pg.goto('file://'+f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(C,k+'.png'))
        await b.close()
asyncio.run(render())
# máscara de cantos arredondados
m=Image.new('L',(PW,PH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,PW-1,PH-1),radius=30,fill=255); m.save(os.path.join(C,'mask.png'))
meta=json.load(open(os.path.join(R,'meta.json'))); fr=meta['frames']; mk=dict(meta['marks'])
def trecho(nome,t0,t1,crop_y,vel=1.0,d=None):
    sel=[(f,t) for f,t in fr if t0-0.05<=t<=t1]
    lst=os.path.join(C,nome+'.txt')
    with open(lst,'w') as o:
        for i,(f,t) in enumerate(sel):
            dur=(sel[i+1][1] if i+1<len(sel) else t1)-t
            o.write(f"file '{os.path.join(R,'frames',f)}'\nduration {max(dur,0.001):.3f}\n")
        o.write(f"file '{os.path.join(R,'frames',sel[-1][0])}'\n")
    ch=int(1080*PH/PW)
    sh(f"ffmpeg -y -f concat -safe 0 -i {lst} -vf \"setpts=PTS/{vel},fps=30,crop=1080:{ch}:0:{crop_y},scale={PW}:{PH}\" -c:v libx264 -crf 16 -pix_fmt yuv420p {os.path.join(C,nome+'_raw.mp4')}")
    sh(f"ffmpeg -y -loop 1 -i {os.path.join(C,nome[0]+'.png')} -i {os.path.join(C,nome+'_raw.mp4')} -i {os.path.join(C,'mask.png')} -filter_complex \"[1:v][2:v]alphamerge[s];[0:v][s]overlay={PX}:{PY}:shortest=1,fps=30,tpad=stop_mode=clone:stop_duration=3,fade=in:st=0:d=0.25,format=yuv420p\" -t {d} -c:v libx264 -crf 17 {os.path.join(C,nome+'.mp4')}")
ch=int(1080*PH/PW)
def dur(f): return float(subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}",shell=True,capture_output=True,text=True).stdout)
VOZF='/tmp/claude-0/-home-claude-fortis-instagram-midia/8778ba83-a35d-5741-b3cc-2f04030852fc/scratchpad/voz/reel1.mp3'
CORTES=[0,5.09,15.25,20.2,24.46,27.73]; VD=dur(VOZF)
ks=['hook','A','B','C','resultado','cta']
DUR={k:(CORTES[i+1] if i+1<len(CORTES) else VD+1.4)-CORTES[i] for i,k in enumerate(ks)}
trecho('A',mk['A0'],mk['A1'],0,(mk['A1']-mk['A0'])/DUR['A'],DUR['A'])
trecho('B',mk['B0'],mk['B1'],560,(mk['B1']-mk['B0'])/DUR['B'],DUR['B'])
trecho('C',mk['B1'],mk['B2'],560,(mk['B2']-mk['B1'])/DUR['C'],DUR['C'])
def card(k,d):
    sh(f"ffmpeg -y -loop 1 -t {d} -i {os.path.join(C,k+'.png')} -vf \"fps=30,zoompan=z='min(1+0.0006*on,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,fade=in:st=0:d=0.25,format=yuv420p\" -c:v libx264 -crf 17 {os.path.join(C,k+'.mp4')}")
card('hook',DUR['hook']); card('resultado',DUR['resultado']); card('cta',DUR['cta'])
ordem=['hook','A','B','C','resultado','cta']
open(os.path.join(C,'ordem.txt'),'w').write(''.join(f"file '{os.path.join(C,k+'.mp4')}'\n" for k in ordem))
sh(f"ffmpeg -y -f concat -safe 0 -i {os.path.join(C,'ordem.txt')} -c copy {os.path.join(C,'video.mp4')}")
VT=dur(os.path.join(C,'video.mp4'))
sh(f"ffmpeg -y -i {VOZF} -af \"highpass=f=60,acompressor=threshold=0.2:ratio=2:attack=10:release=150,apad,atrim=0:{VT},loudnorm=I=-14:TP=-1.5:LRA=8\" -ar 44100 -ac 2 {os.path.join(C,'audio.wav')}")
saida=os.path.join(R,'reel1-cotacao-por-link-voz.mp4')
sh(f"ffmpeg -y -i {os.path.join(C,'video.mp4')} -i {os.path.join(C,'audio.wav')} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart {saida}")
print(DUR, dur(saida))
