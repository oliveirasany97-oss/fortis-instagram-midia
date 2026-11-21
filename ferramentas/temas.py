"""Índice de temas já usados no Instagram (feed, stories, reels), para não repetir.

Uso: python3 ferramentas/temas.py [palavra ...]
Sem argumentos: lista todos os títulos/temas. Com palavras: mostra só as linhas que contêm alguma delas
(sem diferenciar maiúsculas e acentos). Rode ANTES de escolher os temas do dia.
"""
import glob, json, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(t):
    return unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()


def semanas():
    for f in sorted(glob.glob(os.path.join(RAIZ, 'gerador/semanas/*.json'))):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ('titulo', 'tema', 'title') and isinstance(v, (str, list)):
                        yield ' / '.join(v) if isinstance(v, list) else v
                    yield from walk(v)
            elif isinstance(o, list):
                for x in o:
                    yield from walk(x)
        try:
            for t in walk(json.load(open(f))):
                yield os.path.basename(f), t
        except Exception:
            pass


def especiais():
    for f in sorted(glob.glob(os.path.join(RAIZ, 'gerador/especiais/*.py'))):
        s = open(f).read()
        for m in re.finditer(r'(?:titulo|tit)\(\[([^\]]+)\]', s):
            yield os.path.basename(f), ' / '.join(re.findall(r'"([^"]+)"', m.group(1)))
        for m in re.finditer(r'#\s*=+\s*(.+?)\s*=+', s):
            yield os.path.basename(f), m.group(1)


def reels():
    for f in sorted(glob.glob(os.path.join(RAIZ, 'posts/*/reels/*.md'))):
        for linha in open(f):
            if linha.startswith('## '):
                yield os.path.basename(f), linha[3:].strip()
    vistos = set()
    for f in sorted(glob.glob(os.path.join(RAIZ, 'posts/*/reels/*.mp4'))):
        n = re.sub(r'-(narrado|voz-sany|final|movimento|gancho-novo)$', '', os.path.basename(f)[:-4])
        if n not in vistos:
            vistos.add(n); yield 'reel', n.replace('-', ' ')


def todos():
    yield from semanas(); yield from especiais(); yield from reels()


if __name__ == '__main__':
    filtros = [norm(a) for a in sys.argv[1:]]
    for origem, t in todos():
        if not filtros or any(x in norm(t) for x in filtros):
            print(f'{origem:28} | {t}')
