# Como usar, reconstruir e testar

Requisitos: Python 3.10 ou mais recente e Node.js 18 ou mais recente. Os testes de tela usam também o Playwright com o Chromium.

## Rodar o app

```bash
cd app
python3 -m http.server 8000
# abra http://localhost:8000/
```

O app tenta falar com `conta.php` para contar visitas. Sem o contador, essa chamada falha em silêncio e nada aparece no rodapé; o resto funciona igual.

## Reconstruir o banco e a pasta `app/`

```bash
bash testes/montar_app.sh
```

O script copia a tela de `dist/` para `app/` e gera `app/norma.sqlite` a partir de `construir/norma_origem.sqlite` e das fichas em `construir/`. Os sete perfis publicados são o padrão. Para publicar outro conjunto, passe a lista:

```bash
bash testes/montar_app.sh pos,graduacao
```

Perfis disponíveis: `basico`, `graduacao`, `pos`, `profBasico`, `profSuperior`, `gestorEscolar`, `responsavel`. Os perfis antigos (`iniciais`, `finais`, `medio`, `docente*`, `orientador`, `gestor`, `familia`) continuam no gerador só para as baterias antigas.

Para mudar uma ficha, edite o arquivo `construir/sit_*.py` do perfil, reconstrua e rode as baterias. O gerador recusa referências quebradas (artigo, conceito ou ficha inexistente).

## Baterias

| Comando | O que roda |
|---|---|
| `bash testes/todas.sh` | Baterias congeladas sobre `app/`: caixa de busca (c44, r24, x44, y58, z77, s49, u54, v56, w38), linha de apoio e formulário (t95, e60, g60, gf110). |
| `bash testes/pos.sh` | Monta `app/` e roda p48 e a coerência interna (cada ficha encontrada pela própria pergunta-exemplo). |
| `bash testes/tudo.sh` | Reconstrói `dist/norma.sqlite` com todos os perfis, antigos inclusive, e roda q42, n46, a62, h16 e a coerência interna. |

Os resultados vão para `exec/` (fora do controle de versão). Cada linha `FALHA` mostra o critério que não foi atendido. As falhas esperadas estão em [AVALIACAO.md](AVALIACAO.md).

### Testes de tela

```bash
cd app && python3 -m http.server 8765 &
node testes/ui.cjs /tmp/telas pos   # percurso, Voltar/Avançar, caixa, largura no celular
node testes/ui2.cjs                 # acolhimento na caixa, endereços inválidos
```

## Como uma bateria é congelada

1. Antes de mexer no código, escreve-se a bateria (os geradores estão em `congelado/geradores/`) com a pergunta, o perfil e o critério de acerto.
2. Grava-se o hash em `congelado/SHA256_<nome>.txt`.
3. Roda-se a bateria na versão antiga, para registrar o ponto de partida, e depois da correção.
4. A pergunta não muda depois do congelamento; se o critério mudar por decisão, isso fica registrado no CHANGELOG.

Para conferir os hashes: `python3 congelado/conferir.py`. Os registros foram gravados em formatos diferentes ao longo do trabalho; o script lê todos. Cinco linhas antigas apontam para arquivos que não fazem parte desta distribuição (as fontes da versão 3 do app e o `criterios.md` da bateria a62) e aparecem como AUSENTE.

## Contador de visitas (opcional)

`servidor/` tem `conta.php` e `painel.php`, que só funcionam num servidor com PHP. Veja [servidor/LEIAME.md](servidor/LEIAME.md).
