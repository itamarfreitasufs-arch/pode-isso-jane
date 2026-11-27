# Pode isso, Jane? — protocolo do app

Protocolo de **Itamar Freitas** (Universidade Federal de Sergipe), versão **5.23 experimental**, de 26 de novembro de 2026. Documento preparado com assistência de IA (Claude na construção; outro modelo, o GPT, como testador independente que não via o código).

Este documento descreve como o Jane foi construído e como pode ser reconstruído, auditado ou melhorado por qualquer pessoa: o que ele faz, de onde vem cada resposta, como foi testado e como é publicado. Os comandos estão em [COMO_USAR.md](COMO_USAR.md) e os números dos testes em [AVALIACAO.md](AVALIACAO.md).

App publicado: https://iaeduca.online/jane/

---

## 1. O que é

O Jane responde a dúvidas práticas sobre o uso de inteligência artificial na escola e na universidade, com base na Resolução CNE/CP nº 1, de 11 de novembro de 2026. A pessoa escolhe o perfil, o assunto e a situação, ou escreve a dúvida, e recebe uma **ficha**: a resposta curta (pode, depende, não pode), o porquê, o que conferir, o que fazer agora e os dispositivos da norma que fundamentam a resposta.

Princípios fixos:

- **Sem IA.** O app é um sistema de regras escrito à mão. Não chama nenhum modelo de linguagem.
- **Toda resposta cita a norma.** Cada ficha aponta artigos, parágrafos, incisos ou verbetes do Glossário; o gerador do banco recusa ficha que aponte dispositivo inexistente.
- **Nada do que a pessoa escreve sai do aparelho.** O banco roda no navegador (SQLite em WebAssembly). O contador de visitas, opcional, grava só o dia, o tipo de uso, o perfil e o código da ficha, sem IP, cookie nem texto.
- **Separar perfis só onde a norma responde diferente.** Se as perguntas de dois públicos são idênticas, eles ficam num perfil só.
- **Tela enxuta.** Sem ajuda redundante, sem créditos de autoria nem quadro teórico dentro do app. O rodapé diz que o Jane não usa inteligência artificial e traz "Realização: IAEduca".
- **Aguentar perguntas absurdas.** Pergunta fora do tema recebe aviso de escopo; pedido para burlar regras recebe recusa; sinal de risco recebe acolhimento antes de qualquer ficha.
- **Não é serviço de atendimento.** Nas situações de risco, o app orienta e indica canais (CVV 188, Disque 100, Ligue 180, SaferNet, 190, Conselho Tutelar).

---

## 2. Base normativa

**Resolução CNE/CP nº 1, de 11 de novembro de 2026**, publicada no DOU de 12/11/2026, edição 213-B, seção 1 Extra B, p. 7. O texto foi dividido em 349 unidades (artigos, parágrafos, incisos, alíneas, os 94 verbetes do Glossário do Anexo I e o quadro de risco do Anexo II), cada uma com localizador e página, e indexado para busca. A origem e o SHA-256 do PDF usado ficam na tabela `fonte` de `construir/norma_origem.sqlite`.

Como a norma entra nas respostas:

- Cada ficha liga-se a um ou mais dispositivos (tabela `situacao_dispositivo`, 1.282 ligações na versão 5.23).
- O Glossário é citado como "Glossário (Anexo I, verbete N)" quando o verbete prescreve (por exemplo, o 34, sobre detectores, e o 87, sobre uso individual).
- Onde a norma deixa margem à instituição, a ficha diz isso e manda conferir a regra local, em vez de inventar a regra.
- Onde a norma não fala do caso (por exemplo, o TCC), a ficha diz que a norma não fala e indica o dispositivo mais próximo.
- A etapa da educação básica só separa as respostas onde a norma separa: o uso com os alunos e o uso pelos alunos (arts. 20, parágrafo único, 21, 22 e 23).

A caixa "Consultar a norma" busca também o texto da resolução por palavra, por "art. N" e por "verbete N".

---

## 3. Desenho do app

### 3.1 Perfis e fichas

Sete perfis ativos na versão 5.23, com 314 fichas no total:

| Perfil | Chave | Fichas |
| --- | --- | --- |
| Estudante · fundamental e médio | `basico` | 47 |
| Estudante · graduação | `graduacao` | 56 |
| Estudante · pós-graduação | `pos` | 49 |
| Professor · fundamental e médio | `profBasico` | 51 |
| Professor · graduação e pós-graduação | `profSuperior` | 53 |
| Gestor escolar | `gestorEscolar` | 55 |
| Pai, mãe ou responsável | `responsavel` | 46 |

(Uma ficha pode servir a mais de um perfil; por isso a soma passa de 314.)

Decisões de recorte, todas do autor: fundamental e médio num perfil só; professor em dois perfis, porque a norma separa a educação básica da superior mas trata a superior em conjunto; as perguntas próprias da orientação de pós-graduação ficaram dentro do perfil do professor do superior, sem perfil de orientador; a graduação deriva parte das fichas da pós (trocando "programa" por "curso" e "orientador" por "professor ou orientador"), com fichas próprias onde o caso é outro.

### 3.2 Percurso

1. **Perfil.** Sem perfil, a caixa de busca não oferece ficha: pede o perfil (a busca no texto da norma continua).
2. **Assunto.** Doze assuntos: Posso usar IA?; Avisar ou declarar o uso; Trabalho feito com IA; Acusação, detector e punição; Nota ou correção por IA; Decisão ou previsão automática; Câmeras, dados e imagens; Professor e IA; Acessibilidade; Revistas e publicações; Gestão e contratos; Sobre a resolução. Cada perfil vê só os assuntos que têm fichas para ele.
3. **Situação.** A lista de perguntas do assunto, escritas como a pessoa falaria.
4. **Ficha.** Resposta, porquê, o que conferir, o que fazer agora e os dispositivos. O endereço da página guarda perfil, assunto e ficha (`#pos/usar/pos_uso`), e os botões Voltar e Avançar do navegador funcionam.

A dúvida escrita vai pela caixa "Consultar a norma". Quando a frase pode caber em mais de uma ficha, o app pergunta "qual destas é a sua situação?" em vez de escolher sozinho; se nenhuma serve, o botão "Nenhuma dessas" limpa as sugestões e leva de volta à lista de assuntos.

### 3.3 Triagem do texto escrito

A ordem de decisão, em `dist/triagem.js`, é:

1. **Normalização e correção:** minúsculas, sem acento, troca de palavra desconhecida pela que soa igual ou difere em uma letra ("teze", "profesor", "detetor").
2. **Portões**, na ordem do banco: risco à vida, autolesão, aliciamento, assédio, violência, imagem íntima e montagem, humilhação, aflição, e as recusas (burla, dano) e encaminhamentos (penal, judicial, trabalhista). Cada portão tem variantes conforme quem escreve: a própria pessoa atingida, quem relata o caso de outro (colega, professor, familiar) ou um adulto. Os portões de risco respondem com o acolhimento e param ali.
3. **Papel e etapa declarados:** "sou diretora", "sou mãe", "tô no 7º ano", "faço residência" apontam o perfil certo.
4. **Escopo:** pergunta sem relação com IA na educação recebe o aviso "isso foge do que este app consulta".
5. **Fichas:** cada ficha tem conceitos que exige, que reforçam e que a excluem (tabela `conceito`, 207 expressões); as mais pontuadas são oferecidas.
6. **Linha de apoio:** toda resposta sem saída (fora do escopo, não ficou claro, sem correspondência com quatro palavras ou mais) traz "Precisa de ajuda agora? CVV 188 (apoio emocional) · Disque 100 (violência ou abuso)". Motivo: nenhuma regra reconhece todas as formas de pedir ajuda.

### 3.4 Arquitetura

- `index.html`, `estilo.css`: tela.
- `motor.js`: carrega o banco no navegador (sql.js) e faz a busca no texto da norma.
- `triagem.js`: função pura que recebe o texto, o perfil e a base e devolve o tipo de resposta, as fichas, o acolhimento e a linha de apoio.
- `app.js`: telas, endereço, histórico do navegador e o contador opcional.
- `norma.sqlite`: texto da norma, busca, perfis, assuntos, fichas, ligações com os dispositivos, conceitos, portões, papéis, complementos e mensagens.
- `construir/`: o gerador. `build.py` lê `norma_origem.sqlite` e as fichas escritas em Python (`sit_*.py` por perfil, `base.py` com vocabulário, portões e mensagens; `sit_v522.py` e `sit_v523.py` trazem os textos reescritos e as fichas novas da 5.22 e da 5.23, aplicados no fim), valida cada referência e grava o banco. Com a lista de perfis ativos, grava só as fichas deles e ajusta as opções do seletor no `index.html`.

Funciona em qualquer servidor de páginas estáticas.

---

## 4. Método de construção (replicável)

1. **Auditoria antes de reconstruir.** O Jane sucede um protótipo anterior, descartado depois de auditoria. A partir daí, cada correção passou pelo ciclo abaixo.
2. **Um perfil por vez.** Para cada perfil: lista do que a norma diz àquele público, assuntos, situações escritas na voz de quem pergunta, fichas com os dispositivos. Cobertura conferida contra as disposições da norma marcadas como relevantes para o perfil.
3. **Bateria antes da correção.** Antes de escrever fichas ou mexer em regra, escreve-se uma bateria de perguntas com perfil e critério de acerto, grava-se o SHA-256 e roda-se a versão antiga, para registrar o ponto de partida (ver seção 5).
4. **Correção pequena e testada.** Cada correção vira um remendo nas fontes; o gerador reconstrói o banco; rodam a bateria nova e todas as antigas. Nenhuma correção sai com regressão não explicada.
5. **Testador independente.** Outra conversa, com outro modelo, testa o site publicado com frases próprias, sem ver o código nem as baterias, e devolve um parecer com achados classificados por gravidade. Os achados viram a bateria congelada da rodada seguinte.
6. **Decisão do autor rodada a rodada.** O autor decide o que corrigir e quando publicar; a autorização vale para uma rodada, não para as seguintes. As rodadas sobre situações de risco foram encerradas na 5.20 por decisão dele: o acerto em frases inéditas ficava entre 58% e 68%, e a linha de apoio cobre o que escapa.
7. **Revisão humana dos textos e teste com alunos.** Os textos das fichas e de acolhimento são revisados por estudantes de pós-graduação do autor; a revisão está em curso. No teste com alunos de graduação (26/11/2026), só 4 de 13 entenderam "não pode" na ficha das entrevistas do TCC; ela e as fichas irmãs da pós e do professor foram reescritas com veredito "Não" na primeira linha (5.22). O parecer completo desse teste gerou a 5.23: doze fichas da graduação passaram a abrir com "Sim" ou "Não" claros, cinco fichas novas, ajustes na busca e o botão "Nenhuma dessas".
8. **Divisão de trabalho.** Conteúdo (fichas, acolhimento) e desenho com o modelo principal; tarefas mecânicas (publicar, rodar baterias prontas, contador, empacotar) com modelo menor.

---

## 5. Testes

### 5.1 Baterias congeladas

Cada bateria é um JSON com `id`, `perfil`, `q` (a pergunta, como a pessoa escreveria, com erros e abreviações), `classe` (ficha, livre, fora, recusa, cuidado) e os critérios `deve` e `nao` (expressões que a resposta precisa ter ou não pode ter). O pontuador `congelado/pontuar.py` confere cada resposta. Classes têm critérios próprios: FORA exige aviso de escopo e nenhuma ficha; RECUSA exige recusa; CUIDADO exige acolhimento logo no começo.

Regras:

- A bateria é congelada (hash em `congelado/SHA256_<nome>.txt`) **antes** da correção que pretende testar.
- A pergunta não muda depois do congelamento. Se um critério muda por decisão (por exemplo, quando um perfil "em breve" passou a existir), a mudança fica registrada no histórico.
- `congelado/conferir.py` confere todos os hashes registrados.

Executores: `testes/rodar.cjs` envia a pergunta pelo formulário, com o `app.js` verdadeiro numa página simulada e o SQLite verdadeiro; `testes/caixa.cjs` envia pela caixa "Consultar a norma"; `testes/proprias.cjs` confere a coerência interna (cada ficha achada pela própria pergunta-exemplo); `testes/apoio.py` confere a linha de apoio.

### 5.2 Testes de tela

`testes/ui.cjs` e `testes/ui2.cjs` (Playwright, Chromium, tela de 360 px): percurso pelo menu abrindo todas as fichas do perfil, Voltar, Avançar e recarregar, acolhimento na caixa, endereços inválidos, quadro do Anexo II sem transbordo, largura da página no celular.

### 5.3 Resultados

Tabela completa em [AVALIACAO.md](AVALIACAO.md). Na 5.23, todas as baterias das rodadas de correção passam inteiras, salvo critérios estreitos conhecidos (c44 C10, r24 R07), a pergunta "oi" (a62 A11) e as mudanças de gabarito por decisão (x44 G01 a G04, p48 P45 e P46).

### 5.4 Não testado

Firefox, Safari do iPhone e celulares físicos variados. O primeiro teste com alunos de graduação, com folha de avaliação e formulário próprios, foi aplicado em 26/11/2026 e gerou as correções da 5.22 e da 5.23.

---

## 6. Publicação

- Endereço: https://iaeduca.online/jane/. Só com autorização escrita do autor.
- A pasta publicada é `app/`, montada por `testes/montar_app.sh` com os perfis ativos.
- Envia-se só o que mudou. O SHA-256 de cada arquivo no servidor é conferido contra o pacote local, antes e depois do envio.
- Cada versão sobe o número `?v=N` dos scripts e da folha de estilo no `index.html`, e o servidor manda `Cache-Control: no-cache` para os `.html`, `.js`, `.css` e `.sqlite`, para o navegador não ficar com cópia antiga.
- Depois do envio, limpa-se o cache da CDN só do domínio principal e confere-se o site público.
- O testador independente é avisado da hora em que cada mudança entrou no ar.
- O pacote da versão anterior é guardado, para voltar atrás reenviando os arquivos.
- Este repositório acompanha cada versão publicada.

---

## 7. Limites e próximos passos

- As fichas resumem a norma e não a substituem; vale o texto da resolução e as regras de cada instituição.
- A triagem por regras não reconhece todas as formas de escrever uma situação de risco; a linha de apoio existe por isso.
- Limites registrados: três perguntas-exemplo de montagem de imagem caem no acolhimento quando digitadas (as fichas abrem pelo menu); alguns relatos de terceiros em situações de rua, desmaio por fome ou criança deixada com irmãos ficaram sem texto próprio depois do encerramento das rodadas de risco.
- Pendentes: revisão dos textos pelos alunos; teste com alunos e colegas em celulares variados.

---

## 8. Histórico

Protótipo anterior descartado após auditoria → motor de regras com banco da norma no navegador e baterias congeladas por hash → percurso perfil, assunto, situação, com o campo livre recolhido → perfil Pós-graduação (5.7) → Graduação (5.8 e 5.9) → contador de visitas sem cookies (5.10 e 5.11) → Estudante do fundamental e médio (5.12) → professores (5.13) → rodadas do testador independente sobre acolhimento e situações de risco (5.14 a 5.20), com a linha de apoio desde a 5.16 → Gestor escolar e Pai, mãe ou responsável (5.17) → acabamento visual (5.21) → ficha das entrevistas do TCC reescrita a partir do teste com alunos (5.22) → demais correções desse teste: respostas com Sim ou Não claros, fichas novas da graduação, busca e "Nenhuma dessas" (5.23).

Detalhes de cada versão: [CHANGELOG.md](CHANGELOG.md) e [docs/historico_detalhado.md](docs/historico_detalhado.md).
