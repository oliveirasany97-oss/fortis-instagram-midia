"""Bilhete que Fica — padrão caderno aprovado pelo Sâny em 28/11/2026.
Uso: python3 ferramentas/bilhete/gerar.py configs/AAAA-MM-DD.json caminho/saida.png
Config: frase (use [[...]] para o grifo dourado, 1 trecho curto), autor, sub, fs (tamanho), pre (opcional).
AUDITE a imagem com Read antes de publicar."""
import sys, asyncio, os, json
from playwright.async_api import async_playwright
cfg = json.load(open(sys.argv[1]))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cfg.setdefault("saida", sys.argv[2] if len(sys.argv)>2 else "saida.png")
q = cfg['frase']  # use [[...]] para grifar
q = q.replace('[[','<span class="mk">').replace(']]','</span>')
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Kau;src:url(kaushan.ttf)}}
@font-face{{font-family:Ser;src:url(DMSerifDisplay-Regular.ttf)}}
@font-face{{font-family:SerI;src:url(DMSerifDisplay-Italic.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:url(fundo-4x5.jpg) center/cover}}
.pag{{position:absolute;left:225px;top:225px;width:760px;height:1000px;display:flex;flex-direction:column;align-items:center}}
.logo{{width:128px;margin-top:16px}}
.tit{{font-family:Kau;font-size:66px;color:#0E1F39;margin-top:20px;position:relative;line-height:1.1}}
.tit:after{{content:"";position:absolute;left:-14px;right:-20px;bottom:-12px;height:11px;border-radius:12px;background:#D9B579;transform:rotate(-2deg)}}
.q{{font-family:Ser;color:#0E1F39;font-size:{cfg.get('fs',58)}px;line-height:1.22;margin-top:auto;width:100%;padding:0 18px}}
.mk{{background:linear-gradient(100deg,transparent 0 1%,rgba(217,181,121,.92) 3% 97%,transparent 99%);padding:0 10px;margin:0 -4px;border-radius:4px 14px 6px 16px;white-space:nowrap;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.pre{{font-family:SerI;font-size:44px;color:#6b5634}}
.aut{{font-family:SerI;font-size:46px;color:#0E1F39;align-self:flex-end;margin-top:38px;padding-right:22px;text-align:right}}
.aut small{{display:block;font-family:Ser;font-size:25px;color:#6b5634;margin-top:2px}}
.risco{{width:470px;height:11px;border-radius:12px;background:#D9B579;margin-top:56px;margin-bottom:auto;transform:rotate(-1.5deg)}}
.hd{{position:absolute;bottom:26px;font-family:Ser;font-size:22px;color:#6b5634;letter-spacing:2px}}
</style></head><body><div class="pag">
<img class="logo" src="logo.png"><div class="tit">Bilhete que Fica</div>
<div class="q">{("<span class=pre>"+cfg["pre"]+"</span><br>") if cfg.get("pre") else ""}“{q}”</div>
<div class="aut">— {cfg['autor']}<small>{cfg.get('sub','')}</small></div>
<div class="risco"></div>
<div class="hd">@fortismatcon.oficial</div>
</div></body></html>'''
open('_t.html','w').write(html)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
        await pg.goto('file://'+os.path.abspath('_t.html')); await pg.wait_for_timeout(600)
        r=await pg.evaluate("(()=>{const p=document.querySelector('.pag').getBoundingClientRect();const h=document.querySelector('.hd').getBoundingClientRect();const r=document.querySelector('.risco').getBoundingClientRect();return {risco_bottom:r.bottom,hd_top:h.top}})()")
        print('folga risco->rodape:', round(r['hd_top']-r['risco_bottom']))
        await pg.screenshot(path=cfg['saida']); await b.close()
asyncio.run(m())
