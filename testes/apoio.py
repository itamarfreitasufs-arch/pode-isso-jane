# uso: python3 -I testes/apoio.py <perguntas.json> <saida.json>
# Confere a linha de apoio (CVV e Disque 100): presente onde a pergunta pede apoio=true, ausente onde pede false.
import json, sys
Q = {x['id']: x for x in json.load(open(sys.argv[1], encoding='utf8'))}
R = json.load(open(sys.argv[2], encoding='utf8'))
ok = n = 0
for x in R:
    c = Q[x['id']]
    if 'apoio' not in c: continue
    n += 1
    certo = bool(x.get('apoio')) == c['apoio']
    ok += certo
    if not certo: print('FALHA', x['id'], 'apoio esperado:', c['apoio'])
print('apoio', ok, '/', n)
