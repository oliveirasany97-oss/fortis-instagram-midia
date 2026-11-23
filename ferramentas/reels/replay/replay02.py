"""REPLAY DA LOJA #2 (23/11/2026, 18:30) — Lata de tinta pesada no alto da prateleira.
Clipes Kling 2.5 Turbo 9:16 (fluxo ElevenLabs "Replay da Loja #2 · Lata de tinta no alto (23/11)") em r02/v1..v2.mp4, voz do Sâny em r02/voz.mp3.
O clipe 1 aparece duas vezes: na velocidade normal e no replay ampliado. O clipe 2 também, com dois enquadramentos.
Uso: python3 replay02.py
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from replaykit import Replay, tag, hud, G

R = os.path.join(AQUI, 'r02')
V = lambda n: os.path.join(R, f'v{n}.mp4')

FRASES = [
    'REPLAY DA LOJA.',
    'OLHA ESSA **PRATELEIRA DE TINTA**.',
    'LATA DE **18 LITROS** LÁ NO ALTO, **PASSANDO DA BORDA**.',
    'E **CAIU**. BEM DO LADO DO **CLIENTE**.',
    'AGORA, O **JEITO CERTO**.',
    '**PESO EMBAIXO**, LEVE EM CIMA.',
    'LATA GRANDE **NA BASE** OU NO **ESTRADO**.',
    'NADA **PASSANDO DA BORDA** DA PRATELEIRA.',
    'O QUE É PESADO, SEMPRE **AO ALCANCE DA MÃO**.',
    'PRATELEIRA CERTA **NÃO DERRUBA NADA EM NINGUÉM**.',
    'QUER REVISAR A EXPOSIÇÃO DA SUA LOJA?',
    'CHAMA A FORTÍS NO DIRECT.',
]
# silencedetect -38dB d=0.28, mais o corte em 19,02 s achado com -36dB d=0.15
INICIOS = [0.0, 1.56, 3.67, 7.69, 10.78, 12.86, 15.28, 19.02, 21.56, 24.40, 27.62, 29.78]

SECOES = [
    {'clipe': V(1), 'frases': [0, 1, 2], 'replay': True,
     'tags': {2: [tag('✕ LATA PESADA NO ALTO', 470, 'ruim'), tag('✕ PASSANDO DA BORDA', 570, 'ruim')]}},
    # replay ampliado na queda
    {'clipe': V(1), 'frases': [3], 'replay': True, 'crop': (720, 1280, 180, 120),
     'hud': hud('QUEM É MAIS RÁPIDO?', [('LATA CAINDO', 'CHEGOU!', 96, '#e0484f'), ('CLIENTE DESVIANDO', '', 30, '#4fc3f7')])},
    {'clipe': V(2), 'frases': [4, 5, 6],
     'tags': {5: [tag('✓ PESO EMBAIXO, LEVE EM CIMA', 470, 'ok')], 6: [tag('✓ LATA GRANDE NA BASE', 470, 'ok')]}},
    {'clipe': V(2), 'frases': [7, 8, 9], 'crop': (760, 1351, 160, 540),
     'tags': {7: [tag('✓ NADA PASSANDO DA BORDA', 470, 'ok')], 8: [tag('✓ PESADO NA ALTURA DA MÃO', 470, 'ok')],
              9: [tag('✓ CORREDOR SEGURO', 470, 'ok')]}},
]

CTA = f'''<img class="logo" src="{G.A}/logo.png" style="top:300px;width:230px">
 <div class="kicker" style="position:absolute;top:640px;left:0;right:0;text-align:center;font-weight:700;letter-spacing:8px;color:var(--gold);font-size:28px">REPLAY DA LOJA</div>
 <div class="titulo" style="position:absolute;top:710px;left:60px;right:60px;text-align:center;font-family:Osw;font-weight:700;font-size:104px;line-height:1.04"><div class="branco">PESO EMBAIXO,</div><div class="metal">LEVE EM CIMA</div></div>
 <div style="position:absolute;top:980px;left:110px;right:110px;text-align:center;font-size:40px;line-height:1.4;color:#e9edf5">Quer revisar a exposição da sua loja?</div>
 <div style="position:absolute;top:1100px;left:0;right:0;text-align:center"><span style="display:inline-block;border:3px solid #D9B579;border-radius:22px;padding:14px 40px;background:rgba(10,22,42,.85);font-family:Osw;font-weight:700;font-size:60px;color:#D9B579">CHAME NO DIRECT</span></div>
 <div style="position:absolute;top:1260px;left:0;right:0;text-align:center;font-weight:500;color:#c4ccda;font-size:34px">@fortismatcon.oficial</div>
 <div class="rodape" style="position:absolute;top:1400px;left:0;right:0;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>'''

if __name__ == '__main__':
    r = Replay(R, os.path.join(R, 'voz.mp3'), FRASES, SECOES, CTA, inicios=INICIOS, cta_desde=10)
    saida = os.path.join(AQUI, '..', '..', '..', 'posts', '2026-11', 'reels', 'replay02-lata-de-tinta-voz-sany.mp4')
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    print('duração', r.montar(saida))
