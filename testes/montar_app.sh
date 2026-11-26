#!/bin/bash
# Monta a pasta app/ (versão publicada, sete perfis) a partir de dist/ e do gerador do banco.
# Uso: bash testes/montar_app.sh [perfis separados por vírgula]
cd "$(dirname "$0")/.." || exit 1
PERFIS=${1:-pos,graduacao,basico,profBasico,profSuperior,gestorEscolar,responsavel}
rm -rf app && mkdir app && cp dist/index.html dist/*.js dist/estilo.css dist/sql-wasm.wasm dist/sql-js-LICENSE.txt dist/.htaccess app/
python3 -I construir/build.py construir/norma_origem.sqlite app/norma.sqlite "$PERFIS" | head -2
