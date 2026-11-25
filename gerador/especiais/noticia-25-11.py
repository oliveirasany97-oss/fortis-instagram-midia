"""Story 12:00 de 25/11/2026 — notícia do mercado: confiança do consumidor de novembro (FGV/Ibre), menor nível desde agosto de 2022."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: CONFIANÇA DO CONSUMIDOR NOVEMBRO (FGV) =================
def story_icc():
    tab = tabela([("Confiança do consumidor", "83,5 pts"), ("Finanças da família hoje", "69,2 pts"),
                  ("Intenção de comprar bens duráveis", "77,0 pts")],
                 30, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · FGV", 26)}
  {titulo(["CLIENTE MAIS", "CAUTELOSO NO BOLSO"], 80, 900)}
  {sub("A confiança do consumidor caiu 1,2 ponto em novembro e chegou ao menor nível desde agosto de 2022. Só a intenção de comprar bens duráveis subiu (+1,5).", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Com o bolso apertado, <b>parcelar e dividir a obra em etapas</b> ajuda a fechar a venda.</p>''',
      'Fonte: FGV/Ibre, Sondagem do Consumidor nov/2026 · via BM&C News', 80)


itens = [("story-1200-confianca-consumidor-novembro", story_icc(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-25-11')
asyncio.run(renderizar(itens, saida))
