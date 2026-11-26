# uso: python3 -I comparar.py <perguntas.json> <antes.json> <depois.json> [vereditos glob]
import json,sys,glob
Q={x['id']:x for x in json.load(open(sys.argv[1],encoding='utf8'))}
A={x['id']:x for x in json.load(open(sys.argv[2],encoding='utf8'))}
D={x['id']:x for x in json.load(open(sys.argv[3],encoding='utf8'))}
V={}
for f in glob.glob(sys.argv[4]) if len(sys.argv)>4 else []:
    for v in json.load(open(f,encoding='utf8')): V[v['id']]=v
for i,q in Q.items():
    a,d=A[i],D[i]; v=V.get(i,{}).get('veredito','?')[:1]
    ka=a['tipo']+':'+','.join(a['ids']); kd=(d['tipo'] or '')+':'+','.join(d['ids'])
    if d['erro']: print(i,'ERRO',d['erro'][:200])
    print(f"{i} {q['classe'][:4]} {v} {'=' if ka==kd else '≠'} {ka}  →  {kd}")
