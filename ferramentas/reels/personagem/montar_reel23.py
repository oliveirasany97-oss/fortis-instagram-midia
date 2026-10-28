"""Reel 23 — Troca e devolução com regra (personagem). Uso: python3 montar_reel23.py [voz.mp3 cortes]
Fecha com o card do diagnóstico SEM CUSTO pelo link da bio."""
import os, sys
from kitpers import ReelP, duracoes, AQUI
from reelkit import base


def cta_bio(lista):
    return base(f'''<div class="big metal" style="top:600px;font-size:96px;line-height:1.05">DIAGNÓSTICO<br>SEM CUSTO</div>
   <div class="txt" style="top:840px;font-size:40px">{lista}</div>
   <div class="big branco" style="top:1010px;font-size:64px;line-height:1.1">QUER ISSO NA<br>SUA LOJA?</div>
   <div class="top" style="top:1200px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:58px;color:var(--gold);letter-spacing:1px">LINK NA BIO</span></span></div>
   <div class="rodape" style="top:1420px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''', logo_top=230)


def k(t): return f'<div class="k" style="top:230px">{t}</div>'
def t1(t, top=290, fs=84, cls='branco'): return f'<div class="t {cls}" style="top:{top}px;font-size:{fs}px">{t}</div>'
def s(t, top=540): return f'<div class="s" style="top:{top}px">{t}</div>'


OV = {
    'H': t1('DEVOLUÇÃO<br>SEM REGRA<br>É PREJUÍZO', 250, 96, 'metal'),
    'A': k('SOBROU DA OBRA') + t1('CAIXA ABERTA.<br>PEÇA RISCADA.', 290, 90, 'metal'),
    'B': k('ANTES DE ACEITAR') + t1('PRAZO<br>NOTA FISCAL<br>PRODUTO CONFERIDO', 290, 74, 'metal'),
    'C': k('NO MESMO DIA') + t1('REGISTRE O MOTIVO<br>E VOLTE AO ESTOQUE', 290, 70, 'metal') + s('danificado vai para a <b>avaria</b>,<br>não para a prateleira', 520),
    'R': t1('DEVOLUÇÃO COM REGRA', 270, 70) + t1('PROTEGE O CAIXA<br>E MANTÉM O CLIENTE', 360, 84, 'metal'),
}
IMGS = ['r13A', 'r20A', 'r13B', 'r18C', 'r13H']

R = os.path.join(AQUI, 'reel23')
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz, DUR = duracoes(ks, {'H': 3.6, 'A': 5.0, 'B': 5.4, 'C': 6.6, 'R': 4.4, 'cta': 4.6}, sys.argv)
r = ReelP(R, OV, {'cta': cta_bio('Gestão · vendas · equipe<br>compras · FORTÍS FLOW')})
for i, kk in enumerate(['H', 'A', 'B', 'C', 'R']):
    r.foto(kk, IMGS[i] + '.png', DUR[kk], zoom_in=(i % 2 == 0), pan=(1 if i == 1 else 0))
r.card('cta', DUR['cta'])
saida = os.path.join(R, 'reel23-troca-e-devolucao' + ('-narrado' if voz else '') + '.mp4')
print(DUR, r.final(ks, saida, voz))
