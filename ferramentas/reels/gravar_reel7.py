"""Reel 7 — Encomenda de cliente: venda casada registrada, comprada e acompanhada até a entrega."""
from datetime import date, timedelta
from rec import Rec, rodar
r = Rec('reel7')
async def f(pw):
    pg = await r.abrir(pw)
    await r.nav('Nova', 1800)
    await r.start(); r.mark('H0'); await r.w(500)
    await r.tap(pg.locator("text=Encomenda >> visible=true")); await r.w(1300); r.mark('H1')
    # PASSO 1: registrar a encomenda com os dados do cliente
    r.mark('A0')
    await r.digitar('#eCliente', 'Cliente Exemplo 4', 55)
    await r.digitar('#eTel', '(00) 90000-0000', 45)
    await r.digitar('#eEnd', 'Rua Exemplo, 100 - Obra', 40)
    await r.centro("document.getElementById('eProd')", 700)
    await r.digitar('#eProd', 'Porcelanato 90x90 Acetinado', 50)
    await r.digitar('#eMarca', 'Marca F', 70)
    await r.digitar('#eQtd', '48', 120)
    await pg.select_option('#eUn', 'm²'); await r.w(300)
    r.mark('A1')
    # PASSO 2: valor e prazo combinados
    await r.centro("document.getElementById('eVlr')", 800)
    await r.digitar('#eVlr', '129.90', 90)
    await pg.fill('#ePrazo', (date.today()+timedelta(days=10)).isoformat()); await r.w(400)
    await r.centro("document.getElementById('ePrazo')", 900)
    await r.tap(pg.locator("button[onclick=\"salvar('encomenda')\"]")); await r.w(1400)
    await r.nav('Fila', 1000)
    await r.tap(pg.locator('text=MARCA F >> visible=true')); await r.w(1200)
    await r.rolar(330, 1600)
    r.mark('B1')
    # PASSO 3: a encomenda no painel, com cliente, prazo e valor
    await r.nav('Dash', 1200)
    await r.centro("[...document.querySelectorAll('*')].find(e=>e.children.length==0&&/LTIMAS DEMANDAS/i.test(e.textContent))", 1600)
    await r.rolar(200, 1500); r.mark('C1')
    await r.stop(); await r.foto('fim'); await r.fechar()
rodar(f)
