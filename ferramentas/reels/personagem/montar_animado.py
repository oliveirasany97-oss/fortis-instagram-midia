"""Vídeo animado: um dia na loja que funciona com o FORTÍS FLOW (personagem 3D + clipes Kling).
Uso: python3 montar_animado.py voz.mp3 cortes
Clipes em ../animado/clipes/a1.mp4 ... a6.mp4; saída em ../animado/."""
import os, sys
from kitpers import ReelP, AQUI, W, H, sh, dur
from montar_reel23 import k, t1, s
from reelkit import base

ANIM = os.path.join(AQUI, '..', 'animado')
CLIPES = os.path.join(ANIM, 'clipes')


class ReelMov(ReelP):
    def clipe(s, k, arq, d):
        """Clipe em movimento recortado para 9:16; esticado com leveza se for mais curto que a cena."""
        c = os.path.join(CLIPES, arq)
        fator = max(1.0, d / max(dur(c) - 0.05, 0.1))
        sh(f"ffmpeg -y -i {c} -i {os.path.join(s.C, k + '.png')} -filter_complex "
           f"\"[0:v]setpts={fator:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[bg];"
           f"[bg][1:v]overlay=0:0,fade=in:st=0:d=0.25,format=yuv420p\" -an -t {d} -c:v libx264 -crf 17 {os.path.join(s.C, k + '.mp4')}")

# Selo por cima do balão de notificação do clipe 3 (o vídeo gerou letras sem sentido ali).
BADGE = ('<div style="position:absolute;left:372px;top:1312px;width:290px;height:128px;border-radius:64px;'
         'background:#0E1F39;border:3px solid #D9B579;box-shadow:0 0 28px rgba(217,181,121,.55);'
         'display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.05">'
         '<div style="font-family:Osw;font-weight:700;font-size:40px;color:#D9B579;letter-spacing:1px">NOVA FALTA</div>'
         '<div style="font-weight:600;font-size:22px;color:#eef2f8;margin-top:6px">registrada no balcão</div></div>')

OV = {
    'a1': k('7H DA MANHÃ') + t1('UM DIA NA LOJA<br>QUE FUNCIONA', 290, 92, 'metal'),
    'a2': k('NO BALCÃO') + t1('FALTOU?<br>REGISTRA NO FLOW', 290, 88, 'metal'),
    'a3': k('NAS COMPRAS') + t1('A FILA CHEGA<br>SOZINHA', 290, 92, 'metal') + s('o que faltou, <b>na hora</b>', 520) + BADGE,
    'a4': k('NA EXPEDIÇÃO') + t1('ROTA PRONTA.<br>NADA NO CADERNO.', 290, 82, 'metal'),
    'a5': k('NO ESCRITÓRIO') + t1('O DONO<br>VÊ TUDO', 290, 100, 'metal') + s('compras · entregas · <b>metas</b>', 520),
    'a6': t1('EQUIPE QUE SE COMUNICA', 270, 66) + t1('VENDE<br>MAIS', 350, 120, 'metal'),
}

CTA = base('''<div class="big metal" style="top:560px;font-size:112px;line-height:1.05">FORTÍS<br>FLOW</div>
   <div class="txt" style="top:840px;font-size:40px">Balcão · compras · entrega · gestão<br>a equipe inteira na mesma página</div>
   <div class="big branco" style="top:1020px;font-size:72px;line-height:1.1">DIAGNÓSTICO<br>SEM CUSTO</div>
   <div class="top" style="top:1220px"><span class="preco"><span style="font-family:Osw;font-weight:700;font-size:58px;color:var(--gold);letter-spacing:1px">LINK NA BIO</span></span></div>
   <div class="rodape" style="top:1420px;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>''', logo_top=230)

if __name__ == '__main__':
    ks = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'cta']
    voz = sys.argv[1]
    cortes = [float(x) for x in sys.argv[2].split(',')]
    DUR = {kk: (cortes[i + 1] if i + 1 < len(cortes) else dur(voz) + 1.4) - cortes[i] for i, kk in enumerate(ks)}
    r = ReelMov(os.path.join(ANIM, 'montagem'), OV, {'cta': CTA})
    for kk in ks[:-1]:
        r.clipe(kk, kk + '.mp4', DUR[kk])
    r.card('cta', DUR['cta'])
    saida = os.path.join(ANIM, 'fortis-flow-um-dia-na-loja-animado.mp4')
    print(DUR, r.final(ks, saida, voz))
