#!/bin/bash
# Reconstrói o banco e roda todas as baterias. Uso: bash testes/tudo.sh
cd "$(dirname "$0")/.." || exit 1
mkdir -p exec
python3 -I construir/build.py construir/norma_origem.sqlite dist/norma.sqlite | head -1 || exit 1
for par in "q42:congelado/perguntas_q42.json" "n46:congelado/perguntas_n46.json" "a62:testes/perguntas_62.json" "h16:testes/perguntas_h16.json"; do
 n=${par%%:*}; f=${par##*:}
 node testes/rodar.cjs dist $f exec/$n.json && echo "$n: $(python3 -I congelado/pontuar.py $f exec/$n.json | tail -1) | falhas: $(python3 -I congelado/pontuar.py $f exec/$n.json | grep FALHA | cut -d' ' -f2 | tr '\n' ' ')"
done
node testes/rodar.cjs dist testes/perguntas_20.json exec/r20.json; node testes/rodar.cjs dist testes/perguntas_34.json exec/p34.json
node testes/proprias.cjs dist
