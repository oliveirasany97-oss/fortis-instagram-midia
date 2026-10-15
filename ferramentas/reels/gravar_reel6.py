import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D
R=os.path.join(D,'reel6'); OUT=os.path.join(R,'frames'); shutil.rmtree(R,ignore_errors=True); os.makedirs(OUT)
U='file://'+os.path.join(D,'flow_demo.html')
frames=[]; marks=[]
TAP_JS="""window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(217,181,121,.55);border:2px solid #D9B579;z-index:999999;pointer-events:none;transition:all .45s ease-out`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1.8)';d.style.opacity='0'});setTimeout(()=>d.remove(),600)}"""
async def tap(pg,loc,espera=250):
    await loc.scroll_into_view_if_needed(); bb=await loc.bounding_box()
    await pg.evaluate(TAP_JS); await pg.evaluate(f"__tap({bb['x']+bb['width']/2},{bb['y']+bb['height']/2})")
    await pg.wait_for_timeout(espera); await loc.click()
def mark(n): marks.append((n,time.time())); print('mark',n)

NAV="(v)=>navegar(v,document.querySelector('.ni[data-view=\"'+v+'\"]'))"
async def main():
    async with async_playwright() as pw:
        b,ctx,pg=await abrir(pw,uid='u_adm')
        cdp=await ctx.new_cdp_session(pg)
        async def onframe(p):
            frames.append((p['metadata']['timestamp'],p['data']))
            try: await cdp.send('Page.screencastFrameAck',{'sessionId':p['sessionId']})
            except Exception: pass
        cdp.on('Page.screencastFrame',lambda p: asyncio.ensure_future(onframe(p)))
        start=lambda: cdp.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1080,'maxHeight':2338})
        stop=lambda: cdp.send('Page.stopScreencast')
        await pg.evaluate(NAV,'Dash'); await pg.wait_for_timeout(2000); await pg.evaluate("window.scrollTo(0,0)")
        await start(); mark('H0'); await pg.wait_for_timeout(300)
        await tap(pg,pg.locator('.ni[data-view="Proprietario"]').first,200); await pg.wait_for_timeout(1500)
        await pg.evaluate("window.scrollBy({top:160,behavior:'smooth'})"); await pg.wait_for_timeout(1000); mark('H1')
        await pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await pg.wait_for_timeout(900); mark('A0')
        await pg.evaluate("window.scrollBy({top:260,behavior:'smooth'})"); await pg.wait_for_timeout(2600); mark('A1')
        await pg.evaluate("window.scrollBy({top:560,behavior:'smooth'})"); await pg.wait_for_timeout(2800); mark('B1')
        await pg.evaluate("window.scrollBy({top:560,behavior:'smooth'})"); await pg.wait_for_timeout(2800); mark('C1')
        await stop(); await pg.wait_for_timeout(300); await b.close()
    meta=[]
    for i,(ts,data) in enumerate(frames):
        fn=f'{i:05d}.jpg'; open(os.path.join(OUT,fn),'wb').write(base64.b64decode(data)); meta.append((fn,ts))
    json.dump({'frames':meta,'marks':marks},open(os.path.join(R,'meta.json'),'w')); print('frames',len(frames))
asyncio.run(main())
