"""Gerador de artes do Instagram — FORTÍS SOLUÇÕES MATCON.

Uso: python3 gerador.py semanas/2026-10-05.json
Gera JPGs em posts/AAAA-MM/ a partir do JSON da semana.
Identidade fixa: logo oficial (assets/logo.png), azul #0E1F39, dourado #D9B579.
"""
import asyncio, json, os, sys, html
from PIL import Image
from playwright.async_api import async_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
A = "file://" + os.path.join(AQUI, "assets")

ICONES = {
 "ruptura": '<rect x="10" y="14" width="44" height="38" rx="4"/><path d="M10 26h44M24 14v12M40 14v12M26 38l12 8M38 38l-12 8"/>',
 "duplicado": '<rect x="8" y="20" width="30" height="34" rx="4"/><rect x="24" y="10" width="30" height="34" rx="4"/><path d="M32 22h14M32 30h14"/>',
 "cliente_sai": '<circle cx="26" cy="20" r="9"/><path d="M10 52c0-10 7-17 16-17s16 7 16 17M44 30h10M49 25l5 5-5 5"/>',
 "dono": '<circle cx="32" cy="18" r="9"/><path d="M14 54c0-11 8-19 18-19s18 8 18 19"/><path d="M32 35v10"/>',
 "equipe": '<circle cx="20" cy="22" r="7"/><circle cx="44" cy="22" r="7"/><path d="M6 50c0-8 6-14 14-14s14 6 14 14M30 50c0-8 6-14 14-14s14 6 14 14"/>',
 "relogio": '<circle cx="32" cy="32" r="22"/><path d="M32 20v13l9 6"/>',
 "documento": '<path d="M18 8h20l10 10v38H18z"/><path d="M38 8v10h10M25 30h16M25 38h16M25 46h10"/>',
 "telefone": '<path d="M20 8h24v48H20z"/><path d="M28 48h8"/><path d="M26 20l6 6 10-10"/>',
 "alvo": '<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="13"/><circle cx="32" cy="32" r="4"/>',
 "grafico": '<path d="M10 54h44"/><rect x="14" y="36" width="8" height="18"/><rect x="28" y="26" width="8" height="28"/><rect x="42" y="14" width="8" height="40"/>',
 "seta_acao": '<path d="M8 44l14-14 10 10 20-20"/><path d="M40 20h12v12"/>',
 "consultoria": '<path d="M8 30l14 12 8-6 10 6 16-14"/><path d="M22 42l-6 8M40 42l6 8"/><circle cx="32" cy="18" r="6"/>',
 "app": '<rect x="10" y="12" width="44" height="32" rx="3"/><path d="M24 54h16M32 44v10M18 34l8-8 6 6 10-10"/>',
 "capelo": '<path d="M4 26l28-12 28 12-28 12z"/><path d="M16 32v12c0 4 8 8 16 8s16-4 16-8V32M56 28v14"/>',
 "curva": '<path d="M10 54V10M10 54h44"/><path d="M14 46c10-2 14-28 38-30"/>',
 "giro": '<path d="M48 22a18 18 0 1 0 3 16"/><path d="M50 10v12H38"/>',
 "lista": '<path d="M24 16h28M24 32h28M24 48h28"/><path d="M10 14l3 3 5-6M10 30l3 3 5-6M10 46l3 3 5-6"/>',
 "calendario": '<rect x="10" y="14" width="44" height="40" rx="4"/><path d="M10 26h44M22 8v12M42 8v12M20 36h6M30 36h6M40 36h6M20 44h6"/>',
 "carrinho": '<path d="M6 10h8l6 30h30l6-20H18"/><circle cx="24" cy="50" r="4"/><circle cx="46" cy="50" r="4"/>',
}

CSS_BASE = f"""
@font-face{{font-family:Osw;font-weight:700;src:url({A}/fonts/oswald-latin-700-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:400;src:url({A}/fonts/montserrat-latin-400-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:500;src:url({A}/fonts/montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:600;src:url({A}/fonts/montserrat-latin-600-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:700;src:url({A}/fonts/montserrat-latin-700-normal.woff2)}}
:root{{--navy:#0E1F39;--gold:#D9B579}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#060f1f}}
.arte{{position:relative;overflow:hidden;font-family:Mont,sans-serif;color:#fff;
 background:radial-gradient(ellipse 70% 40% at 50% 38%,#16305a 0%,rgba(14,31,57,0) 70%),
 radial-gradient(ellipse 120% 80% at 50% 0%,#0E1F39 0%,#081428 60%,#050c19 100%)}}
.beam{{position:absolute;height:3px;border-radius:3px;transform-origin:left center;filter:blur(.6px);
 background:linear-gradient(90deg,rgba(217,181,121,0),rgba(217,181,121,.95) 55%,rgba(255,236,196,1) 70%,rgba(217,181,121,0))}}
.glow{{position:absolute;border-radius:50%;filter:blur(60px)}}
.ghost{{position:absolute;opacity:.06}}
.logo{{position:absolute;left:50%;transform:translateX(-50%);
 filter:drop-shadow(0 6px 18px rgba(0,0,0,.6)) drop-shadow(0 0 22px rgba(217,181,121,.25))}}
.kicker{{position:absolute;width:100%;text-align:center;font-weight:600;letter-spacing:9px;color:var(--gold)}}
.kicker:before,.kicker:after{{content:"";display:inline-block;width:70px;height:1px;background:var(--gold);vertical-align:middle;margin:0 22px;opacity:.7}}
.titulo{{position:absolute;left:0;right:0;text-align:center;font-family:Osw;font-weight:700;text-transform:uppercase;letter-spacing:1px}}
.titulo div{{white-space:nowrap;width:max-content;margin:0 auto}}
.metal{{background:linear-gradient(180deg,#fff6df 0%,#ecd09a 28%,#D9B579 48%,#a9864a 66%,#e6c98f 82%,#c9a465 100%);
 -webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 4px 0 rgba(60,40,10,.55)) drop-shadow(0 12px 22px rgba(0,0,0,.55))}}
.branco{{color:#fff;filter:drop-shadow(0 10px 20px rgba(0,0,0,.5))}}
.sub{{position:absolute;text-align:center;font-weight:500;color:#e9edf5;line-height:1.45}}
.sub b,.cta b{{color:var(--gold);font-weight:700}}
.card{{border:2px solid rgba(217,181,121,.85);border-radius:22px;text-align:center;
 background:linear-gradient(180deg,rgba(22,44,80,.98),rgba(10,22,42,.98));
 box-shadow:0 0 0 1px rgba(217,181,121,.15) inset,0 18px 40px rgba(0,0,0,.45),0 0 26px rgba(217,181,121,.12)}}
.card svg{{stroke:var(--gold);fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}}
.card h3{{font-weight:700;line-height:1.2}}
.card p{{line-height:1.35;color:#c4ccda;font-weight:500}}
.cta{{position:absolute;width:100%;text-align:center;font-weight:600}}
.rodape{{position:absolute;width:100%;text-align:center;font-weight:600;letter-spacing:10px;color:var(--gold)}}
.rodape:before,.rodape:after{{content:"";display:inline-block;width:130px;height:1px;vertical-align:middle;margin:0 24px;background:linear-gradient(90deg,transparent,var(--gold))}}
.rodape:after{{background:linear-gradient(90deg,var(--gold),transparent)}}
.handle{{position:absolute;width:100%;text-align:center;font-weight:500;color:#9fb0c9;letter-spacing:1px}}
"""

AJUSTE_JS = """
for (const t of document.querySelectorAll('.titulo')) {
  const max = +t.dataset.max; let fs = +t.dataset.fs;
  t.style.fontSize = fs + 'px';
  const largura = () => Math.max(...[...t.children].map(c => c.scrollWidth));
  while (largura() > max && fs > 40) { fs -= 2; t.style.fontSize = fs + 'px'; }
}
"""

def e(s):
    return html.escape(s or "").replace("**", "")

def rich(s):
    # **texto** vira destaque dourado
    partes = html.escape(s or "").split("**")
    res = ""
    for i, p in enumerate(partes):
        res += (f"<b>{p}</b>" if i % 2 else p)
    return res.replace("\n", "<br>")

def icone(nome, tam):
    return f'<svg viewBox="0 0 64 64" style="width:{tam}px;height:{tam}px">{ICONES[nome]}</svg>'

def fundo(w, h, b=.75):
    return f"""
  <div class="glow" style="width:520px;height:220px;left:-160px;top:{int(h*.73)}px;background:rgba(217,181,121,.22)"></div>
  <div class="glow" style="width:480px;height:200px;right:-180px;top:{int(h*.09)}px;background:rgba(217,181,121,.16)"></div>
  <div class="beam" style="width:900px;left:-220px;top:{int(h*b)}px;transform:rotate(-13deg)"></div>
  <div class="beam" style="width:700px;left:-150px;top:{int(h*(b+.035))}px;transform:rotate(-9deg);opacity:.55"></div>
  <div class="beam" style="width:760px;left:{w-520}px;top:{int(h*.385)}px;transform:rotate(-33deg);opacity:.55"></div>
  <div class="beam" style="width:620px;left:{w-440}px;top:{int(h*.445)}px;transform:rotate(-33deg);opacity:.3"></div>
  <img class="ghost" src="{A}/emblema.png" style="right:-120px;top:{int(h*.22)}px;width:460px">"""

def feed(p):
    w, h = 1080, 1350
    cards = "".join(f"""<div class="card" style="padding:30px 18px 28px">{icone(c['icone'],78)}
      <h3 style="margin-top:16px;font-size:27px">{e(c['titulo'])}</h3><p style="margin-top:10px;font-size:20px">{e(c['texto'])}</p></div>"""
      for c in p["cards"])
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{fundo(w,h)}
  <img class="logo" src="{A}/logo.png" style="top:54px;width:170px">
  <div class="kicker" style="top:300px;font-size:24px">{e(p['kicker'])}</div>
  <div class="titulo" data-max="980" data-fs="124" style="top:350px;line-height:1.02">
    <div class="branco">{e(p['titulo'][0])}</div><div class="metal">{e(p['titulo'][1])}</div></div>
  <p class="sub" style="top:628px;left:100px;right:100px;font-size:32px">{rich(p['sub'])}</p>
  <div style="position:absolute;top:800px;left:70px;right:70px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px">{cards}</div>
  <p class="cta" style="top:1135px;font-size:29px;padding:0 60px">{rich(p['frase'])}</p>
  <div class="rodape" style="bottom:52px;font-size:21px">FORTÍS SOLUÇÕES MATCON</div>
</div>"""

def story(s):
    w, h = 1080, 1920
    enquete = ""
    if s.get("enquete"):  # espaço livre para o adesivo de enquete (adicionado no app)
        enquete = '<div style="height:330px;margin:50px 60px 0;border:none"></div>'
    linhas = "".join(f'<div class="{"metal" if i == len(s["titulo"]) - 1 else "branco"}">{e(t)}</div>'
                     for i, t in enumerate(s["titulo"]))
    return f"""<div class="arte" style="width:{w}px;height:{h}px">{fundo(w,h,.87)}
  <img class="logo" src="{A}/logo.png" style="top:150px;width:190px">
  <div style="position:absolute;top:470px;left:0;right:0;bottom:330px;display:flex;flex-direction:column;justify-content:center">
    <div class="kicker" style="position:static;font-size:28px">{e(s['kicker'])}</div>
    <div class="titulo" data-max="960" data-fs="{s.get('fs', 112)}" style="position:static;margin-top:34px;line-height:1.05">{linhas}</div>
    <p class="sub" style="position:static;margin:44px 100px 0;font-size:44px">{rich(s.get('sub', ''))}</p>
    {enquete}
    <p class="cta" style="position:static;margin-top:60px;font-size:36px;padding:0 80px">{rich(s.get('frase', ''))}</p>
  </div>
  <div class="rodape" style="bottom:170px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>
  <div class="handle" style="bottom:120px;font-size:26px">@fortis.solucoesmatcon</div>
</div>"""

def pagina(corpo):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS_BASE}</style></head><body>{corpo}<script>{AJUSTE_JS}</script></body></html>'

async def renderizar(itens, saida_dir):
    os.makedirs(saida_dir, exist_ok=True)
    tmp = os.path.join(AQUI, ".tmp"); os.makedirs(tmp, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for nome, corpo, (w, h) in itens:
            caminho = os.path.join(tmp, nome + ".html")
            open(caminho, "w").write(pagina(corpo))
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto("file://" + caminho); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.evaluate(AJUSTE_JS)
            png = os.path.join(tmp, nome + ".png")
            await pg.screenshot(path=png); await pg.close()
            Image.open(png).convert("RGB").save(os.path.join(saida_dir, nome + ".jpg"), quality=92)
            print("ok", nome)
        await b.close()

def main(arq):
    semana = json.load(open(arq))
    itens = []
    for p in semana["feed"]:
        itens.append((p["arquivo"], feed(p), (1080, 1350)))
    for s in semana["stories"]:
        itens.append((s["arquivo"], story(s), (1080, 1920)))
    asyncio.run(renderizar(itens, os.path.join(RAIZ, semana["pasta"])))

if __name__ == "__main__":
    main(sys.argv[1])
