"""Abre o FORTÍS FLOW com uma loja de demonstração fictícia (sem rede, sem dados reais)."""
import asyncio, json, os, random, sys
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

D = os.path.dirname(os.path.abspath(__file__))
EMP = 'DEMO01'
random.seed(7)

def iso(dias=0, horas=0):
    return (datetime.now() - timedelta(days=dias, hours=horas)).isoformat()

def seed():
    B = f'fortis_demandas_empresas/{EMP}'
    s = {}
    s[B] = {'nome': 'Loja Modelo Materiais', 'nomeFantasia': 'Loja Modelo Materiais', 'cidade': 'Cidade Exemplo - MG', 'ativo': True}
    users = [('u_adm', 'Carlos Gestor', 'admin', True), ('u_ger', 'Ana Gerente', 'gerente', False), ('u_cmp', 'Bruno Compras', 'compras', False),
             ('u_v1', 'João Vendedor', 'vendedor', False), ('u_v2', 'Maria Vendedora', 'vendedor', False), ('u_v3', 'Pedro Vendedor', 'vendedor', False),
             ('u_alm', 'Lucas Almoxarife', 'almoxarife', False)]
    for uid, nome, perfil, dono in users:
        s[f'{B}/usuarios/{uid}'] = {'nome': nome, 'user': nome.split()[0].lower(), 'perfil': perfil, 'ativo': True, 'dono': dono, 'senhaAtualizadaEm': '', 'criadoEm': iso(90)}
    prods = [('Cimento CP II 50kg', 'Marca A', 'Básico', 'sc'), ('Argamassa AC-II 20kg', 'Marca B', 'Básico', 'sc'), ('Tinta Acrílica 18L Branco', 'Marca C', 'Tintas', 'gl'),
             ('Tubo PVC 100mm 6m', 'Marca D', 'Hidráulica', 'un'), ('Cabo Flexível 2,5mm 100m', 'Marca E', 'Elétrica', 'rl'), ('Porcelanato 60x60 Cinza', 'Marca F', 'Pisos', 'm²'),
             ('Vergalhão 10mm 12m', 'Marca G', 'Básico', 'br'), ('Registro de Gaveta 3/4', 'Marca D', 'Hidráulica', 'un'), ('Disjuntor 20A', 'Marca E', 'Elétrica', 'un'),
             ('Massa Corrida 25kg', 'Marca C', 'Tintas', 'bd'), ('Telha Fibrocimento 2,44m', 'Marca H', 'Coberturas', 'un'), ('Rejunte Flexível 1kg', 'Marca B', 'Pisos', 'un'),
             ('Caixa d\'Água 1000L', 'Marca I', 'Hidráulica', 'un'), ('Lâmpada LED 12W', 'Marca E', 'Elétrica', 'un'), ('Areia Média m³', 'Marca J', 'Básico', 'm³')]
    vend = ['João Vendedor', 'Maria Vendedora', 'Pedro Vendedor']
    stat = ['aberto'] * 6 + ['na_fila'] * 4 + ['aguardando_aprovacao'] * 2 + ['comprado'] * 4 + ['resolvido'] * 8 + ['atrasado'] * 2
    tipos = ['ruptura'] * 5 + ['encomenda'] * 2 + ['gondola', 'orcamento']
    for i in range(34):
        p = random.choice(prods); st = stat[i % len(stat)]; tp = random.choice(tipos); d = random.randint(0, 20)
        dem = {'tipo': tp, 'status': st, 'produto': p[0], 'marca': p[1], 'categoria': p[2], 'unidade': p[3], 'qtdSugerida': str(random.choice([5, 10, 20, 30, 50])),
               'qtd': str(random.choice([5, 10, 20])), 'urgencia': random.choice(['alta', 'media', 'baixa']), 'vendedor': random.choice(vend), 'perfil': 'vendedor',
               'criadoEm': iso(d, random.randint(0, 9)), 'atualizadoEm': iso(max(d - 1, 0)), 'comentarios': [], 'estoqueAtual': str(random.randint(0, 3)),
               'historico': [{'acao': 'aberto', 'por': random.choice(vend), 'em': iso(d)}]}
        if tp == 'encomenda':
            dem.update({'cliente': random.choice(['Cliente Exemplo 1', 'Cliente Exemplo 2', 'Cliente Exemplo 3']), 'telefone': '(00) 90000-0000', 'prazo': (datetime.now() + timedelta(days=5)).date().isoformat(), 'valorNegociado': random.choice([480.0, 1250.0, 2300.0])})
        if st in ('comprado','resolvido'): dem['ocValor'] = random.choice([860.0, 1240.0, 2150.0, 3480.0, 4720.0])
        s[f'{B}/demandas/dm{i:03d}'] = dem
    for j,(pp,vt) in enumerate([('Porcelanato 60x60 Cinza',640.0),('Telha Fibrocimento 2,44m',312.0),('Tinta Acrílica 18L Branco',489.0)]):
        s[f'{B}/demandas/av{j}'] = {'tipo':'avaria','status':'resolvido','produto':pp,'marca':'Marca F','categoria':'Pisos','unidade':'un','qtd':'2','valorTotal':vt,'vendedor':'Lucas Almoxarife','perfil':'almoxarife','criadoEm':iso(3+j*4),'atualizadoEm':iso(2),'comentarios':[],'historico':[]}
    # filas de compra por marca, com as demandas "na_fila"
    filas = {}
    for k, dem in [(k, v) for k, v in s.items() if '/demandas/' in k]:
        if dem['status'] in ('na_fila', 'aguardando_aprovacao') and dem['tipo'] not in ('ruptura', 'encomenda'):
            dem['status'] = 'aberto'
        if dem['status'] in ('na_fila', 'aguardando_aprovacao'):
            m = dem['marca'].upper(); fid = 'fila_' + m.replace(' ', '_')
            f = filas.setdefault(fid, {'id': fid, 'tipo': 'marca', 'marca': m, 'repId': None, 'repNome': 'Representante ' + m.split()[-1], 'repTel': None, 'obs': None,
                                       'status': 'ativa', 'itens': [], 'criadoEm': iso(6), 'criadoPor': 'Bruno Compras'})
            f['itens'].append({'demId': k.split('/')[-1], 'produto': dem['produto'], 'codigo': None, 'qtd': dem['qtdSugerida'], 'unidade': dem['unidade'], 'tipo': dem['tipo'],
                               'vendedor': dem['vendedor'], 'marca': dem['marca'], 'copia': False, 'adicionadoEm': iso(3)})
            dem.update({'status': 'na_fila', 'filaId': fid, 'filaMarca': m})
    for fid, f in filas.items():
        s[f'{B}/filas/{fid}'] = f
    # pedido de preço por link na fila da MARCA B
    fb = filas.get('fila_MARCA_B')
    if fb:
        dest = [{'id': 'r1', 'nome': 'Distribuidora Alfa', 'wa': None}, {'id': 'r2', 'nome': 'Atacado Beta', 'wa': None}, {'id': 'r3', 'nome': 'Representante B', 'wa': None}]
        fb.update({'atacCotId': 'cot1', 'atacCotDest': dest})
        s[f'{B}/cotacoes/cot1'] = {'empNome': 'Loja Modelo Materiais', 'status': 'aberta', 'filaId': 'fila_MARCA_B', 'marca': 'MARCA B', 'obs': 'Entrega na loja. Preço válido por 7 dias.',
                                   'itens': [{'demId': it['demId'], 'produto': it['produto'], 'qtd': it['qtd'], 'unidade': it['unidade'], 'codigo': None} for it in fb['itens']],
                                   'representantes': dest, 'propostas': {}, 'criadoEm': iso(1), 'criadoPor': 'Bruno Compras'}
        its = fb['itens']
        for rid, nome, pr, pag in [('r2', 'Atacado Beta', (29.4, 26.9), '28 dias'), ('r3', 'Representante B', (33.2, 23.8), '30/60/90 dias')]:
            precos = {it['demId']: round(pr[i % 2] + .8, 2) for i, it in enumerate(its)}
            s[f'{B}/cotacoes/cot1/respostas/{rid}'] = {'repId': rid, 'nome': nome, 'precos': precos, 'pagamento': pag, 'previsao': (datetime.now() + timedelta(days=6)).date().isoformat(),
                'valorTotal': sum(precos[it['demId']] * float(it['qtd']) for it in its), 'enviadoEm': iso(0, 2),
                'composicao': {it['demId']: {'partida': pr[i % 2], 'frete': .8, 'ipiPct': 0, 'stPct': 0} for i, it in enumerate(its)}}
    # Fortís RH: vaga com link público
    s[f'{B}/rh_vagas/vaga1'] = {'titulo': 'Vendedor(a) de Balcão', 'cargo': 'vendedor', 'descricao': 'Atendimento no balcão e no WhatsApp, orçamento e venda de materiais de construção. Segunda a sábado.',
                                'status': 'aberta', 'criadoEm': iso(4), 'criadoPor': 'Ana Gerente'}
    # metas inteligentes de outubro
    am = datetime.now().strftime('%Y-%m')
    for uid, nome, alvo, base in [('u_v1', 'João Vendedor', 120000, 6100), ('u_v2', 'Maria Vendedora', 110000, 5200), ('u_v3', 'Pedro Vendedor', 95000, 3900)]:
        mid = f'{uid}_{am}'
        s[f'{B}/metas/{mid}'] = {'id': mid, 'tipo': 'vendedor', 'vendedorId': uid, 'vendedorNome': nome, 'setorId': None, 'filialId': None, 'categoriaId': None,
                                 'mes': datetime.now().month, 'ano': datetime.now().year, 'anoMes': am, 'metaMensal': alvo, 'diasUteis': 24,
                                 'atualizadoEm': iso(10), 'atualizadoPor': 'Carlos Gestor', 'criadoEm': iso(10), 'criadoPor': 'Carlos Gestor'}
        dia = datetime.now().replace(day=1)
        while dia.date() < datetime.now().date():
            if dia.weekday() != 6:
                ds = dia.date().isoformat()
                s[f'{B}/metas/{mid}/resultados/{ds}'] = {'id': ds, 'data': ds, 'valor': round(base * random.uniform(.7, 1.3), 2), 'tipo': 'diario', 'diasCobertos': 1, 'criadoEm': iso(0), 'criadoPor': nome}
            dia += timedelta(days=1)
    # rotas de entrega
    regs = ['Centro', 'Bairro Jardim', 'Zona Rural Norte', 'Vila Nova', 'Bairro Industrial', 'Alto da Serra']
    for i in range(10):
        dt = (datetime.now() + timedelta(days=random.randint(-6, 12))).date().isoformat()
        s[f'{B}/rotas/rota_{i}'] = {'data': dt, 'regiao': regs[i % len(regs)], 'obs': None, 'concluida': dt < datetime.now().date().isoformat(),
                                    'entregas': [{'dav': f'DAV-{1000 + i * 3 + j}', 'dataFaturamento': dt, 'cliente': f'Cliente Exemplo {j + 1}'} for j in range(random.randint(2, 5))],
                                    'criadoPor': 'Ana Gerente', 'criadoEm': iso(8), 'atualizadoPor': 'Ana Gerente', 'atualizadoEm': iso(2)}
    return s

FONT_CSS = """
@font-face{font-family:'Bebas Neue';src:url(https://fonts.local/bebas.woff2)}
@font-face{font-family:'Sora';font-weight:300;src:url(https://fonts.local/sora-300.woff2)}
@font-face{font-family:'Sora';font-weight:400;src:url(https://fonts.local/sora-400.woff2)}
@font-face{font-family:'Sora';font-weight:500;src:url(https://fonts.local/sora-500.woff2)}
@font-face{font-family:'Sora';font-weight:600;src:url(https://fonts.local/sora-600.woff2)}
@font-face{font-family:'Sora';font-weight:700;src:url(https://fonts.local/sora-700.woff2)}
@font-face{font-family:'JetBrains Mono';src:url(https://fonts.local/mono.woff2)}
"""
FONTS = {'bebas': 'fontsource-bebas-neue/files/bebas-neue-latin-400-normal.woff2', 'mono': 'fontsource-jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2',
         **{f'sora-{w}': f'fontsource-sora/files/sora-latin-{w}-normal.woff2' for w in (300, 400, 500, 600, 700)}}

async def rotear(route):
    u = route.request.url
    if 'gstatic.com/firebasejs' in u:
        nome = u.split('/')[-1].replace('firebase-', '')
        return await route.fulfill(path=os.path.join(D, 'mock', nome), content_type='application/javascript')
    if 'fonts.googleapis.com' in u:
        return await route.fulfill(body=FONT_CSS, content_type='text/css')
    if 'fonts.local/' in u:
        k = u.split('/')[-1].replace('.woff2', '')
        return await route.fulfill(path=os.path.join(D, 'fonts', FONTS[k]), content_type='font/woff2')
    if 'run.app' in u:
        return await route.fulfill(body=json.dumps({'ok': True, 'email': 'demo@loja.modelo', 'secret': 'x', 'usuarioId': 'u_adm'}), content_type='application/json')
    if u.startswith('file://') or u.startswith('data:') or u.startswith('blob:'):
        return await route.continue_()
    return await route.abort()

async def abrir(pw, mobile=True, video_dir=None, uid='u_adm', qs=''):
    b = await pw.chromium.launch(args=['--lang=pt-BR','--force-device-scale-factor=2.62'])
    vp = {'width': 412, 'height': 892} if mobile else {'width': 1440, 'height': 900}
    ctx = await b.new_context(viewport=vp, device_scale_factor=2.62 if mobile else 1.5, is_mobile=mobile, has_touch=mobile,
                              record_video_dir=video_dir, record_video_size={'width': 1080, 'height': 2338} if mobile else None, locale='pt-BR', timezone_id='America/Sao_Paulo')
    await ctx.route('**/*', rotear)
    perfil = {'u_adm': 'admin', 'u_v1': 'vendedor', 'u_cmp': 'compras'}.get(uid, 'admin')
    init = f"""
      window.__FF_PERSIST = true; window.__FF_SEED = {json.dumps(seed())};
      window.__FF_CLAIMS = {{ff:'loja', emp:'{EMP}', fid:'{uid}', perfil:'{perfil}'}};
      try{{localStorage.setItem('ff_sessao_v1', JSON.stringify({{empCod:'{EMP}', uid:'{uid}', h:'', v:2, em:Date.now()}}));}}catch(e){{}}
      try{{Notification}}catch(e){{}}
    """
    await ctx.add_init_script(init)
    pg = await ctx.new_page()
    pg.on('console', lambda m: m.type in ('error',) and print('CONSOLE', m.type, m.text[:200]))
    pg.on('pageerror', lambda e: print('PAGEERR', str(e)[:300]))
    await pg.goto('file://' + os.path.join(D, 'flow_demo.html') + qs)
    await pg.wait_for_timeout(3500)
    return b, ctx, pg

async def main():
    async with async_playwright() as pw:
        b, ctx, pg = await abrir(pw)
        await pg.screenshot(path=os.path.join(D, 'out_dash.png'))
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
