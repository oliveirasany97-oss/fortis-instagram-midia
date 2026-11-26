"""Story 12:00 de 26/11/2026 — notícia do mercado: INCC-M de novembro (FGV), materiais e equipamentos puxam a alta."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: INCC-M NOVEMBRO (FGV) =================
def story_inccm():
    tab = tabela([("INCC-M de novembro", "0,30%"), ("Materiais e equipamentos", "0,39%"),
                  ("Mão de obra", "0,22%")],
                 30, destaque=(1,))
    return story(f'''{kicker("MERCADO MATCON · FGV", 26)}
  {titulo(["MATERIAL SOBE", "MAIS QUE A OBRA"], 80, 900)}
  {sub("O custo da obra desacelerou (era 0,35% em outubro) e soma 6,77% em 12 meses. Material segue acima do índice.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Material subindo mais que o resto: <b>confira o custo de reposição antes de dar desconto.</b></p>''',
      'Fonte: FGV/Ibre, INCC-M nov/2026 · via Gazeta Mercantil e Revista Construa', 80)


itens = [("story-1200-inccm-novembro", story_inccm(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-26-11')
asyncio.run(renderizar(itens, saida))
