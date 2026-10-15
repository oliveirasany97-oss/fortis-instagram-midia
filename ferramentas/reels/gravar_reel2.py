import asyncio, os, time, json, base64, shutil
from playwright.async_api import async_playwright
from demo import abrir, D
R=os.path.join(D,'reel2'); OUT=os.path.join(R,'frames'); shutil.rmtree(R,ignore_errors=True); os.makedirs(OUT)
U='file://'+os.path.join(D,'flow_demo.html')
frames=[]; marks=[]
TAP_JS="""window.__tap=(x,y)=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(217,181,121,.55);border:2px solid #D9B579;z-index:999999;pointer-events:none;transition:all .45s ease-out`;document.body.appendChild(d);requestAnimationFrame(()=>{d.style.transform='scale(1.8)';d.style.opacity='0'});setTimeout(()=>d.remove(),600)}"""
async def tap(pg,loc,espera=250):
    await loc.scroll_into_view_if_needed(); bb=await loc.bounding_box()
    await pg.evaluate(TAP_JS); await pg.evaluate(f"__tap({bb['x']+bb['width']/2},{bb['y']+bb['height']/2})")
    await pg.wait_for_timeout(espera); await loc.click()
def mark(n): marks.append((n,time.time())); print('mark',n)
ESCOLHAS_JS="""(a)=>{const [pref,nivel]=a;const R=window.__RH;const vaga={cargo:'vendedor'};const out=[];
  R.rhRequisitosDoCargo('vendedor').forEach(q=>{const vals=q.o.map((o,i)=>o.v!==undefined?o.v:String(i));
    const ok=vals.filter(v=>{try{const st=R.rhStatusRequisito(q,v,vaga);return st&&st.st==='ok'}catch(e){return false}});
    out.push(['candPub_req_'+q.id, nivel>=2&&ok.length?ok[ok.length-1]:(ok[0]||vals[0])]);});
  R.rhSituacoesDoCargo('vendedor').forEach((q,n)=>{const alvo=nivel===3?(n===1?1:3):(nivel===2?[3,2,2,2,1][n%5]:(n%2?1:2));
    let i=q.o.findIndex(o=>o.s===alvo);if(i<0)i=q.o.findIndex(o=>o.s===3);out.push(['candPub_sit_'+q.id,String(i)]);});
  const g={};document.querySelectorAll('input[name^="candPub_q"]').forEach(r=>{(g[r.name]=g[r.name]||[]).push(r)});
  Object.entries(g).forEach(([n,rs],k)=>{const want=(k%3===2&&pref==='I')?'D':pref;out.push([n,(rs.find(r=>r.value===want)||rs[0]).value]);});
  return out;}"""
async def candidatar(pg,nome,tel,pref,nivel,filmar=False):
    await pg.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('ffrh_')).forEach(k=>localStorage.removeItem(k))")
    await pg.goto(U+'?rhVaga=DEMO01_vaga1'); await pg.wait_for_timeout(2500)
    if filmar:
        await pg.add_style_tag(content='#candPubCurriculo{visibility:hidden}')
        await start(); mark('B0'); await pg.wait_for_timeout(1500)
    esc=await pg.evaluate(ESCOLHAS_JS,[pref,nivel])
    if filmar:
        await tap(pg,pg.locator('#candPubNome')); await pg.keyboard.type(nome,delay=70)
        await tap(pg,pg.locator('#candPubTelefone')); await pg.keyboard.type(tel,delay=60)
        for n,v in esc:
            loc=pg.locator(f'input[name="{n}"][value="{v}"]')
            await pg.evaluate("(e)=>e.closest('.rh-q').scrollIntoView({behavior:'smooth',block:'center'})",await loc.element_handle()); await pg.wait_for_timeout(420)
            await tap(pg,loc.locator('xpath=..'),180); await pg.wait_for_timeout(120)
        await tap(pg,pg.locator('#candPubLgpd').locator('xpath=..'))
        await tap(pg,pg.locator('#btnCandPubEnviar')); await pg.wait_for_timeout(300)
        await pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await pg.wait_for_timeout(2300); mark('B1'); await stop()
    else:
        await pg.fill('#candPubNome',nome); await pg.fill('#candPubTelefone',tel)
        for n,v in esc: await pg.locator(f'input[name="{n}"][value="{v}"]').check()
        await pg.locator('#candPubLgpd').check()
        await pg.evaluate("enviarCandidaturaPublica('DEMO01','vaga1')"); await pg.wait_for_timeout(1500)
async def irRH(pg):
    await pg.goto(U); await pg.wait_for_timeout(3500)
    await pg.evaluate("navegar('RH',document.querySelector('.ni[data-view=\"RH\"]'))"); await pg.wait_for_timeout(2000)
    await pg.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.resolve()},configurable:true})")
async def main():
    global start, stop
    async with async_playwright() as pw:
        b,ctx,pg=await abrir(pw)
        pg.on('dialog',lambda d: asyncio.ensure_future(d.accept()))
        cdp=await ctx.new_cdp_session(pg)
        async def onframe(p):
            frames.append((p['metadata']['timestamp'],p['data']))
            try: await cdp.send('Page.screencastFrameAck',{'sessionId':p['sessionId']})
            except Exception: pass
        cdp.on('Page.screencastFrame',lambda p: asyncio.ensure_future(onframe(p)))
        start=lambda: cdp.send('Page.startScreencast',{'format':'jpeg','quality':88,'maxWidth':1080,'maxHeight':2338})
        stop=lambda: cdp.send('Page.stopScreencast')
        # candidatos de fundo (fora da gravação)
        await candidatar(pg,'Candidata Exemplo B','(00) 92222-2222','S',1)
        await candidatar(pg,'Candidato Exemplo C','(00) 93333-3333','D',2)
        # A: gestor gera o link da vaga
        await irRH(pg); await start(); mark('A0'); await pg.wait_for_timeout(1600)
        await tap(pg,pg.get_by_text('Link de divulgação').first); await pg.wait_for_timeout(2400); mark('A1'); await stop()
        # B: candidata responde pelo celular
        await candidatar(pg,'Candidata Exemplo A','(00) 91111-1111','I',3,filmar=True)
        # C: banco de talentos
        await irRH(pg); await pg.evaluate("rhTab('talentos')"); await pg.wait_for_timeout(1500)
        await start(); mark('C0'); await pg.wait_for_timeout(2800)
        await pg.evaluate("window.scrollBy({top:260,behavior:'smooth'})"); await pg.wait_for_timeout(1800); mark('C1')
        # D: painel da candidata
        await tap(pg,pg.get_by_text('Candidata Exemplo A').first); await pg.wait_for_timeout(1000); mark('D0'); await pg.wait_for_timeout(2600)
        SCR="(t)=>document.querySelectorAll('.mo').forEach(m=>{const b=m.querySelector('.mo-box');if(b&&b.offsetParent)b.scrollTo({top:t,behavior:'smooth'})})"
        await pg.evaluate(SCR,520); await pg.wait_for_timeout(2600)
        alvo=await pg.evaluate("""()=>{for(const m of document.querySelectorAll('.mo')){const b=m.querySelector('.mo-box');if(!b||!b.offsetParent)continue;
            const el=[...b.querySelectorAll('.sec-label,div')].find(x=>/PERFIL COMPORTAMENTAL/i.test(x.textContent)&&x.children.length<3);return el?el.getBoundingClientRect().top-b.getBoundingClientRect().top+b.scrollTop-120:1400}return 1400}""")
        await pg.evaluate(SCR,alvo); await pg.wait_for_timeout(3000); mark('D1')
        alvo2=await pg.evaluate("""()=>{for(const m of document.querySelectorAll('.mo')){const b=m.querySelector('.mo-box');if(!b||!b.offsetParent)continue;
            const el=[...b.querySelectorAll('div')].find(x=>/ROTEIRO SUGERIDO/i.test(x.textContent)&&x.children.length<3);return el?el.getBoundingClientRect().top-b.getBoundingClientRect().top+b.scrollTop-120:null}return null}""")
        if alvo2: await pg.evaluate(SCR,alvo2); await pg.wait_for_timeout(3000)
        mark('D2'); await stop(); await pg.wait_for_timeout(300)
        await b.close()
    meta=[]
    for i,(ts,data) in enumerate(frames):
        fn=f'{i:05d}.jpg'; open(os.path.join(OUT,fn),'wb').write(base64.b64decode(data)); meta.append((fn,ts))
    json.dump({'frames':meta,'marks':marks},open(os.path.join(R,'meta.json'),'w')); print('frames',len(frames))
asyncio.run(main())
