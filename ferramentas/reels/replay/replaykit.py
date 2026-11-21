"""Série REPLAY DA LOJA (reels 1080x1920): clipes 3D em câmera lenta + rótulos + HUD de jogo + legenda por frase + voz do Sâny.

Uso típico (ver replay01.py):
    r = Replay(pasta, voz_mp3, frases, secoes, cta_html)
    r.montar(saida_mp4)
- frases: lista de textos (um por trecho falado, na ordem); **palavra** vira dourado.
- secoes: lista de dicts {clipe, frases:[índices], tags:[html], hud: html|None, lenta: bool}
  Cada seção cobre do início da sua 1ª frase até o início da 1ª frase da próxima seção.
- As frases são casadas com os trechos de fala achados por silencedetect (mesmo número; se não bater, o script para).
Áreas seguras de reel: nada importante acima de 220px nem abaixo de 1920-420px; laterais 70px (direita 140px por causa dos ícones).
"""
import asyncio, os, re, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'gerador'))
import gerador as G
from playwright.async_api import async_playwright

W, H = 1080, 1920
CSS = """
body{margin:0;background:transparent!important}
.ov{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Mont,sans-serif;color:#fff}
.gt{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(180deg,rgba(14,31,57,.80),rgba(14,31,57,0))}
.gb{position:absolute;left:0;right:0;bottom:0;height:820px;background:linear-gradient(0deg,rgba(14,31,57,.92) 0%,rgba(14,31,57,.55) 55%,rgba(14,31,57,0) 100%)}
.serie{position:absolute;left:70px;top:235px;display:flex;align-items:center;gap:14px;font-weight:700;letter-spacing:5px;font-size:24px;color:#D9B579}
.serie img{width:58px}
.replay{position:absolute;right:150px;top:240px;background:#c8202d;color:#fff;font-weight:800;letter-spacing:3px;font-size:24px;padding:8px 18px;border-radius:10px}
.replay:before{content:"";display:inline-block;width:14px;height:14px;border-radius:50%;background:#fff;margin-right:10px;vertical-align:1px}
.tag{position:absolute;left:70px;right:140px;text-align:center}
.tag span{display:inline-block;background:rgba(10,22,42,.92);border:3px solid #D9B579;color:#fff;font-family:Osw;font-weight:700;font-size:46px;letter-spacing:1px;padding:10px 28px;border-radius:16px;text-transform:uppercase}
.tag span.ok{border-color:#3fb37f}
.tag span.ruim{border-color:#e0484f}
.hud{position:absolute;left:110px;right:180px;top:330px;background:rgba(10,22,42,.92);border:3px solid #e0484f;border-radius:20px;padding:20px 28px}
.hud h4{margin:0 0 14px;text-align:center;font-family:Osw;font-size:40px;letter-spacing:1px;color:#fff}
.hud .l{font-weight:700;font-size:24px;letter-spacing:2px;color:#dfe5ee;margin:8px 0 6px;display:flex;justify-content:space-between}
.hud .b{height:22px;border-radius:11px;background:rgba(255,255,255,.12);overflow:hidden}
.hud .b i{display:block;height:100%;border-radius:11px}
.leg{position:absolute;left:70px;right:140px;top:1240px;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase;font-size:64px;line-height:1.1;letter-spacing:.5px;text-shadow:0 4px 18px rgba(0,0,0,.8)}
.leg b{color:#D9B579}
.fonte{position:absolute;left:70px;right:140px;top:1455px;text-align:center}
.fonte span{display:inline-block;font-size:21px;color:#b3bfd1;background:rgba(5,12,25,.88);padding:8px 16px;border-radius:10px}
"""


def sh(c):
    r = subprocess.run(c, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def dur(f):
    return float(subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{f}'", shell=True,
                                capture_output=True, text=True).stdout)


def falas(voz, n, ruido='-38dB', minimo=0.28):
    """Início de cada trecho falado (silencedetect)."""
    out = subprocess.run(f"ffmpeg -i '{voz}' -af silencedetect=noise={ruido}:d={minimo} -f null -", shell=True,
                         capture_output=True, text=True).stderr
    fins = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    inicios = [0.0] + [f - 0.05 for f in fins if f < dur(voz) - 0.3]
    if len(inicios) != n:
        raise SystemExit(f'Esperava {n} trechos de fala e achei {len(inicios)}: {inicios}. Ajuste ruido/minimo ou as frases.')
    return inicios


def leg_html(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


class Replay:
    def __init__(s, pasta, voz, frases, secoes, cta_html, serie='REPLAY DA LOJA', inicios=None, cta_desde=None):
        s.P = pasta; s.C = os.path.join(pasta, 'tmp'); os.makedirs(s.C, exist_ok=True)
        s.voz, s.frases, s.secoes, s.cta, s.serie = voz, frases, secoes, cta_html, serie
        s.ini = inicios or falas(voz, len(frases))
        s.cta_desde = cta_desde if cta_desde is not None else len(frases) - 1
        s.total = dur(voz) + 1.2

    def _ov(s, sec, frase, frase_idx=None):
        logo = f'<img src="{G.A}/logo.png">'
        corpo = f'<div class="gt"></div><div class="gb"></div><div class="serie">{logo}{s.serie}</div>'
        if sec.get('replay'): corpo += '<div class="replay">REPLAY</div>'
        if sec.get('hud'): corpo += sec['hud']
        tg = sec.get('tags', [])
        if isinstance(tg, dict): tg = tg.get(frase_idx, [])
        for t in tg: corpo += t
        corpo += f'<div class="leg">{leg_html(frase)}</div>'
        if sec.get('fonte'): corpo += f'<div class="fonte"><span>{sec["fonte"]}</span></div>'
        return f'<div class="ov">{corpo}</div>'

    async def _render(s, itens):
        async with async_playwright() as pw:
            b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': W, 'height': H})
            for nome, html, transp in itens:
                f = os.path.join(s.C, nome + '.html')
                open(f, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{G.CSS_BASE}{CSS}</style></head><body>{html}</body></html>')
                await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=os.path.join(s.C, nome + '.png'), omit_background=transp)
            await b.close()

    def montar(s, saida):
        itens = []
        for i, sec in enumerate(s.secoes):
            for j in sec['frases']:
                itens.append((f'ov{j:02d}', s._ov(sec, s.frases[j], j), True))
        itens.append(('cta', f'<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W, H, 1.3)}{s.cta}</div>', False))
        asyncio.run(s._render(itens))
        partes = []
        for i, sec in enumerate(s.secoes):
            t0 = s.ini[sec['frases'][0]]
            t1 = s.ini[s.secoes[i + 1]['frases'][0]] if i + 1 < len(s.secoes) else s.ini[s.cta_desde]
            d = t1 - t0
            clip = sec['clipe']
            fator = max(1.0, d / max(dur(clip) - 0.05, 0.1))
            ins, flt = [f"-i '{clip}'"], [f"[0:v]{'crop=%d:%d:%d:%d,' % sec['crop'] if sec.get('crop') else ''}setpts={fator:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[v0]"]
            ult = 'v0'
            for k, j in enumerate(sec['frases']):
                a = s.ini[j] - t0
                b = (s.ini[j + 1] - t0) if j + 1 < len(s.frases) and j != sec['frases'][-1] else d
                ins.append(f"-i '{os.path.join(s.C, f'ov{j:02d}.png')}'")
                flt.append(f"[{ult}][{k + 1}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k + 1}]")
                ult = f'v{k + 1}'
            flt.append(f"[{ult}]format=yuv420p[out]")
            p = os.path.join(s.C, f'sec{i}.mp4')
            sh(f"ffmpeg -y {' '.join(ins)} -filter_complex \"{';'.join(flt)}\" -map [out] -an -t {d:.3f} -c:v libx264 -crf 17 '{p}'")
            partes.append(p)
        # encerramento: card parado com zoom leve a partir da última frase (a do CTA)
        tc = s.ini[s.cta_desde]
        dc = s.total - tc
        p = os.path.join(s.C, 'cta.mp4')
        sh(f"ffmpeg -y -loop 1 -t {dc:.3f} -i '{os.path.join(s.C, 'cta.png')}' -vf \"fps=30,zoompan=z='min(1+0.0006*on,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,fade=in:st=0:d=0.25,format=yuv420p\" -c:v libx264 -crf 17 '{p}'")
        partes.append(p)
        lst = os.path.join(s.C, 'lista.txt')
        open(lst, 'w').write(''.join(f"file '{x}'\n" for x in partes))
        v = os.path.join(s.C, 'video.mp4')
        sh(f"ffmpeg -y -f concat -safe 0 -i '{lst}' -c copy '{v}'")
        a = os.path.join(s.C, 'audio.wav')
        sh(f"ffmpeg -y -i '{s.voz}' -af \"highpass=f=60,acompressor=threshold=0.2:ratio=2:attack=10:release=150,apad,atrim=0:{dur(v):.3f},loudnorm=I=-14:TP=-1.5:LRA=8\" -ar 44100 -ac 2 '{a}'")
        sh(f"ffmpeg -y -i '{v}' -i '{a}' -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart '{saida}'")
        return dur(saida)


def tag(txt, top, cls=''):
    return f'<div class="tag" style="top:{top}px"><span class="{cls}">{txt}</span></div>'


def hud(titulo, linhas):
    """linhas: [(rotulo, direita, pct, cor)]"""
    corpo = ''.join(f'<div class="l"><span>{a}</span><span style="color:{c}">{d}</span></div><div class="b"><i style="width:{p}%;background:{c}"></i></div>' for a, d, p, c in linhas)
    return f'<div class="hud"><h4>{titulo}</h4>{corpo}</div>'
