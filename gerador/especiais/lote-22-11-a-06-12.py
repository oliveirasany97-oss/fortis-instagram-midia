"""Lote de 22/11 a 06/12/2026: feed (10:30, 15:30, 19:30, 22:30), stories 18:00 e 21:00 de cada dia e story 06:00 de 23/11 a 07/12.
A notícia das 12:00 fica com a tarefa diária leve; os reels (Replay da Loja) voltam em 29/11, quando os créditos do ElevenLabs renovam.
Uso: python3 gerador/especiais/lote-22-11-a-06-12.py [dia ...]   (sem argumento = todos; ex.: 22-11 23-11)
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

FONTE_EC = 'Fonte: EC 141/2026 (DOU de 16/10/2026) · conforme InfoMoney, A Crítica e Caltrab'
VALIDE = 'Cada loja deve validar a escala com o seu <b>contador ou advogado trabalhista.</b>'


def capa(k, linhas, s, fs=118):
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {sub(s, 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)


def slide(k, linhas, itens, fs=96, ini=1, num=True, fonte=None, extra=''):
    return feed(f'''{kicker(k) if k else ''}
  {titulo(linhas, fs)}
  {lista(itens, 33, 24, num=num, ini=ini)}{extra}''', 110, 1.3, fonte=fonte)


def fim(linhas, itens, cta, fs=100, extra=''):
    return feed(f'''{titulo(linhas, fs)}
  {lista(itens, 32, 23, num=False)}{extra}
  <p class="cta k" style="font-size:30px;padding:0 90px">{cta.replace(' <b>', '<br><b>', 1)}</p>''', 110, 1.3)


def unico(k, linhas, s, itens, cta, fs=96, num=True):
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {sub(s, 29, 100)}
  {lista(itens, 31, 23, num=num)}
  <p class="cta k" style="font-size:29px;padding:0 80px">{cta}</p>''', 96, 1.3)


def conta(linhas, s, tab, dest, cta, fs=88, tfs=28):
    return feed(f'''{kicker("A CONTA DA LOJA")}
  {titulo(linhas, fs)}
  {sub(s, 29, 100)}
  {card(tabela(tab, tfs, destaque=dest), "4px 0", 880)}
  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>
  <p class="cta k" style="font-size:29px;padding:0 80px">{cta.replace(' <b>', '<br><b>', 1)}</p>''', 110, 1.3)


def espelho(linhas, itens, cta, fs=92):
    return feed(f'''{kicker("ESPELHO DO DONO")}
  {titulo(linhas, fs)}
  {lista(itens, 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 80px">{cta} <b>Se você se viu aqui, chame no direct.</b></p>''', 120, 1.3)


def toda(linhas, s, itens, fs=96):
    return unico("TODA LOJA PRECISA TER", linhas, s, itens, 'Sua loja já tem? <b>Diagnóstico sem custo no direct.</b>', fs)


def tec(linhas, s, tab, nota, fonte, fs=96, tfs=27, k="ENTENDA A DIFERENÇA"):
    return story(f'''{kicker(k, 26)}
  {titulo(linhas, fs, 900)}
  {sub(s, 28, 90)}
  {card(tabela(tab, tfs))}
  <p class="cta k" style="font-size:28px;padding:0 80px">{nota}</p>''', fonte, 90)


def flow(linhas, itens, tela=None, fs=84):
    if tela:
        esq = lista(itens, 30, 22, w=470)
        cel = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:44px">
      <div class="k" style="width:280px;height:440px;border-radius:40px;border:8px solid #0b1424;outline:3px solid rgba(217,181,121,.85);box-shadow:0 0 40px rgba(217,181,121,.25);overflow:hidden;background:#0E1F39">
        <img src="{A}/telas/{tela}.png" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block"></div>
      <div class="k" style="font-weight:600;letter-spacing:4px;color:#D9B579;font-size:16px">TELA REAL · DADOS FICTÍCIOS</div></div>'''
        meio = row(esq, cel)
    else:
        meio = lista(itens, 31, 23, w=880)
    return story(f'''{kicker("FORTÍS FLOW", 28)}
  {titulo(linhas, fs, 900)}
  {meio}
  <p class="cta k" style="font-size:32px;padding:0 80px">Quer ver na sua loja? <b>Chame no direct.</b></p>''', None, 90)


def obras(linhas, s, itens, fs=92):
    return story(f'''{kicker("FORTÍS OBRAS", 28)}
  {titulo(linhas, fs, 900)}
  {sub(s, 31, 90)}
  {lista(itens, 30, 23, w=880)}
  <p class="cta k" style="font-size:34px;padding:0 80px">Quer ver como funciona? <b>Chame no direct.</b></p>''', None, 120)


def bomdia(linhas, s, frase, fs=104):
    return story(f'''<div class="kicker k" style="font-size:28px;margin-bottom:12px">BOM DIA, LOJISTA</div>
  {titulo(linhas, fs, 900)}
  {sub(s, 38, 90)}
  <p class="cta k" style="font-size:36px;padding:0 80px">{frase}</p>''', None, 170)


HT = '#materialdeconstrucao #lojadematerialdeconstrucao #varejomatcon'
DIAS = {}

# ======================================================================= 22/11 (dom)
DIAS['22-11'] = dict(
  f1030=('telhado', [
    capa("MANDE PARA SUA EQUIPE", ["TELHADO:", "O QUE O CLIENTE ESQUECE"], "A telha ele já sabe. <b>O resto da lista</b> é o vendedor que lembra.", 104),
    slide("NA HORA DO ORÇAMENTO", ["PERGUNTE E", "COMPLETE"], [("Cumeeira e espigão", "Fecham o topo e as quinas do telhado."), ("Fixação certa", "Parafuso, prego ou gancho do tipo da telha."), ("Rufo e calha", "Onde o telhado encontra a parede e onde a água escoa.")]),
    slide("NÃO DEIXE DE FORA", ["O QUE EVITA", "GOTEIRA"], [("Vedação", "Arruela de vedação e massa onde o fabricante indica."), ("Telha de reserva", "Algumas a mais para quebra no transporte e no corte."), ("Ficha do fabricante", "Inclinação mínima e sobreposição de cada modelo.")], ini=4),
    fim(["PEDIDO", "COMPLETO"], [("Uma viagem só", "Cliente não volta à loja no meio do serviço."), ("Telhado bem feito", "Sem goteira, sem reclamação depois.")], 'Quer montar as listas de venda da sua loja? <b>Chame no direct.</b>')],
    'Telhado na loja de material de construção: além da telha, o que o cliente esquece de levar.\n\nCumeeira, fixação certa, rufo, calha, vedação e telha de reserva. Salve e mande para sua equipe.\n\nQuer montar as listas de venda da sua loja? Chame no direct.', '#telhado #vendedordebalcao'),
  f1530=('conta-ponto-de-equilibrio', conta(["QUANTO SUA LOJA PRECISA", "VENDER PARA EMPATAR?"], "Com <b>margem bruta de 25%</b>, cada R$ 1 vendido deixa R$ 0,25 para pagar as contas fixas.",
    [("Custos fixos do mês", "R$ 30.000"), ("Margem bruta média", "25%"), ("Venda para empatar (30.000 ÷ 0,25)", "R$ 120.000")], (2,),
    'Abaixo disso, a loja paga para abrir. <b>Sabe o número da sua? Chame no direct.</b>', 80),
    'Ponto de equilíbrio da loja de material de construção: quanto vender por mês só para empatar.\n\nCustos fixos de R$ 30.000 com margem bruta de 25% pedem R$ 120.000 de venda. Exemplo ilustrativo: cada loja tem o seu número.\n\nSabe o da sua? Chame no direct.', '#pontodeequilibrio #donodeloja'),
  f1930=('espelho-apagar-incendio', espelho(["SEU DIA É SÓ", "APAGAR INCÊNDIO"], [("Chega com um plano", "Às 8h15 já foi esquecido."), ("Um problema puxa outro", "Entrega, caixa, fornecedor, cliente irritado."), ("Decide tudo na correria", "Sem tempo de olhar um número."), ("À noite, a mesma sensação", "Trabalhou muito e a loja não andou.")], 'Incêndio todo dia é sinal de processo faltando.'),
    'Rotina do dono de loja de material de construção: quando o dia inteiro vira apagar incêndio.\n\nIncêndio todo dia é sinal de processo faltando. Se você se viu aqui, chame no direct.', '#gestaodeloja #donodeloja'),
  f2230=('toda-loja-epi', toda(["EPI NO", "DEPÓSITO"], "Depósito tem peso e altura. <b>Proteção não é opcional.</b>",
    [("Luva e bota de segurança", "Para quem carrega, descarrega e separa."), ("Óculos e máscara", "No corte, na poeira de cimento e de cal."), ("Registro de entrega", "Quem recebeu, quando e o quê."), ("Cobrança no dia a dia", "EPI na prateleira não protege ninguém.")]),
    'Segurança no depósito da loja de material de construção: o EPI que toda equipe precisa usar.\n\nLuva, bota, óculos, máscara, registro de entrega e cobrança no dia a dia. Sua loja já tem? Diagnóstico sem custo no direct.', '#segurancadotrabalho #depositodematerial'),
  s1800=('tinta-acrilica-pva', tec(["ACRÍLICA", "OU PVA?"], "As duas são tinta látex. <b>O ambiente é que decide.</b>",
    [("<span class='h'>TINTA</span>", "<span class='h'>ONDE USAR</span>"), ("Látex PVA", "interno seco"), ("Acrílica", "interno e externo"), ("Acrílica", "áreas úmidas e laváveis")],
    'Fachada, cozinha e banheiro pedem <b>acrílica</b>.', 'Fonte: fichas técnicas dos fabricantes (Suvinil, Coral)')),
  s2100=('obras-esfriando', obras(["A OBRA QUE", "ESTÁ ESFRIANDO"], "Obra boa é a que <b>ainda não comprou</b>. O Fortís Obras avisa antes de ela sumir.",
    [("Temperatura da obra", "Quente, morna, fria ou em risco."), ("Dias sem contato", "O radar mostra quem ficou esquecido."), ("Prioridade certa", "Primeiro as que estão esfriando.")])),
  s0600=('23-11-mais-dificil', bomdia(["COMECE PELO", "MAIS DIFÍCIL"], "A ligação chata, a conversa adiada, a conta que incomoda. <b>Resolva antes das 10h.</b>", "O resto do dia fica mais leve.")),
)

# ======================================================================= 23/11 (seg)
DIAS['23-11'] = dict(
  f1030=('escala-5x2-parte3', [
    capa("ESCALA 5x2 NA LOJA · PARTE 3", ["FALTAM 3", "SEMANAS"], "A jornada de 42 horas começa em <b>16 de dezembro de 2026</b>. O que a loja já pode deixar pronto.", 120),
    slide("O QUE JÁ ESTÁ DEFINIDO", ["A REGRA"], [("42 horas por semana", "A partir de 16/12/2026. Em 16/12/2027, 40 horas."), ("Dois dias de descanso", "Um deles preferencialmente no domingo."), ("Sem redução de salário", "A emenda proíbe reduzir salários.")], fonte=FONTE_EC),
    slide("ESTA SEMANA", ["DEIXE PRONTO"], [("Lista da equipe por setor", "Quem faz o quê, em que horário."), ("Rascunho da escala", "Com o mínimo de cada setor no pico."), ("Reunião com o contador", "Para validar antes de comunicar a equipe.")]),
    fim(["ATENÇÃO"], [("Regras de transição no STF", "A análise ainda não terminou. Acompanhe com o contador."), ("Nada de improviso", "Escala nova comunicada com antecedência.")], 'Quer ajuda para organizar a equipe? <b>Chame no direct.</b>', 120, extra=f'\n  {sub(VALIDE, 28, 120)}')],
    'Escala 5x2 na loja de material de construção: a jornada de 42 horas começa em 16 de dezembro de 2026.\n\nParte 3 da série: o que está definido, o que deixar pronto esta semana e o que ainda está em análise. Cada loja deve validar a escala com o seu contador ou advogado trabalhista.\n\nQuer ajuda para organizar a equipe? Chame no direct.', '#escala5x2 #gestaodeequipe'),
  f1530=('conta-calote', conta(["1 CALOTE EM 10", "COME 40% DO LUCRO"], "10 vendas a prazo de R$ 1.000, com <b>margem bruta de 25%</b>.",
    [("Lucro esperado nas 10 vendas", "R$ 2.500"), ("Recebido (9 pagaram)", "R$ 9.000"), ("Custo das 10 vendas", "R$ 7.500"), ("Lucro que sobrou", "R$ 1.500")], (3,),
    'Crédito sem regra sai caro. <b>Quer organizar a cobrança? Chame no direct.</b>', 92),
    'Venda a prazo na loja de material de construção: um calote em dez vendas leva 40% do lucro.\n\nDe R$ 2.500 esperados, sobram R$ 1.500. Exemplo ilustrativo.\n\nQuer organizar crédito e cobrança na sua loja? Chame no direct.', '#vendaaprazo #donodeloja'),
  f1930=('espelho-fiado-caderno', espelho(["O FIADO VIROU", "CADERNO"], [("Cada vendedor anota de um jeito", "E ninguém sabe o total."), ("O cliente jura que já pagou", "E não tem como provar o contrário."), ("Cobrar dá vergonha", "Então ninguém cobra."), ("No fim do mês, falta caixa", "E sobra nome no caderno.")], 'Dinheiro na rua também é estoque parado.'),
    'Fiado na loja de material de construção: quando o crédito vira caderno e ninguém sabe o total.\n\nSe você se viu aqui, chame no direct.', '#gestaofinanceira #donodeloja'),
  f2230=('toda-loja-sazonalidade', toda(["CALENDÁRIO DE", "SAZONALIDADE"], "Cada época tem o seu produto. <b>Antecipe-se.</b>",
    [("Chuva", "Impermeabilizante, calha, lona e telha."), ("Fim de ano", "Tinta, pintura e pequenas reformas."), ("Volta do calor", "Ventilador de teto, iluminação e área externa."), ("Compra com antecedência", "O estoque chega antes da procura.")]),
    'Sazonalidade na loja de material de construção: o calendário que diz o que comprar antes da procura.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#comprasinteligentes #gestaodeestoque'),
  s1800=('bloco-ceramico-concreto', tec(["BLOCO CERÂMICO", "OU DE CONCRETO?"], "Os dois têm versão de <b>vedação</b> e versão <b>estrutural</b>.",
    [("<span class='h'>TIPO</span>", "<span class='h'>FUNÇÃO</span>"), ("Vedação", "fecha o vão, não segura carga"), ("Estrutural", "faz parte da estrutura")],
    'Estrutural só com <b>projeto de engenheiro</b>.', 'Fonte: ABNT NBR 15270 (bloco cerâmico) e NBR 6136 (bloco de concreto)', 84)),
  s2100=('flow-avarias', flow(["AVARIA REGISTRADA", "NA HORA"], [("Foto e prejuízo", "Registrados na descarga."), ("Status à vista", "Identificada, notificada, em negociação."), ("Fornecedor avisado", "Direto pelo Flow.")], 'avarias')),
  s0600=('24-11-o-que-travou', bomdia(["O QUE TRAVOU", "ONTEM?"], "Pergunte à equipe antes de abrir. <b>Uma resposta por pessoa</b>, sem procurar culpado.", "O que trava todo dia vira processo.")),
)

# ======================================================================= 24/11 (ter)
DIAS['24-11'] = dict(
  f1030=('cliente-indeciso', [
    capa("MANDE PARA SUA EQUIPE", ["MARCA A", "OU MARCA B?"], "Como ajudar o cliente <b>indeciso</b> sem empurrar a mais cara.", 128),
    slide("PRIMEIRO, ENTENDA", ["PERGUNTE"], [("“Onde vai usar?”", "Área interna, externa, molhada."), ("“Quem vai aplicar?”", "O profissional costuma ter preferência."), ("“O que pesa mais?”", "Preço, durabilidade ou prazo.")]),
    slide("DEPOIS, COMPARE", ["MOSTRE", "A DIFERENÇA"], [("Lado a lado", "Rendimento, garantia e indicação de uso."), ("Custo por m²", "Nem sempre a mais barata no balcão sai mais barata na obra."), ("Sua recomendação", "Diga qual levaria e por quê.")], ini=4),
    fim(["O CLIENTE", "DECIDE"], [("Sem pressão", "Quem decide com segurança volta."), ("Anote a escolha", "Ajuda na próxima compra da obra.")], 'Quer treinar o atendimento da sua equipe? <b>Chame no direct.</b>')],
    'Atendimento na loja de material de construção: como ajudar o cliente indeciso entre duas marcas.\n\nPergunte onde vai usar, quem aplica e o que pesa mais. Depois compare lado a lado e recomende. Salve e mande para sua equipe.', '#atendimentoaocliente #vendedordebalcao'),
  f1530=('conta-quebra-telha', conta(["3% DE QUEBRA", "NA TELHA"], "Carga de <b>1.000 telhas</b>, custo de R$ 4 cada.",
    [("Telhas quebradas por carga (3%)", "30"), ("Prejuízo por carga", "R$ 120"), ("8 cargas no mês", "R$ 960")], (2,),
    'Quebra sem registro vira custo fixo. <b>Quer reduzir a sua? Chame no direct.</b>', 104),
    'Quebra de telha na loja de material de construção: 3% por carga viram quase R$ 1.000 por mês.\n\nExemplo ilustrativo com carga de 1.000 telhas a R$ 4. Quer reduzir a quebra na sua loja? Chame no direct.', '#avaria #depositodematerial'),
  f1930=('espelho-preco-representante', espelho(["ACEITA O PREÇO QUE", "O REPRESENTANTE DÁ"], [("Ele chega com a tabela", "E você só confere a quantidade."), ("Não sabe o último preço pago", "Nem o do concorrente dele."), ("Prazo e frete ficam para depois", "E vêm piores do que podiam."), ("A margem começa na compra", "E você perde antes de vender.")], 'Compra boa é negociada com número na mão.', 88),
    'Compras na loja de material de construção: quando o preço é o que o representante dá.\n\nA margem começa na compra. Se você se viu aqui, chame no direct.', '#compras #donodeloja'),
  f2230=('toda-loja-canal-equipe', toda(["UM CANAL PARA", "A EQUIPE FALAR"], "Quem está no balcão vê <b>o que o dono não vê</b>.",
    [("Espaço fixo na semana", "Dez minutos só para ouvir a equipe."), ("Sugestão anotada", "Com nome e data."), ("Resposta sempre", "Sim, não ou depois, mas com motivo."), ("Ideia boa reconhecida", "Em público.")]),
    'Gestão de equipe na loja de material de construção: o canal para o funcionário falar o que vê.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#gestaodeequipe #lideranca'),
  s1800=('ca50-ca60', tec(["CA-50", "OU CA-60?"], "Muda a forma <b>e a resistência</b>.",
    [("<span class='h'>AÇO</span>", "<span class='h'>CARACTERÍSTICA</span>"), ("CA-50", "barra nervurada · 500 MPa"), ("CA-60", "fio de menor bitola · 600 MPa")],
    'Qual usar em cada peça é o <b>projeto</b> que define.', 'Fonte: ABNT NBR 7480 (aço destinado a armaduras para estruturas de concreto)')),
  s2100=('obras-pontos-indicacao', obras(["QUEM INDICA,", "ACUMULA"], "O profissional ganha <b>pontos por venda indicada</b>, com a regra que a loja define.",
    [("Regra configurável", "A loja decide quantos pontos por valor vendido."), ("Campanha com prazo", "Início e fim definidos pela loja."), ("Resgate", "Prêmio ou valor, a critério da loja.")])),
  s0600=('25-11-celular-no-bolso', bomdia(["CELULAR NO BOLSO,", "CLIENTE NA FRENTE"], "Cliente no balcão é <b>prioridade número um</b>. Mensagem espera, ele não.", "Combine isso com a equipe hoje.", 92)),
)

# ======================================================================= 25/11 (qua)
DIAS['25-11'] = dict(
  f1030=('venda-de-tinta', [
    capa("MANDE PARA SUA EQUIPE", ["VENDA DE TINTA:", "O QUE PERGUNTAR"], "Tinta certa, <b>na quantidade certa</b>, com tudo o que a pintura pede.", 104),
    slide("ANTES DA COR", ["ENTENDA", "A PAREDE"], [("“Interna ou externa?”", "Define o tipo de tinta."), ("“Parede nova ou repintura?”", "Reboco novo pede preparo antes."), ("“Tem mofo ou descascado?”", "Primeiro tratar, depois pintar.")]),
    slide("NA QUANTIDADE", ["FAÇA A CONTA", "COM ELE"], [("Metragem da parede", "Altura vezes largura, menos portas e janelas."), ("Rendimento da lata", "Está na embalagem do fabricante."), ("Número de demãos", "Indicado pelo fabricante para cada cor e superfície.")], ini=4),
    fim(["NÃO ESQUEÇA"], [("Rolo, pincel e bandeja", "E fita crepe."), ("Lixa e massa", "Se a parede pedir."), ("Lona para o piso", "A pintura agradece.")], 'Quer treinar a venda técnica da sua equipe? <b>Chame no direct.</b>', 120)],
    'Venda de tinta na loja de material de construção: o que perguntar antes de escolher a cor.\n\nTipo de parede, preparo, metragem, rendimento e demãos. Salve e mande para sua equipe.', '#tinta #vendedordebalcao'),
  f1530=('conta-arredondamento', conta(["O ARREDONDAMENTO", "DE R$ 7"], "Vendedor que arredonda <b>R$ 7 para baixo</b> em cada venda, para agradar.",
    [("Por venda", "R$ 7"), ("30 vendas por dia", "R$ 210"), ("26 dias no mês", "R$ 5.460")], (2,),
    'Desconto pequeno, todo dia, vira conta grande. <b>Chame no direct.</b>', 96),
    'Desconto no balcão da loja de material de construção: R$ 7 de arredondamento por venda somam R$ 5.460 no mês.\n\nExemplo ilustrativo. Quer colocar regra no desconto da sua loja? Chame no direct.', '#margemdelucro #vendedordebalcao'),
  f1930=('espelho-cabeca-nao-desliga', espelho(["O EXPEDIENTE ACABA,", "A CABEÇA NÃO"], [("Jantar com o celular na mão", "Respondendo cliente e vendedor."), ("Deita pensando no pedido", "Que ninguém mais sabe fazer."), ("Acorda com a lista do dia", "Antes mesmo de levantar."), ("Fim de semana sem folga", "Mesmo com a loja fechada.")], 'Loja que depende da sua cabeça não descansa.', 88),
    'Dono de loja de material de construção: quando o expediente acaba e a cabeça continua na loja.\n\nSe você se viu aqui, chame no direct.', '#donodeloja #gestaodeloja'),
  f2230=('toda-loja-treinamento-produto', toda(["TREINAMENTO DE", "PRODUTO TODO MÊS"], "Vendedor que conhece o produto <b>vende com segurança.</b>",
    [("Um tema por mês", "Tinta, hidráulica, elétrica, revestimento."), ("Com o fabricante", "Muitos oferecem treinamento para lojas."), ("Na prática", "Produto na mão, dúvida real do balcão."), ("Registro de presença", "Para saber quem já foi treinado.")], 92),
    'Treinamento na loja de material de construção: um tema de produto por mês, de preferência com o fabricante.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#treinamentodeequipe #vendedordebalcao'),
  s1800=('disjuntor-dr', tec(["DISJUNTOR", "OU DR?"], "Os dois ficam no quadro, mas <b>protegem coisas diferentes</b>.",
    [("<span class='h'>DISPOSITIVO</span>", "<span class='h'>PROTEGE</span>"), ("Disjuntor", "o circuito (sobrecarga e curto)"), ("DR", "as pessoas (choque elétrico)")],
    'A norma pede <b>DR de 30 mA</b> em áreas molhadas e externas.', 'Fonte: ABNT NBR 5410 · O Setor Elétrico', 96)),
  s2100=('flow-dono-ve-tudo', flow(["O DONO VÊ TUDO", "SEM PERGUNTAR"], [("Demandas e pendências", "Quanto entrou e quanto foi resolvido."), ("Compras do período", "E o que aguarda aprovação."), ("Prejuízo de avarias", "O que ainda não foi ressarcido.")], 'proprietario')),
  s0600=('26-11-agradeca', bomdia(["AGRADEÇA QUEM", "ENTREGOU NO PRAZO"], "O fornecedor pontual e o motorista caprichoso. <b>Reconheça em público.</b>", "Quem é lembrado capricha de novo.", 96)),
)

# ======================================================================= 26/11 (qui)
DIAS['26-11'] = dict(
  f1030=('escala-5x2-parte4', [
    capa("ESCALA 5x2 NA LOJA · PARTE 4", ["PASSAGEM DE", "TURNO"], "Com mais gente revezando, <b>a informação não pode ficar com quem saiu.</b>", 120),
    slide("EM 5 MINUTOS", ["QUEM SAI", "PASSA"], [("Entregas em andamento", "O que saiu, o que falta, o que mudou."), ("Clientes aguardando", "Orçamento, retirada ou retorno combinado."), ("Problemas do dia", "Avaria, falta, reclamação.")]),
    slide("NO PAPEL OU NO SISTEMA", ["QUEM ENTRA", "CONFERE"], [("Lê antes de assumir", "Nada de “ninguém me falou”."), ("Pergunta o que não entendeu", "Antes de quem saiu ir embora."), ("Assina ou marca como lido", "Fica registrado.")], ini=4),
    fim(["RESULTADO"], [("Cliente atendido igual", "Seja qual for o turno."), ("Ninguém liga para quem está de folga", "A folga é de verdade.")], 'Quer ajuda para organizar a escala nova? <b>Chame no direct.</b>', 120, extra=f'\n  {sub(VALIDE, 28, 120)}')],
    'Escala 5x2 na loja de material de construção, parte 4: a passagem de turno em 5 minutos.\n\nQuem sai passa entregas, clientes e problemas. Quem entra confere e registra. Cada loja deve validar a escala com o seu contador ou advogado trabalhista.', '#escala5x2 #gestaodeequipe'),
  f1530=('conta-caminhao', conta(["MESMO CAMINHÃO,", "METADE DO CUSTO"], "Caminhão próprio custando <b>R$ 300 por dia</b> entre motorista, combustível e desgaste.",
    [("3 entregas no dia", "R$ 100 cada"), ("6 entregas no dia", "R$ 50 cada")], (1,),
    'Rota planejada divide o custo. <b>Quer organizar a sua? Chame no direct.</b>', 96, 32),
    'Logística da loja de material de construção: o mesmo caminhão pode custar metade por entrega.\n\nCom R$ 300 por dia, 3 entregas saem a R$ 100 cada e 6 saem a R$ 50. Exemplo ilustrativo. Quer organizar as rotas da sua loja? Chame no direct.', '#logistica #entrega'),
  f1930=('espelho-loja-nova-esquina', espelho(["ABRIU UMA LOJA", "NOVA NA ESQUINA"], [("Você corre baixar o preço", "Antes de entender o que ela faz."), ("Fala mal do concorrente", "Para o cliente que já foi lá."), ("Não pergunta por que saíram", "Os clientes que sumiram."), ("Esquece o que só você tem", "Anos de cidade, de obra, de confiança.")], 'Concorrente novo é hora de melhorar, não de baixar a margem.', 96),
    'Concorrência na loja de material de construção: o que fazer quando abre uma loja nova perto.\n\nSe você se viu aqui, chame no direct.', '#concorrencia #donodeloja'),
  f2230=('toda-loja-ferias-equipe', toda(["CALENDÁRIO DE", "FÉRIAS DA EQUIPE"], "Férias de surpresa <b>desmontam qualquer escala.</b>",
    [("Um calendário do ano", "Visível para a liderança."), ("Pedido com antecedência", "Combinado com quem aprova."), ("Nunca dois do mesmo setor", "Na mesma semana."), ("Alerta de férias vencendo", "Para não virar passivo.")], 92),
    'Gestão de pessoas na loja de material de construção: o calendário de férias da equipe.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#gestaodeequipe #rh'),
  s1800=('drywall-st-ru-rf', tec(["PLACA BRANCA,", "VERDE OU ROSA?"], "No drywall, <b>a cor da placa indica o uso</b>.",
    [("<span class='h'>PLACA</span>", "<span class='h'>USO</span>"), ("ST · branca", "áreas secas"), ("RU · verde", "áreas úmidas"), ("RF · rosa", "resistência ao fogo")],
    'Banheiro com placa branca é <b>problema na certa</b>.', 'Fonte: ABNT NBR 14715 · fabricantes de chapas de gesso', 92)),
  s2100=('obras-podio', obras(["O PÓDIO DOS", "PARCEIROS"], "Ranking automático dos profissionais que <b>mais trazem obra</b> para a loja.",
    [("Pódio visual", "Os três primeiros em destaque."), ("Filtros", "Por especialidade e por período."), ("Sobe e desce", "Mostra quem ganhou ou perdeu posição.")])),
  s0600=('27-11-escute-mais', bomdia(["HOJE, ESCUTE", "MAIS"], "Deixe o cliente terminar de explicar a obra. <b>Quem escuta descobre o que vender.</b>", "Pergunte, ouça, depois indique.")),
)

# ======================================================================= 27/11 (sex)
DIAS['27-11'] = dict(
  f1030=('pedir-indicacao', unico("MANDE PARA SUA EQUIPE", ["COMO PEDIR", "INDICAÇÃO"], "Cliente satisfeito indica, <b>mas só se alguém pedir.</b>",
    [("Na hora certa", "Quando ele elogiar o atendimento ou a entrega."), ("Pedido simples", "“Conhece alguém que vai construir ou reformar?”"), ("Facilite", "Mande o contato da loja pelo WhatsApp dele."), ("Agradeça a indicação", "Mesmo que não vire venda.")],
    'Quer montar o roteiro da sua equipe? <b>Chame no direct.</b>', 104),
    'Indicação na loja de material de construção: como pedir ao cliente satisfeito sem constrangimento.\n\nNa hora certa, com uma pergunta simples, facilitando o contato e agradecendo. Salve e mande para sua equipe.', '#indicacao #atendimentoaocliente'),
  f1530=('conta-validade', conta(["VALIDADE VENCIDA", "NO DEPÓSITO"], "Argamassa, rejunte e cimento <b>têm data de validade</b>.",
    [("Sacos vencidos no mês", "12"), ("Custo de cada saco", "R$ 25"), ("Perda no mês", "R$ 300"), ("Perda no ano", "R$ 3.600")], (3,),
    'Primeiro que entra, primeiro que sai. <b>Quer organizar o depósito? Chame no direct.</b>', 96),
    'Validade no depósito da loja de material de construção: 12 sacos vencidos por mês somam R$ 3.600 no ano.\n\nExemplo ilustrativo. Quer organizar o giro do depósito? Chame no direct.', '#gestaodeestoque #depositodematerial'),
  f1930=('espelho-familia', espelho(["FAMÍLIA NA LOJA,", "CADA UM NO SEU PAPEL?"], [("Todo mundo manda um pouco", "E a equipe não sabe a quem obedecer."), ("Ninguém tem horário", "Nem meta, nem função escrita."), ("A briga de casa vai para o balcão", "E o cliente percebe."), ("Sucessão nunca foi conversada", "E o tempo está passando.")], 'Empresa familiar cresce quando cada um sabe o seu lugar.', 88),
    'Empresa familiar na loja de material de construção: quando todos mandam e ninguém tem papel definido.\n\nSe você se viu aqui, chame no direct.', '#empresafamiliar #donodeloja'),
  f2230=('toda-loja-backup', toda(["BACKUP E SENHAS", "ORGANIZADAS"], "O sistema é da loja. <b>O acesso também precisa ser.</b>",
    [("Backup automático", "E alguém confere se está funcionando."), ("Senhas em lugar seguro", "Não no papel colado no monitor."), ("Acesso por pessoa", "Cada um com o seu login."), ("Funcionário saiu, acesso sai", "No mesmo dia.")], 92),
    'Segurança digital na loja de material de construção: backup e senhas organizadas.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#tecnologia #gestaodeloja'),
  s1800=('areia-fina-media-grossa', tec(["AREIA FINA,", "MÉDIA OU GROSSA?"], "O tamanho do grão <b>muda o uso na obra</b>.",
    [("<span class='h'>AREIA</span>", "<span class='h'>USO MAIS COMUM</span>"), ("Fina", "reboco e acabamento"), ("Média", "assentamento e contrapiso"), ("Grossa", "concreto")],
    'Areia errada <b>racha o reboco e enfraquece o concreto</b>.', 'Fonte: Votorantim Cimentos · Sienge · ABNT NBR 7211 (agregados para concreto)', 92)),
  s2100=('flow-aviso-celular', flow(["O AVISO CHEGA", "NO CELULAR"], [("Notificação no celular", "Como uma mensagem, mesmo com o app fechado."), ("Cada um recebe o seu", "Compra aprovada, mercadoria chegou, encomenda pronta."), ("Silenciar por tipo", "Cada usuário escolhe o que quer receber.")])),
  s0600=('28-11-balcao-almoco', bomdia(["BALCÃO NUNCA", "VAZIO NO ALMOÇO"], "Combine hoje quem almoça em cada horário. <b>Cliente do meio-dia também compra.</b>", "Escala de almoço é venda garantida.", 100)),
)

# ======================================================================= 28/11 (sáb)
DIAS['28-11'] = dict(
  f1030=('venda-de-piso', [
    capa("MANDE PARA SUA EQUIPE", ["PISO: 4 COISAS", "PARA COMBINAR"], "Antes de fechar a venda de piso ou porcelanato, <b>combine com o cliente</b>.", 104),
    slide("NA METRAGEM", ["COMBINE"], [("Área real", "Medida pelo profissional, não no olho."), ("Margem de perda", "Recorte e quebra, conforme o tipo de assentamento."), ("Tudo do mesmo lote", "Separado de uma vez para não variar a tonalidade.")]),
    slide("NOS MATERIAIS", ["COMPLETE"], [("Argamassa certa", "Conforme a placa e o local."), ("Rejunte e espaçador", "Na cor e na medida da junta.")], ini=4),
    fim(["E POR", "ESCRITO"], [("Prazo de entrega", "E onde descarregar."), ("Política de troca", "Para sobra de caixa fechada.")], 'Quer padronizar a venda de revestimento? <b>Chame no direct.</b>')],
    'Venda de piso e porcelanato na loja de material de construção: metragem, perda, lote, argamassa e rejunte combinados antes de fechar.\n\nSalve e mande para sua equipe.', '#porcelanato #vendedordebalcao'),
  f1530=('conta-multa-boleto', conta(["MULTA DE BOLETO", "TAMBÉM É CUSTO"], "Boleto de fornecedor de <b>R$ 8.000</b> pago com atraso, com <b>multa de 2%</b>.",
    [("Multa por boleto", "R$ 160"), ("3 boletos atrasados no mês", "R$ 480"), ("Sem contar os juros", "por dia de atraso")], (1,),
    'Contas a pagar com agenda não pagam multa. <b>Chame no direct.</b>', 96),
    'Contas a pagar na loja de material de construção: três boletos atrasados no mês custam R$ 480 só de multa.\n\nExemplo ilustrativo. Quer organizar o financeiro da sua loja? Chame no direct.', '#gestaofinanceira #contasapagar'),
  f1930=('espelho-promocao-escondida', espelho(["A PROMOÇÃO QUE", "SÓ VOCÊ CONHECE"], [("Comprou bem e baixou o preço", "Mas nada mudou na loja."), ("Sem placa, sem post", "Sem aviso para quem compra sempre."), ("O vendedor nem sabe", "E vende pelo preço antigo de cabeça."), ("No fim do mês", "O produto continua parado.")], 'Oferta que ninguém vê não vende.', 92),
    'Promoção na loja de material de construção: quando a oferta existe, mas o cliente nunca fica sabendo.\n\nSe você se viu aqui, chame no direct.', '#marketingdevarejo #donodeloja'),
  f2230=('toda-loja-sistema-caiu', toda(["PLANO PARA QUANDO", "O SISTEMA CAIR"], "Internet ou sistema fora do ar <b>não pode fechar a loja.</b>",
    [("Bloco de pedido numerado", "Para vender sem sistema e lançar depois."), ("Tabela de preços impressa", "Dos itens que mais vendem."), ("Contato do suporte à mão", "E quem liga para ele."), ("Lançamento no mesmo dia", "Quando o sistema voltar.")], 88),
    'Contingência na loja de material de construção: o plano para vender quando o sistema ou a internet cair.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#tecnologia #gestaodeloja'),
  s1800=('retificado-bold', tec(["RETIFICADO", "OU BOLD?"], "A diferença está <b>na borda da placa</b>.",
    [("<span class='h'>BORDA</span>", "<span class='h'>RESULTADO</span>"), ("Retificado", "borda reta, junta mais fina"), ("Bold", "borda arredondada, junta maior")],
    'A junta mínima de cada placa está na <b>orientação do fabricante</b>.', 'Fonte: orientações técnicas de fabricantes (Portobello, Eliane) · ANFACER')),
  s2100=('obras-pontos-whatsapp', obras(["O PROFISSIONAL", "VÊ OS PONTOS"], "A pontuação <b>vai pelo WhatsApp</b> para cada parceiro.",
    [("Saldo atualizado", "O profissional sabe quanto acumulou."), ("Motivo para voltar", "Cada indicação conta."), ("Relacionamento", "A loja lembra dele, ele lembra da loja.")])),
  s0600=('29-11-desligue-grupo', bomdia(["DESLIGUE O GRUPO", "DA LOJA POR UMAS HORAS"], "Domingo também é para <b>recarregar a cabeça</b> de quem lidera.", "Uma loja bem organizada aguenta algumas horas sem você.", 88)),
)

# ======================================================================= 29/11 (dom)
DIAS['29-11'] = dict(
  f1030=('lista-alvenaria', [
    capa("MANDE PARA SUA EQUIPE", ["MURO E ALVENARIA:", "A LISTA COMPLETA"], "O cliente pede o bloco. <b>A obra pede mais.</b>", 100),
    slide("ESTRUTURA E BASE", ["NÃO ESQUEÇA"], [("Ferragem", "Conforme o projeto ou o profissional."), ("Cimento, areia e brita", "Para fundação, vigas e pilares."), ("Impermeabilização da base", "Antes de subir a parede.")]),
    slide("NA PAREDE", ["COMPLETE"], [("Argamassa de assentamento", "Pronta ou cimento, cal e areia."), ("Canaleta e verga", "Sobre portas e janelas."), ("Reboco e acabamento", "Para a próxima etapa da obra.")], ini=4),
    fim(["PENSE NA", "PRÓXIMA ETAPA"], [("Anote a fase da obra", "E volte a falar com o cliente."), ("Ofereça a entrega programada", "Na hora em que a obra precisa.")], 'Quer montar as listas de venda da sua loja? <b>Chame no direct.</b>')],
    'Muro e alvenaria na loja de material de construção: a lista completa que o cliente não traz.\n\nFerragem, base impermeabilizada, argamassa, verga, canaleta e reboco. Salve e mande para sua equipe.', '#alvenaria #vendedordebalcao'),
  f1530=('conta-prazo-60-dias', conta(["QUEM FINANCIA", "SEU CLIENTE É VOCÊ"], "Venda a prazo de 60 dias, mercadoria <b>paga ao fornecedor em 30</b>.",
    [("Venda a prazo", "R$ 10.000"), ("Custo da mercadoria (margem 25%)", "R$ 7.500"), ("Dias que a loja banca o custo", "30"), ("Custo do dinheiro (2% ao mês)", "R$ 150")], (3,),
    'Prazo para o cliente também tem preço. <b>Chame no direct.</b>', 92),
    'Prazo de recebimento na loja de material de construção: quando a loja financia o cliente com o próprio caixa.\n\nExemplo ilustrativo. Quer equilibrar prazos de compra e de venda? Chame no direct.', '#fluxodecaixa #gestaofinanceira'),
  f1930=('espelho-caminhao-sumiu', espelho(["O CAMINHÃO SAIU E", "NINGUÉM SABE QUANDO VOLTA"], [("O cliente liga perguntando", "E o balcão não sabe responder."), ("Duas entregas no mesmo bairro", "Em viagens separadas."), ("O motorista decide a ordem", "No caminho."), ("Pedido urgente espera", "O caminhão que ninguém sabe onde está.")], 'Entrega sem rota é custo sem controle.', 76),
    'Entregas da loja de material de construção: quando o caminhão sai e ninguém sabe a rota.\n\nSe você se viu aqui, chame no direct.', '#logistica #entrega'),
  f2230=('toda-loja-banco-profissionais', toda(["BANCO DE", "PROFISSIONAIS PARCEIROS"], "O cliente pergunta <b>“conhece um bom pedreiro?”</b>. A loja precisa ter a resposta.",
    [("Lista por especialidade", "Pedreiro, eletricista, encanador, pintor."), ("Contato atualizado", "E região onde trabalha."), ("Histórico de indicação", "Quem atende bem continua na lista."), ("Relação de mão dupla", "Ele indica a loja, a loja indica ele.")], 88),
    'Relacionamento com profissionais na loja de material de construção: o banco de parceiros que o cliente procura.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#pedreiro #relacionamento'),
  s1800=('lampada-temperatura-cor', tec(["LUZ AMARELA", "OU BRANCA?"], "Na lâmpada, a cor da luz vem em <b>Kelvin (K)</b>.",
    [("<span class='h'>TEMPERATURA</span>", "<span class='h'>EFEITO E USO</span>"), ("2.700 K a 3.000 K", "quente · quarto e sala"), ("4.000 K", "neutra · uso geral"), ("6.500 K", "fria · cozinha e serviço")],
    'Pergunte o ambiente <b>antes de vender a lâmpada</b>.', 'Fonte: catálogos técnicos de fabricantes de iluminação (Philips, Osram)', 92)),
  s2100=('flow-performance', flow(["A PERFORMANCE DE", "CADA VENDEDOR"], [("Meta e realizado", "Por vendedor, no mês."), ("Comparativo", "Entre vendedores e entre meses."), ("Projeção", "Se o ritmo atual fecha a meta.")], 'metas')),
  s0600=('30-11-delegue', bomdia(["DELEGUE UMA TAREFA", "QUE SÓ VOCÊ FAZ"], "Escolha uma e <b>ensine hoje.</b>", "Dono que ensina ganha tempo para crescer.", 92)),
)

# ======================================================================= 30/11 (seg)
DIAS['30-11'] = dict(
  f1030=('escala-5x2-parte5', [
    capa("ESCALA 5x2 NA LOJA · PARTE 5", ["COMO CONTAR", "PARA A EQUIPE"], "Escala nova comunicada mal <b>vira boato.</b>", 120),
    slide("ANTES DA REUNIÃO", ["PREPARE"], [("Escala validada", "Com o contador ou advogado trabalhista."), ("Folgas de cada um", "Já distribuídas, por escrito."), ("Regras de troca", "Quem aprova e com quanta antecedência.")]),
    slide("NA REUNIÃO", ["EXPLIQUE"], [("O que muda", "42 horas e dois dias de descanso por semana, a partir de 16/12."), ("O que não muda", "O salário, que a emenda proíbe reduzir."), ("Como fica o sábado", "E por que o pico precisa da equipe.")], ini=4, fonte=FONTE_EC),
    fim(["DEPOIS"], [("Escala visível", "No quadro ou no sistema."), ("Dúvidas respondidas", "Na primeira semana, todo dia.")], 'Quer ajuda para preparar essa conversa? <b>Chame no direct.</b>', 120, extra=f'\n  {sub(VALIDE, 28, 120)}')],
    'Escala 5x2 na loja de material de construção, parte 5: como comunicar a escala nova para a equipe.\n\nPrepare, explique o que muda e o que não muda e deixe a escala visível. Cada loja deve validar a escala com o seu contador ou advogado trabalhista.', '#escala5x2 #gestaodeequipe'),
  f1530=('conta-despesa-venda', conta(["R$ 1 DE DESPESA =", "R$ 4 DE VENDA"], "Com <b>margem bruta de 25%</b>, cada real de despesa nova pede quatro reais de venda a mais.",
    [("Despesa nova no mês", "R$ 2.000"), ("Margem bruta", "25%"), ("Venda a mais só para pagar", "R$ 8.000")], (2,),
    'Antes de assumir um custo fixo, faça essa conta. <b>Chame no direct.</b>', 92),
    'Despesas da loja de material de construção: com margem de 25%, cada R$ 1 de custo novo pede R$ 4 de venda a mais.\n\nExemplo ilustrativo. Quer olhar as despesas da sua loja? Chame no direct.', '#gestaofinanceira #margemdelucro'),
  f1930=('espelho-sistema-caderno', espelho(["PAGA UM SISTEMA E", "VIVE NO CADERNO"], [("O sistema faz a nota", "E o resto fica no papel."), ("Ninguém foi treinado", "Então cada um usa do seu jeito."), ("Relatório? Nunca abriu", "Nem sabe que existe."), ("A mensalidade vence todo mês", "E a loja usa uma parte.")], 'Ferramenta que ninguém usa é custo, não gestão.', 92),
    'Tecnologia na loja de material de construção: quando a loja paga o sistema e continua no caderno.\n\nSe você se viu aqui, chame no direct.', '#tecnologia #donodeloja'),
  f2230=('toda-loja-produto-aplicado', toda(["PRODUTO APLICADO", "À VISTA"], "O cliente compra <b>o resultado</b>, não a caixa.",
    [("Painel com o piso assentado", "Com rejunte e junta reais."), ("Parede pintada", "Com as cores que mais saem."), ("Etiqueta com nome e preço", "Para achar o produto na hora."), ("Troca a cada estação", "Para a vitrine não envelhecer.")], 92),
    'Exposição na loja de material de construção: produto aplicado vende mais do que a caixa na prateleira.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#visualmerchandising #varejo'),
  s1800=('rejunte-cimenticio-epoxi', tec(["REJUNTE CIMENTÍCIO", "OU EPÓXI?"], "Mesma junta, <b>resistências diferentes</b>.",
    [("<span class='h'>REJUNTE</span>", "<span class='h'>INDICAÇÃO</span>"), ("Cimentício", "uso geral, interno e externo"), ("Epóxi", "mais resistente a manchas e químicos")],
    'Cozinha industrial e piscina pedem <b>atenção ao tipo</b>.', 'Fonte: ABNT NBR 14992 (rejunte cimentício) · fichas técnicas de fabricantes', 84)),
  s2100=('obras-eventos', obras(["TREINAMENTO QUE", "NINGUÉM ESQUECE"], "Eventos do ano <b>com alertas automáticos</b>.",
    [("Calendário do ano", "Treinamentos e encontros com profissionais."), ("Alertas antes do evento", "Com 30, 20, 15, 10, 5 e 1 dia de antecedência."), ("Empresa aplicadora", "O fabricante que vai dar o treinamento.")])),
  s0600=('01-12-pergunta-a-mais', bomdia(["UMA PERGUNTA", "A MAIS"], "Antes de fechar cada venda hoje: <b>“falta alguma coisa para essa etapa da obra?”</b>", "Uma pergunta evita a segunda viagem.")),
)

# ======================================================================= 01/12 (ter)
DIAS['01-12'] = dict(
  f1030=('cliente-pj', [
    capa("MANDE PARA SUA EQUIPE", ["CLIENTE", "EMPRESA"], "Condomínio, construtora, comércio. <b>O comprador PJ tem outras perguntas.</b>", 128),
    slide("ELE PRECISA DE", ["DOCUMENTO", "EM ORDEM"], [("Cadastro completo", "Razão social, CNPJ e quem pode comprar."), ("Nota fiscal certa", "Sem erro de dados, de primeira."), ("Orçamento formal", "Com validade, prazo e condição.")], 84),
    slide("E DE", ["CONFIANÇA"], [("Prazo cumprido", "Obra de empresa tem cronograma."), ("Um contato fixo", "Que conhece o histórico do cliente."), ("Retorno rápido", "Quem demora perde o próximo pedido.")], ini=4),
    fim(["RESULTADO"], [("Compra recorrente", "Empresa satisfeita repete."), ("Indicação", "Para outras empresas.")], 'Quer estruturar a venda para empresas? <b>Chame no direct.</b>', 120)],
    'Venda para empresas na loja de material de construção: o que o cliente PJ precisa para comprar de novo.\n\nCadastro, nota correta, orçamento formal, prazo cumprido e contato fixo. Salve e mande para sua equipe.', '#vendasb2b #construtora'),
  f1530=('conta-segunda-viagem', conta(["A SEGUNDA VIAGEM", "DO CAMINHÃO"], "Entrega errada volta. <b>Cada viagem extra custa R$ 80</b>.",
    [("2 erros por semana", "R$ 160"), ("No mês (4 semanas)", "R$ 640"), ("No ano", "R$ 7.680")], (2,),
    'Conferência antes de sair custa menos. <b>Chame no direct.</b>', 96),
    'Entrega errada na loja de material de construção: duas viagens extras por semana custam R$ 7.680 no ano.\n\nExemplo ilustrativo. Quer reduzir o erro de entrega? Chame no direct.', '#logistica #entrega'),
  f1930=('espelho-so-voce-sabe-margem', espelho(["SÓ VOCÊ SABE", "A MARGEM"], [("O vendedor dá desconto", "Sem saber quanto a loja ganha."), ("O gerente não decide", "Porque não tem o número."), ("Cada negociação passa por você", "Até no seu dia de folga."), ("E a margem escorre", "Em vendas que pareciam boas.")], 'Informação certa para a pessoa certa.', 104),
    'Margem de lucro na loja de material de construção: quando só o dono sabe quanto pode negociar.\n\nSe você se viu aqui, chame no direct.', '#margemdelucro #donodeloja'),
  f2230=('toda-loja-janela-recebimento', toda(["JANELA DE", "RECEBIMENTO"], "Caminhão de fornecedor <b>no horário de pico</b> trava a loja.",
    [("Horário combinado", "Com cada fornecedor."), ("Fora do pico do balcão", "Quando há gente para conferir."), ("Doca ou área livre", "Antes do caminhão chegar."), ("Responsável definido", "Quem confere e quem assina.")], 104),
    'Recebimento de mercadoria na loja de material de construção: a janela de horário que evita travar o balcão.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#compras #depositodematerial'),
  s1800=('brita-0-1-2', tec(["BRITA 0,", "1 OU 2?"], "Quanto maior o número, <b>maior a pedra</b>.",
    [("<span class='h'>BRITA</span>", "<span class='h'>USO MAIS COMUM</span>"), ("Brita 0 (pedrisco)", "peças finas e pré-moldados"), ("Brita 1", "concreto de lajes, vigas e pilares"), ("Brita 2", "concreto de peças mais robustas")],
    'O traço certo é o <b>projeto ou o engenheiro</b> que define.', 'Fonte: Votorantim Cimentos · Sienge · ABNT NBR 7211 (agregados para concreto)', 96, 25)),
  s2100=('flow-varios-atacadistas', flow(["UM ITEM,", "VÁRIOS ATACADISTAS"], [("Mesmo item em várias filas", "Cada atacadista cota o seu preço."), ("Compra pelo melhor", "Atacadista por atacadista."), ("Sem item duplicado", "Fechou com um, sai das outras filas.")], fs=92)),
  s0600=('02-12-avise-antes', bomdia(["AVISE O CLIENTE", "ANTES DO CAMINHÃO"], "Uma mensagem: <b>“sua entrega sai agora e chega até tal hora”.</b>", "Cliente avisado recebe melhor.", 96)),
)

# ======================================================================= 02/12 (qua)
DIAS['02-12'] = dict(
  f1030=('dizer-nao-desconto', [
    capa("MANDE PARA SUA EQUIPE", ["COMO DIZER NÃO", "AO DESCONTO"], "Sem perder o cliente <b>e sem perder a margem.</b>", 108),
    slide("EM VEZ DE CEDER", ["MOSTRE O", "VALOR"], [("Entrega e prazo", "“A gente entrega amanhã cedo na obra.”"), ("Qualidade e garantia", "“Essa marca não dá problema no assentamento.”"), ("Atendimento", "“Qualquer dúvida na obra, me chama.”")]),
    slide("SE PRECISAR CEDER", ["TROQUE"], [("Desconto por quantidade", "Leva tudo e ganha a condição."), ("Desconto por pagamento", "À vista tem condição diferente."), ("Brinde em vez de preço", "Um item de custo menor que o desconto.")], ini=4),
    fim(["COMBINE", "COM A EQUIPE"], [("Até onde cada um pode ir", "Por escrito."), ("Quem aprova acima disso", "E com que rapidez.")], 'Quer montar a política de desconto da sua loja? <b>Chame no direct.</b>', 104)],
    'Negociação na loja de material de construção: como dizer não ao desconto sem perder o cliente.\n\nMostre valor, troque desconto por quantidade ou pagamento e combine o limite com a equipe. Salve e mande para sua equipe.', '#negociacao #vendedordebalcao'),
  f1530=('conta-diferenca-caixa', conta(["R$ 20 POR DIA DE", "DIFERENÇA NO CAIXA"], "Diferença pequena que <b>ninguém registra</b>.",
    [("Por dia", "R$ 20"), ("26 dias no mês", "R$ 520"), ("12 meses", "R$ 6.240")], (2,),
    'Caixa conferido todo dia não deixa a conta crescer. <b>Chame no direct.</b>', 92),
    'Fechamento de caixa na loja de material de construção: R$ 20 por dia de diferença viram R$ 6.240 no ano.\n\nExemplo ilustrativo. Quer organizar o caixa da sua loja? Chame no direct.', '#fluxodecaixa #gestaofinanceira'),
  f1930=('espelho-cada-vendedor', espelho(["CADA VENDEDOR,", "UMA LOJA DIFERENTE"], [("Um dá desconto, outro não", "E o cliente escolhe com quem falar."), ("Um oferece entrega, outro esquece", "O mesmo cliente, duas experiências."), ("Orçamento em três formatos", "Nenhum igual ao outro."), ("O cliente sente", "Que depende da sorte.")], 'Padrão de atendimento é o que faz a loja ser uma só.', 96),
    'Padrão de atendimento na loja de material de construção: quando cada vendedor parece uma loja diferente.\n\nSe você se viu aqui, chame no direct.', '#atendimentoaocliente #gestaodeloja'),
  f2230=('toda-loja-pergunta-fim-compra', toda(["UMA PERGUNTA NO", "FIM DA COMPRA"], "<b>“De 0 a 10, quanto indicaria a loja?”</b> Simples e revelador.",
    [("Sempre a mesma pergunta", "Para comparar mês a mês."), ("Anote a nota e o motivo", "O motivo vale mais que a nota."), ("Nota baixa, retorno rápido", "Ligue no mesmo dia."), ("Mostre para a equipe", "Toda semana.")], 92),
    'Satisfação do cliente na loja de material de construção: uma pergunta no fim da compra que mostra onde melhorar.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#atendimentoaocliente #experienciadocliente'),
  s1800=('massa-corrida-acrilica', tec(["MASSA CORRIDA", "OU ACRÍLICA?"], "As duas nivelam a parede. <b>O ambiente decide.</b>",
    [("<span class='h'>MASSA</span>", "<span class='h'>ONDE USAR</span>"), ("Corrida (PVA)", "interno seco"), ("Acrílica", "externo e áreas úmidas")],
    'Massa corrida no banheiro <b>estufa e descasca</b>.', 'Fonte: fichas técnicas dos fabricantes (Suvinil, Coral)', 92)),
  s2100=('obras-convite', obras(["NENHUM PROFISSIONAL", "FICA DE FORA"], "Para o treinamento, <b>a lista já está pronta</b>.",
    [("Fila de convite", "Todos os profissionais cadastrados."), ("Marca quem já foi chamado", "Ninguém esquecido."), ("Por especialidade", "Convite certo para cada evento.")], 84)),
  s0600=('03-12-termine', bomdia(["TERMINE O QUE", "COMEÇOU ONTEM"], "Antes de começar outra, <b>feche uma antiga.</b>", "Pendência acumulada pesa na equipe toda.")),
)

# ======================================================================= 03/12 (qui)
DIAS['03-12'] = dict(
  f1030=('escala-5x2-parte6', [
    capa("ESCALA 5x2 NA LOJA · PARTE 6", ["CHECKLIST", "FINAL"], "Duas semanas para <b>16 de dezembro</b>. Confira se a loja está pronta.", 128),
    slide("DOCUMENTOS", ["CONFIRA"], [("Escala validada", "Pelo contador ou advogado trabalhista."), ("Controle de jornada", "Ajustado para 42 horas semanais."), ("Equipe avisada", "Com a escala por escrito.")], fonte=FONTE_EC),
    slide("OPERAÇÃO", ["TESTE"], [("Sábado e pico cobertos", "Com o mínimo de cada setor."), ("Almoço e folgas fora do pico", "Sem balcão vazio."), ("Passagem de turno funcionando", "Antes da data.")], ini=4),
    fim(["ACOMPANHE"], [("Decisões do STF", "As regras de transição ainda estão em análise."), ("Ajustes nas primeiras semanas", "Escala nova sempre pede correção.")], 'Quer revisar a escala da sua loja? <b>Chame no direct.</b>', 120, extra=f'\n  {sub(VALIDE, 28, 120)}')],
    'Escala 5x2 na loja de material de construção, parte 6: checklist final antes de 16 de dezembro.\n\nDocumentos, operação e acompanhamento das regras de transição. Cada loja deve validar a escala com o seu contador ou advogado trabalhista.', '#escala5x2 #gestaodeequipe'),
  f1530=('conta-mix-margem', conta(["MESMA VENDA,", "LUCROS DIFERENTES"], "R$ 1.000 vendidos não são iguais: <b>cada categoria tem a sua margem</b>.",
    [("R$ 1.000 em cimento (margem 8%)", "R$ 80"), ("R$ 1.000 em acabamento (margem 35%)", "R$ 350")], (1,),
    'Saber o que vende é bom. Saber o que dá lucro é melhor. <b>Chame no direct.</b>', 104, 28),
    'Mix de produtos na loja de material de construção: a mesma venda pode deixar R$ 80 ou R$ 350 de lucro.\n\nExemplo ilustrativo. Quer conhecer a margem por categoria da sua loja? Chame no direct.', '#margemdelucro #mixdeprodutos'),
  f1930=('espelho-cliente-sabe-antes', espelho(["O CLIENTE SABE", "ANTES DE VOCÊ"], [("Que a entrega atrasou", "Porque está esperando na obra."), ("Que o produto acabou", "Porque foi buscar e não tinha."), ("Que o vendedor foi grosso", "E contou para o vizinho."), ("Você descobre por último", "Quando ele já foi embora.")], 'Loja com processo avisa antes de o cliente reclamar.', 96),
    'Gestão da loja de material de construção: quando o cliente descobre os problemas antes do dono.\n\nSe você se viu aqui, chame no direct.', '#experienciadocliente #donodeloja'),
  f2230=('toda-loja-caminho-cliente', toda(["UM CAMINHO QUE LEVA", "O CLIENTE ATÉ O FUNDO"], "Quem só passa no balcão <b>não vê o resto da loja</b>.",
    [("Básico no fundo", "Cimento e argamassa puxam o cliente para dentro."), ("Impulso no caminho", "Ferramenta, fita, luva, lâmpada."), ("Corredores livres", "Sem caixa no meio da passagem."), ("Sinalização por setor", "Visível de longe.")], 84),
    'Layout da loja de material de construção: o caminho que leva o cliente até o fundo e aumenta a compra.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#layoutdeloja #varejo'),
  s1800=('impermeabilizantes', tec(["MANTA, ARGAMASSA", "OU MEMBRANA?"], "Cada impermeabilizante tem <b>o seu lugar na obra</b>.",
    [("<span class='h'>PRODUTO</span>", "<span class='h'>USO MAIS COMUM</span>"), ("Manta asfáltica", "lajes e coberturas"), ("Argamassa polimérica", "baldrame, caixa d’água, banheiro"), ("Membrana acrílica", "lajes sem tráfego")],
    'O sistema certo é <b>definido no projeto</b>.', 'Fonte: ABNT NBR 9575 (impermeabilização) · fichas técnicas de fabricantes', 84, 25)),
  s2100=('flow-catalogo-marca', flow(["ACHE PELO CÓDIGO", "DA MARCA"], [("Catálogo da marca", "Importado por planilha."), ("Código e código de barras", "Ao lado do código da loja."), ("Busca pelo nome", "Na hora de lançar a demanda.")], fs=88)),
  s0600=('04-12-como-conheceu', bomdia(["COMO O CLIENTE", "CONHECEU A LOJA?"], "Pergunte a cada cliente novo e <b>anote.</b>", "Em uma semana, você sabe onde investir.", 96)),
)

# ======================================================================= 04/12 (sex)
DIAS['04-12'] = dict(
  f1030=('orcamento-grande', [
    capa("MANDE PARA SUA EQUIPE", ["ORÇAMENTO GRANDE", "SE APRESENTA"], "Obra inteira não se fecha <b>com uma foto no WhatsApp.</b>", 104),
    slide("ANTES DE ENVIAR", ["ORGANIZE"], [("Por etapa da obra", "Fundação, alvenaria, instalações, acabamento."), ("Com validade e prazo", "Claros, na primeira página."), ("Opções lado a lado", "Quando houver marcas diferentes.")]),
    slide("NA APRESENTAÇÃO", ["CONVERSE"], [("Marque um horário", "Na loja ou por vídeo."), ("Explique as escolhas", "Por que cada produto."), ("Ofereça a entrega programada", "Por etapa, quando a obra precisar.")], ini=4),
    fim(["DEPOIS"], [("Retorno combinado", "Dia e hora para a resposta."), ("Ajuste rápido", "Se o cliente pedir.")], 'Quer padronizar os orçamentos da sua loja? <b>Chame no direct.</b>', 120)],
    'Orçamento de obra na loja de material de construção: como apresentar o orçamento grande em vez de só enviar.\n\nOrganize por etapa, converse com o cliente e combine o retorno. Salve e mande para sua equipe.', '#orcamento #vendedordebalcao'),
  f1530=('conta-vender-a-custo', conta(["VENDER A PREÇO DE", "CUSTO PODE DAR LUCRO"], "Item <b>parado há 12 meses</b>, vendido pelo que custou.",
    [("Dinheiro que volta ao caixa", "R$ 5.000"), ("Ganho por giro (25%)", "R$ 1.250"), ("4 giros no ano", "R$ 5.000")], (2,),
    'Estoque parado também tem saída. <b>Chame no direct.</b>', 80, 26),
    'Estoque parado na loja de material de construção: vender a preço de custo e reinvestir em produto que gira.\n\nR$ 5.000 parados, reinvestidos com ganho de 25% em 4 giros, rendem R$ 5.000 no ano. Exemplo ilustrativo.', '#gestaodeestoque #giro'),
  f1930=('espelho-tudo-na-cabeca', espelho(["TUDO NA SUA", "CABEÇA"], [("Quanto custa cada fornecedor", "Ninguém mais sabe."), ("Quem deve para a loja", "Só você lembra."), ("Como fazer o pedido", "Nunca foi escrito."), ("Se você ficar doente", "A loja para junto.")], 'O que está só na cabeça do dono é risco para a loja.', 104),
    'Processos na loja de material de construção: quando tudo está só na cabeça do dono.\n\nSe você se viu aqui, chame no direct.', '#processos #donodeloja'),
  f2230=('toda-loja-amostra', toda(["AMOSTRA QUE", "VAI PARA CASA"], "O cliente decide <b>vendo na luz da casa dele</b>.",
    [("Peça de piso e revestimento", "Para ver no ambiente."), ("Cartela de cor", "Com o código anotado."), ("Prazo para devolver", "E nome do cliente registrado."), ("Contato no dia seguinte", "“Gostou? Vamos fechar?”")], 104),
    'Venda de acabamento na loja de material de construção: a amostra que o cliente leva para decidir em casa.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#acabamento #vendas'),
  s1800=('tinta-economica-premium', tec(["ECONÔMICA, STANDARD", "OU PREMIUM?"], "É a <b>classificação de desempenho</b> da tinta látex.",
    [("<span class='h'>LINHA</span>", "<span class='h'>DESEMPENHO</span>"), ("Econômica", "menor cobertura e resistência"), ("Standard", "intermediária"), ("Premium", "maior cobertura e durabilidade")],
    'Na premium, <b>menos demãos</b> podem compensar o preço.', 'Fonte: ABNT NBR 15079 (tintas látex) · Programa Setorial da Qualidade de Tintas', 84)),
  s2100=('obras-campanha', obras(["CAMPANHA DE PONTOS", "COM PRÊMIO"], "Campanhas para profissionais <b>com começo e fim</b>.",
    [("Período definido", "Data de início e de fim."), ("Regra da loja", "Pontos por valor indicado."), ("Resgate", "Prêmio ou valor, a critério da loja.")], 84)),
  s0600=('05-12-sua-equipe', bomdia(["COMO ESTÁ", "SUA EQUIPE?"], "Fim de ano pesa para todo mundo. <b>Pergunte, escute e ajuste o que der.</b>", "Equipe cuidada cuida do cliente.", 104)),
)

# ======================================================================= 05/12 (sáb)
DIAS['05-12'] = dict(
  f1030=('vitrine-dezembro', unico("MANDE PARA SUA EQUIPE", ["A VITRINE DE", "DEZEMBRO"], "Fim de ano é época de <b>pintura e pequena reforma</b>.",
    [("Tinta e acessórios na frente", "Rolo, fita, lona e massa juntos."), ("Kits prontos", "Para quem quer resolver rápido."), ("Ferramenta para presente", "Bem exposta, com preço visível."), ("Troque antes do dia 10", "Para aproveitar o mês inteiro.")],
    'Quer planejar a exposição da sua loja? <b>Chame no direct.</b>', 108),
    'Vitrine de dezembro na loja de material de construção: pintura, pequenas reformas e ferramenta para presente.\n\nSalve e mande para sua equipe.', '#vitrine #visualmerchandising'),
  f1530=('conta-desconto-a-vista', conta(["3% À VISTA NO", "PEDIDO DO FORNECEDOR"], "Quando o caixa permite, <b>o desconto à vista</b> vira margem.",
    [("Pedido de", "R$ 20.000"), ("Desconto à vista (3%)", "R$ 600"), ("4 pedidos no mês", "R$ 2.400")], (2,),
    'Planejar o caixa abre espaço para negociar. <b>Chame no direct.</b>', 88),
    'Compras na loja de material de construção: 3% de desconto à vista em quatro pedidos somam R$ 2.400 no mês.\n\nExemplo ilustrativo, quando o caixa permite. Quer planejar o caixa da sua loja? Chame no direct.', '#compras #fluxodecaixa'),
  f1930=('espelho-mais-horas', espelho(["MAIS HORAS,", "MESMO RESULTADO"], [("Abre mais cedo", "E fecha mais tarde."), ("Trabalha no sábado inteiro", "E no domingo responde mensagem."), ("A venda não cresce", "Na mesma proporção."), ("O cansaço cresce", "Todo mês.")], 'Resultado vem de processo, não só de esforço.', 104),
    'Produtividade do dono de loja de material de construção: trabalhar mais horas e ter o mesmo resultado.\n\nSe você se viu aqui, chame no direct.', '#produtividade #donodeloja'),
  f2230=('toda-loja-instagram', toda(["A LOJA NO INSTAGRAM", "TODA SEMANA"], "O cliente procura a loja <b>no celular antes de ir até ela</b>.",
    [("Horário e endereço atualizados", "No perfil e no Google."), ("Produto chegando", "Novidade vende."), ("Obra de cliente", "Com autorização dele."), ("Equipe aparecendo", "Gente gera confiança.")], 92),
    'Instagram da loja de material de construção: o mínimo para o cliente encontrar e confiar na loja.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#marketingdigital #varejo'),
  s1800=('selador-fundo-preparador', tec(["SELADOR OU FUNDO", "PREPARADOR?"], "Os dois vêm <b>antes da tinta</b>. A parede decide.",
    [("<span class='h'>PRODUTO</span>", "<span class='h'>QUANDO USAR</span>"), ("Selador acrílico", "reboco novo, para uniformizar"), ("Fundo preparador", "superfície que esfarela ou solta pó")],
    'Pergunte como está a parede <b>antes de vender a tinta</b>.', 'Fonte: fichas técnicas dos fabricantes (Suvinil, Coral)', 88)),
  s2100=('flow-propostas-lado-a-lado', flow(["COMPARE AS PROPOSTAS", "LADO A LADO"], [("Cotação por link", "O fornecedor responde de onde estiver."), ("Propostas juntas", "Preço e condição na mesma tela."), ("Decisão registrada", "Quem comprou, de quem e por quê.")], fs=80)),
  s0600=('06-12-familia-agenda', bomdia(["FAMÍLIA TAMBÉM", "É AGENDA"], "Marque hoje um compromisso com quem você ama <b>e trate como reunião importante.</b>", "Ninguém cresce sozinho.", 100)),
)

# ======================================================================= 06/12 (dom)
DIAS['06-12'] = dict(
  f1030=('ferramenta-presente', unico("DEZEMBRO NA LOJA", ["FERRAMENTA", "É PRESENTE"], "Quem tem obra em casa <b>gosta de ganhar ferramenta</b>.",
    [("Kits de presente", "Montados e embalados."), ("Faixas de preço", "Para cada bolso."), ("Expostos na entrada", "Com placa de presente."), ("Troca combinada", "Para quem recebe o presente.")],
    'Quer planejar o fim de ano da sua loja? <b>Chame no direct.</b>', 120),
    'Natal na loja de material de construção: ferramenta é presente, e a loja pode vender mais em dezembro.\n\nKits montados, faixas de preço e exposição na entrada. Quer planejar o fim de ano? Chame no direct.', '#natal #ferramentas'),
  f1530=('conta-brinde-desconto', conta(["BRINDE DE R$ 30 OU", "DESCONTO DE 5%?"], "Venda de <b>R$ 2.000</b> e o cliente pedindo condição.",
    [("Desconto de 5%", "R$ 100 a menos"), ("Brinde com custo de", "R$ 30"), ("Diferença para a loja", "R$ 70")], (2,),
    'Às vezes o brinde agrada mais e custa menos. <b>Chame no direct.</b>', 88),
    'Negociação na loja de material de construção: brinde de R$ 30 ou desconto de 5% numa venda de R$ 2.000.\n\nA diferença para a loja é de R$ 70. Exemplo ilustrativo. Quer montar a política comercial da sua loja? Chame no direct.', '#negociacao #margemdelucro'),
  f1930=('espelho-2026-cresceu', espelho(["2026 ACABANDO.", "SUA LOJA CRESCEU?"], [("Vendeu mais que em 2025?", "Você sabe dizer quanto?"), ("A margem melhorou ou piorou?", "Por quê?"), ("A equipe ficou mais forte?", "Ou mais dependente de você?"), ("Qual decisão mudou a loja?", "E qual faltou tomar?")], 'Fechar o ano com números é o primeiro passo de 2027.', 100),
    'Balanço do ano na loja de material de construção: quatro perguntas para saber se a loja cresceu em 2026.\n\nSe você não sabe responder, chame no direct.', '#planejamento #donodeloja'),
  f2230=('toda-loja-cantinho-profissional', toda(["UM CANTINHO PARA", "O PROFISSIONAL"], "Pedreiro bem recebido <b>volta e traz o cliente</b>.",
    [("Café e água", "Sempre disponíveis."), ("Atendimento rápido", "Ele está com a obra parada."), ("Mural de avisos", "Treinamentos e novidades."), ("Chamado pelo nome", "Ele faz parte da loja.")], 92),
    'Relacionamento com o pedreiro na loja de material de construção: o cantinho do profissional.\n\nSua loja já tem? Diagnóstico sem custo no direct.', '#pedreiro #relacionamento'),
  s1800=('argamassa-tipos-uso', tec(["ASSENTAR, REBOCAR", "OU COLAR?"], "Cada argamassa tem <b>uma função na obra</b>.",
    [("<span class='h'>ARGAMASSA</span>", "<span class='h'>FUNÇÃO</span>"), ("De assentamento", "levantar a parede de blocos"), ("De revestimento", "reboco da parede"), ("Colante (AC)", "fixar piso e revestimento")],
    'Argamassa trocada é <b>retrabalho na obra</b>.', 'Fonte: fichas técnicas de fabricantes (Quartzolit, Votorantim)', 88)),
  s2100=('obras-quentes-primeiro', obras(["AS OBRAS QUENTES", "PRIMEIRO"], "O painel abre mostrando <b>a venda de agora</b>.",
    [("Obras quentes em destaque", "No topo do painel."), ("Esfriando em alerta", "Antes de virar perda."), ("Contexto de cada obra", "Fase e último contato.")], 88)),
  s0600=('07-12-chegue-com-plano', bomdia(["CHEGUE COM", "UM PLANO"], "Três prioridades para a semana, <b>escritas antes de abrir a porta.</b>", "Semana com plano rende mais.")),
)


def montar(dias):
    itens, meta = [], []
    for d in dias:
        c = DIAS[d]
        pasta = os.path.join(G.RAIZ, 'posts', '2026-' + d[3:], 'dia-' + d)
        for chave, hora in (('f1030', '1030'), ('f1530', '1530'), ('f1930', '1930'), ('f2230', '2230')):
            nome, arte, leg, tags = c[chave]
            if isinstance(arte, list):
                arqs = [f'{hora}-{nome}-{i + 1}' for i in range(len(arte))]
                for a, h in zip(arqs, arte): itens.append((pasta, a, h, (W, H)))
            else:
                arqs = [f'{hora}-{nome}']; itens.append((pasta, arqs[0], arte, (W, H)))
            meta.append(dict(dia=d, hora=hora, tipo='POST', arquivos=[os.path.relpath(os.path.join(pasta, a + '.jpg'), G.RAIZ) for a in arqs], legenda=leg + '\n\n' + HT + ' ' + tags, titulo=nome))
        for chave, hora in (('s1800', '1800'), ('s2100', '2100'), ('s0600', '0600')):
            nome, arte = c[chave]
            a = f'story-{hora}-{nome}'; itens.append((pasta, a, arte, (SW, SH)))
            meta.append(dict(dia=d, hora=hora, tipo='STORY', arquivos=[os.path.relpath(os.path.join(pasta, a + '.jpg'), G.RAIZ)], titulo=nome))
    return itens, meta


if __name__ == '__main__':
    dias = sys.argv[1:] or list(DIAS)
    itens, meta = montar(dias)
    por_pasta = {}
    for p, n, h, wh in itens: por_pasta.setdefault(p, []).append((n, h, wh))
    for p, lst in por_pasta.items():
        print('==', os.path.basename(p)); asyncio.run(renderizar(lst, p))
    json.dump(meta, open(os.path.join(G.RAIZ, 'gerador', 'semanas', 'lote-22-11-a-06-12.json'), 'w'), ensure_ascii=False, indent=1)
