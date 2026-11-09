"""Reels 30 a 35 com movimento real (clipes Kling 2.6 Pro) e narração na voz clonada do Sâny.
Uso: python3 montar_30a35_mov.py <n> voz.mp3 c0,c1,...   (cortes = início de cada cena na ordem de ORDEM[n])
Clipes em personagem/clipes/v<n><cena>.mp4. Mesmo padrão visual do montar_reel23_mov.py."""
import os, sys
from kitpers import ReelP, AQUI, sh, dur, W, H
from montar_reel23 import cta_bio, k, t1, s

CLIPES = os.path.join(AQUI, 'clipes')
LISTA = 'Gestão · vendas · equipe<br>compras · FORTÍS FLOW'

REELS = {
 '30': ('ligacao-perdida', ['H', 'A', 'B', 'C', 'R'], {
    'H': t1('O TELEFONE TOCA<br>E NINGUÉM<br>ATENDE?', 250, 96, 'metal'),
    'A': k('LIGAÇÃO PERDIDA') + t1('É CLIENTE NO<br>CONCORRENTE', 290, 88, 'metal'),
    'B': k('ORGANIZE') + t1('QUEM ATENDE EM<br>CADA HORÁRIO', 290, 80, 'metal') + s('perdeu a ligação? <b>retorno em até 1 hora</b>', 520),
    'C': k('NUNCA') + t1('DEIXE O CLIENTE<br>ESPERANDO NA LINHA', 290, 74, 'metal'),
    'R': t1('QUEM ATENDE PRIMEIRO', 270, 64) + t1('VENDE<br>PRIMEIRO', 360, 110, 'metal')}),
 '31': ('orcamento-perdido', ['H', 'R', 'A', 'B', 'C'], {
    'H': t1('POR QUE O<br>ORÇAMENTO<br>NÃO FECHOU?', 250, 96, 'metal'),
    'R': k('SEM SABER O MOTIVO') + t1('O ERRO SE<br>REPETE', 290, 100, 'metal'),
    'A': k('LIGUE E PERGUNTE') + t1('PREÇO? PRAZO?<br>FALTOU PRODUTO?', 290, 80, 'metal'),
    'B': k('ANOTE') + t1('O MOTIVO DE CADA<br>ORÇAMENTO PERDIDO', 290, 70, 'metal'),
    'C': k('NO FIM DO MÊS') + t1('O MOTIVO MAIS<br>COMUM É O PRIMEIRO<br>A RESOLVER', 290, 70, 'metal') + s('orçamento perdido <b>também ensina</b>', 580)}),
}


class ReelMov(ReelP):
    def clipe(s_, k_, arq, d):
        c = os.path.join(CLIPES, arq)
        fator = max(1.0, d / max(dur(c) - 0.05, 0.1))
        sh(f"ffmpeg -y -i {c} -i {os.path.join(s_.C, k_ + '.png')} -filter_complex "
           f"\"[0:v]setpts={fator:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[bg];"
           f"[bg][1:v]overlay=0:0,fade=in:st=0:d=0.25,format=yuv420p\" -an -t {d} -c:v libx264 -crf 17 {os.path.join(s_.C, k_ + '.mp4')}")


if __name__ == '__main__':
    n, voz, cortes = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(',')]
    nome, ordem, ov = REELS[n]
    ks = ordem + ['cta']
    DUR = {kk: (cortes[i + 1] if i + 1 < len(cortes) else dur(voz) + 1.4) - cortes[i] for i, kk in enumerate(ks)}
    R = os.path.join(AQUI, f'reel{n}')
    r = ReelMov(R, ov, {'cta': cta_bio(LISTA)})
    for kk in ordem:
        r.clipe(kk, f'v{n}{kk}.mp4', DUR[kk])
    r.card('cta', DUR['cta'])
    saida = os.path.join(R, f'reel{n}-{nome}-voz-sany.mp4')
    print(DUR, r.final(ks, saida, voz))
