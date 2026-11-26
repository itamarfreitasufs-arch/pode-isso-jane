# Avaliação

Resultados da versão 5.21 nesta distribuição, obtidos com `bash testes/todas.sh`, `bash testes/pos.sh` e `bash testes/tudo.sh` em 26/11/2026. A 5.21 mudou só a aparência; os números são os mesmos da 5.20. Os arquivos de `app/` gerados por `testes/montar_app.sh` são byte a byte iguais aos do pacote da versão publicada em https://iaeduca.online/jane/.

## Método

Cada bateria foi escrita e congelada (hash SHA-256 em `congelado/`) **antes** da correção que pretendia testar e foi rodada na versão anterior e na nova. As perguntas imitam a escrita real: erros de digitação, abreviações, frases incompletas, perguntas fora do tema e absurdas. Parte delas foi escrita por um testador independente (outro modelo de IA) que não via o código.

## Resultados

| Bateria | O que testa | Antes da correção | 5.21 |
|---|---|---|---|
| w38 | aliciamento em outras palavras | 15/38 (5.19) | 38/38 |
| v56 | violência, fome e negligência em casa | 18/56 (5.18) | 56/56 |
| u54 | aliciamento, violência doméstica, família | 19/54 (5.17) | 54/54 |
| s49 | ameaça, assédio, perfis novos | 11/49 (5.16) | 49/49 |
| z77 | autolesão, risco à vida, bullying | 28/77 (5.15) | 77/77 |
| y58 | sofrimento, montagem, apresentação | 16/58 (5.14) | 58/58 |
| x44 | achados do teste da 5.13 | 10/44 (5.13) | 40/44 * |
| gf110 | gestor e família | 73/110 (fichas antigas) | 110/110 |
| t95 | professores | 74/95 (fichas antigas) | 95/95 |
| e60 | fundamental e médio | 46/60 (fichas antigas) | 60/60 |
| g60 | graduação | | 60/60 |
| c44 | caixa de busca | | 43/44 |
| r24 | reteste da 5.8 | 11/24 (5.8) | 23/24 |
| p48 | pós-graduação | | 46/48 * |
| q42, n46, a62, h16 | baterias antigas, todos os perfis | | 42/42, 46/46, 61/62, 16/16 |
| linha de apoio | respostas sem saída trazem CVV e Disque 100 | | 10/10 |
| coerência interna | cada ficha achada pela própria pergunta-exemplo | | 349/352 |
| tela (`ui.cjs`, `ui2.cjs`) | percurso, Voltar/Avançar, caixa, celular de 360 px | | sem falha |

\* Mudança de gabarito por decisão: x44 G01 a G04 pediam o aviso "em breve" para gestor e família, que hoje têm perfil próprio; p48 P45 e P46 pediam o aviso de perfil inativo e hoje apontam os perfis de professor e de responsável.

## Falhas conhecidas

- c44 C10 e r24 R07: critérios estreitos (a ficha certa aparece, com outras palavras).
- a62 A11: a pergunta é "oi"; não há ficha a oferecer.
- Coerência interna: três perguntas-exemplo sobre montagem de imagem (`eb_montagem`, `fa_montagem`, `fa_filho_fez`) caem antes no acolhimento quando digitadas. As fichas abrem pelo menu.

## Limites

- Acerto em frases inéditas sobre situações de risco ficou entre 58% e 68% nos retestes independentes. Por isso toda resposta sem correspondência traz a linha de apoio.
- Os textos das fichas e de acolhimento estão em revisão por estudantes de pós-graduação. O teste com estudantes e colegas em celulares variados está pendente.
- Os testes de tela rodaram no Chromium. Firefox e Safari não foram testados nesta distribuição.
