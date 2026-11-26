#!/bin/bash
# Roda as baterias congeladas sobre app/ (versão publicada). Uso: bash testes/todas.sh
cd "$(dirname "$0")/.." || exit 1
mkdir -p exec
for b in c44 r24 x44 y58 z77 s49 u54 v56 w38; do f=congelado/perguntas_$b.json; node testes/caixa.cjs app $f exec/$b.json >/dev/null; echo "== $b (caixa)"; python3 -I congelado/pontuar.py $f exec/$b.json | grep -v '^OK' | cut -c1-230; done
python3 -I testes/apoio.py congelado/perguntas_z77.json exec/z77.json
for b in t95 e60 g60 gf110; do f=congelado/perguntas_$b.json; node testes/rodar.cjs app $f exec/$b.json >/dev/null; echo "== $b (formulário)"; python3 -I congelado/pontuar.py $f exec/$b.json | grep -v '^OK' | cut -c1-230; done
