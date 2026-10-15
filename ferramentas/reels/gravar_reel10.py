"""Reel 10 — Pedido de preço por link (nova versão do reel 1, sem preço do FLOW)."""
import datetime
from rec import Rec, rodar
from demo import D
import os
r = Rec('reel10')
U = 'file://' + os.path.join(D, 'flow_demo.html')
async def f(pw):
    # gancho + passo 2/3: a fila da MARCA B no FLOW do comprador
    pg = await r.abrir(pw, qs='?prop=DEMO01_cot1_r1')
    # PASSO 1: o fornecedor preenche os preços pelo link
    await r.start(); r.mark('A0'); await r.w(1800)
    ids = await pg.eval_on_selector_all('[id^="propPreco_"]', 'e=>e.map(x=>x.id.slice(10))')
    for i, d in enumerate(ids):
        await r.digitar('#propPreco_' + d, ['31.9', '24.5'][i % 2], 140)
        await r.digitar('#propFrete_' + d, '0.80', 120); await r.w(400)
    await r.centro("document.getElementById('propPagamento')")
    await r.digitar('#propPagamento', '30/60 dias', 90)
    await pg.fill('#propPrevisao', (datetime.date.today() + datetime.timedelta(days=5)).isoformat())
    await r.centro("document.getElementById('propTotalTxt')", 1200)
    await r.tap(pg.get_by_text('Enviar Proposta')); await r.w(2300); r.mark('A1')
    await r.stop()
    await pg.goto(U); await r.w(3500)
    await r.nav('Fila', 1500)
    await r.start(); r.mark('H0'); await r.w(500)
    await r.rolar(240, 1300); r.mark('H1')
    await r.pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await r.w(700); r.mark('B0')
    await r.tap(pg.locator('text=MARCA B >> visible=true')); await r.w(1800)
    await r.centro("[...document.querySelectorAll('b')].find(x=>x.textContent.includes('Pedido de preço')&&x.offsetParent)", 2600)
    r.mark('B1')
    await r.tap(pg.locator('text=Aplicar menor preço >> visible=true')); await r.w(2500)
    await r.rolar(420, 2800); r.mark('B2')
    await r.stop(); await r.foto('fim'); await r.fechar()
rodar(f)
