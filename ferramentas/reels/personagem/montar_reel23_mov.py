"""Reel 23 com movimento real: clipes de imagem-para-vídeo (ElevenLabs/Kling) no lugar do zoom nas fotos.
Uso: python3 montar_reel23_mov.py voz.mp3 cortes   (clipes em reel23/clipes/v23H.mp4 ... v23R.mp4)"""
import os, sys
from kitpers import ReelP, duracoes, AQUI, sh, dur, W, H
import montar_reel23 as base23

OV, cta_bio = base23.OV, base23.cta_bio
R = os.path.join(AQUI, 'reel23')
CLIPES = os.path.join(R, 'clipes')
ks = ['H', 'A', 'B', 'C', 'R', 'cta']
voz, DUR = duracoes(ks, None, sys.argv)


class ReelMov(ReelP):
    def clipe(s, k, arq, d):
        """Clipe em movimento, recortado para 9:16 e esticado com leveza se for mais curto que a cena."""
        c = os.path.join(CLIPES, arq)
        fator = max(1.0, d / max(dur(c) - 0.05, 0.1))
        sh(f"ffmpeg -y -i {c} -i {os.path.join(s.C, k + '.png')} -filter_complex "
           f"\"[0:v]setpts={fator:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30[bg];"
           f"[bg][1:v]overlay=0:0,fade=in:st=0:d=0.25,format=yuv420p\" -an -t {d} -c:v libx264 -crf 17 {os.path.join(s.C, k + '.mp4')}")


r = ReelMov(R, OV, {'cta': cta_bio('Gestão · vendas · equipe<br>compras · FORTÍS FLOW')})
for kk in ['H', 'A', 'B', 'C', 'R']:
    r.clipe(kk, f'v23{kk}.mp4', DUR[kk])
r.card('cta', DUR['cta'])
saida = os.path.join(R, 'reel23-troca-e-devolucao-movimento.mp4')
print(DUR, r.final(ks, saida, voz))
