# Perfil Graduação (v5.8, 25/11/2026) sobre a base única de fichas do ensino superior.
# - DERIVADAS: fichas da pós-graduação reaproveitadas. O texto é o da pós, com trocas de vocabulário
#   (programa -> curso, orientador -> professor ou orientador) e os ajustes indicados em cada linha.
#   Quando o texto da pós mudar, a graduação muda junto; os textos publicados da pós não são alterados aqui.
# - COMUNS: fichas que servem aos dois perfis sem mudança.
# - NOVAS: 7 fichas comuns à pós e à graduação e 11 próprias da graduação.
# Escolhas reversíveis (aceitas pelo autor em 25/11/2026): uma ficha só de estágio; técnicos e tecnólogos
# dentro da ficha de prática; TCC e iniciação científica tratados como pesquisa (art. 28).
import re, unicodedata

GRA, POS = 'graduacao', 'pos'
V, R_, A, Z = 'verde', 'vermelho', 'amarelo', 'azul'
G87, G88, G19, G23, G52, G73 = ('Glossário, verbete %d' % n for n in (87, 88, 19, 23, 52, 73))

MENSAGEM_INATIVO = 'Por enquanto, este app responde só a dúvidas de estudantes de graduação e de pós-graduação. Se é o seu caso, escolha o seu perfil e o assunto na lista ou reescreva a pergunta.'

# Conceitos novos.
CONCEITOS = {
 'tcc': r'\b(tcc|tccs|monografia\w*|trabalho de conclusao|iniciacao cientifica|pibic)\b',
 'recomendacao': r'\b(plataforma|sistema|aplicativo|app|ia|algoritmo|ambiente virtual|ava) .{0,60}\b(recomend\w*|suger\w*|indic\w+) .{0,40}\b(disciplina\w*|materia\w*|trilha\w*|optativa\w*|conteudo\w*|percurso\w*)\b|\b(so|apenas|somente) .{0,40}\b(disciplinas|materias|trilhas|conteudos|optativas|opcoes) que (ela|ele|o sistema|a plataforma|a ia) (recomend\w*|suger\w*|indic\w*|mostra|libera)\b|\b(so|apenas|somente) .{0,40}\bo que (ela|ele|o sistema|a plataforma|a ia) (recomend|suger|indic)\w*\b|\brecomendac\w+ (automatic\w*|d[ao] (sistema|plataforma|algoritmo))\b',
 'licenciatura': r'\b(licenciatura\w*|pedagogia|formacao (inicial )?(de professores|docente)|futur[oa]s? professor\w*)\b',
 'ensinar_ia': r'\b(ensin\w+|aprend\w+|prepar\w+|form\w+|capacit\w+) .{0,40}\b(usar|uso|sobre|a lidar|para) .{0,20}\b(ia|inteligencia artificial)\b|\b(disciplina|materia|aula|aulas|conteudo|formacao|curso) (sobre|de|em) (ia|inteligencia artificial)\b|\b(obrigad\w+|tem que|precisa|deve) .{0,30}\b(ter|oferecer|ensinar|incluir) .{0,30}\b(ia|inteligencia artificial)\b|\b(grade curricular|curriculo|ppc|projeto pedagogico)\b',
 'monitor': r'\b(sou|fui|virei|como|sendo) monitor\w*\b|\bmonitor(a|es|as)? d[aeo]s? (disciplina|turma|materia|curso|laboratorio)\b|\bna monitoria\b',
}
# Alternativas acrescentadas a conceitos que já existem.
AMPLIA = {
 'sem_acesso': r'\b(nao tenho|sem) (dinheiro|grana|condic\w+)\b|\b(ia|ferramenta|versao|assinatura|plano|conta) pag[ao]\b|\bnao (posso|consigo|tenho como) pagar\b',
 'avaliado_por_ia': r'\b(professor\w*|banca|avaliador\w*|orientador\w*|tutor\w*) .{0,30}\b(corrigiu|corrige|avaliou|deu (a )?nota) .{0,50}\b(com|pela|pelo|usando|na|no) (a |o )?(ia|chat\w*|gpt)\b',
 'predicao': r'\b(disse|apontou|calculou|indicou|mostrou) (que|q) eu (ia|vou|iria) (abandonar|reprovar|desistir|evadir|trancar)\b',
 'dados_identificados': r'\bdados (de|do|da|dos|das) (pacientes?|clientes?)\b',
 'incompleta': r'\bdeclarei (que|q) .{0,30}\b(so|apenas|somente)\b',
 'revisao_ling': r'\bcorrig\w+ (o |a |meu |minha )?(portugues|ingles|escrita)\b',
 'panorama': r'\bo que (a |essa |esta )?(resolucao|norma)( d[oe] (cne|mec))? (muda|mudou|altera|traz)\b',
}
NUCLEOS = {'decisao': 'recomendacao', 'usar': 'licenciatura', 'professor': 'monitoria'}

# Fichas que servem aos dois perfis como estão.
COMUNS = ['sup_regimento', 'sup_sancao', 'sup_assistiva', 'geral_ia_disse', 'pos_gravar']

# Trocas de vocabulário aplicadas a toda ficha derivada, nesta ordem.
TROCAS = [('O programa', 'O curso'), ('o programa', 'o curso'), ('programas', 'cursos'),
          ('o orientador', 'o professor ou orientador'), ('O seu orientador', 'O professor')]
CAMPOS = ('tema', 'pergunta', 'resposta', 'motivo', 'conferir', 'acao', 'modelo')
MARCAS = r'\b(programa|orientador\w*|tese|teses|dissertac\w*|mestrado|doutorado|pos|pos-graduacao|qualificacao|defes\w*|defendid\w*|parecer)\b'

def D(origem, id, troca=(), **campos):
    return (origem, id, list(troca), campos)

DERIVADAS = [
 D('pos_disciplina', 'gr_disciplina', [('O trabalho vai virar artigo ou capítulo da tese?', 'O trabalho vai ser aproveitado no TCC ou num artigo?')],
   pergunta='Posso usar IA para fazer um trabalho de disciplina?', exige='ia+disciplina|tarefa+permissao',
   exclui='ferramenta_imposta gravar_aula tcc ead inventar texto_alheio', peso=1, destaque=1),
 D('pos_uso', 'gr_tcc',
   [('Na pesquisa científica, o uso de IA deve preservar', 'A resolução não cita o TCC pelo nome; por serem trabalhos de pesquisa, o TCC e a iniciação científica seguem a regra da pesquisa científica. Nela, o uso de IA deve preservar'),
    ('Combine o uso com a orientação.', 'Combine o uso com o professor orientador.')],
   tema='Uso de IA no TCC e na iniciação científica', pergunta='Posso usar IA no TCC ou na iniciação científica?',
   exige='ia+pesquisa|tcc+permissao', exclui='percentual', peso=2, destaque=1),
 D('pos_ferramenta', 'gr_ferramenta', [('em mensagem do orientador', 'em mensagem do professor')],
   tema='Ferramenta exigida pelo professor', pergunta='O professor exige ou recomenda uma ferramenta de IA. Quem responde por ela?',
   exclui='declarar nao_declarei sem_acesso'),
 D('pos_assistente', 'gr_assistente', pergunta='A faculdade oferece um assistente de IA. O que ela me deve?'),
 D('pos_melhor', 'gr_melhor', [('Se o programa ou o orientador indicarem', 'Se o curso ou um professor indicarem')],
   pergunta='Qual é a melhor IA para estudar?'),
 D('pos_disc_declarar', 'gr_disc_declarar', [('O texto vai ser aproveitado na dissertação ou na tese?', 'O texto vai ser aproveitado no TCC ou num artigo?')],
   pergunta='Usei IA num trabalho de disciplina. Tenho que declarar?', exige='ia+disciplina|tarefa+usei|declarar',
   exclui='ferramenta_imposta tcc pesquisa nao_declarei incompleta revisao_ling grupo professor_usou inventar suspeita detector revista', peso=0),
 D('pos_declarar', 'gr_declarar', pergunta='Usei IA no TCC ou num artigo de iniciação científica. Preciso declarar?', reforca='declarar pesquisa tcc'),
 D('pos_revisao', 'gr_revisao', **{'motivo+': ' Em trabalho de disciplina, a resolução não exige declaração por si: vale a regra do professor e da instituição.'}),
 D('pos_nao_declarei', 'gr_nao_declarei',
   [('O art. 28 exige declarar a contribuição relevante da IA, mas a resolução não fixa sanção para o descumprimento.',
     'Na pesquisa, incluídos o TCC e a iniciação científica, o art. 28 exige declarar a contribuição relevante da IA; em trabalho de disciplina, a declaração depende da regra da instituição (art. 27, § 2º). Em nenhum dos casos a resolução fixa sanção para o descumprimento.'),
    ('O trabalho já foi defendido ou publicado?', 'O trabalho já foi entregue, avaliado ou publicado?')],
   pergunta='Usei IA e não declarei. O que pode acontecer?', **{'disp+': ['Art. 27, § 2º'], 'reforca': 'pesquisa tcc'}),
 D('pos_incompleta', 'gr_incompleta'),
 D('pos_ordem', 'gr_ordem', [('Mostre à orientadora o art. 28', 'Mostre ao professor o art. 28')],
   pergunta='O professor ou orientador mandou usar IA e não declarar. Obedeço?'),
 D('pos_historico', 'gr_historico'),
 D('sup_percentual', 'gr_percentual'),
 D('sup_retroativo', 'gr_retroativo'),
 D('pos_inventar', 'gr_inventar'),
 D('pos_suspeita', 'gr_suspeita', tema='Trabalho apontado como IA', pergunta='Meu trabalho foi marcado como IA pelo detector. Como respondo?'),
 D('pos_nota', 'gr_nota', pergunta='Uma plataforma corrigiu meu texto e fechou a nota. Posso pedir revisão?'),
 D('pos_parecer_ia', 'gr_correcao_ia',
   [('O parecer trata de pontos específicos', 'A correção trata de pontos específicos'), ('Anote o que no parecer levanta a dúvida.', 'Anote o que na correção levanta a dúvida.'),
    ('[nota ou parecer]', '[nota ou correção]')],
   tema='Correção ou nota sem leitura', pergunta='Desconfio que o professor corrigiu meu texto com IA, sem ler. O que posso pedir?'),
 D('pos_selecao', 'gr_selecao', pergunta='Um sistema de IA decidiu matrícula, bolsa, monitoria, vaga de estágio ou desligamento. Vale?'),
 D('pos_predicao', 'gr_predicao'),
 D('pos_camera', 'gr_camera', pergunta='A instituição quer me filmar ou me monitorar com IA durante a prova. Pode?'),
 D('pos_vigilancia', 'gr_vigilancia'),
 D('pos_textos', 'gr_textos', tema='Textos e materiais de outras pessoas',
   pergunta='Posso colar numa IA o trabalho de um colega, um artigo ou o material do professor?',
   **{'motivo+': ' Slides, apostilas e provas preparados pelo professor também são produção de outra pessoa.'}),
 D('pos_dados', 'gr_dados', pergunta='Posso mandar a uma IA as entrevistas ou os questionários do meu TCC?', peso=24),
 D('pos_dados_sensiveis', 'gr_dados_sensiveis',
   tema='Dados de pacientes, alunos ou clientes',
   pergunta='Posso enviar a uma IA aberta prontuários ou dados de pacientes, alunos ou clientes do estágio?',
   **{'motivo+': ' No estágio, o sigilo profissional e as regras do local de prática somam-se a isso e vão além desta resolução.'}),
 D('pos_meus_textos', 'gr_meus_textos', pergunta='Meus trabalhos vão alimentar o sistema de IA de uma empresa. Pode, sem me perguntar?'),
 D('pos_revista', 'gr_revista', pergunta='A revista ou o evento vai aceitar um trabalho em que usei IA?'),
 D('pos_prazo', 'gr_prazo',
   [('valem as regras que o programa já tem, as vedações do art. 41 e o que a resolução pede de quem pesquisa.', 'valem as regras que o curso já tem, as vedações do art. 41 e os deveres que a resolução já põe sobre você.'),
    ('o que ela pede de quem pesquisa não depende da política: declarar a contribuição relevante da IA (art. 28) e responder pelo conteúdo (art. 10, § 1º)',
     'o que ela pede de você não depende da política: responder pelo conteúdo que apresenta (art. 10, § 1º) e, na pesquisa, declarar a contribuição relevante da IA (art. 28)'),
    ('O seu orientador combinou alguma regra?', 'O professor combinou alguma regra?'),
    ('Combine o uso por escrito com o orientador. Declare desde já o uso relevante na pesquisa.', 'Combine o uso por escrito com o professor. No TCC e na iniciação científica, declare desde já o uso relevante.')],
   tema='Curso sem política de IA', pergunta='Minha faculdade ainda não tem política de IA. O que vale até lá?'),
]

def F(id, perfis, nucleo, sinal, tema, pergunta, resposta, motivo, conferir, acao, disp, exige, reforca='', exclui='', peso=0, destaque=0, modelo=''):
    return dict(id=id, nucleo=nucleo, perfis=list(perfis), tema=tema, pergunta=pergunta, resposta=resposta, motivo=motivo, conferir=conferir,
                acao=acao, disp=disp, exige=exige, reforca=reforca, exclui=exclui, peso=peso, destaque=destaque, sinal=sinal, modelo=modelo)

SUP, SO_GRA = (POS, GRA), (GRA,)

NOVAS = [
 # --- Comuns à pós-graduação e à graduação ---
 F('sup_sem_acesso', SUP, 'sem_acesso', Z, 'Sem acesso à ferramenta',
   'A atividade exige uma IA paga, ou não tenho computador nem internet. E agora?',
   'Avise o professor e peça alternativa: a equidade é princípio da resolução, e a instituição deve pesar acesso e inclusão antes de adotar uma ferramenta.',
   'Inclusão, equidade e acessibilidade são princípios do uso de IA na educação (art. 4º, IV). Antes de adotar uma aplicação, a instituição deve avaliar as condições de infraestrutura e conectividade e o impacto sobre a inclusão dos diferentes perfis de estudantes (art. 6º, VII e VIII). Quando um docente exige ferramenta externa no exercício da função, o uso se equipara ao institucional (Glossário, Anexo I, verbete 88), e esses deveres passam a valer. A resolução não diz quem paga a ferramenta nem cria, com essas palavras, um direito a atividade alternativa na educação superior.',
   'A ferramenta é exigida ou é uma opção? A instituição oferece laboratório, licença ou ferramenta própria? Há outra forma de cumprir a atividade?',
   'Diga ao professor, por escrito, que não tem acesso e peça outra forma de fazer a atividade. Se não resolver, leve à coordenação ou à assistência estudantil.',
   ['Art. 4, caput, inciso IV', 'Art. 6, caput, inciso VII', 'Art. 6, caput, inciso VIII', G88], 'sem_acesso', exclui='suspeita', peso=20),
 F('sup_erro_ia', SUP, 'erro_ia_estudante', Z, 'Erro da IA',
   'A IA errou e eu fui prejudicado na nota. De quem é a responsabilidade?',
   'De quem apresenta o trabalho: usar IA não transfere à ferramenta a responsabilidade pelo conteúdo.',
   'Quem usa a IA responde pela veracidade e pela consistência do que apresenta, e cabe a essa pessoa selecionar e conferir as informações (art. 10, § 1º). Os resultados gerados por IA ficam sempre sujeitos à análise crítica e à responsabilidade humana (art. 13, parágrafo único). Se a ferramenta foi exigida ou recomendada por um docente, o uso se equipara ao institucional (Glossário, Anexo I, verbete 88): a instituição também tem deveres, mas a conferência do que você entrega continua sua.',
   'Você conferiu o resultado em outra fonte ou refez a conta? A ferramenta foi escolha sua ou exigência da disciplina? A regra da atividade permitia o uso?',
   'Mostre ao professor como usou a ferramenta e onde ela errou. Pergunte se cabe refazer ou revisar. Da próxima vez, confira antes de entregar.',
   ['Art. 10, § 1º', 'Art. 13, Parágrafo único', G88], 'ia+culpa|responsavel', reforca='culpa',
   exclui='professor_usou ferramenta_imposta coautor_usou grupo avaliado_por_ia inventar', peso=7),
 F('sup_recomendacao', SUP, 'recomendacao', Z, 'Recomendação automática de disciplinas e trilhas',
   'A plataforma só me mostra ou só me deixa escolher o que ela recomenda. Pode?',
   'Recomendar, pode; a sugestão não pode virar decisão disfarçada: você precisa ver as alternativas e poder escolher.',
   'Mecanismos de recomendação acadêmica sem efeito decisório automático são aplicações de risco moderado (art. 39, § 1º, V). O Glossário da resolução (Anexo I, verbete 52) diz que a recomendação não é ato neutro e veda que a sugestão se converta em decisão dissimulada, por desenho de interface, por omissão de alternativas ou por aceitação tácita; ele exige transparência sobre os critérios gerais e preservação da liberdade de escolha. A instituição deve prever revisão humana quando a recomendação influenciar o seu percurso e manter canal para esclarecer e contestar (art. 39, § 2º, III e VI). Se o sistema passa a decidir matrícula, permanência ou benefício, a decisão exclusivamente automatizada é vedada (art. 41, V).',
   'Você consegue ver e escolher opções fora da lista recomendada? A instituição explicou o critério da recomendação? Existe uma pessoa ou um canal para pedir outra opção?',
   'Peça à coordenação ou à secretaria acadêmica, por escrito, o critério da recomendação e a liberação das outras opções. Guarde a tela que mostra o bloqueio.',
   ['Art. 39, § 1º, inciso V', G52, 'Art. 39, § 2º, inciso III', 'Art. 39, § 2º, inciso VI', 'Art. 41, caput, inciso V'], 'recomendacao', peso=30),
 F('sup_facial', SUP, 'identidade', A, 'Reconhecimento facial na entrada ou na chamada',
   'A instituição pôs catraca ou chamada por reconhecimento facial. Sou obrigado?',
   'Conferir a identidade num momento pontual não é a vigilância vedada, mas o rosto é dado biométrico sensível: exige necessidade estrita e a alternativa menos invasiva.',
   'A verificação pontual de identidade, quando estritamente necessária para acesso a ambientes virtuais, avaliações ou atividades acadêmicas, não se confunde com vigilância biométrica contínua, mas deve observar finalidade, necessidade e proporcionalidade (art. 41, § 1º). O Glossário da resolução (Anexo I) trata a biometria como dado pessoal sensível, que exige necessidade estrita e justificada e a alternativa menos invasiva (verbete 23), e submete o reconhecimento facial a restrição rigorosa, com admissão excepcional, especialmente quando ligado a controle disciplinar ou aferição de frequência (verbete 73). Aplicações que tratam biometria são de alto risco (art. 40, § 1º, V). Se o sistema acompanha as pessoas de forma contínua, passa a ser vedado (art. 41, VI). A resolução não diz, com essas palavras, que você pode recusar; ela exige da instituição a justificativa e a alternativa.',
   'O sistema só confere a identidade num momento ou acompanha as pessoas ao longo do dia? Há outra forma de entrar ou de registrar presença? A instituição explicou a necessidade e o destino dos dados?',
   'Peça à coordenação ou ao encarregado de dados, por escrito, a justificativa da necessidade, o destino dos dados biométricos e a alternativa para quem não quiser usar o rosto.',
   ['Art. 41, § 1º', G23, G73, 'Art. 40, § 1º, inciso V', 'Art. 41, caput, inciso VI'], 'identidade', peso=26),
 F('sup_propaganda', SUP, 'propaganda', R_, 'Publicidade com dados de estudantes',
   'A plataforma do curso me mostra propaganda com base nos meus dados. Pode?',
   'Não: é vedado usar IA e dados educacionais para publicidade direcionada ou exploração comercial.',
   'A resolução veda, nas instituições educacionais, o uso de sistemas de IA para publicidade direcionada, perfilização mercadológica ou exploração comercial dos dados educacionais de estudantes e docentes (art. 16). A mesma prática está entre as vedações de aplicação imediata (art. 41, VII; art. 46). Os contratos da instituição devem prever governança e responsabilização dos fornecedores (art. 5º).',
   'A propaganda aparece dentro da plataforma indicada pela instituição? Ela parece se basear no que você faz ou escreve ali? A plataforma é contratada pela instituição ou é uma conta pessoal sua?',
   'Guarde capturas de tela com data. Comunique à coordenação ou ao encarregado de dados da instituição e peça que o fornecedor seja cobrado.',
   ['Art. 16, caput', 'Art. 41, caput, inciso VII', 'Art. 46, caput', 'Art. 5, caput'], 'publicidade', peso=24),
 F('sup_prof_usou', SUP, 'professor_usou', Z, 'IA usada pelo professor',
   'O professor fez a prova, a aula ou o material com IA e tinha erro. Pode?',
   'O professor pode usar IA como apoio, mas deve informar o uso e responde pelo conteúdo.',
   'O uso de IA para elaborar, adaptar e revisar materiais e atividades deve ser informado de forma clara e não afasta a responsabilidade do autor pela verificação do conteúdo (art. 14, § 2º). Cabe à mediação docente a interpretação crítica do que a IA produz (art. 8º, § 1º), e os resultados ficam sujeitos à análise crítica e à responsabilidade humana (art. 13, parágrafo único).',
   'O erro afetou a sua nota? O uso de IA foi informado à turma? O erro está registrado (questão, slide, data)?',
   'Mostre o erro ao professor e peça a correção. Se a nota foi afetada, peça a revisão da questão; se não resolver, leve à coordenação.',
   ['Art. 14, § 2º', 'Art. 8, § 1º', 'Art. 13, Parágrafo único'], 'professor_usou', exclui='avaliado_por_ia ordem', peso=19),
 F('sup_substituir', SUP, 'substituir_estudante', R_, 'Professor substituído por IA',
   'A instituição pode trocar o professor por uma IA ou deixar a IA dar a aula sozinha?',
   'Não: a resolução veda substituir a atuação docente por sistemas automatizados.',
   'É vedada a substituição da atuação docente por sistemas automatizados e a transferência da responsabilidade pedagógica para a IA (art. 14). A centralidade da regência humana é princípio da resolução e compreende essa vedação (art. 4º, § 1º, III). A IA pode apoiar a aula, em caráter complementar à atuação docente (art. 8º). Na educação a distância, a mediação feita por IA não conta para cumprir os requisitos de tutoria e interação (art. 9º, § 2º).',
   'Há um professor responsável pela disciplina, que você consegue acionar? A IA apoia a aula ou ocupa o lugar dele? Quem responde pela avaliação?',
   'Pergunte à coordenação, por escrito, quem é o docente responsável pela disciplina. Se não houver, leve o caso ao colegiado ou à ouvidoria.',
   ['Art. 14, caput', 'Art. 4, § 1º, inciso III', 'Art. 8, caput', 'Art. 9, § 2º'], 'prof_ia|substituir', exclui='ead', peso=18),
 # --- Próprias da graduação ---
 F('gr_ead', SO_GRA, 'ead', A, 'Tutoria por IA no curso a distância',
   'No meu curso a distância, o tutor é uma IA. Pode?',
   'A IA pode apoiar a tutoria, mas não substitui o professor nem o tutor, e não conta como a tutoria que o curso é obrigado a oferecer.',
   'Na educação a distância, a IA pode apoiar mediação, tutoria, atendimento e acompanhamento, desde que subordinada ao planejamento pedagógico, à curadoria docente e à supervisão humana significativa (art. 9º). Ela não pode substituir as responsabilidades do professor, do tutor ou da instituição (art. 9º, § 1º), e a mediação feita por IA não é computada para cumprir os requisitos de tutoria e de interação previstos na regulação da educação a distância (art. 9º, § 2º). Sistemas de tutoria automatizada são aplicações de risco moderado, e a instituição deve comunicar o uso, as finalidades, os limites e os responsáveis (art. 39, § 1º, I, e § 2º, I).',
   'Há um professor ou tutor humano que você consegue acionar? A instituição avisou que o atendimento é feito por IA? Quem responde quando a IA erra?',
   'Pergunte à coordenação ou ao polo quem é o tutor responsável e como falar com ele. Se só houver a IA, registre o pedido por escrito.',
   ['Art. 9, caput', 'Art. 9, § 1º', 'Art. 9, § 2º', 'Art. 39, § 1º, inciso I', 'Art. 39, § 2º, inciso I'], 'ead+ia|sistema', peso=16),
 F('gr_pratica', SO_GRA, 'pratica', A, 'Laboratório, prática profissional e cursos de tecnologia',
   'No laboratório ou na aula prática, posso seguir o que um aplicativo de IA sugere?',
   'Como apoio, sim, desde que você continue capaz de fazer e de decidir sem ele: a IA não pode comprometer a competência prática que o curso forma.',
   'Em cursos com atividades laboratoriais, práticas profissionais, estágios, simulações ou uso de equipamentos, a IA pode ser instrumento de apoio, desde que não comprometa o desenvolvimento das competências práticas, da autonomia profissional, do julgamento técnico, da segurança das atividades e da responsabilidade ética (art. 33). Os cursos superiores de tecnologia seguem essa mesma regra (art. 34). A educação superior deve formar para o uso da IA como apoio à tomada de decisão profissional (art. 30, I), e o que a ferramenta sugere fica sujeito à análise crítica e à responsabilidade humana (art. 13, parágrafo único).',
   'Você saberia executar o procedimento sem o aplicativo? O professor ou o supervisor autorizou o uso naquela atividade? Há risco para a segurança de alguém se a sugestão estiver errada?',
   'Use a sugestão como segunda opinião e confira com o protocolo e com o professor. Peça para treinar e ser avaliado também sem o aplicativo.',
   ['Art. 33, caput', 'Art. 34, caput', 'Art. 30, caput, inciso I', 'Art. 13, Parágrafo único'], 'pratica+ia|sistema', exclui='estagio', peso=16),
 F('gr_estagio', SO_GRA, 'estagio', A, 'Estágio',
   'No estágio, posso usar IA nas tarefas, ou para corrigir trabalhos de alunos?',
   'Como apoio, sim, com o conhecimento do supervisor e sem enviar dados de outras pessoas. Na escola, a nota de texto autoral exige leitura e correção de um professor.',
   'No estágio, a IA pode apoiar a formação, desde que não comprometa as competências práticas, a autonomia profissional, o julgamento técnico e a responsabilidade ética (art. 33). O uso por conta própria segue as normas da instituição e não admite inserir em plataformas externas dados pessoais de terceiros nem informações sigilosas (Glossário, Anexo I, verbete 87); as regras do local de estágio vão além desta resolução. No estágio em escola, materiais feitos com apoio de IA devem ter o uso informado e ser conferidos por quem os prepara (art. 14, § 2º), e a correção de redações e textos autorais só admite a IA como etapa preparatória, com leitura integral e correção humana (art. 40, § 4º; art. 41, IX). No ensino fundamental, os alunos não usam IA generativa por conta própria: nos anos iniciais a interação é vedada (art. 22, § 2º) e nos anos finais só ocorre com mediação (art. 23). Nas licenciaturas, a formação sobre IA se articula ao estágio supervisionado (art. 26, parágrafo único).',
   'O supervisor do estágio e o professor orientador sabem do uso? O que você vai enviar à ferramenta tem dados de pacientes, clientes, alunos ou da empresa? Quem lê e assina o que você produz?',
   'Combine o uso com o supervisor e siga a regra do local. Não envie dados de outras pessoas a ferramenta externa. Na escola, deixe a leitura e a nota de cada texto com o professor da turma.',
   ['Art. 33, caput', G87, 'Art. 14, § 2º', 'Art. 40, § 4º, inciso II', 'Art. 41, caput, inciso IX', 'Art. 22, § 2º', 'Art. 23, caput', 'Art. 26, Parágrafo único'],
   'estagio', reforca='ia nota', exclui='dados_identificados decisao_auto', peso=26),
 F('gr_licenciatura', SO_GRA, 'licenciatura', V, 'IA na licenciatura',
   'Faço licenciatura. O curso tem que me preparar para usar IA em sala de aula?',
   'Sim: a formação de professores deve contemplar explicitamente a IA, do uso pedagógico aos aspectos éticos.',
   'Nos cursos de licenciatura, a formação relacionada à IA contemplará explicitamente o letramento digital docente, a utilização pedagógica de tecnologias emergentes, a análise crítica de dados educacionais, a avaliação assistida por tecnologias digitais e os aspectos éticos do uso da IA nos ambientes escolares (art. 26). Esses conhecimentos se articulam, sempre que possível, ao estágio supervisionado, à extensão e à pesquisa (art. 26, parágrafo único), e a política da instituição deve prever estratégias de formação inicial docente (art. 27, § 3º). As instituições têm doze meses, contados da publicação, para se adequar (art. 46). A resolução não fixa carga horária nem obriga a criar uma disciplina específica.',
   'O projeto pedagógico do curso já trata de IA? O tema aparece em alguma disciplina, no estágio ou na extensão?',
   'Consulte o projeto pedagógico do curso. Se o tema não aparecer, leve o art. 26 ao colegiado ou à coordenação e pergunte como a adequação será feita.',
   ['Art. 26, caput', 'Art. 26, Parágrafo único', 'Art. 27, § 3º', 'Art. 46, caput'], 'licenciatura+ensinar_ia', peso=14),
 F('gr_curriculo', SO_GRA, 'curriculo', Z, 'IA no currículo do curso',
   'Meu curso é obrigado a ensinar IA ou a ter uma disciplina sobre o tema?',
   'A resolução manda a educação superior desenvolver competências para o uso crítico da IA, mas não obriga a criar disciplina: a forma é definida no projeto de cada curso.',
   'A educação superior promoverá competências para usar a IA de forma crítica, ética e responsável, como o apoio à decisão profissional, o uso de dados, a compreensão dos limites e dos riscos e a distinção entre apoio tecnológico e produção própria (art. 30). A IA pode entrar na formação como objeto de estudo e como recurso de apoio, respeitadas as especificidades dos cursos, as diretrizes curriculares e os projetos pedagógicos (art. 25). A resolução não fixa disciplina, carga horária nem conteúdo mínimo. As instituições têm doze meses, contados da publicação, para se adequar (art. 46).',
   'O projeto pedagógico do curso menciona IA? O tema aparece dentro de alguma disciplina, mesmo sem nome próprio?',
   'Leia o projeto pedagógico do curso. Se o tema não aparecer, pergunte à coordenação ou ao colegiado como o art. 30 será atendido.',
   ['Art. 30, caput', 'Art. 25, caput', 'Art. 46, caput'], 'ensinar_ia', exclui='licenciatura', peso=22),
 F('gr_prova', SO_GRA, 'uso_prova', Z, 'IA em prova',
   'Posso usar IA na prova?',
   'Só se a regra da prova permitir: a resolução não decide isso e deixa a política com a instituição.',
   'A resolução deixa às instituições de educação superior definir as regras de uso de IA no ensino (art. 27) e não trata de cada prova. O que ela fixa é que você responde pelo que apresenta e que a autoria deve corresponder à sua contribuição (art. 10, § 1º); a formação superior inclui compreender os limites entre apoio tecnológico e produção intelectual própria (art. 30, VII). Se a prova for monitorada por IA, valem os limites do monitoramento em avaliações (art. 40, § 1º, II).',
   'O professor ou o plano de ensino disseram o que pode ser consultado? A prova avalia justamente o que a ferramenta faria por você?',
   'Leia as instruções da prova. Se não disserem nada, pergunte ao professor antes; sem autorização, não use.',
   ['Art. 27, caput', 'Art. 10, § 1º', 'Art. 30, caput, inciso VII', 'Art. 40, § 1º, inciso II'], 'prova+permissao+ia',
   exclui='camera melhor_ferramenta assistiva professor_usou objetiva', peso=6),
 F('gr_autoria', SO_GRA, 'autoria_superior', R_, 'Trabalho feito pela IA',
   'A IA fez meu trabalho ou TCC inteiro. Entrego assim?',
   'Não como seu: um texto que a IA escreveu inteiro não corresponde à sua autoria.',
   'Quem usa a IA responde pelo conteúdo, e a autoria deve ser compatível com a contribuição humana efetiva (art. 10, § 1º). O Glossário da resolução (Anexo I, verbete 19) define autoria intelectual como atribuição a pessoa natural pela concepção, elaboração e argumentação do trabalho. No TCC e na iniciação científica, a IA não assume autoria nem responsabilidade, e a contribuição relevante dela deve ser declarada (art. 28). A educação superior deve formar para os limites entre apoio tecnológico e produção intelectual própria (art. 30, VII), e a conduta e a consequência são definidas pela política da instituição (art. 27).',
   'O que a regra do curso ou da disciplina diz sobre IA? Você leu, conferiu as fontes e consegue sustentar cada parte do texto?',
   'Não entregue como está. Conte ao professor ou orientador o que a IA produziu e reescreva a partir da sua leitura e dos seus argumentos, declarando o apoio que restar.',
   ['Art. 10, § 1º', G19, 'Art. 28, caput', 'Art. 28, Parágrafo único', 'Art. 30, caput, inciso VII', 'Art. 27, caput'], 'ia+autoria', reforca='tarefa tcc',
   exclui='ferramenta_imposta coautor_usou texto_alheio grupo avaliado_por_ia sem_acesso', peso=18, destaque=1),
 F('gr_grupo', SO_GRA, 'grupo', Z, 'Trabalho em grupo',
   'Um colega usou IA na parte dele do trabalho em grupo. Eu respondo junto?',
   'A resolução não reparte a responsabilidade dentro do grupo: quem assina o trabalho responde pelo que entrega, e a regra da disciplina define o resto.',
   'Quem apresenta um conteúdo responde pela sua veracidade e consistência (art. 10, § 1º), e a resolução não diz como dividir essa responsabilidade entre os integrantes de um grupo: isso é regra da atividade e da instituição (art. 27). Decisões com repercussão sobre a trajetória dos estudantes ficam sujeitas a supervisão e validação humanas (art. 14, § 1º), e uma sanção não pode se fundar exclusivamente em detector de IA (art. 41, X).',
   'A atividade tinha regra sobre IA? O grupo conferiu a parte feita com IA antes de entregar? Dá para mostrar quem fez cada parte (versões, mensagens)?',
   'Antes de entregar, peça ao colega que diga o que a IA fez e confiram juntos esse trecho. Se já houve questionamento, reúnam o que mostra a parte de cada um e peçam que as partes sejam examinadas separadamente.',
   ['Art. 10, § 1º', 'Art. 27, caput', 'Art. 14, § 1º', 'Art. 41, caput, inciso X'], 'grupo+sancao|suspeita|usei|ia', peso=16),
 F('gr_objetiva', SO_GRA, 'correcao_objetiva', R_, 'Prova objetiva corrigida por sistema',
   'A prova objetiva foi corrigida pelo sistema e ninguém conferiu. Vale?',
   'Não sem validação humana: na prova objetiva o sistema pode corrigir como auxiliar, mas a nota só vale depois de conferida por uma pessoa.',
   'A correção automatizada de avaliações objetivas ou de resposta fechada é aplicação de alto risco e só pode ser usada como instrumento auxiliar: é vedada a atribuição automática de nota, aprovação ou reprovação sem validação humana efetiva, prévia, qualificada e documentada (art. 40, § 1º, I). Você tem direito a explicação e a contestação com revisão humana (art. 40, § 2º, V e VI), e a decisão sobre a nota fica com o profissional responsável (art. 40, § 3º).',
   'A nota já foi lançada? Algum professor conferiu o gabarito e o resultado antes? Há questão com gabarito errado ou anulada?',
   'Peça ao professor, por escrito, a conferência do gabarito e da sua prova. Se não houver resposta, peça revisão pelo canal do curso.',
   ['Art. 40, § 1º, inciso I', 'Art. 40, § 2º, inciso V', 'Art. 40, § 2º, inciso VI', 'Art. 40, § 3º'], 'objetiva', reforca='nota sistema ia', exclui='professor_usou', peso=22),
 F('gr_monitor', SO_GRA, 'monitoria', A, 'Monitoria',
   'Sou monitor da disciplina. Posso usar IA para tirar dúvidas, preparar material ou corrigir listas?',
   'Para preparar e tirar dúvidas, sim, informando o uso e conferindo. Para corrigir, só como apoio: a nota é do professor, e trabalho de colega não vai para plataforma externa.',
   'Materiais feitos com apoio de IA devem ter o uso informado e ser conferidos por quem os prepara (art. 14, § 2º). Na correção de textos autorais, a IA só entra como etapa preparatória, com leitura integral e correção humana (art. 40, § 4º; art. 41, IX); em listas e questões objetivas, a nota não pode ser atribuída automaticamente, sem validação humana (art. 40, § 1º, I). A avaliação permanece sob supervisão e validação humanas (art. 14, § 1º), e o monitor não substitui o professor nessa responsabilidade. Os trabalhos dos colegas são produções alheias e trazem dados pessoais: não entram em plataformas externas (Glossário, Anexo I, verbete 87).',
   'O professor da disciplina sabe e concorda com o uso? As listas trazem o nome dos colegas? Quem confere e lança a nota?',
   'Combine o uso com o professor da disciplina. Não envie trabalhos de colegas a ferramenta externa. Entregue ao professor a sua correção como sugestão, para que ele valide.',
   ['Art. 14, § 2º', 'Art. 40, § 4º, inciso II', 'Art. 41, caput, inciso IX', 'Art. 40, § 1º, inciso I', 'Art. 14, § 1º', G87], 'monitor+ia', peso=18),
 F('gr_panorama', SO_GRA, 'panorama', Z, 'O que muda na graduação',
   'O que a resolução permite e o que ela proíbe na graduação?',
   'Ela não proíbe a IA na graduação: manda a instituição ter política, deixa com você a responsabilidade pelo que entrega e fixa o que não vai para plataforma externa.',
   'Quatro regras alcançam você diretamente. A instituição deve estabelecer política própria de IA para ensino, pesquisa e gestão (art. 27), em até doze meses (art. 46), e o curso deve formar para o uso crítico da IA (art. 30). Quem apresenta um trabalho responde pelo conteúdo, e a autoria deve corresponder à contribuição humana (art. 10, § 1º); no TCC e na iniciação científica, a contribuição relevante da IA deve ser declarada (art. 28). No uso por conta própria, não entram em plataformas externas dados pessoais de terceiros, produções alheias nem informações sigilosas (Glossário, Anexo I, verbete 87). Valem desde já as vedações do art. 41, como nota de texto autoral dada só por IA e sanção fundada só em detector.',
   'A sua instituição já tem política de IA? A sua dúvida é sobre usar, declarar, dados ou avaliação?',
   'Escolha o assunto na lista para ver a ficha do seu caso.',
   ['Art. 27, caput', 'Art. 46, caput', 'Art. 30, caput', 'Art. 10, § 1º', 'Art. 28, caput', G87, 'Art. 41, caput, inciso IX', 'Art. 41, caput, inciso X'], 'panorama', reforca='ia', peso=15),
]

def _n(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))

def aplicar(sits, sinal_de, modelos):
    """Tira a graduação das fichas antigas, marca as comuns e acrescenta as derivadas e as novas."""
    por_id = {s['id']: s for s in sits}
    for s in sits:
        s['perfis'] = [p for p in s['perfis'] if p != GRA]
    for id_ in COMUNS:
        assert POS in por_id[id_]['perfis'], id_
        por_id[id_]['perfis'] = por_id[id_]['perfis'] + [GRA]
    novas = []
    for origem, id_, troca, campos in DERIVADAS:
        o = por_id[origem]
        assert POS in o['perfis'], origem
        s = dict(o, id=id_, perfis=[GRA], disp=list(o['disp']))
        s['sinal'] = o.get('sinal') or sinal_de(origem)
        s['modelo'] = o.get('modelo') or modelos.get(origem, '')
        for a, b in troca:
            assert any(a in s[c] for c in CAMPOS), (id_, a)
            for c in CAMPOS: s[c] = s[c].replace(a, b)
        for a, b in TROCAS:
            for c in CAMPOS: s[c] = s[c].replace(a, b)
        for k, v in campos.items():
            if k.endswith('+'): s[k[:-1]] = s[k[:-1]] + v
            else: s[k] = v
        texto = _n(' '.join(s[c] for c in CAMPOS)).replace('professor ou orientador', '').replace('professor orientador', '')
        m = re.search(MARCAS, texto)
        assert not m, (id_, m.group(0), texto[max(0, m.start() - 60):m.end() + 40])
        novas.append(s)
    return sits + novas + [dict(s, disp=list(s['disp'])) for s in NOVAS]

# Para o documento de revisão: o que mudou em cada ficha derivada.
def relatorio(sits):
    por_id = {s['id']: s for s in sits}
    return [(o, i, por_id[o], por_id[i]) for o, i, _, _ in DERIVADAS]
