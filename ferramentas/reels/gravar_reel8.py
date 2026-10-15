"""Reel 8 — Fila de compras por marca: cada falta vira item no pedido certo."""
from rec import Rec, rodar
r = Rec('reel8')
async def f(pw):
    pg = await r.abrir(pw)
    await r.nav('Fila', 1800)
    await r.start(); r.mark('H0'); await r.w(400)
    await r.rolar(220, 1300); await r.w(300); r.mark('H1')
    await r.pg.evaluate("window.scrollTo({top:0,behavior:'smooth'})"); await r.w(700); r.mark('A0')
    # PASSO 1: as faltas já estão separadas por marca
    await r.tap(pg.locator('text=MARCA E >> visible=true')); await r.w(1500)
    await r.rolar(380, 1500); r.mark('A1')
    # PASSO 2: itens com quantidade sugerida
    await r.centro("[...document.querySelectorAll('button')].find(b=>b.textContent.includes('Registrar OC')&&b.offsetParent)", 2600); r.mark('B1')
    # PASSO 3: fechar o pedido da fila
    await r.tap(pg.locator('text=Registrar OC >> visible=true')); await r.w(1300)
    await r.digitar('#filaOCvalor', '3840.00', 90)
    await r.w(500)
    await r.pg.evaluate("document.querySelector('.mo.open .mo-box')?.scrollBy({top:700,behavior:'smooth'})"); await r.w(1800); r.mark('C1')
    await r.stop(); await r.foto('fim'); await r.fechar()
rodar(f)
