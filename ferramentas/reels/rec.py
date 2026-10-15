"""Gravador comum dos reels (a partir do reel 7): screencast CDP + toques dourados + marcas de tempo."""
import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D

TAP_JS = """window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(217,181,121,.55);border:2px solid #D9B579;z-index:999999;pointer-events:none;transition:all .45s ease-out`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1.8)';d.style.opacity='0'});setTimeout(()=>d.remove(),600)}"""
NAV = "(v)=>navegar(v,document.querySelector('.ni[data-view=\"'+v+'\"]'))"


class Rec:
    def __init__(s, nome):
        s.R = os.path.join(D, nome); s.OUT = os.path.join(s.R, 'frames')
        shutil.rmtree(s.R, ignore_errors=True); os.makedirs(s.OUT)
        s.frames = []; s.marks = []

    def mark(s, n): s.marks.append((n, time.time())); print('mark', n)

    async def abrir(s, pw, **kw):
        s.b, s.ctx, s.pg = await abrir(pw, **kw)
        s.pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
        s.cdp = await s.ctx.new_cdp_session(s.pg)
        async def onframe(p):
            s.frames.append((p['metadata']['timestamp'], p['data']))
            try: await s.cdp.send('Page.screencastFrameAck', {'sessionId': p['sessionId']})
            except Exception: pass
        s.cdp.on('Page.screencastFrame', lambda p: asyncio.ensure_future(onframe(p)))
        return s.pg

    async def start(s): await s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 88, 'maxWidth': 1080, 'maxHeight': 2338})
    async def stop(s): await s.cdp.send('Page.stopScreencast')
    async def nav(s, v, espera=1500):
        await s.pg.evaluate(NAV, v); await s.pg.wait_for_timeout(espera); await s.pg.evaluate("window.scrollTo(0,0)")
    async def w(s, ms): await s.pg.wait_for_timeout(ms)

    async def tap(s, loc, espera=250):
        loc = loc.first if hasattr(loc, 'first') else loc
        await loc.evaluate("e=>e.scrollIntoView({behavior:'smooth',block:'center'})"); await s.pg.wait_for_timeout(450); bb = await loc.bounding_box()
        await s.pg.evaluate(TAP_JS); await s.pg.evaluate(f"__tap({bb['x']+bb['width']/2},{bb['y']+bb['height']/2})")
        await s.pg.wait_for_timeout(espera)
        try: await loc.click(timeout=2500)
        except Exception: await loc.evaluate('e=>{e.click();if(e.focus)e.focus()}')

    async def digitar(s, sel, txt, delay=70):
        await s.tap(s.pg.locator(sel), 150); await s.pg.keyboard.type(txt, delay=delay)

    async def centro(s, js, ms=900):
        await s.pg.evaluate(f"({js}).scrollIntoView({{behavior:'smooth',block:'center'}})"); await s.pg.wait_for_timeout(ms)

    async def rolar(s, px, ms=1200):
        await s.pg.evaluate(f"window.scrollBy({{top:{px},behavior:'smooth'}})"); await s.pg.wait_for_timeout(ms)

    async def foto(s, nome): await s.pg.screenshot(path=os.path.join(s.R, nome + '.png'))

    async def fechar(s):
        await s.b.close()
        meta = []
        for i, (ts, data) in enumerate(s.frames):
            fn = f'{i:05d}.jpg'; open(os.path.join(s.OUT, fn), 'wb').write(base64.b64decode(data)); meta.append((fn, ts))
        json.dump({'frames': meta, 'marks': s.marks}, open(os.path.join(s.R, 'meta.json'), 'w'))
        print('frames', len(s.frames))


def rodar(fn):
    async def main():
        async with async_playwright() as pw:
            await fn(pw)
    asyncio.run(main())
