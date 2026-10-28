# Ferramentas de reels — FORTÍS FLOW (dados fictícios)

Grava telas reais do FORTÍS FLOW numa loja de demonstração fictícia ("Loja Modelo Materiais"),
com Firebase simulado em memória (pasta `mock/`). Nada acessa o Firebase real.

**O arquivo do FLOW (`flow.html`) NÃO fica neste repositório** (código proprietário, repo público).
Para usar: pedir ao Sâny o HTML do FLOW, salvar como `flow.html` nesta pasta (fora do git) e gerar
`flow_demo.html` inserindo antes do último `</script>` do módulo principal:
`window.__RH={RH_SIT,rhSituacoesDoCargo,rhRequisitosDoCargo,rhStatusRequisito};`

Fontes: extrair `fonts/*.tgz` em `fonts/` (`tar xzf ... ` → pasta `package` → renomear para
`fontsource-sora`, `fontsource-bebas-neue`, `fontsource-jetbrains-mono`).

Fluxo de um reel: `python3 gravar_reelN.py` (screencast CDP 1080x2338, marcas de tempo) →
`python3 montar_reelN.py` (versão sem som) → com o MP3 do ElevenLabs:
`python3 montar_reelN.py voz.mp3 0,c1,c2,...` (cortes = início de cada cena, achados com
`ffmpeg -af silencedetect=noise=-38dB:d=0.2`). `reelkit.py` tem cards, `cta_diag()` e a montagem;
`montar_reel5.py` tem a função `gancho()` (abertura com tela em movimento).

A partir do reel 7: `rec.py` (classe `Rec`) concentra a gravação (toques, digitação, rolagem, marcas) e
`reelkit.gancho()` faz a abertura em movimento. Cada reel tem `gravar_reelN.py` + `montar_reelN.py`
(sem argumentos = versão sem som; com `voz.mp3 cortes` = narrada). O `demo.py` também semeia o módulo
Avarias e filas de compra mais cheias (marcas D e E).

## Narração (regras fixas, aprovadas pelo Sâny em 28/10/2026)
- ElevenLabs, voz **Roger (premade, CwhRBWXzGAHq8TQ4Fs17)**, modelo **eleven_v4** (o Multilingual v2 deixa a voz lenta e tremida).
- O nome da empresa é oxítono: **for-TÍS**. No texto da narração, escrever **"Fortíss"** (grafia aprovada pelo ouvido do Sâny; "Fortís" sai FÓR-tis).
- Reels com movimento real: cenas do personagem animadas no ElevenLabs (Kling 2.6 Pro, 9:16, 5 s, sem áudio) e montadas com `personagem/montar_reel23_mov.py` como modelo.
