"""Reels 12 a 15 (personagem). Uso: python3 montar_12a15.py N [voz.mp3 cortes]"""
import os, sys
from kitpers import ReelP, duracoes, cta_diag, AQUI

def k(t): return f'<div class="k" style="top:230px">{t}</div>'
def t1(t, top=290, fs=84, cls='branco'): return f'<div class="t {cls}" style="top:{top}px;font-size:{fs}px">{t}</div>'

REELS = {
 12: ('desconto-com-troca', {
   'H': t1('SEU VENDEDOR DÁ<br>DESCONTO DE GRAÇA?', 260, 96, 'metal'),
   'A': k('TODO DESCONTO PRECISA DE UMA TROCA') + t1('PAGAMENTO<br>À VISTA', 290, 110, 'metal') + '<div class="s" style="top:540px">no lugar do cartão parcelado</div>',
   'B': k('TODO DESCONTO PRECISA DE UMA TROCA') + t1('COMPRA<br>MAIOR', 290, 110, 'metal') + '<div class="s" style="top:540px">a obra inteira, <b>não só o cimento</b></div>',
   'C': k('TODO DESCONTO PRECISA DE UMA TROCA') + t1('RETIRADA<br>NA LOJA', 290, 110, 'metal') + '<div class="s" style="top:540px">sem custo de entrega</div>',
   'R': t1('DESCONTO COM TROCA', 270, 74) + t1('É NEGOCIAÇÃO', 360, 110, 'metal') + '<div class="s" style="top:520px">Sem contrapartida, é <b>margem jogada fora</b>.</div>',
 }, ['r12H', 'r12A', 'r12B', 'r12C', 'r12H']),
 13: ('quem-fala-o-numero-primeiro', {
   'H': t1('O CLIENTE PEDIU<br>DESCONTO.', 250, 96, 'metal') + '<div class="s" style="top:470px">O que você responde primeiro?</div>',
   'A': k('NÃO DÊ O NÚMERO DE CARA') + t1('PERGUNTE:', 290, 74) + t1('"QUANTO O SENHOR<br>TEM EM MENTE?"', 380, 86, 'metal'),
   'B': k('O QUE ACONTECE NA PRÁTICA') + t1('O CLIENTE PEDE<br>MENOS DO QUE VOCÊ<br>IA OFERECER', 290, 86, 'metal'),
   'C': k('ANTES DE MEXER NO PREÇO') + t1('OFEREÇA<br>CONDIÇÃO', 290, 110, 'metal') + '<div class="s" style="top:540px">prazo · entrega · um item a mais</div>',
   'R': t1('QUEM FALA O NÚMERO<br>PRIMEIRO', 260, 80) + t1('PERDE MARGEM', 450, 110, 'metal'),
 }, ['r13H', 'r13A', 'r13B', 'r13C', 'r13H']),
 14: ('frete-gratis-nao-e-gratis', {
   'H': t1('VOCÊ DÁ<br>FRETE GRÁTIS?', 250, 110, 'metal') + '<div class="s" style="top:500px">para fechar a venda</div>',
   'A': k('CADA ENTREGA TEM CUSTO') + t1('CAMINHÃO · COMBUSTÍVEL<br>MOTORISTA · AJUDANTE', 300, 66, 'metal'),
   'B': k('ENTREGA DE R$ 80 EM VENDA DE R$ 500') + t1('= 16%', 290, 150, 'metal') + '<div class="s" style="top:500px">do valor da venda <b>vai embora</b></div>',
   'C': k('A REGRA') + t1('FRETE GRÁTIS SÓ<br>ACIMA DE UM MÍNIMO', 290, 80, 'metal') + '<div class="s" style="top:500px">abaixo dele, <b>cobre a entrega</b></div>',
   'R': t1('O FRETE QUE VOCÊ<br>DÁ DE PRESENTE', 260, 80) + t1('SAI DO SEU LUCRO', 450, 100, 'metal'),
 }, ['r14H', 'r14A', 'r14B', 'r14C', 'r14H']),
 15: ('como-a-fortis-trabalha', {
   'H': t1('COMO A FORTÍS<br>TRABALHA NA<br>SUA LOJA?', 250, 96, 'metal'),
   'A': k('1 · VISITA') + t1('A GENTE VAI<br>ATÉ VOCÊ', 290, 100, 'metal') + '<div class="s" style="top:540px">do balcão ao estoque</div>',
   'B': k('2 · DIAGNÓSTICO') + t1('ONDE A LOJA PERDE<br>DINHEIRO E TEMPO', 290, 84, 'metal'),
   'C': k('3 · PLANO E EXECUÇÃO') + t1('AÇÕES PRÁTICAS<br>ATÉ O RESULTADO', 290, 84, 'metal'),
   'R': t1('SEM RECEITA PRONTA', 270, 80) + '<div class="s" style="top:390px">Cada loja tem <b>a sua realidade</b>.</div>',
 }, ['r15H', 'r15A', 'r15B', 'r15C', 'r15H']),
}

n = int(sys.argv[1]); slug, OV, IMGS = REELS[n]
R = os.path.join(AQUI, f'reel{n}')
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz, DUR = duracoes(ks, {'H': 3.6, 'A': 5.2, 'B': 4.6, 'C': 4.0, 'R': 5.0, 'cta': 4.4}, sys.argv[1:])
r = ReelP(R, OV, {'cta': cta_diag('Gestão · negociação · equipe<br>compras · FORTÍS FLOW')})
for i, kk in enumerate(['H', 'A', 'B', 'C', 'R']):
    r.foto(kk, IMGS[i] + '.png', DUR[kk], zoom_in=(i % 2 == 0), pan=(1 if i == 1 else 0))
r.card('cta', DUR['cta'])
saida = os.path.join(R, f'reel{n}-{slug}' + ('-narrado' if voz else '') + '.mp4')
print(n, DUR, r.final(ks, saida, voz))
