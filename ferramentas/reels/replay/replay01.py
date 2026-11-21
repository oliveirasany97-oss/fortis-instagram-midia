"""REPLAY DA LOJA #1 (21/11/2026, 18:00) — Pilha de cimento que desaba.
Clipes Kling 2.6 Pro 9:16 (fluxo ElevenLabs "Replay da Loja #1 · Pilha de cimento (21/11)") em r01/v1..v4.mp4, voz do Sâny em r01/voz.mp3.
Uso: python3 replay01.py
Fontes: NR-11, itens 11.3.2 (não obstruir portas, extintores e saídas) e 11.3.3 (material empilhado a pelo menos 0,50 m das estruturas laterais).
"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from replaykit import Replay, tag, hud, G

R = os.path.join(AQUI, 'r01')
V = lambda n: os.path.join(R, f'v{n}.mp4')

FRASES = [
    'REPLAY DA LOJA.',
    'OLHA ESSA **PILHA DE CIMENTO**.',
    'ALTA, TORTA, **ENCOSTADA NA PAREDE** E NO **CHÃO MOLHADO**.',
    'E **CAIU**.',
    'AGORA, O **JEITO CERTO**.',
    'SACO NO **ESTRADO**, NUNCA DIRETO NO CHÃO.',
    'PILHA **BAIXA E TRAVADA**, COM OS SACOS CRUZADOS.',
    'PELO MENOS **50 CM DA PAREDE**, COMO PEDE A NR-11.',
    'NADA NA FRENTE DO **EXTINTOR** NEM DA **SAÍDA**.',
    'PILHA CERTA **NÃO CAI EM CIMA DE NINGUÉM**.',
    'QUER REVISAR O DEPÓSITO DA SUA LOJA?',
    'CHAMA A FORTÍS NO DIRECT.',
]
# início de cada frase (silencedetect -38dB d=0.28, mais o corte em 19,25 s achado com d=0.2)
INICIOS = [0.0, 1.54, 3.62, 8.62, 9.78, 11.99, 15.88, 19.25, 24.60, 27.87, 31.00, 33.17]

SECOES = [
    {'clipe': V(1), 'frases': [0, 1, 2], 'replay': True,
     'tags': {2: [tag('✕ ENCOSTADA NA PAREDE', 470, 'ruim'), tag('✕ CHÃO MOLHADO', 570, 'ruim')]}},
    {'clipe': V(2), 'frases': [3, 4], 'replay': True,
     'hud': hud('QUEM É MAIS RÁPIDO?', [('PILHA CAINDO', 'CHEGOU!', 96, '#e0484f'), ('VOCÊ CORRENDO', '', 22, '#4fc3f7')])},
    {'clipe': V(3), 'frases': [5, 6],
     'tags': {5: [tag('✓ ESTRADO', 470, 'ok')], 6: [tag('✓ PILHA BAIXA E TRAVADA', 470, 'ok')]}},
    # cena 4: recorte abaixo da placa de saída gerada com letras sem sentido
    {'clipe': V(4), 'frases': [7, 8, 9], 'crop': (640, 1138, 100, 782),
     'tags': {7: [tag('✓ 50 CM DA PAREDE', 470, 'ok')], 8: [tag('✓ EXTINTOR E SAÍDA LIVRES', 470, 'ok')],
              9: [tag('✓ DEPÓSITO SEGURO', 470, 'ok')]},
     'fonte': 'Fonte: NR-11, itens 11.3.2 e 11.3.3'},
]

CTA = f'''<img class="logo" src="{G.A}/logo.png" style="top:300px;width:230px">
 <div class="kicker" style="position:absolute;top:640px;left:0;right:0;text-align:center;font-weight:700;letter-spacing:8px;color:var(--gold);font-size:28px">REPLAY DA LOJA</div>
 <div class="titulo" style="position:absolute;top:710px;left:60px;right:60px;text-align:center;font-family:Osw;font-weight:700;font-size:104px;line-height:1.04"><div class="branco">PILHA CERTA</div><div class="metal">NÃO CAI</div></div>
 <div style="position:absolute;top:980px;left:110px;right:110px;text-align:center;font-size:40px;line-height:1.4;color:#e9edf5">Quer revisar o depósito da sua loja?</div>
 <div style="position:absolute;top:1100px;left:0;right:0;text-align:center"><span style="display:inline-block;border:3px solid #D9B579;border-radius:22px;padding:14px 40px;background:rgba(10,22,42,.85);font-family:Osw;font-weight:700;font-size:60px;color:#D9B579">CHAME NO DIRECT</span></div>
 <div style="position:absolute;top:1260px;left:0;right:0;text-align:center;font-weight:500;color:#c4ccda;font-size:34px">@fortismatcon.oficial</div>
 <div class="rodape" style="position:absolute;top:1400px;left:0;right:0;font-size:24px">FORTÍS SOLUÇÕES MATCON</div>'''

if __name__ == '__main__':
    r = Replay(R, os.path.join(R, 'voz.mp3'), FRASES, SECOES, CTA, inicios=INICIOS, cta_desde=10)
    saida = os.path.join(AQUI, '..', '..', '..', 'posts', '2026-11', 'reels', 'replay01-pilha-de-cimento-voz-sany.mp4')
    print('duração', r.montar(saida))
