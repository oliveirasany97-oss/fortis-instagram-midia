"""Kit de montagem de reels FORTÍS (1080x1920): cards + tela gravada + voz opcional."""
import asyncio, os, json, subprocess, sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','gerador'))
import gerador as G
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
W,H=1080,1920; PX,PY,PW,PH=150,570,780,910
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
def sh(c):
    r=subprocess.run(c,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])
def dur(f): return float(subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}",shell=True,capture_output=True,text=True).stdout)
def base(corpo,logo_top=None):
    lg=f'<img class="logo" src="{G.A}/logo.png" style="top:{logo_top}px;width:260px">' if logo_top is not None else ''
    return f'<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W,H,.80)}{lg}{corpo}</div>'
def cena_tela(passo,leg):
    return base(f'<div class="passo">{passo}</div><div class="leg">{leg}</div><div class="moldura" style="left:{PX-6}px;top:{PY-6}px;width:{PW+12}px;height:{PH+12}px"></div>'
                f'<div class="top" style="top:{PY+PH+34}px;font-weight:600;letter-spacing:8px;color:var(--gold);font-size:22px">FORTÍS FLOW · TELA REAL · DADOS FICTÍCIOS</div>')
def cta(lista):
    return base(f'''<div class="big metal" style="top:610px;font-size:120px">FORTÍS FLOW</div>
   <div class="txt" style="top:780px;font-size:40px">{lista}</div>
   <div class="top" style="top:950px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:96px;color:var(--gold)">R$ 649,90</span><span style="font-size:40px;font-weight:600;color:#e9edf5">/mês</span></span></div>
   <div class="txt" style="top:1160px;font-size:42px">Quer ver funcionando na sua loja?<br><b>Chame no direct.</b></div>
   <div class="rodape" style="top:1330px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''',logo_top=230)

class Reel:
    def __init__(s,R,cards):
        s.R=R; s.C=os.path.join(R,'cenas'); os.makedirs(s.C,exist_ok=True)
        asyncio.run(s._render(cards))
        m=Image.new('L',(PW,PH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,PW-1,PH-1),radius=30,fill=255); m.save(os.path.join(s.C,'mask.png'))
        meta=json.load(open(os.path.join(R,'meta.json'))); s.fr=meta['frames']; s.mk=dict(meta['marks'])
    async def _render(s,cards):
        async with async_playwright() as pw:
            b=await pw.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':H})
            for k,corpo in cards.items():
                f=os.path.join(s.C,k+'.html'); open(f,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{G.CSS_BASE}{CSS}</style></head><body>{corpo}</body></html>')
                await pg.goto('file://'+f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=os.path.join(s.C,k+'.png'))
            await b.close()
    def tela(s,nome,bg,m0,m1,crop_y,d,fade=True):
        t0,t1=s.mk[m0],s.mk[m1]; vel=(t1-t0)/d
        ant=[(f,t) for f,t in s.fr if t<t0]
        sel=([(ant[-1][0],t0)] if ant else [])+[(f,t) for f,t in s.fr if t0<=t<=t1]
        lst=os.path.join(s.C,nome+'.txt')
        with open(lst,'w') as o:
            for i,(f,t) in enumerate(sel):
                o.write(f"file '{os.path.join(s.R,'frames',f)}'\nduration {max((sel[i+1][1] if i+1<len(sel) else t1)-t,0.001):.3f}\n")
            o.write(f"file '{os.path.join(s.R,'frames',sel[-1][0])}'\n")
        ch=int(1080*PH/PW)
        sh(f"ffmpeg -y -f concat -safe 0 -i {lst} -vf \"setpts=PTS/{vel},fps=30,crop=1080:{ch}:0:{crop_y},scale={PW}:{PH}\" -c:v libx264 -crf 16 -pix_fmt yuv420p {os.path.join(s.C,nome+'_raw.mp4')}")
        sh(f"ffmpeg -y -loop 1 -i {os.path.join(s.C,bg+'.png')} -i {os.path.join(s.C,nome+'_raw.mp4')} -i {os.path.join(s.C,'mask.png')} -filter_complex \"[1:v][2:v]alphamerge[s];[0:v][s]overlay={PX}:{PY}:shortest=1,fps=30,tpad=stop_mode=clone:stop_duration=3{',fade=in:st=0:d=0.25' if fade else ''},format=yuv420p\" -t {d} -c:v libx264 -crf 17 {os.path.join(s.C,nome+'.mp4')}")
    def card(s,k,d):
        sh(f"ffmpeg -y -loop 1 -t {d} -i {os.path.join(s.C,k+'.png')} -vf \"fps=30,zoompan=z='min(1+0.0006*on,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,fade=in:st=0:d=0.25,format=yuv420p\" -c:v libx264 -crf 17 {os.path.join(s.C,k+'.mp4')}")
    def final(s,ordem,saida,voz=None):
        open(os.path.join(s.C,'ordem.txt'),'w').write(''.join(f"file '{os.path.join(s.C,k+'.mp4')}'\n" for k in ordem))
        sh(f"ffmpeg -y -f concat -safe 0 -i {os.path.join(s.C,'ordem.txt')} -c copy {os.path.join(s.C,'video.mp4')}")
        VT=dur(os.path.join(s.C,'video.mp4')); a=os.path.join(s.C,'audio.wav')
        if voz: sh(f"ffmpeg -y -i {voz} -af \"highpass=f=60,acompressor=threshold=0.2:ratio=2:attack=10:release=150,apad,atrim=0:{VT},loudnorm=I=-14:TP=-1.5:LRA=8\" -ar 44100 -ac 2 {a}")
        else: sh(f"ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {VT} {a}")
        sh(f"ffmpeg -y -i {os.path.join(s.C,'video.mp4')} -i {a} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart {saida}")
        return dur(saida)

def cta_diag(lista):
    """Fechamento sem preço (padrão a partir do reel 4): gera conversa no direct."""
    return base(f'''<div class="big metal" style="top:610px;font-size:120px">FORTÍS FLOW</div>
   <div class="txt" style="top:780px;font-size:40px">{lista}</div>
   <div class="big branco" style="top:960px;font-size:64px;line-height:1.1">QUER VER FUNCIONANDO<br>NA SUA LOJA?</div>
   <div class="top" style="top:1140px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:58px;color:var(--gold);letter-spacing:1px">PEÇA SEU DIAGNÓSTICO</span></span></div>
   <div class="txt" style="top:1300px;font-size:40px"><b>Chame no direct.</b></div>
   <div class="rodape" style="top:1420px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''',logo_top=230)
