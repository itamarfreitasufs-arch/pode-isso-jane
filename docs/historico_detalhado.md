# Histórico detalhado das versões 5.9 a 5.22

Notas de trabalho escritas a cada versão, na ordem em que foram registradas. O resumo, da mais nova para a mais antiga, está em `CHANGELOG.md`. Nomes de pasta antigos: `dist_pos/` é hoje `app/`; os scripts de `publicar/` (envio ao servidor e remendos `c5xx.py`, já aplicados às fontes) não fazem parte desta distribuição, exceto `ui.cjs`, `ui2.cjs` e `todas.sh` (agora em `testes/`) e os geradores de bateria (agora em `congelado/geradores/`).


## v5.11: número de visitas no rodapé

- A pedido do autor, o total de visitas aparece discreto no rodapé, na linha "Realização: IAEduca · N visitas". `conta.php` por GET devolve só esse total; se o servidor não responder, nada aparece. `index.html` ganhou `<span id="visitas">` e `app.js?v=5.11`. Baterias com saída idêntica à v5.9; ui2.cjs 7/7.

## v5.10: contador de usos

- `conta.php` recebe do app só o tipo de uso (visita, perfil escolhido, ficha aberta, dúvida escrita, busca na norma), o perfil e o código da ficha, e soma por dia em `contagem/AAAA-MM.json`. Não grava IP, navegador, hora, cookie nem texto digitado. Eventos e perfis fora da lista são recusados; no máximo 400 chaves por dia.
- Visita = uma aba aberta (sessionStorage, nada é enviado); recarregar, Voltar e Avançar não contam de novo a visita nem a mesma ficha.
- `painel.php?k=CHAVE` mostra os totais só para o autor; a chave fica em `contagem/chave.txt` no servidor (não vai no pacote). `contagem/.htaccess` fecha a pasta ao navegador.
- Mudou só `app.js` (função `contar`) e `index.html` (`app.js?v=5.10`). Baterias: saídas byte a byte iguais às da v5.9 (g60 60/60, p48 48/48, c44 43/44, r24 23/24, q42 42/42, n46 46/46); tela ui2.cjs 7/7.

# v5.9 (25/11/2026)

- `dist/`: fontes de tela (HTML, JS, CSS) e banco com todos os perfis.
- `construir/`: gerador do banco. `sit_pos.py` traz as fichas da pós; `sit_gra.py` deriva delas as da graduação e traz as fichas novas.
- `testes/` e `congelado/`: baterias. `bash testes/tudo.sh` (todos os perfis) e `bash testes/pos.sh pos,graduacao` (versão publicada).
  Baterias congeladas novas: `perguntas_g60.json` (graduação) e `perguntas_c44.json` (caixa de busca), com hash em `SHA256_*.txt`.
- `publicar/`: scripts de envio ao servidor e teste de tela (`ui.cjs`).

Resultados desta versão: g60 60/60, p48 48/48, c44 43/44, q42 42/42, n46 46/46, a62 61/62, h16 16/16, exemplos próprios 100/100 (publicada) e 318/326 (todos os perfis).

## v5.9: os 6 problemas do reteste da v5.8

- Sem perfil escolhido, a caixa "Consultar a norma" não oferece ficha: pede o perfil (artigo, verbete, termo da norma e acolhimento seguem funcionando sem perfil).
- A ficha geral de declaração só entra em "Você quis dizer" quando pontua perto da primeira.
- Pergunta fora do tema na caixa recebe o aviso de escopo, não "Sem correspondência".
- Erros de digitação: `corrigir()` em `dist/triagem.js` troca a palavra que as fichas não conhecem pela que soa igual ("teze", "profesor", "trabaio", "detetor") ou, nas longas, difere em uma letra.
- Acolhimento na caixa: a ficha aberta sai da tela e o título não repete a primeira frase.
- Endereço de perfil desativado ou de ficha inexistente: a tela avisa e corrige o endereço.

Bateria congelada antes das correções: `perguntas_r24.json` (hash em `SHA256_r24.txt`): v5.8 11/24, v5.9 23/24 (R07 é critério estreito: exige "sem ler" e a ficha da pós diz "sem leitura"). Tela: `publicar/ui2.cjs`, 7 de 7 (antes 1 de 7).
Sem regressão: g60 60/60, p48 48/48, c44 43/44, q42 42/42, n46 46/46, a62 61/62, h16 16/16, exemplos próprios 100/100 e 318/326.

## v5.12: perfil Estudante da educação básica (fundamental e médio)

- Um perfil só (`basico`), a pedido do autor: fundamental e médio não se separam, a não ser onde a norma obriga. A norma só responde diferente por etapa em "Posso usar IA?" (arts. 22, 23 e 20, parágrafo único); ali há uma pergunta para cada etapa. Nos outros nove assuntos a regra é a mesma.
- `construir/sit_bas.py`: 46 fichas próprias (ids `eb_*`) mais a ficha comum `geral_ia_disse`, em 10 assuntos. Os perfis antigos por etapa (`iniciais`, `finais`, `medio`) continuam no construtor para as baterias antigas e saem da lista da tela quando `basico` está ativo.
- `dist/triagem.js`: `etapaBasica()` lê a etapa escrita pela pessoa ("to no 7 ano", "tenho 9 anos", "2 ano do médio") e a transforma nos conceitos `eb_iniciais`, `eb_finais` e `eb_medio`; "1º ano", "2º ano" e "3º ano" sozinhos não decidem e levam à ficha geral por etapa.
- Contador (`app.js`, `conta.php`, `painel.php`) passa a contar também o perfil `basico`.
- Publicação: `python3 -I construir/build.py construir/norma_origem.sqlite dist_pos/norma.sqlite pos,graduacao,basico` (ou `bash testes/pos.sh pos,graduacao,basico`).

Bateria congelada antes de escrever as fichas: `perguntas_e60.json` (hash em `SHA256_e60.txt`): fichas antigas por etapa 46/60, v5.12 60/60.
Sem regressão: g60 60/60 (saída idêntica à v5.11), p48 48/48, c44 43/44, r24 23/24, q42 42/42, n46 46/46, a62 61/62, h16 16/16. Exemplos próprios 146/147 (publicada) e 364/373 (todos os perfis): a falha nova é esperada, a pergunta da ficha `eb_montagem` (montagem ou vídeo falso) cai antes no acolhimento quando digitada; a ficha abre pelo menu. Tela: `publicar/ui.cjs` e `publicar/ui2.cjs` sem falha, 47 fichas abertas pelo menu.

## v5.13: perfis de professor

- Dois perfis, e não três: `profBasico` ("Professor · fundamental e médio", 50 fichas próprias `pb_*`/`pf_*` mais a comum `geral_ia_disse`) e `profSuperior` ("Professor · graduação e pós-graduação", 52 próprias `ps_*`/`pf_*` mais a comum). A norma separa a educação básica da superior, mas trata a superior em conjunto; entre graduação e pós as perguntas de quem dá aula são quase todas idênticas, e as poucas próprias da pós (orientação de TCC, dissertação e tese, responsabilidade do orientador, IA como coautora, dados de participantes, revistas e parecer) ficaram dentro do mesmo perfil. Regra do autor: se as perguntas forem idênticas, não forçar perfis separados.
- No perfil da educação básica a etapa só separa "uso com os alunos" (arts. 21, 22, 23 e 20, parágrafo único); há duas perguntas da educação infantil.
- `construir/sit_prof.py`: fichas, conceitos `pf_*`, núcleos `p_*` e a mensagem de perfil inativo. `construir/base.py`: rótulos dos perfis; o do estudante passou a "Estudante do ensino fundamental e médio" (na tela, "Estudante · fundamental e médio", sem "educação básica" e sem parênteses).
- `dist/triagem.js`: perfis de professor novos (`docentesNovos`), temas próprios de docente, inferência de "sou professora de...", erro de letra em "criança", "alunos", "corrigir".
- Contador (`app.js`, `conta.php`, `painel.php`) conta também `profBasico` e `profSuperior`.
- Publicação: `bash testes/pos.sh pos,graduacao,basico,profBasico,profSuperior`.

Bateria congelada antes de escrever as fichas: `perguntas_t95.json` (hash em `SHA256_t95.txt`): fichas antigas de docente 74/95, v5.13 95/95.
Sem regressão: e60 60/60, g60 60/60 (saída idêntica), c44 43/44, r24 23/24, q42 42/42, n46 46/46, a62 61/62, h16 16/16. p48 47/48: a P45 ("sou professora do 3o ano, posso usar chatgpt com as crianças?", com o perfil Pós selecionado) mudou de propósito; o critério esperava o aviso de perfil inativo e agora, com o perfil de professor ativo, a resposta é a ficha `pb_iniciais` (art. 22). Exemplos próprios 250/251 (publicada) e 468/477 (todos os perfis), as mesmas falhas esperadas de antes. Tela: `publicar/ui.cjs` (51 e 53 fichas abertas pelo menu) e `publicar/ui2.cjs` sem falha.

## v5.14: achados do teste independente da v5.13

Publicada em 26/11/2026, 07h06 de Brasília. Mesmos perfis e mesmas fichas, com uma ficha a mais (`ps_material`).

- Montagem íntima relatada por quem não é a vítima (professor, colega, familiar): variante `imagem_intima_outro` em `construir/base.py`, com título próprio em `dist/app.js` ("Proteja quem foi atingido"). A decisão está em `dist/triagem.js` (`imagemPropria`, `imagemDeOutro`). Quem é a vítima continua recebendo o texto "a culpa não é sua".
- Sofrimento sem palavra de risco ("estão me zuando no grupo", "ninguém gosta de mim", "não tenho amigos"): portões `humilhacao` e `aflicao` ampliados, só para frases em primeira pessoa; textos reescritos.
- "Posso colar na prova com IA?" é pergunta de permissão e vai para a ficha da prova; "como colar sem o professor perceber" continua recusado, e na caixa "Consultar a norma" a recusa passou a vir antes dos trechos da norma.
- "Sou orientador..." responde com as fichas do professor da graduação e pós-graduação enquanto o perfil próprio não existe.
- "A revista exige declaração de IA" leva à ficha "Uso IA na minha pesquisa" (conceito `pf_rev_exige`).
- Quem se apresenta como gestor ou família é avisado de que esses perfis estão em preparo.
- A ficha de planejamento do professor do superior (`ps_material`) não fala mais de educação infantil nem de 1º ao 5º ano.
- Acolhimento de ameaça ao professor fala em "direção da escola ou coordenação do curso"; títulos dos blocos de cuidado não repetem a primeira frase.

Bateria congelada antes das correções: `perguntas_x44.json` (hash em `SHA256_x44.txt`, roda com `testes/caixa.cjs`): v5.13 10/44, v5.14 44/44.
Sem regressão: t95 95/95, e60 60/60, g60 60/60, c44 43/44, r24 23/24, q42 42/42, n46 46/46, a62 61/62, h16 16/16, p48 47/48, exemplos próprios 250/251 e 468/477 (as mesmas falhas esperadas de antes). `publicar/ui.cjs` e `publicar/ui2.cjs` sem falha.
Limites conhecidos: "posso fazer montagem de um colega com ia?" recebe o acolhimento de quem relata; "meu amigo disse que ninguém gosta dele" cai fora do escopo.

## v5.15: achados do reteste da v5.14

Publicada em 26/11/2026, 10h53 de Brasília. Mesmos perfis e mesmas fichas.

- Automutilação: portão `autolesao` em `construir/base.py`, logo depois de `vida`, com a variante `autolesao_outro` para quem relata (professor, colega, família). O acolhimento é a resposta inteira, como no risco à vida.
- Quem sofre: `relatoDeOutro` em `dist/triagem.js` decide, para `autolesao`, `humilhacao` e `aflicao`, se quem escreve é a pessoa atingida ou alguém que relata. Variantes novas: `humilhacao_outro`, `aflicao_outro`, `aflicao_adulto`.
- Sofrimento em primeira pessoa: mais formas nos portões `humilhacao` e `aflicao`. Na caixa "Consultar a norma", o acolhimento de frase com três palavras ou mais não some quando a busca acha palavras soltas na norma.
- Pedido para fazer ou espalhar montagem de outra pessoa: recusa `montagem_dano` (`querMontagem`, `alvoDeMontagem`, `relatoDeMontagem`). Pedido de montagem sem pessoa atingida não abre o acolhimento da vítima.
- Intimidação e coação entram no portão `violencia`.
- Quem só se apresenta ("sou orientadora de mestrado", "sou professora", "sou aluno do 7 ano") recebe a mensagem `apresentacao`, com o nome do perfil como aparece na tela (`rotuloDeTela`).
- Papéis de gestor e de família reconhecem mais formas ("trabalho na secretaria de educação", "sou supervisora pedagógica", "tenho dois filhos na escola").
- A opção "Orientador de pós-graduação" sai da lista quando o perfil não está ativo (`construir/build.py`).

Bateria congelada antes das correções: `perguntas_y58.json` (hash em `SHA256_y58.txt`, roda com `testes/caixa.cjs`): v5.14 16/58, v5.15 58/58.
Sem regressão: x44 44/44, t95 95/95, e60 60/60, g60 60/60, c44 43/44, r24 23/24, q42 42/42, n46 46/46, a62 61/62, h16 16/16, p48 47/48, exemplos próprios 250/251 e 468/477.
Publicação: `faz_pacote.py` (na pasta `publicar/`) compara a pasta publicada com a nova e monta o pacote em pedaços.

## v5.16: achados do reteste da v5.15 e linha de apoio

Publicada em 26/11/2026, 11h10 de Brasília. Mesmos perfis e mesmas fichas.

- Linha de apoio: toda resposta "isso foge do que este app consulta" e "não ficou claro" (e "sem correspondência", quando a pessoa escreveu quatro palavras ou mais) traz a linha "Precisa de ajuda agora? CVV 188 · Disque 100". `triar()` e `consultarCaixa()` devolvem `apoio`; `app.js` desenha a linha. Motivo: nenhuma regra reconhece toda forma de pedir ajuda.
- Autolesão sem corte (bater a cabeça, bater-se, morder-se, queimar-se, arrancar cabelo, socar a parede), em primeira e em terceira pessoa.
- Risco à vida em outras palavras (vontade de sumir, pensar em desaparecer, largar tudo e sumir, nunca ter nascido, vida sem sentido); "sumir com" deixou de acionar o portão.
- Risco à vida relatado ("uma mãe me contou que a filha quer morrer"): `relatoDeOutro` trata `vida` pelo verbo na terceira pessoa.
- Bullying relatado sem as palavras de sempre (é chamado de, apelido maldoso, virou piada da turma, ninguém deixa jogar).
- Sofrimento (me sinto incapaz, sou uma farsa, ninguém me escolhe, sempre sobro, vontade de largar o curso). "Incapaz de usar IA" não aciona.
- Foto editada, perfil falso e meme: recusa para quem anuncia que vai fazer ou espalhar; acolhimento para quem foi alvo. Na caixa, o acolhimento de imagem não some quando a busca acha palavras na norma (quatro palavras ou mais).
- "Sou estudante de enfermagem", "sou universitário", "sou aluno do ensino médio": `etapaDeclarada` aponta o perfil.
- Bateria z77 (`congelado/perguntas_z77.json`, congelada antes, roda com `testes/caixa.cjs`; a linha de apoio se confere com `testes/apoio.py`): v5.15 28/77, v5.16 77/77. Sem regressão nas demais.

## v5.17: perfis Gestor escolar e Pai, mãe ou responsável, e achados do teste da v5.16

Publicada em 26/11/2026, 11h55 de Brasília.

- Perfis novos: "Gestor escolar" (`gestorEscolar`, 54 fichas `ge_*` em `construir/sit_ge.py`) e "Pai, mãe ou responsável" (`responsavel`, 45 fichas `fa_*` em `construir/sit_fa.py`). As linhas antigas "Gestor de escola" e "Família ou responsável" (em breve) saem da lista. O perfil vazio de orientador já tinha saído na v5.15.
- Quem escreve "sou diretora", "sou mãe" sem escolher perfil é levado ao perfil novo. Temas próprios desses perfis (escola pequena, fiscalização, vigilância em prova, vigência) entram no escopo mesmo sem a palavra IA.
- Contador e painel contam os dois perfis novos.
- Ameaça de morte vinda de outra pessoa ("minha mãe disse que vai me matar") recebe o texto de violência (Disque 100, 190), e não o de suicídio. Formas figuradas ("vai me matar se souber que usei IA", "esse TCC vai me matar") não acionam.
- Sinais de violência relatados por professor (hematomas, marcas, "apanha do pai") apontam o Conselho Tutelar.
- Portão novo `assedio` (Ligue 180, Disque 100, ouvidoria, 190), em primeira pessoa, relatado por outra pessoa e para adulto.
- Montagem com IA dita de outras formas (rosto em vídeo, voz imitada em áudio): acolhimento para quem foi alvo, recusa para quem quer fazer.
- Autolesão leve (beliscar, morder) e sofrimento (não paro de chorar, burnout, crise de ansiedade, pânico, desistir do mestrado).
- Bullying relatado por professor em outras palavras (alvo de risadas, motivo de gozação, pegam no pé).
- "Sou residente", "faço residência", "aluno de especialização", "mestrando", "doutoranda": aponta o perfil de pós-graduação.
- Baterias congeladas antes: s49 (`congelado/perguntas_s49.json`, com `testes/caixa.cjs`) v5.16 11/49, v5.17 49/49; gf110 (`congelado/perguntas_gf110.json`) fichas antigas 73/110, v5.17 110/110.
- Sem regressão: y58 58/58, z77 77/77, c44 43/44, r24 23/24, t95 95/95, e60 60/60, g60 60/60, q42, n46, a62 61/62, h16. Mudaram de gabarito por decisão: x44 G01 a G04 (pediam "em breve" para gestor e família, agora apontam os perfis novos) e p48 P45 e P46 (agora apontam os perfis de professor e de responsável).
- Remendos em `publicar/c517*.py`; `publicar/todas.sh` roda as baterias da caixa e do motor de uma vez.

## v5.18: achados do teste da v5.17

Publicada em 26/11/2026, 12h34 de Brasília. Mesmos sete perfis e mesmas fichas (nenhuma ficha nova).

- Portão novo `aliciamento`: adulto ou desconhecido que pede fotos, segredo ou encontro a criança ou adolescente. Texto próprio para quem sofre (Disque 100, SaferNet, 190), para o adulto que relata (polícia, Conselho Tutelar, Disque 100, SaferNet) e para adulto que é alvo. Vem antes de assédio e de imagem íntima.
- Violência doméstica: "meu marido me bate" recebe o Ligue 180 e o 190, e não o texto feito para a escola (`violencia_domestica`). Há texto para quem relata a violência sofrida por uma adulta (`violencia_domestica_outro`), para o familiar que relata agressão a criança (`violencia_outro_familia`) e para a criança que vê a agressão em casa (`violencia_em_casa`).
- Negligência relatada (aluno que não come há dias, vem sem banho, fica sozinho em casa, foi abandonado pelos pais) aponta o Conselho Tutelar.
- Risco à vida relatado por gestor, colega ou familiar sobre um adulto ("uma professora disse que vai se matar") recebe o texto de quem relata.
- Família: "meu filho usa chatgpt pra fazer o dever", "posso ver as conversas do meu filho com a IA" abrem a ficha do uso em casa (`fa_casa`); "qual IA é segura para criança" abre a ficha da conta própria (`fa_conta`).
- Gestor: "um professor usou chatgpt para dar nota" abre a ficha da correção com IA (`ge_correcao`).
- "Meu filho tem 10 anos", "sou tia e responsável por uma menina do 2º ano", sem perfil, apontam o perfil Pai, mãe ou responsável.
- Contagem: o menu mostra 55 fichas no gestor e 46 na família porque a ficha comum "A IA disse que…" (`geral_ia_disse`) aparece nos dois; as fichas próprias são 54 e 45.
- Bateria u54 (`congelado/perguntas_u54.json`, congelada antes, com `testes/caixa.cjs`): v5.17 19/54, v5.18 54/54. Sem regressão nas demais (mesmos resultados da v5.17).
- Remendo em `publicar/c518.py`.

## v5.19: achados do teste da v5.18

Publicada em 26/11/2026, 12h54 de Brasília. Remendo em `publicar/c519.py`; bateria `congelado/perguntas_v56.json` (gerada por `publicar/gera_v.py`, congelada antes das correções): v5.18 18/56, v5.19 56/56. Demais baterias iguais (`publicar/todas.sh`, `testes/tudo.sh`).

- U1: violência, briga e falta de comida em casa ditas de outras formas pela criança ("meu padrasto me machuca", "meus pais brigam e quebram tudo", "não tem comida em casa", medo de alguém da família, fuga de casa). Textos novos `fome_em_casa` e `fome_adulto`; abuso dito de outras formas entra no portão de assédio.
- U2: aliciamento contado por quem cuida ou ensina ("minha filha conversa com um desconhecido", mensagens de adulto pedindo fotos, presentes, encontro, namorado bem mais velho). Na graduação e na pós, relato sobre adultos não dispara.
- U3: violência doméstica revelada na escola: texto `violencia_casa_relato` (Conselho Tutelar, Disque 100, Ligue 180).
- U4: negligência dita de outras formas, trabalho infantil e criança que cuida sozinha dos irmãos: texto `negligencia_outro`.
- U5: conversa com a IA de madrugada abre a ficha fa_amigo; a vizinha achada só pelas palavras não entra quando a ficha se exclui do assunto.
- Linha de apoio: "CVV 188 (apoio emocional) · Disque 100 (violência ou abuso)".
- Os padrões de fome, violência no lar e negligência são escritos uma vez em c519.py e gravados no portão (base.py) e na escolha do texto (triagem.js).

## v5.20: aliciamento dito com outras palavras (última rodada de situações de risco)

Publicada em 26/11/2026, 13h16 de Brasília. Remendo em `publicar/c520.py`; bateria `congelado/perguntas_w38.json` (gerada por `publicar/gera_w.py`, congelada antes): v5.19 15/38, v5.20 38/38. Demais baterias iguais.

- O portão de aliciamento passa a combinar quem aborda (desconhecido, adulto, alguém "da internet" ou "do jogo", youtuber, jogador) com o que faz (pede contato, endereço, encontro, câmera ou segredo; dá presente ou crédito; manda mensagens a uma criança; ronda a porta da escola).
- O adulto que conta um contato comum, sem criança nem sinal de risco no texto ("um desconhecido pediu meu whatsapp no grupo da faculdade"), não recebe o alerta.
- Decisão do autor (26/11/2026): esta é a última rodada de correção de situações de risco, salvo novo pedido. O que escapar fica coberto pela linha de apoio (CVV 188 e Disque 100).

## v5.21 (26/11/2026): acabamento visual
Só mudaram index.html, estilo.css e app.js (em dist/ e app/) (o "·" da linha de apoio virou span.sep). Nenhum texto de ficha, de acolhimento nem o fluxo. Título numa linha no celular; linha de cima sem ponto solto; perfil em destaque e consulta à norma secundária; assuntos sem quebra no meio da palavra; rótulo "Escolha a situação" e seta alinhada; veredito mais largo no celular; rodapé sem vãos nem "·" no fim da linha; cores dos cartões contidas para telas de cores vivas; serifa com Noto Serif no Android; tela inicial centrada em tela grande. Baterias de testes/todas.sh com saída idêntica à v5.20.

## v5.22 (27/11/2026): ficha das entrevistas do TCC
No teste dos alunos (26/11), só 4 de 13 entenderam "não pode" na ficha gr_dados. Ela e as irmãs pos_dados e ps_dados_pesquisa passam a cartão vermelho ("Não"), com "Não." na primeira linha e a saída legítima (ferramenta da instituição, projeto e termo, anonimização) só no "O que fazer". Textos em construir/sit_v522.py, aplicados no fim de build.py. Só mudou o banco (app/norma.sqlite) (3 linhas de situacao). Baterias de testes/todas.sh idênticas à v5.21.
