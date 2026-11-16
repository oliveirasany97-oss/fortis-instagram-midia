"""Reel 36 (16/11/2026, 21:30) — As 2 vendas que a loja perde sem ver: ligação sem resposta e orçamento sem retorno.
~60 s, narração com a voz clonada do Sâny (eleven_v4), clipes em movimento dos reels 30 e 31 (Kling 2.6 Pro).
Uso: python3 montar_reel36_mov.py voz.mp3 c0,c1,...   (11 cortes = início de cada cena em ORDEM; a última é o encerramento, também em movimento)"""
import os, sys
from kitpers import ReelP, AQUI, sh, dur, W, H
from montar_reel23 import k, t1, s
from reelkit import base, G
A_LOGO = G.A + '/logo.png'

CLIPES = os.path.join(AQUI, 'clipes')

ORDEM = ['30H', '30A', '30B', '30C', '31H', '31A', '31B', '31C', '31R', '30R', '23R']
OV = {
    '30H': t1('SUA LOJA PERDE<br>VENDA TODO DIA', 250, 100, 'metal') + s('e você <b>nem vê</b>', 500),
    '30A': k('VENDA PERDIDA Nº 1') + t1('O TELEFONE TOCA<br>E NINGUÉM ATENDE', 290, 82, 'metal'),
    '30B': k('ORGANIZE') + t1('QUEM ATENDE EM<br>CADA HORÁRIO', 290, 84, 'metal'),
    '30C': k('PERDEU A LIGAÇÃO?') + t1('RETORNE EM<br>ATÉ 1 HORA', 290, 100, 'metal'),
    '31H': k('VENDA PERDIDA Nº 2') + t1('O ORÇAMENTO<br>QUE NÃO FECHOU', 290, 88, 'metal'),
    '31A': k('LIGUE E PERGUNTE') + t1('PREÇO? PRAZO?<br>FALTOU PRODUTO?', 290, 80, 'metal'),
    '31B': k('ANOTE') + t1('O MOTIVO DE CADA<br>ORÇAMENTO PERDIDO', 290, 72, 'metal'),
    '31C': k('NO FIM DO MÊS') + t1('O MOTIVO MAIS<br>COMUM SE RESOLVE<br>PRIMEIRO', 290, 72, 'metal'),
    '31R': k('TODA SEMANA') + t1('ALINHE COM<br>A EQUIPE', 290, 100, 'metal'),
    '30R': t1('QUEM ATENDE PRIMEIRO', 270, 64) + t1('VENDE<br>MAIS', 360, 120, 'metal'),
    # encerramento também em movimento (sem card parado)
    '23R': f'<img src="{A_LOGO}" style="position:absolute;left:50%;transform:translateX(-50%);top:200px;width:140px">'
           + t1('ROTINA QUE<br>NÃO PERDE VENDA', 420, 88, 'metal')
           + '<div class="t" style="top:690px;font-size:56px"><span style="border:3px solid #D9B579;border-radius:22px;padding:10px 34px;background:rgba(10,22,42,.85);color:#D9B579">CHAME NO DIRECT</span></div>'
           + '<div class="s" style="top:810px;font-size:38px"><span style="background:rgba(10,22,42,.88);border-radius:14px;padding:6px 22px;color:#fff">@fortismatcon.oficial</span></div>',
}


def cta_direct():
    return base('''<div class="big metal" style="top:600px;font-size:100px;line-height:1.05">ROTINA QUE<br>NÃO PERDE VENDA</div>
   <div class="txt" style="top:860px;font-size:40px">A Fortís organiza a rotina<br>da sua loja de material de construção.</div>
   <div class="top" style="top:1040px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:62px;color:var(--gold);letter-spacing:1px">CHAME NO DIRECT</span></span></div>
   <div class="top" style="top:1215px;font-weight:500;color:#c4ccda;font-size:34px">@fortismatcon.oficial</div>
   <div class="rodape" style="top:1330px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''', logo_top=230)


class ReelMov(ReelP):
    def clipe(s_, k_, arq, d):
        c = os.path.join(CLIPES, arq)
        fator = max(1.0, d / max(dur(c) - 0.05, 0.1))
        sh(f"ffmpeg -y -i {c} -i {os.path.join(s_.C, k_ + '.png')} -filter_complex "
           f"\"[0:v]setpts={fator:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[bg];"
           f"[bg][1:v]overlay=0:0,fade=in:st=0:d=0.25,format=yuv420p\" -an -t {d} -c:v libx264 -crf 17 {os.path.join(s_.C, k_ + '.mp4')}")


if __name__ == '__main__':
    voz = sys.argv[1]
    ks = ORDEM
    R = os.path.join(AQUI, 'reel36')
    r = ReelMov(R, OV, {})
    if len(sys.argv) < 3:
        print('cards renderizados em', r.C); sys.exit()
    cortes = [float(x) for x in sys.argv[2].split(',')]
    DUR = {kk: (cortes[i + 1] if i + 1 < len(cortes) else dur(voz) + 1.4) - cortes[i] for i, kk in enumerate(ks)}
    for kk in ORDEM:
        r.clipe(kk, f'v{kk}.mp4', DUR[kk])
    saida = os.path.join(R, 'reel36-duas-vendas-perdidas-voz-sany.mp4')
    print(DUR, r.final(ks, saida, voz))
