"""Reels 24 a 29 (personagem, voz do Sâny). Uso: python3 montar_24a29.py N
Cortes já calculados pelas pausas da narração (silencedetect). Fecha com o card
do diagnóstico SEM CUSTO pelo link da bio."""
import os, sys
from kitpers import ReelP, duracoes, AQUI
from montar_reel23 import cta_bio, k, t1, s

REELS = {
 24: ('caixa-conferido', '0,3.05,6.77,11.25,18.44,25.0', {
   'H': t1('O CAIXA DA<br>SUA LOJA FECHA<br>CERTO TODO DIA?', 250, 86, 'metal'),
   'A': k('DIFERENÇA SEM EXPLICAÇÃO') + t1('DEZ REAIS HOJE.<br>MIL NO ANO.', 290, 92, 'metal'),
   'B': k('FECHAMENTO EM 3 PASSOS') + t1('1. CONTAR<br>O DINHEIRO', 290, 104, 'metal'),
   'C': k('2. CONFERIR · 3. ANOTAR') + t1('CARTÃO E PIX<br>COM O SISTEMA', 290, 84, 'metal') + s('diferença anotada com o <b>nome de quem fechou</b>', 520),
   'R': t1('DIFERENÇA ANOTADA NO DIA', 270, 62) + t1('SE<br>EXPLICA', 360, 116, 'metal') + s('descoberta no fim do mês vira <b>prejuízo</b>', 640),
 }),
 25: ('entrega-pequena', '0,2.69,7.12,10.28,15.7,23.42', {
   'H': t1('O CAMINHÃO<br>SAIU POR UM<br>SACO DE CIMENTO?', 250, 86, 'metal'),
   'A': k('A CONTA NÃO FECHA') + t1('COMBUSTÍVEL<br>MOTORISTA<br>TEMPO', 290, 90, 'metal') + s('custam mais do que a <b>venda</b>', 640),
   'B': k('REGRA CLARA') + t1('VALOR MÍNIMO<br>PARA ENTREGA<br>SEM TAXA', 290, 88, 'metal'),
   'C': k('ABAIXO DELE') + t1('COBRE UMA TAXA<br>OU JUNTE COM A<br>MESMA REGIÃO', 290, 74, 'metal'),
   'R': t1('ENTREGA SEM REGRA', 270, 70) + t1('É LUCRO<br>SAINDO PELA<br>PORTA', 360, 104, 'metal'),
 }),
 26: ('limite-de-credito', '0,4.32,7.82,15.69,19.14,24.77', {
   'H': t1('QUEM DECIDE<br>QUANTO O CLIENTE<br>COMPRA A PRAZO?', 250, 80, 'metal'),
   'A': k('SE É O VENDEDOR, NA HORA') + t1('O RISCO<br>É DA LOJA', 290, 110, 'metal'),
   'B': k('ANTES DA PRIMEIRA VENDA') + t1('UM LIMITE<br>PARA CADA<br>CLIENTE', 290, 96, 'metal') + s('comece baixo e aumente conforme <b>paga em dia</b>', 660),
   'C': k('PASSOU DO LIMITE') + t1('SÓ COM<br>AUTORIZAÇÃO<br>DO GERENTE', 290, 92, 'metal'),
   'R': t1('VENDER A PRAZO É BOM', 270, 66) + t1('SEM LIMITE<br>É EMPRÉSTIMO<br>SEM GARANTIA', 360, 88, 'metal'),
 }),
 27: ('reclamacao-24h', '0,2.15,7.75,12.23,18.85,23.27', {
   'H': t1('CLIENTE<br>RECLAMOU.<br>E AGORA?', 250, 104, 'metal'),
   'A': k('RECLAMAÇÃO ESQUECIDA') + t1('CLIENTE PERDIDO<br>E FALATÓRIO<br>NA CIDADE', 290, 82, 'metal'),
   'B': k('ANOTE TODA RECLAMAÇÃO') + t1('NOME<br>TELEFONE<br>PROBLEMA', 290, 104, 'metal'),
   'C': k('DEFINA QUEM RESOLVE') + t1('RESPOSTA<br>EM ATÉ 24H', 290, 112, 'metal') + s('mesmo que seja só o <b>próximo passo</b>', 560),
   'R': t1('BEM ATENDIDO DEPOIS DO PROBLEMA', 270, 50) + t1('VOLTA<br>MAIS FIEL', 350, 116, 'metal'),
 }),
 28: ('conferencia-de-saida', '0,2.31,6.56,9.35,16.15,19.35', {
   'H': t1('QUEM CONFERE<br>O QUE SAI DO<br>SEU DEPÓSITO?', 250, 88, 'metal'),
   'A': k('MERCADORIA A MAIS NO CAMINHÃO') + t1('PREJUÍZO<br>QUE NINGUÉM<br>PERCEBE', 290, 96, 'metal'),
   'B': k('TODA SAÍDA PRECISA DE') + t1('TRÊS<br>COISAS', 290, 130, 'metal'),
   'C': k('ANTES DE CARREGAR') + t1('PEDIDO IMPRESSO<br>CONFERÊNCIA ITEM A ITEM<br>DUAS ASSINATURAS', 290, 60, 'metal') + s('quem <b>separou</b> e quem <b>conferiu</b>', 560),
   'R': t1('LEVA DOIS MINUTOS', 270, 70) + t1('PROTEGE O<br>SEU ESTOQUE', 360, 104, 'metal'),
 }),
 29: ('pro-labore', '0,2.72,5.4,10.97,18.11,22.8', {
   'H': t1('VOCÊ TIRA O<br>DINHEIRO DA LOJA<br>QUANDO PRECISA?', 250, 82, 'metal'),
   'A': k('ENTÃO VOCÊ NÃO SABE') + t1('SE A LOJA<br>DÁ LUCRO', 290, 110, 'metal'),
   'B': k('DEFINA UM PRÓ-LABORE') + t1('VALOR FIXO<br>POR MÊS<br>PARA VOCÊ', 290, 96, 'metal') + s('como se fosse <b>salário</b>', 660),
   'C': k('CONTA DA LOJA ≠ CONTA PESSOAL') + t1('O QUE SOBRA<br>É O RESULTADO<br>REAL DA LOJA', 290, 84, 'metal'),
   'R': t1('MISTURAR AS CONTAS', 270, 70) + t1('É TRABALHAR<br>SEM SABER<br>QUANTO GANHA', 360, 92, 'metal'),
 }),
}

n = int(sys.argv[1]); slug, cortes, OV = REELS[n]
R = os.path.join(AQUI, f'reel{n}')
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz_arq = os.path.join(AQUI, f'reel{n}-voz-sany.mp3')
voz, DUR = duracoes(ks, {}, ['', voz_arq, cortes])
r = ReelP(R, OV, {'cta': cta_bio('Gestão · vendas · equipe<br>compras · FORTÍS FLOW')})
IMGS = [f'r{n}H', f'r{n}A', f'r{n}B', f'r{n}C', f'r{n}H']
for i, kk in enumerate(['H', 'A', 'B', 'C', 'R']):
    r.foto(kk, IMGS[i] + '.png', DUR[kk], zoom_in=(i % 2 == 0), pan=(1 if i in (1, 3) else 0))
r.card('cta', DUR['cta'])
saida = os.path.join(R, f'reel{n}-{slug}-voz-sany.mp4')
print(n, {k: round(v, 2) for k, v in DUR.items()}, r.final(ks, saida, voz))
