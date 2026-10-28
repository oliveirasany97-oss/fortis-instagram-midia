"""Reel do depoimento de Geise Oliveira (Fortaleza Materiais de Construção, Mariana/MG).
Uso: python3 montar_geise.py video_original.mp4 saida.mp4"""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from reelkit import G, CSS, W, H, sh, dur, base
from playwright.async_api import async_playwright

AQUI = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(AQUI, 'tmp'); os.makedirs(T, exist_ok=True)
CSS2 = """body{margin:0;background:transparent}
.ov{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Mont,sans-serif;color:#fff}
.gb{position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(0deg,rgba(14,31,57,.96) 0%,rgba(14,31,57,.85) 40%,rgba(14,31,57,0) 100%)}
.k{position:absolute;left:0;right:0;text-align:center;font-weight:700;letter-spacing:8px;color:var(--gold);font-size:26px}
.n{position:absolute;left:40px;right:40px;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase;font-size:92px;line-height:1}
.c{position:absolute;left:80px;right:80px;text-align:center;font-weight:500;color:#eef2f8;font-size:36px;line-height:1.35}
.sig{position:absolute;left:0;right:0;bottom:130px;text-align:center;font-weight:600;letter-spacing:10px;color:var(--gold);font-size:22px}"""
SIG = '<div class="ov"><div class="sig">FORTÍS SOLUÇÕES MATCON</div></div>'
OV_SANY = '''<div class="ov"><div class="gb"></div>
<div class="k" style="top:1440px">FORTÍS SOLUÇÕES MATCON</div>
<div class="n metal" style="top:1490px">SÂNY OLIVEIRA</div>
<div class="c" style="top:1606px">Fundador e CEO da Fortís</div>
<div class="sig">FORTÍS SOLUÇÕES MATCON</div></div>'''
OV = '''<div class="ov"><div class="gb"></div>
<div class="k" style="top:1440px">DEPOIMENTO DE CLIENTE</div>
<div class="n metal" style="top:1490px">GEISE OLIVEIRA</div>
<div class="c" style="top:1606px">Proprietária da <b style="color:var(--gold)">Fortaleza Materiais de Construção</b><br>Mariana/MG</div>
<div class="sig">FORTÍS SOLUÇÕES MATCON</div></div>'''
CTA = base('''<div class="big metal" style="top:600px;font-size:96px;line-height:1.05">DIAGNÓSTICO<br>GRATUITO</div>
   <div class="txt" style="top:840px;font-size:40px">Consultoria · Fortís Flow<br>compras · equipe · metas</div>
   <div class="big branco" style="top:1010px;font-size:64px;line-height:1.1">QUER ISSO NA<br>SUA LOJA?</div>
   <div class="top" style="top:1200px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:58px;color:var(--gold);letter-spacing:1px">LINK NA BIO</span></span></div>
   <div class="rodape" style="top:1420px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''', logo_top=230)

async def render():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': W, 'height': H})
        for nome, html, transp in [('ov', OV, True), ('ovs', OV_SANY, True), ('sig', SIG, True), ('cta', CTA, False)]:
            f = os.path.join(T, nome + '.html')
            open(f, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{G.CSS_BASE}{CSS}{CSS2 if transp else ""}{"body{background:transparent!important}" if transp else ""}</style></head><body>{html}</body></html>')
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(T, nome + '.png'), omit_background=transp)
        await b.close()

src, saida = sys.argv[1], sys.argv[2]
asyncio.run(render())
D = dur(src)
v1 = os.path.join(T, 'v1.mp4'); v2 = os.path.join(T, 'v2.mp4')
# Corte vertical central (9:16) do vídeo 16:9 + faixa com o nome; fade no fim.
# Faixas: nome da Geise durante a entrevista dela; nome do Sâny na fala dele; só assinatura nas cenas do evento.
G1, G2, S1, S2 = 8.1, 51.2, 59.8, 70.4
sh(f'ffmpeg -y -i {src} -i {T}/ov.png -i {T}/ovs.png -i {T}/sig.png -filter_complex "[0:v]crop=ih*9/16:ih,scale={W}:{H},setsar=1,fps=30[v];[v][1:v]overlay=0:0:enable=\'between(t,{G1},{G2})\'[a1];[a1][2:v]overlay=0:0:enable=\'between(t,{S1},{S2})\'[a2];[a2][3:v]overlay=0:0:enable=\'not(between(t,{G1},{G2})+between(t,{S1},{S2}))\',fade=out:st={D-0.6}:d=0.6,format=yuv420p[o];[0:a]afade=out:st={D-0.8}:d=0.8,loudnorm=I=-14:TP=-1.5:LRA=9[a]" -map "[o]" -map "[a]" -c:v libx264 -crf 21 -preset veryfast -c:a aac -b:a 160k -ar 44100 -ac 2 {v1}')
sh(f'ffmpeg -y -loop 1 -t 4 -i {T}/cta.png -f lavfi -t 4 -i anullsrc=r=44100:cl=stereo -vf "fps=30,fade=in:st=0:d=0.3,format=yuv420p" -c:v libx264 -crf 19 -c:a aac -b:a 160k -shortest {v2}')
open(os.path.join(T, 'l.txt'), 'w').write(f"file '{v1}'\nfile '{v2}'\n")
sh(f'ffmpeg -y -f concat -safe 0 -i {T}/l.txt -c copy -movflags +faststart {saida}')
print(saida, dur(saida))
