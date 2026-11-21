"""Conteúdo de 21/11/2026 (feed 1080x1440, stories 1080x1920) + story 06:00 de 22/11.

Mesmo layout em fluxo e checagem automática de sobreposição/áreas seguras de dia-16-11.py.
"""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gerador as G
from PIL import Image
from playwright.async_api import async_playwright

A = G.A
W, H = 1080, 1440
SW, SH = 1080, 1920
G.ICONES["obra"] = '<path d="M8 54h48M14 54V26l18-14 18 14v28"/><path d="M26 54V38h12v16"/><path d="M4 30l28-22 28 22"/>'

CSS = """
.col{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center}
.col>*{position:static!important}
.meio{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;width:100%;gap:72px}
.zona .meio{gap:62px}
.zona .tab .lin{padding:13px 30px}
.meio>*{position:static!important}
.base>*{position:static!important}
.col .logo{transform:none}
.col .titulo,.col .kicker,.col .cta,.col .sub,.col .rodape,.col .handle,.meio .sub,.meio .cta{width:100%}
.base{display:flex;flex-direction:column;align-items:center;gap:40px;width:100%}
.fonte{max-width:900px;text-align:center;font-size:20px;line-height:1.4;color:#b3bfd1;background:rgba(5,12,25,.88);padding:12px 20px;border-radius:12px}
.selo{display:inline-block;font-weight:700;letter-spacing:4px;font-size:18px;color:#0E1F39;background:#D9B579;padding:6px 14px;border-radius:8px}
.tab{width:100%;text-align:left}
.tab .lin{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:18px 30px;border-bottom:1px solid rgba(217,181,121,.25)}
.tab .lin:last-child{border-bottom:none}
.tab .lin.d{background:rgba(217,181,121,.14)}
.tab .a{font-weight:700;color:#fff}
.tab .b{font-weight:700;color:#D9B579;text-align:right}
.tab .h{color:#D9B579;font-weight:600;letter-spacing:3px}
.check:last-child{margin-bottom:0!important}
"""


def tit(linhas):
    return "".join(f'<div class="{"metal" if i == len(linhas) - 1 else "branco"}">{G.e(t)}</div>' for i, t in enumerate(linhas))


def titulo(linhas, fs, mx=920, lh=1.04):
    return f'<div class="titulo k" data-max="{mx}" data-fs="{fs}" style="line-height:{lh}">{tit(linhas)}</div>'


def kicker(t, fs=24):
    return f'<div class="kicker k" style="font-size:{fs}px">{t}</div>'


def sub(t, fs=34, lr=100):
    return f'<p class="sub k" style="font-size:{fs}px;padding:0 {lr}px">{t}</p>'


def lista(itens, fs_b=32, fs_s=23, num=True, w=860, ini=1):
    lis = "".join(f'<div class="check"><div class="box">{(k + ini) if num else "✓"}</div><div><b style="font-size:{fs_b}px">{G.e(a)}</b><span style="font-size:{fs_s}px">{G.e(b)}</span></div></div>' for k, (a, b) in enumerate(itens))
    return f'<div class="k" style="width:{w}px">{lis}</div>'


def rodape_feed():
    return '<div class="base"><div class="rodape k" style="font-size:21px">FORTÍS SOLUÇÕES MATCON</div></div>'


def feed(meio, logo_w=130, b=.75, fonte=None):
    """Feed 3:4. Coluna de 60px no topo a 56px na base."""
    f = f'<div class="fonte k">{fonte}</div>' if fonte else ''
    return f'''<div class="arte" style="width:{W}px;height:{H}px">{G.fundo(W, H, b)}
  <div class="col" style="top:64px;bottom:56px">
    <img class="logo k" src="{A}/logo.png" style="width:{logo_w}px;margin-bottom:44px">
    <div class="meio">{meio}</div>
    <div class="base" style="margin-top:40px">{f}<div class="rodape k" style="font-size:21px">FORTÍS SOLUÇÕES MATCON</div></div>
  </div></div>'''


def story(meio, fonte=None, logo_w=150):
    """Story 9:16. Tudo dentro de 250px (topo) e 400px (base). Ordem: conteúdo, rodapé, @, fonte."""
    f = f'<div class="fonte k" style="font-size:19px;max-width:880px">{fonte}</div>' if fonte else ''
    return f'''<div class="arte" style="width:{SW}px;height:{SH}px">{G.fundo(SW, SH, .93)}
  <div class="col zona" style="top:262px;bottom:410px">
    <img class="logo k" src="{A}/logo.png" style="width:{logo_w}px;margin-bottom:44px">
    <div class="meio">{meio}</div>
    <div class="base" style="margin-top:50px">
      <div class="rodape k" style="font-size:22px">FORTÍS SOLUÇÕES MATCON</div>
      <div class="handle k" style="font-size:24px">@fortismatcon.oficial</div>
      {f}
    </div>
  </div></div>'''


def card(html, pad="6px 0", w=900):
    return f'<div class="card k" style="width:{w}px;padding:{pad}">{html}</div>'


def tabela(linhas, fs=32, destaque=()):
    return '<div class="tab">' + "".join(f'<div class="lin{" d" if i in destaque else ""}"><span class="a" style="font-size:{fs}px">{a}</span><span class="b" style="font-size:{fs}px">{b}</span></div>' for i, (a, b) in enumerate(linhas)) + '</div>'



def row(left, right, gap=40):
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:{gap}px;width:100%">{left}{right}</div>'


# ================= FEED 10:30 — CARROSSEL SALVÁVEL: TEMPORADA DE CHUVA =================
def chuva():
    capa = feed(f'''{kicker("MANDE PARA SUA EQUIPE")}
  {titulo(["CHOVEU.", "A LOJA ESTÁ PRONTA?"], 112)}
  {sub("Ajustes para a temporada de chuva: <b>vender o que ela pede e não perder estoque.</b>", 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)
    s2 = feed(f'''{kicker("NA FRENTE DA LOJA")}
  {titulo(["EXPONHA O QUE", "A CHUVA PEDE"], 96)}
  {lista([("Impermeabilizante e manta", "Perto da entrada, com o vendedor sabendo indicar o uso."),
          ("Calha, rufo e telha", "Quem está com goteira quer resolver no mesmo dia."),
          ("Lona", "Obra parada pela chuva precisa cobrir o material.")], 34, 24)}''', 110, 1.3)
    s3 = feed(f'''{kicker("NO DEPÓSITO")}
  {titulo(["PROTEJA", "O ESTOQUE"], 100)}
  {lista([("Saco fora do chão", "Cimento, argamassa e rejunte sobre estrado, longe da parede."),
          ("Olhe o telhado do depósito", "Goteira em cima de saco é prejuízo que ninguém vê."),
          ("Saco mais antigo sai primeiro", "Quanto mais tempo parado na umidade, maior o risco de perda.")], 32, 23, ini=4)}''', 110, 1.3)
    fim = feed(f'''{titulo(["E NA", "ENTREGA"], 104)}
  {lista([("Confirme antes de sair", "A obra consegue receber hoje?"),
          ("Lona no caminhão", "Material molhado na entrega volta como reclamação."),
          ("Reagende avisando", "Cliente avisado não fica esperando à toa.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 90px">Quer preparar a loja para a chuva? <b>Chame no direct.</b></p>''', 110, 1.3)
    return [("1030-temporada-de-chuva-1", capa), ("1030-temporada-de-chuva-2", s2), ("1030-temporada-de-chuva-3", s3), ("1030-temporada-de-chuva-4", fim)]


# ================= FEED 15:30 — A CONTA DA LOJA: TAXA DA MAQUININHA =================
def conta_taxa():
    tab = tabela([("Venda no crédito", "R$ 1.000"), ("Lucro bruto (margem de 25%)", "R$ 250"),
                  ("Taxa da maquininha (4%)", "− R$ 40"), ("O que sobra do lucro", "R$ 210")], 30, destaque=(3,))
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(["A MAQUININHA", "É SÓCIA DA VENDA"], 92)}
  {sub("Perto da venda, a taxa parece pequena. <b>Perto do lucro, ela leva 16%.</b>", 30, 100)}
  {card(tab, "4px 0", 860)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>
  <p class="cta k" style="font-size:29px;padding:0 80px">Você sabe quanto paga de taxa em cada forma de pagamento? <b>Chame no direct.</b></p>''', 110, 1.3)


# ================= FEED 19:30 — ESPELHO DO DONO =================
def espelho():
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(["VENDE BEM, MAS O", "DINHEIRO NÃO APARECE"], 88)}
  {lista([("O mês foi bom de venda", "Mas a conta do banco não acompanhou."),
          ("Parte do lucro virou mercadoria", "Compra a mais fica no depósito, não no caixa."),
          ("O prazo do cliente esticou", "A venda saiu, o dinheiro ainda não entrou."),
          ("A conta da casa e a da loja se misturam", "E ninguém sabe quanto a loja lucrou de verdade.")], 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">Vender bem e lucrar bem são coisas diferentes. <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


# ================= FEED 22:30 — TODA LOJA PRECISA TER =================
def toda_loja():
    return feed(f'''{kicker("TODA LOJA PRECISA TER")}
  {titulo(["A CALCULADORA", "DO BALCÃO"], 104)}
  {sub("O cliente pergunta <b>quanto precisa levar</b>. Quem responde certo vende a quantidade certa.", 29, 100)}
  {lista([("Rendimento dos fabricantes à mão", "Argamassa, rejunte e tinta: o consumo está na embalagem e na ficha técnica."),
          ("Uma folha de cálculo padrão", "Área, consumo e quantidade, do mesmo jeito para todo vendedor."),
          ("Conta feita na frente do cliente", "Ele vê de onde saiu o número e confia no pedido."),
          ("Perda combinada", "Recorte e quebra entram na conta, sem chute.")], 31, 23)}
  <p class="cta k" style="font-size:29px;padding:0 80px">Sua loja já tem? <b>Diagnóstico sem custo no direct.</b></p>''', 96, 1.3)


# ================= STORY 12:00 — MERCADO: PMC SETEMBRO =================
def story_pmc():
    tab = tabela([("Material de construção", "−1,3%"), ("Varejo (restrito)", "+0,2%"),
                  ("Varejo ampliado", "+0,2%")], 32, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · IBGE", 26)}
  {titulo(["VENDAS DE MATERIAL", "RECUAM 1,3%"], 88, 900)}
  {sub("Setembro contra agosto, na Pesquisa Mensal de Comércio.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Mercado parado pede <b>loja afinada: estoque, preço e atendimento.</b></p>''',
      'Fonte: IBGE, PMC set/2026 · via InfoMoney e Brasil em Folhas', 80)


# ================= STORY 18:00 — PRODUTO: FIO 1,5 x 2,5 (NBR 5410) =================
def story_fios():
    tab = tabela([("<span class='h'>CIRCUITO</span>", "<span class='h'>SEÇÃO MÍNIMA</span>"),
                  ("Iluminação", "1,5 mm²"), ("Tomadas de uso geral", "2,5 mm²")], 30)
    return story(f'''{kicker("ENTENDA A DIFERENÇA", 26)}
  {titulo(["FIO 1,5", "OU 2,5?"], 96, 900)}
  {card(tab)}
  {sub("A norma pede <b>circuitos separados</b> para iluminação e tomadas. Equipamento acima de 10 A, como chuveiro e ar-condicionado, tem <b>circuito próprio, dimensionado pelo eletricista.</b>", 28, 80)}
  <p class="cta k" style="font-size:30px;padding:0 80px">Vendedor que sabe isso <b>vende o fio certo.</b></p>''',
      'Fonte: ABNT NBR 5410 · O Setor Elétrico · Sienge · Cidesp', 80)


# ================= STORY 21:00 — FORTÍS FLOW: ROTA DE ENTREGA =================
def story_flow():
    esq = lista([("Calendário de rotas", "Entregas planejadas com antecedência."),
                 ("Busca por bairro", "Encaixe o pedido na rota da região."),
                 ("Próximas rotas à vista", "Balcão e entrega olhando a mesma agenda.")], 30, 22, w=470)
    cel = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:44px">
      <div class="k" style="width:280px;height:440px;border-radius:40px;border:8px solid #0b1424;outline:3px solid rgba(217,181,121,.85);box-shadow:0 0 40px rgba(217,181,121,.25);overflow:hidden;background:#0E1F39">
        <img src="{A}/telas/rota.png" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>
      <div class="k" style="font-weight:600;letter-spacing:4px;color:#D9B579;font-size:16px">TELA REAL · DADOS FICTÍCIOS</div></div>'''
    return story(f'''{kicker("FORTÍS FLOW", 28)}
  {titulo(["O CLIENTE SABE", "O DIA DA ENTREGA"], 84, 900)}
  {row(esq, cel)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Quer ver na sua loja? <b>Chame no direct.</b></p>''', None, 90)


# ================= STORY 06:00 (22/11) — BOM DIA, LOJISTA =================
def story_bomdia():
    return story(f'''<div class="kicker k" style="font-size:28px;margin-bottom:12px">BOM DIA, LOJISTA</div>
  {titulo(["QUEM COBRE", "QUEM?"], 112, 900)}
  {sub("Caixa, balcão, entrega, depósito: para cada função, <b>defina quem assume se alguém faltar.</b> Escreva e deixe à vista.", 38, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">A falta de um não pode parar a loja.</p>''', None, 170)

CHECA_JS = """
() => {
  const r = [];
  const arte = document.querySelector('.arte').getBoundingClientRect();
  const story = arte.height > 1500;
  const top = story ? 250 : 40, bot = story ? arte.height - 400 : arte.height - 40;
  const caixa = e => { if (e.tagName === 'IMG' || e.classList.contains('card') || e.classList.contains('fonte')) return e.getBoundingClientRect();
    const g = document.createRange(); g.selectNodeContents(e); const b = g.getBoundingClientRect(); return b.width ? b : e.getBoundingClientRect(); };
  const els = [...document.querySelectorAll('.k')].map(e => ({e, b: caixa(e), n: (e.className + ' ' + (e.innerText || 'img')).slice(0, 50)}));
  for (const x of els) {
    if (x.b.top < top || x.b.bottom > bot) r.push('FORA DA AREA SEGURA: ' + x.n + ' ' + Math.round(x.b.top) + '-' + Math.round(x.b.bottom));
    if (x.b.left < 50 || x.b.right > arte.width - 50) r.push('BORDA LATERAL: ' + x.n);
    if (x.e.scrollWidth > x.e.clientWidth + 2 && !x.e.classList.contains('titulo')) r.push('TEXTO TRANSBORDA: ' + x.n);
  }
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i].b, b = els[j].b;
    if (els[i].e.contains(els[j].e) || els[j].e.contains(els[i].e)) continue;
    const hOver = a.left < b.right && b.left < a.right;
    if (!hOver) continue;
    const gap = Math.max(b.top - a.bottom, a.top - b.bottom);
    const sameBase = els[i].e.parentElement === els[j].e.parentElement && els[i].e.parentElement.classList.contains('base');
    const minimo = 40;
    if (gap < minimo) r.push('FOLGA ' + Math.round(gap) + 'px entre [' + els[i].n + '] e [' + els[j].n + ']');
  }
  const t = [...document.querySelectorAll('.titulo')].map(t => +t.style.fontSize.replace('px',''));
  return {r, t};
}
"""


async def renderizar(itens, saida):
    os.makedirs(saida, exist_ok=True)
    tmp = os.path.join(G.AQUI, ".tmp"); os.makedirs(tmp, exist_ok=True)
    falhas = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for nome, corpo, (w, h) in itens:
            caminho = os.path.join(tmp, nome + ".html")
            pag = G.pagina(corpo).replace("</style>", CSS + "</style>", 1)
            open(caminho, "w").write(pag)
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto("file://" + caminho); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.evaluate(G.AJUSTE_JS)
            res = await pg.evaluate(CHECA_JS)
            png = os.path.join(tmp, nome + ".png")
            await pg.screenshot(path=png); await pg.close()
            Image.open(png).convert("RGB").save(os.path.join(saida, nome + ".jpg"), quality=92)
            falhas += len(res["r"])
            print("ok" if not res["r"] else "ATENÇÃO", nome, "títulos(px):", res["t"])
            for x in res["r"]:
                print("   -", x)
        await b.close()
    print("TOTAL DE PROBLEMAS:", falhas)



itens = [(n, c, (W, H)) for n, c in chuva()]
itens += [("1530-conta-taxa-maquininha", conta_taxa(), (W, H)), ("1930-espelho-dinheiro-nao-aparece", espelho(), (W, H)),
          ("2230-toda-loja-calculadora-balcao", toda_loja(), (W, H))]
itens += [("story-1200-pmc-setembro", story_pmc(), (SW, SH)), ("story-1800-fio-15-ou-25", story_fios(), (SW, SH)),
          ("story-2100-flow-rota", story_flow(), (SW, SH)), ("story-0600-22-11-quem-cobre-quem", story_bomdia(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-21-11')
asyncio.run(renderizar(itens, saida))
