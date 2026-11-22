"""Série "Calculadora da escala 5x2": leva o lojista para a calculadora do site.

Horários NOVOS, somados à grade (nada da grade muda): feed 13:30 e story 09:00
em 24/11, 27/11, 02/12, 08/12 e 14/12/2026. Números dos exemplos saem da própria
calculadora (modelo "Loja pequena", Simples Nacional, encargos 29%).
Uso: python3 gerador/especiais/serie-calculadora-5x2.py
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *

URL = 'fortismatcon.com.br/ferramentas'
HT = '#materialdeconstrucao #lojadematerialdeconstrucao #varejomatcon #escala5x2 #fimda6x1'
FONTE_DEC = 'Fonte: EC 141/2026 e decreto de 19/11/2026 (divisor 220 → 210 → 200)'


def capa(k, linhas, s, fs=112):
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {sub(s, 36, 110)}
  <p class="cta k" style="font-size:30px;color:var(--gold)">Deslize para o lado →</p>''', 170, 1.3)


def slide(k, linhas, itens, fs=96, ini=1, num=True):
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {lista(itens, 33, 24, num=num, ini=ini)}''', 110, 1.3)


def fim(linhas, itens, cta, fs=100):
    return feed(f'''{titulo(linhas, fs)}
  {lista(itens, 32, 23, num=False)}
  <p class="cta k" style="font-size:30px;padding:0 90px">{cta}</p>''', 110, 1.3)


def conta(k, linhas, s, tab, dest, cta, fs=88, tfs=28, selo=True, fonte=None):
    s_html = '\n  <div class="k"><span class="selo">EXEMPLO ILUSTRATIVO</span></div>' if selo else ''
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {sub(s, 29, 100)}
  {card(tabela(tab, tfs, destaque=dest), "4px 0", 880)}{s_html}
  <p class="cta k" style="font-size:29px;padding:0 80px">{cta}</p>''', 110, 1.3, fonte=fonte)


def unico(k, linhas, s, itens, cta, fs=96):
    return feed(f'''{kicker(k)}
  {titulo(linhas, fs)}
  {sub(s, 29, 100)}
  {lista(itens, 31, 23, num=False)}
  <p class="cta k" style="font-size:29px;padding:0 80px">{cta}</p>''', 96, 1.3)


def chamada(k, linhas, s, fs=100):
    return story(f'''{kicker(k, 26)}
  {titulo(linhas, fs, 900)}
  {sub(s, 34, 90)}
  {card(f'<p style="font-size:26px;color:#c4ccda;margin:0 0 8px">Calculadora gratuita</p><p style="font-size:38px;font-weight:700;color:#D9B579;margin:0">{URL}</p>', "34px 30px", 860)}''', None, 130)


SITE = (URL, 'Recursos → Calculadora da escala 5x2')
SERIE = {}

# ======================================================================= 24/11 (ter)
SERIE['24-11'] = dict(
  feed=('calculadora-5x2-lancamento', [
    capa("NOVO NO SITE DA FORTÍS", ["CALCULADORA DA", "ESCALA 5x2"], "Gratuita. Em poucos minutos você sabe <b>quantas pessoas a sua loja vai precisar</b> em 16 de dezembro."),
    slide("VOCÊ INFORMA", ["3 COISAS"], [("Horário da loja", "Cada dia da semana, inclusive sábado e domingo."), ("Equipe por função", "Vendas, caixa, depósito, entrega."), ("Salário e tributação", "Simples Nacional ou Lucro Presumido/Real.")]),
    slide("ELA MOSTRA", ["A RESPOSTA"], [("Quantas pessoas", "Hoje, com 42 horas e com 40 horas."), ("Quanto custa cada saída", "Hora extra, contratação ou a combinação mais barata."), ("A escala da semana pronta", "Quem trabalha e quem folga em cada dia.")], ini=4),
    fim(["FAÇA A SUA", "SIMULAÇÃO"], [SITE, ("Seus dados ficam com você", "O cálculo roda no seu celular, nada é enviado.")], 'Quer ajuda para montar a escala? <b>Chame no direct.</b>')],
    'Lançamos no site da Fortís a calculadora da escala 5x2, gratuita para lojas de material de construção.\n\nVocê informa o horário da loja, a equipe por função e os salários. Ela mostra quantas pessoas a loja vai precisar com 42 horas (16/12/2026) e com 40 horas (16/12/2027), quanto custa cada saída e a escala da semana pronta.\n\nAcesse: fortismatcon.com.br/ferramentas\n\nQuer ajuda para montar a escala? Chame no direct.'),
  story=('calculadora-5x2-lancamento', chamada("NOVO NO SITE", ["QUANTAS PESSOAS", "SUA LOJA VAI PRECISAR?"], "A jornada de 42 horas começa em <b>16 de dezembro</b>. Simule a sua equipe agora.", 92)),
)

# ======================================================================= 27/11 (sex)
SERIE['27-11'] = dict(
  feed=('escala-5x2-sabado', [
    capa("ESCALA 5x2 · O PONTO CEGO", ["O SÁBADO", "VIROU O PROBLEMA"], "Hoje todo mundo trabalha 6 dias. <b>Com 5, alguém precisa folgar durante a semana</b> para cobrir o sábado.", 108),
    slide("POR QUE A CONTA NÃO FECHA", ["DIAS, NÃO", "SÓ HORAS"], [("5 dias por pessoa", "A loja abre 6: um dia fica para outra pessoa cobrir."), ("Quem cobre o sábado", "Folga num dia da semana, e alguém cobre essa folga."), ("Caixa e balcão", "São os primeiros setores a ficar descobertos.")], 92),
    conta("EXEMPLO · LOJA PEQUENA", ["A CONTA DA", "CALCULADORA"], "Turnos 7h–17h e 8h–18h com 2 h de almoço, sábado 7h–11h. <b>Sem hora extra:</b>",
      [("Equipe hoje", "8 pessoas"), ("Precisa hoje, na 6x1", "8 pessoas"), ("Precisa com 42 h, na 5x2", "11 pessoas")], (2,),
      'A diferença está no <b>desenho da semana.</b>', 84),
    fim(["SIMULE A", "SUA LOJA"], [SITE, ("Escala pronta", "Quem trabalha e quem folga, dia a dia.")], 'Quer ajuda para montar? <b>Chame no direct.</b>')],
    'Escala 5x2 na loja de material de construção: o sábado virou o problema.\n\nCom 5 dias de trabalho por pessoa e a loja aberta 6, alguém precisa folgar durante a semana para cobrir o sábado. No exemplo da loja pequena, com turnos das 7h às 17h e das 8h às 18h e sábado de manhã, a equipe de 8 pessoas que fecha a semana hoje passa a precisar de 11.\n\nSimule a sua loja na calculadora gratuita: fortismatcon.com.br/ferramentas\n\nExemplo ilustrativo. Cada loja deve validar a escala com o seu contador.'),
  story=('escala-5x2-sabado', chamada("ESCALA 5x2", ["QUEM VAI FOLGAR", "NO SÁBADO?"], "Com 5 dias por pessoa, <b>o sábado precisa sair da folga de alguém.</b> A calculadora monta a escala.", 100)),
)

# ======================================================================= 02/12 (qua)
SERIE['02-12'] = dict(
  feed=('escala-5x2-extra-ou-contratar', conta("A CONTA DA LOJA", ["HORA EXTRA", "OU CONTRATAR?"], "Loja pequena, 8 pessoas, Simples Nacional, <b>a partir de 16/12/2026:</b>",
      [("Pessoas necessárias", "11 (hoje 8)"), ("Só hora extra", "não fecha"), ("Contratar 3 pessoas", "R$ 7.676/mês")], (2,),
      f'Calcule a da sua loja:<br><b>{URL}</b>', 88, 27),
    'Escala 5x2: pagar hora extra ou contratar?\n\nNo exemplo da loja pequena (8 pessoas, Simples Nacional), só com hora extra a conta não fecha: as duas folgas são obrigatórias e ninguém pode cobrir o sábado como sexto dia. A saída é contratar 3 pessoas, por R$ 7.676 por mês com encargos.\n\nA calculadora gratuita compara os três caminhos para a sua loja: fortismatcon.com.br/ferramentas\n\nExemplo ilustrativo, com encargos estimados. Confirme os números com o seu contador.'),
  story=('escala-5x2-extra-ou-contratar', chamada("A CONTA DA LOJA", ["HORA EXTRA", "OU CONTRATAR?"], "Na 5x2, <b>hora extra não cobre o sábado:</b> as duas folgas são obrigatórias.", 94)),
)

# ======================================================================= 08/12 (ter)
SERIE['08-12'] = dict(
  feed=('escala-5x2-hora-mais-cara', conta("A CONTA DA LOJA", ["A MESMA HORA", "FICOU MAIS CARA"], "Salário de <b>R$ 3.000</b>: o salário não pode cair, mas o divisor da hora muda.",
      [("Até 15/12/2026 (÷ 220)", "R$ 13,64"), ("A partir de 16/12/2026 (÷ 210)", "R$ 14,29"), ("A partir de 16/12/2027 (÷ 200)", "R$ 15,00"), ("Hora extra 50% em 2026", "R$ 21,43")], (1,),
      f'Veja o impacto na sua folha:<br><b>{URL}</b>', 88, 27, selo=False, fonte=FONTE_DEC),
    'Escala 5x2: a mesma hora ficou mais cara.\n\nO salário não pode ser reduzido, mas o divisor do salário-hora cai de 220 para 210 em 16/12/2026 e para 200 em 16/12/2027. Num salário de R$ 3.000, a hora passa de R$ 13,64 para R$ 14,29 e depois para R$ 15,00, e a hora extra acompanha.\n\nVeja o impacto na folha da sua loja na calculadora gratuita: fortismatcon.com.br/ferramentas'),
  story=('escala-5x2-hora-mais-cara', chamada("ESCALA 5x2", ["SUA FOLHA", "FICOU MAIS CARA"], "A mesma hora custa <b>4,8% a mais</b> a partir de 16/12 e <b>10% a mais</b> em 2027.", 94)),
)

# ======================================================================= 14/12 (seg)
SERIE['14-12'] = dict(
  feed=('escala-5x2-faltam-2-dias', unico("ESCALA 5x2 · QUARTA, 16/12", ["FALTAM", "2 DIAS"], "Quarta-feira a loja já trabalha com <b>42 horas e duas folgas por semana.</b> Três decisões que não podem ficar para depois:",
      [("Quantas pessoas por função", "Inclusive no sábado e no caixa."), ("Hora extra, contratação ou as duas", "A combinação mais barata para a sua loja."), ("A escala de cada pessoa", "Com as duas folgas, avisada à equipe.")],
      f'Ainda não simulou?<br><b>{URL}</b>', 110),
    'Faltam 2 dias para a escala 5x2. Na quarta-feira, 16/12/2026, a jornada máxima passa a 42 horas, com duas folgas remuneradas por semana.\n\nTrês decisões que não podem ficar para depois: quantas pessoas cada função precisa, como cobrir a diferença (hora extra, contratação ou as duas) e a escala de cada pessoa.\n\nAinda não simulou? Calculadora gratuita: fortismatcon.com.br/ferramentas\n\nQuer ajuda para fechar a escala? Chame no direct.'),
  story=('escala-5x2-faltam-2-dias', chamada("QUARTA, 16 DE DEZEMBRO", ["FALTAM", "2 DIAS"], "Sua escala já está pronta? <b>Simule em poucos minutos.</b>", 96)),
)


def montar():
    itens, meta = [], []
    for d, c in SERIE.items():
        pasta = os.path.join(G.RAIZ, 'posts', '2026-' + d[3:], 'dia-' + d)
        nome, arte, leg = c['feed']
        if isinstance(arte, list):
            arqs = [f'1330-{nome}-{i + 1}' for i in range(len(arte))]
            for a, h in zip(arqs, arte): itens.append((pasta, a, h, (W, H)))
        else:
            arqs = [f'1330-{nome}']; itens.append((pasta, arqs[0], arte, (W, H)))
        meta.append(dict(dia=d, hora='1330', tipo='POST', arquivos=[os.path.relpath(os.path.join(pasta, a + '.jpg'), G.RAIZ) for a in arqs], legenda=leg + '\n\n' + HT, titulo=nome))
        nome, arte = c['story']
        a = f'story-0900-{nome}'; itens.append((pasta, a, arte, (SW, SH)))
        meta.append(dict(dia=d, hora='0900', tipo='STORY', arquivos=[os.path.relpath(os.path.join(pasta, a + '.jpg'), G.RAIZ)], titulo=nome))
    return itens, meta


if __name__ == '__main__':
    itens, meta = montar()
    por_pasta = {}
    for p, n, h, wh in itens: por_pasta.setdefault(p, []).append((n, h, wh))
    for p, lst in por_pasta.items():
        print('==', os.path.basename(p)); asyncio.run(renderizar(lst, p))
    json.dump(meta, open(os.path.join(G.RAIZ, 'gerador', 'semanas', 'serie-calculadora-5x2.json'), 'w'), ensure_ascii=False, indent=1)
