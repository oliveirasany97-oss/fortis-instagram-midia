"""Story 12:00 de 23/11/2026 — notícia do mercado: INCC-10 de novembro (FGV)."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: INCC-10 NOVEMBRO (FGV) =================
def story_incc10():
    tab = tabela([("INCC-10 de outubro", "0,28%"), ("INCC-10 de novembro", "0,33%")],
                 32, destaque=(1,))
    return story(f'''{kicker("MERCADO MATCON · FGV", 26)}
  {titulo(["CUSTO DA OBRA", "ACELERA EM NOVEMBRO"], 80, 900)}
  {sub("A prévia da FGV mostra o custo da construção subindo mais rápido que no mês anterior.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Custo subindo é hora de <b>rever a tabela de preço e cotar antes de repor o estoque.</b></p>''',
      'Fonte: FGV/IBRE, INCC-10 nov/2026 · via Times Brasil e A Crítica (Estadão Conteúdo)', 80)


itens = [("story-1200-incc10-novembro", story_incc10(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-23-11')
asyncio.run(renderizar(itens, saida))
