import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D
R=os.path.join(D,'reel3'); OUT=os.path.join(R,'frames'); shutil.rmtree(R,ignore_errors=True); os.makedirs(OUT)
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
        b,ctx,pg=await abrir(pw,uid='u_v1')
        pg.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
        cdp=await ctx.new_cdp_session(pg)
        async def onframe(p):
            frames.append((p['metadata']['timestamp'],p['data']))
            try: await cdp.send('Page.screencastFrameAck',{'sessionId':p['sessionId']})
            except Exception: pass
        cdp.on('Page.screencastFrame',lambda p: asyncio.ensure_future(onframe(p)))
        start=lambda: cdp.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1080,'maxHeight':2338})
        stop=lambda: cdp.send('Page.stopScreencast')
        # A: vendedor registra a ruptura
        await pg.evaluate(NAV,'Nova'); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.getElementById('rMarca').placeholder='Ex: Marca A'")
        await start(); mark('A0'); await pg.wait_for_timeout(1300)
        await tap(pg,pg.locator('#typeGrid .tb').first); await pg.wait_for_timeout(900)
        await tap(pg,pg.locator('#rProd')); await pg.keyboard.type('Argamassa AC-III 20kg',delay=60)
        await pg.evaluate("document.getElementById('rSkuSugest').style.display='none'")
        await tap(pg,pg.locator('#rMarca')); await pg.keyboard.type('Marca B',delay=70)
        await tap(pg,pg.locator('#rEstq')); await pg.keyboard.type('0',delay=80)
        await tap(pg,pg.locator('#rQtd')); await pg.keyboard.type('60',delay=80)
        try: await pg.select_option('#rUn',label='saco')
        except Exception as e: print('un',e)
        try:
            opts=await pg.eval_on_selector_all('#rCat option','o=>o.map(x=>x.value)'); 
            if len(opts)>1: await pg.select_option('#rCat',opts[1])
        except Exception as e: print('cat',e)
        try: await pg.select_option('#rUrg',value='critica')
        except Exception as e: print('urg',e)
        await pg.wait_for_timeout(500)
        await tap(pg,pg.locator('#moRuptura .btn-primary')); await pg.wait_for_timeout(2600); mark('A1'); await stop()
        # troca para o gestor
        await ctx.add_init_script("""window.__FF_CLAIMS={ff:'loja',emp:'DEMO01',fid:'u_adm',perfil:'admin'};try{localStorage.setItem('ff_sessao_v1',JSON.stringify({empCod:'DEMO01',uid:'u_adm',h:'',v:2,em:Date.now()}))}catch(e){}""")
        await pg.goto(U); await pg.wait_for_timeout(3500)
        # C: fila da marca
        await pg.evaluate(NAV,'Fila'); await pg.wait_for_timeout(1500); await pg.evaluate("window.scrollTo(0,0)")
        await start(); mark('C0'); await pg.wait_for_timeout(1200)
        await tap(pg,pg.locator('text=MARCA B >> visible=true').first); await pg.wait_for_timeout(1500)
        await pg.evaluate("[...document.querySelectorAll('*')].find(e=>e.children.length==0&&/Argamassa AC-III/.test(e.textContent)&&e.offsetParent)?.scrollIntoView({behavior:'smooth',block:'center'})"); await pg.wait_for_timeout(2800); mark('C1'); await stop()
        # D: painel do dono
        await pg.evaluate(NAV,'Proprietario'); await pg.wait_for_timeout(2000); await pg.evaluate("window.scrollTo(0,0)")
        await start(); mark('D0'); await pg.wait_for_timeout(2200)
        await pg.evaluate("window.scrollBy({top:700,behavior:'smooth'})"); await pg.wait_for_timeout(2600); mark('D1'); await stop()
        await pg.wait_for_timeout(300); await b.close()
    meta=[]
    for i,(ts,data) in enumerate(frames):
        fn=f'{i:05d}.jpg'; open(os.path.join(OUT,fn),'wb').write(base64.b64decode(data)); meta.append((fn,ts))
    json.dump({'frames':meta,'marks':marks},open(os.path.join(R,'meta.json'),'w')); print('frames',len(frames))
asyncio.run(main())
