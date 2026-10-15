import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D
OUT=os.path.join(D,'reel1','frames'); shutil.rmtree(os.path.join(D,'reel1'),ignore_errors=True); os.makedirs(OUT)
U='file://'+os.path.join(D,'flow_demo.html')
frames=[]; marks=[]
TAP_JS="""window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(217,181,121,.55);border:2px solid #D9B579;z-index:999999;pointer-events:none;transition:all .45s ease-out`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1.8)';d.style.opacity='0'});setTimeout(()=>d.remove(),600)}"""
async def tap(pg,loc):
    await loc.scroll_into_view_if_needed(); bb=await loc.bounding_box()
    await pg.evaluate(TAP_JS); await pg.evaluate(f"__tap({bb['x']+bb['width']/2},{bb['y']+bb['height']/2})")
    await pg.wait_for_timeout(250); await loc.click()
async def suave(pg,sel_js):
    await pg.evaluate(f"({sel_js}).scrollIntoView({{behavior:'smooth',block:'center'}})"); await pg.wait_for_timeout(900)
def mark(n): marks.append((n,time.time())); print('mark',n)
async def main():
    async with async_playwright() as pw:
        b,ctx,pg=await abrir(pw,qs='?prop=DEMO01_cot1_r1')
        pg.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
        cdp=await ctx.new_cdp_session(pg)
        async def onframe(p):
            frames.append((p['metadata']['timestamp'],p['data']))
            try: await cdp.send('Page.screencastFrameAck',{'sessionId':p['sessionId']})
            except Exception: pass
        cdp.on('Page.screencastFrame',lambda p: asyncio.ensure_future(onframe(p)))
        start=lambda: cdp.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1080,'maxHeight':2338,'everyNthFrame':1})
        await start(); mark('A0'); await pg.wait_for_timeout(1800)
        ids=await pg.eval_on_selector_all('[id^="propPreco_"]','e=>e.map(x=>x.id.slice(10))')
        precos=['31.9','24.5']
        for i,d in enumerate(ids):
            await tap(pg,pg.locator('#propPreco_'+d)); await pg.keyboard.type(precos[i],delay=140)
            await tap(pg,pg.locator('#propFrete_'+d)); await pg.keyboard.type('0.80',delay=120)
            await pg.wait_for_timeout(500)
            if i==0: await suave(pg,"document.getElementById('propPreco_"+ids[1]+"')")
        await suave(pg,"document.getElementById('propPagamento')")
        await tap(pg,pg.locator('#propPagamento')); await pg.keyboard.type('30/60 dias',delay=90)
        await pg.fill('#propPrevisao',(__import__('datetime').date.today()+__import__('datetime').timedelta(days=5)).isoformat())
        await suave(pg,"document.getElementById('propTotalTxt')"); await pg.wait_for_timeout(1200)
        await tap(pg,pg.get_by_text('Enviar Proposta')); await pg.wait_for_timeout(2300); mark('A1')
        await cdp.send('Page.stopScreencast')
        await pg.goto(U); await pg.wait_for_timeout(3500)
        await pg.evaluate("navegar('Fila',document.querySelector('.ni[data-view=\"Fila\"]'))"); await pg.wait_for_timeout(1500)
        await pg.evaluate("window.scrollTo(0,0)")
        await start(); mark('B0'); await pg.wait_for_timeout(1500)
        await tap(pg,pg.locator('text=MARCA B >> visible=true').first); await pg.wait_for_timeout(1800)
        await suave(pg,"[...document.querySelectorAll('b')].find(x=>x.textContent.includes('Pedido de preço')&&x.offsetParent)"); await pg.wait_for_timeout(2600)
        mark('B1')
        await tap(pg,pg.locator('text=Aplicar menor preço >> visible=true').first); await pg.wait_for_timeout(2500)
        await pg.evaluate("window.scrollBy({top:420,behavior:'smooth'})"); await pg.wait_for_timeout(2800); mark('B2')
        await cdp.send('Page.stopScreencast'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=os.path.join(D,'reel1','fim.png'))
        await b.close()
    meta=[]
    for i,(ts,data) in enumerate(frames):
        fn=f'{i:05d}.jpg'; open(os.path.join(OUT,fn),'wb').write(base64.b64decode(data)); meta.append((fn,ts))
    json.dump({'frames':meta,'marks':marks},open(os.path.join(D,'reel1','meta.json'),'w'))
    print('frames',len(frames))
asyncio.run(main())
