"""Story 12:00 de 22/11/2026 — notícia do mercado: vendas de cimento em outubro (SNIC)."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: CIMENTO OUTUBRO (SNIC) =================
def story_cimento():
    tab = tabela([("Outubro de 2026", "5,9 mi t"), ("Contra outubro de 2025", "−6,1%"),
                  ("Acumulado jan–out", "+0,1%")], 32, destaque=(1,))
    return story(f'''{kicker("MERCADO MATCON · SNIC", 26)}
  {titulo(["VENDA DE CIMENTO", "CAI 6,1%"], 88, 900)}
  {sub("Menos dias úteis e muita chuva seguraram as obras em outubro.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Com chuva, cimento fica mais tempo no depósito: <b>saco sobre estrado e o mais antigo sai primeiro.</b></p>''',
      'Fonte: SNIC, vendas internas out/2026 · via CNN Brasil, Revista Construa e Brasil 61', 80)


itens = [("story-1200-cimento-outubro", story_cimento(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-22-11')
asyncio.run(renderizar(itens, saida))
