"""Reels com o personagem (Sâny com uniforme Fortís): cena = foto em movimento lento + texto dourado por cima."""
import asyncio, os, sys, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from reelkit import G, CSS, W, H, sh, dur, cta_diag
from playwright.async_api import async_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
CENAS = os.path.join(AQUI, 'cenas')
CSS2 = """
body{margin:0;background:transparent}
.ov{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Mont,sans-serif;color:#fff}
.gt{position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,rgba(14,31,57,.92) 0%,rgba(14,31,57,.78) 45%,rgba(14,31,57,0) 100%)}
.gb{position:absolute;left:0;right:0;bottom:0;height:380px;background:linear-gradient(0deg,rgba(14,31,57,.9) 0%,rgba(14,31,57,0) 100%)}
.k{position:absolute;left:0;right:0;text-align:center;font-weight:700;letter-spacing:8px;color:var(--gold);font-size:26px}
.t{position:absolute;left:60px;right:60px;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase;line-height:1.06}
.s{position:absolute;left:90px;right:90px;text-align:center;font-weight:500;color:#eef2f8;line-height:1.35;font-size:42px}
.s b{color:var(--gold)}
.sig{position:absolute;left:0;right:0;bottom:120px;text-align:center;font-weight:600;letter-spacing:10px;color:var(--gold);font-size:22px}
"""

def overlay(corpo):
    return f'<div class="ov"><div class="gt"></div><div class="gb"></div>{corpo}<div class="sig">FORTÍS SOLUÇÕES MATCON</div></div>'


class ReelP:
    def __init__(s, R, overlays, cards):
        s.R = R; s.C = os.path.join(R, 'cenas'); os.makedirs(s.C, exist_ok=True)
        asyncio.run(s._render(overlays, cards))

    async def _render(s, overlays, cards):
        async with async_playwright() as pw:
            b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': W, 'height': H})
            for k, corpo in list(overlays.items()) + list(cards.items()):
                ov = k in overlays
                html = overlay(corpo) if ov else corpo
                f = os.path.join(s.C, k + '.html')
                open(f, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{G.CSS_BASE}{CSS}{CSS2}{"body{background:transparent!important}" if ov else ""}</style></head><body>{html}</body></html>')
                await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=os.path.join(s.C, k + '.png'), omit_background=ov)
            await b.close()

    def foto(s, k, img, d, zoom_in=True, pan=0):
        """Foto com zoom lento (Ken Burns) + texto por cima."""
        n = int(d * 30) + 2
        z = f"1+0.10*on/{n}" if zoom_in else f"1.10-0.10*on/{n}"
        x = f"iw/2-(iw/zoom/2)+{pan}*on/{n}*20"
        sh(f"ffmpeg -y -loop 1 -i {os.path.join(CENAS, img)} -i {os.path.join(s.C, k + '.png')} -filter_complex "
           f"\"[0:v]scale=2160:3840,zoompan=z='{z}':d={n}:x='{x}':y='0':s={W}x{H}:fps=30[bg];"
           f"[bg][1:v]overlay=0:0,fade=in:st=0:d=0.25,format=yuv420p\" -t {d} -c:v libx264 -crf 17 {os.path.join(s.C, k + '.mp4')}")

    def card(s, k, d):
        sh(f"ffmpeg -y -loop 1 -t {d} -i {os.path.join(s.C, k + '.png')} -vf \"fps=30,zoompan=z='min(1+0.0006*on,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,fade=in:st=0:d=0.25,format=yuv420p\" -c:v libx264 -crf 17 {os.path.join(s.C, k + '.mp4')}")

    def final(s, ordem, saida, voz=None):
        open(os.path.join(s.C, 'ordem.txt'), 'w').write(''.join(f"file '{os.path.join(s.C, k + '.mp4')}'\n" for k in ordem))
        sh(f"ffmpeg -y -f concat -safe 0 -i {os.path.join(s.C, 'ordem.txt')} -c copy {os.path.join(s.C, 'video.mp4')}")
        VT = dur(os.path.join(s.C, 'video.mp4')); a = os.path.join(s.C, 'audio.wav')
        if voz: sh(f"ffmpeg -y -i {voz} -af \"highpass=f=60,acompressor=threshold=0.2:ratio=2:attack=10:release=150,apad,atrim=0:{VT},loudnorm=I=-14:TP=-1.5:LRA=8\" -ar 44100 -ac 2 {a}")
        else: sh(f"ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {VT} {a}")
        sh(f"ffmpeg -y -i {os.path.join(s.C, 'video.mp4')} -i {a} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart {saida}")
        return dur(saida)


def duracoes(ks, padrao, argv):
    if len(argv) > 1:
        voz = argv[1]; CORTES = [float(x) for x in argv[2].split(',')]
        return voz, {k: (CORTES[i + 1] if i + 1 < len(CORTES) else dur(voz) + 1.4) - CORTES[i] for i, k in enumerate(ks)}
    return None, padrao
