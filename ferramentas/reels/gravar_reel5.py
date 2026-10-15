import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D
R=os.path.join(D,'reel5'); OUT=os.path.join(R,'frames'); shutil.rmtree(R,ignore_errors=True); os.makedirs(OUT)
U='file://'+os.path.join(D,'flow_demo.html')
frames=[]; marks=[]
TAP_JS="""window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(217,181,121,.55);border:2px solid #D9B579;z-index:999999;pointer-events:none;transition:all .45s ease-out`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1.8)';d.style.opacity='0'});setTimeout(()=>d.remove(),600)}"""
async def tap(pg,loc,espera=250):
    await loc.scroll_into_view_if_needed(); bb=await loc.bounding_box()
    await pg.evaluate(TAP_JS); await pg.evaluate(f"__tap({bb['x']+bb['width']/2},{bb['y']+bb['height']/2})")
    await pg.wait_for_timeout(espera); await loc.click()
def mark(n): marks.append((n,time.time())); print('mark',n)

NAV="(v)=>navegar(v,document.querySelector('.ni[data-view=\"'+v+'\"]'))"
import datetime as dt
async def main():
    async with async_playwright() as pw:
        b,ctx,pg=await abrir(pw,uid='u_adm')
        pg.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
        cdp=await ctx.new_cdp_session(pg)
        async def onframe(p):
            frames.append((p['metadata']['timestamp'],p['data']))
            try: await cdp.send('Page.screencastFrameAck',{'sessionId':p['sessionId']})
            except Exception: pass
        cdp.on('Page.screencastFrame',lambda p: asyncio.ensure_future(onframe(p)))
        start=lambda: cdp.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1080,'maxHeight':2338})
        stop=lambda: cdp.send('Page.stopScreencast')
        await pg.evaluate(NAV,'Rota'); await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content='#rotaEntData{display:none!important}')
        # dia futuro sem rota
        dias=await pg.evaluate("[...document.querySelectorAll('[onclick^=\"rotaAbrirDia\"]')].map(e=>[e.getAttribute('onclick').match(/'(.*)'/)[1], e.innerText.trim()])")
        hoje=dt.date.today().isoformat()
        livre=[d for d,t in dias if d>hoje and '\n' not in t]
        com=[d for d,t in dias if d>=hoje and '\n' in t]
        print('livre',livre[:3],'com',com[:3])
        alvo=livre[1] if len(livre)>1 else livre[0]
        # H: rola a lista de próximas rotas (movimento contínuo)
        await pg.evaluate("window.scrollTo(0,0)")
        await start(); mark('H0'); await pg.wait_for_timeout(500)
        await pg.evaluate("window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'})"); await pg.wait_for_timeout(2200)
        await pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await pg.wait_for_timeout(1600); mark('H1')
        # A: nova rota
        await tap(pg,pg.locator(f'[onclick="rotaAbrirDia(\'{alvo}\')"]').first); await pg.wait_for_timeout(1000)
        await tap(pg,pg.locator('text=Nova rota para este dia >> visible=true').first); await pg.wait_for_timeout(900); mark('A0')
        await tap(pg,pg.locator('#rotaRegiao')); await pg.keyboard.type('Centro + Bairro Jardim',delay=60)
        await tap(pg,pg.locator('#rotaObs')); await pg.keyboard.type('Sair às 8h. Obra da Rua 3 primeiro.',delay=45)
        for dav,cli in [('1052','Cliente Exemplo 4'),('1053','Cliente Exemplo 5')]:
            await tap(pg,pg.locator('#rotaEntDav')); await pg.keyboard.type(dav,delay=70)
            await pg.evaluate(f"document.getElementById('rotaEntData').value='{alvo}'")
            await tap(pg,pg.locator('#rotaEntCliente')); await pg.keyboard.type(cli,delay=55)
            await tap(pg,pg.locator('text=+ Adicionar entrega >> visible=true').first); await pg.wait_for_timeout(500)
        await tap(pg,pg.locator('#moRotaForm .btn-primary').last); await pg.wait_for_timeout(1500); mark('A1')
        await pg.evaluate("document.querySelectorAll('.mo.open,.mo.show').forEach(m=>{});")
        try: await pg.evaluate("fecharMo('moRota')")
        except Exception: pass
        await pg.wait_for_timeout(1500); mark('B0')
        await pg.evaluate("window.scrollBy({top:420,behavior:'smooth'})"); await pg.wait_for_timeout(2400); mark('B1')
        await pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await pg.wait_for_timeout(1000)
        # C: concluir uma rota
        dc=com[0]
        await tap(pg,pg.locator(f'[onclick="rotaAbrirDia(\'{dc}\')"]').first); await pg.wait_for_timeout(1500); mark('C0')
        await tap(pg,pg.locator('text=Concluir >> visible=true').first); await pg.wait_for_timeout(2200); mark('C1'); await stop()
        await pg.wait_for_timeout(300); await b.close()
    meta=[]
    for i,(ts,data) in enumerate(frames):
        fn=f'{i:05d}.jpg'; open(os.path.join(OUT,fn),'wb').write(base64.b64decode(data)); meta.append((fn,ts))
    json.dump({'frames':meta,'marks':marks},open(os.path.join(R,'meta.json'),'w')); print('frames',len(frames))
asyncio.run(main())
