"""Feed 19:30 de 25/11 a 06/12/2026: substitui o "Espelho do dono" pelos 4 novos modelos intercalados
(Sâny Responde, FORTÍS FLOW na prática, FORTÍS OBRAS, Ferramenta no site).
Uso: python3 gerador/especiais/lote-1930-25-11-a-06-12.py
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelos_base import *

HT = "#materialdeconstrucao #lojadematerialdeconstrucao #varejomatcon #donodeloja"
G_ = 'style="color:#D9B579"'


def url(rotulo, link):
    return f'<div class="url k" style="left:70px;right:70px;bottom:120px;padding:22px 20px;font-size:30px">{rotulo} <b>{link}</b></div>'


def responde(pergunta, resposta, texto, rot, link):
    return base(f'''
  <img class="foto" src="{FOTO}" style="right:-110px;bottom:215px;width:640px">
  <div class="esq" style="left:70px;top:250px;width:600px"><div class="kl k">O LOJISTA PERGUNTOU</div></div>
  <div class="balao k" style="left:70px;top:310px;width:560px;padding:30px 34px">
    <div style="font-size:31px;font-weight:600;line-height:1.35">“{pergunta}”</div></div>
  <div class="esq" style="left:70px;top:590px;width:440px">
    <div class="kl k" style="margin-bottom:18px">SÂNY RESPONDE</div>
    <div class="titulo k" data-max="440" data-fs="96" style="position:static;line-height:1.02">{tl(resposta, 96)}</div>
    <p class="k" style="margin-top:26px;font-size:25px;line-height:1.42;color:#e9edf5">{texto}</p>
  </div>{url(rot, link)}''', cls="suave")


def flow(titulo, lst, tela, link="fortismatcon.com.br/fortis-flow"):
    return base(f'''
  <div class="esq" style="left:70px;top:230px;width:560px">
    <div class="tag k">FORTÍS FLOW NA PRÁTICA</div>
    <div class="titulo k" data-max="540" data-fs="84" style="position:static;margin-top:30px;line-height:1.04">{tl(titulo, 84)}</div>
    <div style="margin-top:46px">{itens(lst)}</div>
  </div>
  <div class="celular" style="right:62px;top:220px;width:390px;height:880px"><div class="tela"><img src="{A}/telas/{tela}"></div></div>
  {url("Conheça o Flow:", link)}''')


def obras(titulo, texto, lst):
    return base(f'''
  <div class="retrato" style="right:70px;top:230px;width:300px;height:300px"><img src="{FOTO}"></div>
  <div class="esq" style="left:70px;top:240px;width:580px">
    <div class="tag k">FORTÍS OBRAS</div>
    <div class="titulo k" data-max="580" data-fs="90" style="position:static;margin-top:30px;line-height:1.04">{tl(titulo, 90)}</div>
  </div>
  <p class="k" style="position:absolute;left:70px;right:70px;top:600px;font-size:30px;line-height:1.45;color:#e9edf5">{texto}</p>
  <div style="position:absolute;left:70px;right:70px;top:800px">{itens(lst)}</div>
  {url("Quer ver na sua loja?", "Chame no direct.")}''', cls="suave")


def ferramenta(titulo, rotulo, lst, link):
    return base(f'''
  <img class="foto" src="{FOTO}" style="left:-50px;bottom:215px;width:560px">
  <div class="esq" style="left:70px;top:230px;width:940px">
    <div class="tag k">GRÁTIS NO SITE DA FORTÍS</div>
    <div class="titulo k" data-max="940" data-fs="92" style="position:static;margin-top:30px;line-height:1.04">{tl(titulo, 92)}</div>
  </div>
  <div class="esq" style="left:520px;top:600px;width:500px">
    <div class="kl k" style="margin-bottom:26px">{rotulo}</div>{itens(lst)}
  </div>{url("Use agora:", link)}''')


POSTS = [
 ("25-11", "sany-responde-erp",
  responde(f'Para organizar minhas compras, eu preciso <b {G_}>trocar de ERP</b>?', ["NÃO", "PRECISA."],
   f'O ERP cuida do <b {G_}>produto e da nota</b>. O FORTÍS FLOW cuida das <b {G_}>pessoas, pedidos e prazos</b>. Um completa o outro.',
   "Veja como funciona:", "fortismatcon.com.br/fortis-flow"),
  "Preciso trocar de ERP para organizar as compras da loja de material de construção? Não precisa.\n\nO ERP continua cuidando de produto, venda e nota fiscal. O FORTÍS FLOW organiza o que fica fora dele: quem pediu, quem comprou, o que está atrasado e quem é responsável.\n\nVeja como funciona: fortismatcon.com.br/fortis-flow (link na bio)\n\nTem uma pergunta sobre a sua loja? Mande no direct que eu respondo aqui.\n\nSâny Oliveira · FORTÍS SOLUÇÕES MATCON"),
 ("26-11", "flow-pedido-whatsapp",
  flow(["O PEDIDO", "QUE SE PERDIA", "NO WHATSAPP"], [("Vendedor pede no app", "Item, quantidade e cliente, no mesmo lugar."), ("Comprador vê a fila", "Nada some no meio da conversa."), ("Dono acompanha", "Quem pediu, quem comprou e quando.")], "fila.png"),
  "Loja de material de construção: o pedido de compra que se perde no WhatsApp.\n\nO vendedor manda áudio, o comprador está em outra conversa, e o item só aparece quando o cliente volta reclamando. No FORTÍS FLOW, cada pedido entra numa fila com responsável e prazo.\n\nTela real do app, com dados de exemplo.\n\nConheça o Flow: fortismatcon.com.br/fortis-flow (link na bio)"),
 ("27-11", "ferramenta-calculadoras",
  ferramenta(["O CLIENTE PERGUNTOU", "QUANTO LEVAR?"], "CALCULADORAS", [("Telhado", "Telha, cumeeira e fixação."), ("Tinta", "Litros por parede e demão."), ("Piso e reboco", "Metragem com a perda certa.")], "fortismatcon.com.br/ferramentas"),
  "Calculadoras grátis para o balcão da loja de material de construção: telhado, tinta, piso e reboco.\n\nO cliente pergunta quanto levar e o vendedor responde na hora, com a conta certa. Sem cadastro, direto no celular.\n\nUse agora: fortismatcon.com.br/ferramentas (link na bio)\nSalve e mande para a sua equipe de balcão."),
 ("28-11", "obras-vendedor-externo",
  obras(["O VENDEDOR", "VOLTOU DA RUA"], f'E agora? Sem registro, a visita vira lembrança. No FORTÍS OBRAS, <b {G_}>cada obra visitada fica na tela</b> de quem vende.',
        [("Obra registrada na visita", "Endereço, contato e o que ela precisa."), ("Dias sem contato à vista", "A obra não esfria sem ninguém ver."), ("Radar comercial", "Quem ligar hoje, em ordem de prioridade.")]),
  "Vendedor externo da loja de material de construção: o que ele trouxe da rua?\n\nSe a visita não fica registrada, a obra some da memória e vai comprar no concorrente. O FORTÍS OBRAS guarda cada obra visitada e mostra quem precisa de contato hoje.\n\nQuer ver o Obras funcionando na sua loja? Chame no direct."),
 ("29-11", "sany-responde-loja-pequena",
  responde(f'Consultoria é <b {G_}>só para loja grande</b>?', ["NÃO", "É."],
   f'Loja de bairro tem os mesmos problemas de uma rede: <b {G_}>compra sem controle, equipe sem meta e margem que some</b>. Muda o tamanho, não o método.',
   "Diagnóstico sem custo:", "fortismatcon.com.br/diagnostico"),
  "Consultoria é só para loja grande de material de construção? Não é.\n\nA loja de bairro sofre com as mesmas coisas: compra sem controle, equipe sem meta, margem que some no balcão. O tamanho muda, o método é o mesmo.\n\nDiagnóstico sem custo, 15 minutos: fortismatcon.com.br/diagnostico (link na bio)\n\nSâny Oliveira · FORTÍS SOLUÇÕES MATCON"),
 ("30-11", "flow-meta-vendedor",
  flow(["QUANTO FALTA", "PARA A META?", "O VENDEDOR SABE."], [("Meta do mês na tela", "Realizado e quanto falta, em reais."), ("Meta diária necessária", "O ritmo certo para cada dia útil."), ("Projeção de fechamento", "O mês visto antes de acabar.")], "metas.png"),
  "Meta de vendedor na loja de material de construção: ele sabe quanto falta?\n\nNo FORTÍS FLOW, cada vendedor vê no celular a meta do mês, quanto já vendeu, quanto precisa vender por dia e a projeção de fechamento. Meta que ninguém vê não é meta.\n\nTela real do app, com dados de exemplo.\n\nConheça o Flow: fortismatcon.com.br/fortis-flow (link na bio)"),
 ("01-12", "ferramenta-escala-5x2",
  ferramenta(["SUA ESCALA 5x2", "JÁ ESTÁ PRONTA?"], "CALCULADORA 5x2", [("Equipe por setor", "Quantas pessoas cada setor precisa."), ("Folgas sem buraco", "Sábado e setores cobertos."), ("Antes de 16/12", "Organize com tempo.")], "fortismatcon.com.br/ferramentas"),
  "Escala 5x2 na loja de material de construção: a sua já está pronta?\n\nA Fortís criou uma calculadora grátis para ajudar o lojista a montar a escala por setor, sem deixar o sábado descoberto. Cada loja deve validar a escala com o seu contador ou advogado trabalhista.\n\nUse agora: fortismatcon.com.br/ferramentas (link na bio)"),
 ("02-12", "obras-profissionais-parceiros",
  obras(["QUEM SÃO OS", "PARCEIROS DA LOJA?"], f'Pedreiro, eletricista, pintor: quem traz obra merece <b {G_}>cadastro, regra clara e reconhecimento</b>.',
        [("Cadastro por especialidade", "Cada profissional no lugar certo."), ("Pontos por venda indicada", "Com a regra que a loja define."), ("Pontuação no WhatsApp", "O parceiro acompanha sem perguntar.")]),
  "Profissionais parceiros da loja de material de construção: você sabe quem traz obra para você?\n\nNo FORTÍS OBRAS, cada pedreiro, eletricista e pintor fica cadastrado por especialidade, acumula pontos pelas vendas que indica e recebe a pontuação pelo WhatsApp.\n\nQuer ver o Obras funcionando na sua loja? Chame no direct."),
 ("03-12", "sany-responde-por-onde-comecar",
  responde(f'Quero organizar a loja. <b {G_}>Por onde eu começo</b>?', ["PELO", "NÚMERO."],
   f'Antes de mudar qualquer coisa, descubra <b {G_}>onde a loja está</b>: compras, equipe, estoque e margem. O teste leva poucos minutos.',
   "Faça o teste:", "fortismatcon.com.br/ferramentas"),
  "Por onde começar a organizar a loja de material de construção? Pelo número.\n\nAntes de trocar processo, sistema ou gente, descubra onde a loja está hoje em compras, equipe, estoque e margem. A Fortís deixou um teste de maturidade grátis no site.\n\nFaça o teste: fortismatcon.com.br/ferramentas (link na bio)\n\nSâny Oliveira · FORTÍS SOLUÇÕES MATCON"),
 ("04-12", "flow-avaria-cobrada",
  flow(["A TELHA", "QUEBRADA QUE", "NINGUÉM COBROU"], [("Avaria registrada na hora", "Foto, quantidade e prejuízo."), ("Fornecedor notificado", "Do app, sem papel perdido."), ("Status até o fim", "Em negociação ou ressarcida.")], "avarias.png"),
  "Avaria na loja de material de construção: quanto você deixou de cobrar do fornecedor este mês?\n\nTelha quebrada no palete, porcelanato trincado na descarga: no FORTÍS FLOW a avaria é registrada na hora, o fornecedor é notificado e o prejuízo fica à vista até ser ressarcido.\n\nTela real do app, com dados de exemplo.\n\nConheça o Flow: fortismatcon.com.br/fortis-flow (link na bio)"),
 ("05-12", "ferramenta-preco-de-venda",
  ferramenta(["SEU PREÇO", "COBRE A CONTA?"], "SIMULADOR DE PREÇO", [("Custo do produto", "Com frete e impostos."), ("Despesas da loja", "O que o preço precisa pagar."), ("Margem desejada", "O preço de venda certo.")], "fortismatcon.com.br/ferramentas"),
  "Preço de venda na loja de material de construção: o seu cobre custo, despesa e margem?\n\nO simulador grátis da Fortís mostra o preço certo a partir do custo, das despesas da loja e da margem que você quer ter.\n\nUse agora: fortismatcon.com.br/ferramentas (link na bio)"),
 ("06-12", "sany-responde-vendedor-processo",
  responde(f'Meu vendedor não segue processo. <b {G_}>O problema é ele</b>?', ["QUASE", "NUNCA."],
   f'Quando ninguém sabe a regra, cada um faz do seu jeito. <b {G_}>Processo escrito, meta à vista e conversa curta</b> resolvem antes de trocar gente.',
   "Mais no blog:", "fortismatcon.com.br/blog"),
  "Vendedor que não segue processo na loja de material de construção: o problema é ele? Quase nunca.\n\nSe a regra não está escrita, cada um faz do seu jeito. Processo claro, meta à vista e uma conversa curta antes de abrir a loja resolvem a maior parte antes de pensar em trocar gente.\n\nMais conteúdo para donos de loja: fortismatcon.com.br/blog (link na bio)\n\nSâny Oliveira · FORTÍS SOLUÇÕES MATCON"),
]

if __name__ == "__main__":
    saida = os.path.join(G.RAIZ, "posts", "2026-11", "lote-1930")
    asyncio.run(renderizar([(f"{d}-1930-{n}", h, (W, H)) for d, n, h, _ in POSTS], saida))
    json.dump([dict(dia=d, arquivo=f"posts/2026-11/lote-1930/{d}-1930-{n}.jpg", legenda=l + "\n\n" + HT) for d, n, _, l in POSTS],
              open(os.path.join(G.RAIZ, "gerador", "semanas", "lote-1930-25-11-a-06-12.json"), "w"), ensure_ascii=False, indent=1)
