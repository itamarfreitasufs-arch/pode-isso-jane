#!/bin/bash
# Monta app/ com os perfis indicados (padrão: os sete publicados) e roda a bateria p48 e os exemplos próprios.
cd "$(dirname "$0")/.." || exit 1
mkdir -p exec
bash testes/montar_app.sh "$1" || exit 1
f=congelado/perguntas_p48.json
node testes/rodar.cjs app $f exec/p48.json && python3 -I congelado/pontuar.py $f exec/p48.json | grep -v '^OK'
node testes/proprias.cjs app
