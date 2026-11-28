"""Story 12:00 de 28/11/2026 — notícia do mercado: Termômetro Anamaco de outubro, menos lojas vendendo mais."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *


# ================= STORY 12:00 — MERCADO: TERMÔMETRO ANAMACO OUTUBRO =================
def story_termometro():
    tab = tabela([("Lojas que venderam mais", "37%"), ("Lojas estáveis", "37%"),
                  ("Lojas que venderam menos", "26%")],
                 30, destaque=(0,))
    return story(f'''{kicker("MERCADO MATCON · ANAMACO", 26)}
  {titulo(["MENOS LOJAS", "VENDENDO MAIS"], 80, 900)}
  {sub("Em outubro, a fatia de lojas com vendas em alta caiu de 43% (setembro) para 37%. Em outubro de 2025 eram 42%.", 28, 90)}
  {card(tab)}
  <p class="cta k" style="font-size:32px;padding:0 80px">Mês mais morno: <b>retome os orçamentos parados antes de baixar preço.</b></p>''',
      'Fonte: Termômetro Anamaco, out/2026 · anamaco.com.br', 80)


itens = [("story-1200-termometro-anamaco-outubro", story_termometro(), (SW, SH))]
saida = os.path.join(G.RAIZ, 'posts', '2026-11', 'dia-28-11')
asyncio.run(renderizar(itens, saida))
