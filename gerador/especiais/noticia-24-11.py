"""Story 12:00 de 24/11/2026 — notícia do mercado: CUB paulista de outubro (SindusCon-SP/FGV), insumos que mais subiram em 12 meses."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: CUB-SP OUTUBRO (SINDUSCON-SP) =================
def story_cub():
    tab = tabela([("Fio de cobre 2,5 mm²", "+13,8%"), ("Tubo PVC esgoto 150 mm", "+12,2%"),
                  ("Cimento saco 50 kg", "+11,3%")],
                 32, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · SINDUSCON-SP", 26)}
  {titulo(["FIO, TUBO E CIMENTO", "LIDERAM AS ALTAS"], 80, 900)}
  {sub("Alta em 12 meses até outubro, no estado de São Paulo. Os materiais, na média, subiram 6,2%.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Itens que sobem mais que a média pedem <b>margem revisada a cada nova compra.</b></p>''',
      'Fonte: SindusCon-SP/FGV, CUB-SP out/2026 · via SindusCon-SP e ALEC', 80)


itens = [("story-1200-cub-sp-outubro", story_cub(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-24-11')
asyncio.run(renderizar(itens, saida))
