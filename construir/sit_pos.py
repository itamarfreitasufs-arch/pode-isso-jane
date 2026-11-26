# Revisão do perfil Pós-graduação (v5.7, 25/11/2026), feita a partir da codificação da norma em 170 disposições.
# - As fichas passam a citar os anexos: 'Glossário, verbete N' (Anexo I) e 'Anexo II, quadro' ou 'Anexo II, critérios gerais'.
# - O perfil ganha fichas próprias no lugar das que vinham do ensino básico (SAI_DO_POS).
# - ALTERA corrige fichas existentes; SITUACOES traz as novas. Aqui o peso informado é o valor final.

POS = 'pos'
V, R_, A, Z = 'verde', 'vermelho', 'amarelo', 'azul'
G87, G88, G34, G27, G19, G86 = ('Glossário, verbete %d' % n for n in (87, 88, 34, 27, 19, 86))
QUADRO, GUIA = 'Anexo II, quadro', 'Anexo II, critérios gerais'

# Perfis publicados nesta versão. Os demais continuam no construtor e voltam ao tirar o argumento do build.
MENSAGEM_INATIVO = 'Por enquanto, este app responde só a dúvidas de estudantes de pós-graduação. Se é o seu caso, escolha o assunto na lista ou reescreva a pergunta.'

CONCEITOS = {
 'texto_alheio': r'\b(capitulo|texto|artigo|tese|dissertacao|projeto|manuscrito|trabalho|rascunho|codigo|parecer|relatorio|tcc|resumo)s? (d[aeo]s? )?(meu|minha|um|uma|outr[oa]|noss[oa]|algum|alguma)s? (colega\w*|amig\w*|orientand\w*|coorientand\w*|alun\w*|autor\w*|pessoa|pesquisador\w*)\b|\b(de|d[oa]s?) outr[oa]s? (autor\w*|pessoa\w*|pesquisador\w*)\b|\b(pdfs?|artigos|papers?|livros?|capitulos) .{0,40}\b(resenh\w*|resum\w*|fich\w*|ler|leia|analis\w*|revis\w*)\b|\b(subir|subo|colar|colo|jogar|jogo|mandar|mando|enviar|envio|carregar|carrego|upload|anexar|anexo) .{0,40}\b(pdfs?|artigos|papers?|livros?)\b|\b(sigilos\w*|confidencia\w*|documento\w* intern\w*|relatorio\w* intern\w*|patente\w*|nao publicad\w*|inedit\w*)\b',
 'ferramenta_imposta': r'\b(orientador\w*|professor\w*|coordenador\w*|coordenacao|programa|laboratorio|grupo) .{0,50}\b(exig\w*|obrig\w*|recomend\w*|indic\w*|impos|impoe|quer que|pediu que|pede que|mandou|manda) .{0,70}\b(us(ar|e|em|emos)|assin\w*|ferramenta\w*|pag\w*|instal\w*)\b|\b(sou|somos|e) obrigad\w+ a (usar|assinar|pagar|instalar)\b|\bquem (paga|responde) (pel[ao]|por) .{0,20}(ferramenta|assinatura|ia)\b',
 'sem_politica': r'\b(nao tem|sem|ainda nao (tem|existe|ha|criou|fez|aprovou)|nao existe|nao ha|nenhuma|nao criou|nao fez) .{0,30}\b(politica|regra|regras|norma|normas|regulament\w*|orientac\w*|diretriz\w*)\b|\b(ate quando|prazo|quando) .{0,60}\b(politica|adequ\w*|se adaptar|regulament\w*)\b',
 'disciplina': r'\b(disciplina\w*|materia|creditos|cadeira|trabalho final|seminario\w*|plano de ensino)\b',
 'selecao_bolsa': r'\b(selecao|processo seletivo|seletiv\w*|edital|candidat\w*|bolsas?|ranque\w*|classific\w+ (os )?(projetos|candidatos|curriculos)|comissao de (bolsas|selecao)|credenciamento|desligamento)\b',
 'prova_pos': r'\b(proficiencia|exame de qualificacao|qualificacao|prova d[ae] selecao|prova escrita|prova de (ingles|lingua\w*|conhecimentos)|anteprojeto|pre-?projeto)\b',
 'avaliado_por_ia': r'\b(parecer|nota|correcao|avaliacao|feedback|devolutiva|arguicao|ata)\b(?:(?!\b(texto|trabalho|tese|dissertacao|artigo|dizendo|disse|porque|alegando)\b).){0,60}\b(escrit\w*|feit\w*|gerad\w*|dad\w*|produzid\w*|redigid\w*) (por|pela|pelo|com|na|no) (uma? )?(ia|chat\w*|gpt|maquina|robo|sistema|plataforma)\b|\b(banca|professor\w*|avaliador\w*|orientador\w*) .{0,40}\b(usou|usaram|usa|colou|jogou) .{0,40}\b(ia|chat\w*|gpt)\b.{0,60}\b(corrig\w*|avali\w*|parecer|nota|ler)\b|\b(sem|nem) (ninguem|nenhum\w*( professor\w*| humano| avaliador\w*)?|a banca|o professor) (ler|leu|ter lido)\b|\b(ninguem|nenhum professor|nenhum humano|nenhum avaliador) (leu|le)\b',
 'docencia': r'\b(estagio (de |em )?docen\w*|docencia|monitoria|tirocinio)\b',
 'ajuste_fino': r'\b(fine-?tun\w*|ajuste fino|ajustar (um |o )?modelo|retreinar|treinar (um|o|meu|nosso) (proprio )?(modelo|llm|classificador|algoritmo))\b',
 'alimentar_empresa': r'\b(aliment\w*|abastec\w*|treinar|treinam|treinando|usad[oa]s? (pra|para) treinar|ced\w+|compartilh\w+|vend\w+|repass\w+) .{0,50}\b(empresa\w*|fornecedor\w*|terceir\w*|big tech|openai|google|microsoft|turnitin)\b|\b(minha|meu|minhas|meus|noss[oa]s?) (tese|dissertac\w+|texto|trabalho|artigo|dado)s? .{0,40}\b(treinar|aliment\w*|treinamento)\b',
 'minha_pesquisa': r'\b(minha|meu|nossa|nosso) (pesquisa|projeto|tese|dissertacao|estudo|experimento|coleta|doutorado|mestrado)\b .{0,80}\b(usa|utiliza|envolve|coleta|capta|analisa|mede|vai usar|vai medir|preve|inclui)\b|\b(pesquis\w+|estud\w+|investig\w+) (sobre|com|usando) (reconhecimento|emoc\w*|biometr\w*)\b',
 'ferramenta_ies': r'\b(universidade|faculdade|instituicao|programa|ies|biblioteca|reitoria|pro-?reitoria|campus) .{0,40}\b(liberou|oferec\w*|disponibiliz\w*|contratou|assinou|comprou|lancou|adotou|criou|fornece) .{0,40}\b(assistente\w*|ia|chat\w*|ferramenta\w*|copilot|gemini|gpt\w*|licenca\w*|tutor\w*)\b|\b(assistente|chatbot|ia|ferramenta) (institucional|oficial|da (universidade|faculdade|instituicao|biblioteca)|do programa)\b',
 'coautor_usou': r'\b(coautor\w*|co-autor\w*|colega\w*|parceir\w*|outro autor|segundo autor|primeiro autor) .{0,40}\b(usou|usaram|gerou|geraram|escreveu|fez|colocou|inseriu) .{0,60}\b(ia|chat\w*|gpt\w*|gemini|claude|copilot)\b',
 'fomento': r'\b(capes|cnpq|fapesp|faperj|fapemig|fapesb|facepe|fapitec|finep|agencias? de fomento|fomento|financiador\w*|relatorio (de|da) bolsa|prestacao de contas|pedido de (bolsa|auxilio))\b',
 'nao_declarei': r'\b(nao|nem|sem) (declarei|declarar|avisei|avisar|informei|mencionei|contei|falei|citei)\b|\bomiti\b|\bescondi\b|\besqueci de (declarar|avisar|mencionar|citar)\b',
}

# Núcleos novos e o assunto do menu a que pertencem.
NUCLEOS = {
 'usar': 'ferramenta_imposta assistente_ies uso_disciplina prova_pos',
 'avisar': 'declarar_disciplina nao_declarei',
 'autoria': 'coautor',
 'dados': 'textos_alheios treinar_pesquisa pesquisa_emocoes',
 'professor': 'estagio_docente',
 'pesquisa': 'fomento',
}

# Fichas compartilhadas com o ensino básico: saem do perfil, que recebe versão própria abaixo.
SAI_DO_POS = ['est_camera', 'est_gravar', 'est_melhor', 'prof_panorama', 'est_vigilancia', 'est_predicao', 'est_decisao']

DECLARAR_46 = ' As instituições têm doze meses, contados da publicação, para adequar políticas e práticas (art. 46).'

# Correções em fichas existentes. 'motivo+' acrescenta ao fim do texto; 'disp+' acrescenta dispositivos.
ALTERA = {
 'pos_uso': dict(
  pergunta='Posso usar IA na pesquisa do mestrado ou do doutorado, para revisar literatura, analisar dados, programar ou escrever?',
  resposta='Como apoio, com declaração do que for relevante; dados de outras pessoas e textos alheios não entram em plataforma externa.',
  motivo='Na pesquisa científica, o uso de IA deve preservar a integridade científica, a transparência metodológica e a responsabilidade intelectual, e a contribuição relevante da IA deve ser declarada (art. 28). A autoria e a responsabilidade pelos resultados permanecem com as pessoas pesquisadoras (art. 28, parágrafo único). O Glossário da resolução (Anexo I, verbete 87) sujeita o uso por conta própria às normas da instituição e veda inserir em plataformas externas dados pessoais de terceiros, produções alheias e informações institucionais sigilosas. A instituição deve ter política própria (art. 27) e tem até novembro de 2027 para adequá-la (art. 46).',
  conferir='O programa já tem política sobre IA? Você consegue conferir e explicar tudo o que a IA produziu? O que você vai enviar à ferramenta contém dados de participantes, texto de outra pessoa ou informação sigilosa?',
  acao='Combine o uso com a orientação. Registre em que etapas a IA entrou e confira cada resultado nas fontes. Antes de enviar um arquivo a uma ferramenta externa, retire dados de pessoas e textos que não são seus.',
  disp=['Art. 28, caput', 'Art. 28, Parágrafo único', G87, 'Art. 27, caput', 'Art. 46, caput']),
 'pos_declarar': dict(
  motivo='O art. 28 exige a declaração quando a contribuição da IA for relevante e mantém a autoria e a responsabilidade integralmente com a pessoa pesquisadora (parágrafo único). A resolução não diz quem decide o que é relevante: o juízo começa com você, e na dúvida é mais seguro declarar. A instituição pode definir a forma da declaração (art. 27, § 2º); se ainda não definiu, declare na seção de método ou em nota.',
  conferir='Sem a IA, esse trecho, essa análise ou esse código existiriam do mesmo jeito? O que a IA fez e o que entrou na versão final? O programa tem modelo ou local próprio para a declaração?'),
 'pos_revisao': dict(
  motivo='O art. 28 vincula a declaração à relevância da contribuição, e esse juízo cabe primeiro a você. Como indício, a resolução trata revisão textual não avaliativa, tradução e formatação como aplicações de baixo risco quando a instituição as adota (art. 38, § 1º, III e IV). A instituição pode pedir declaração também nesses casos (art. 27, § 2º).'),
 'pos_ordem': dict(
  resposta='A ordem de alguém não afasta o seu dever de declarar contribuição relevante; e a ferramenta que um docente exige passa a ser responsabilidade também da instituição.',
  motivo='O art. 28 exige a declaração do uso relevante e deixa a responsabilidade pelos resultados com a pessoa pesquisadora (parágrafo único): quem assina o trabalho responde por ele. Quanto à ferramenta, o Glossário da resolução (Anexo I, verbete 88) equipara ao uso institucional a recomendação ou a exigência de ferramenta externa por docente, no exercício da função e com anuência ou tolerância da instituição.',
  conferir='A contribuição da IA é relevante para o texto ou a análise? O programa tem regra escrita sobre declaração? A ferramenta exigida recebe dados de participantes ou textos de outras pessoas?',
  disp=['Art. 28, caput', 'Art. 28, Parágrafo único', G88], peso=14),
 'pos_historico': {
  'motivo+': ' O Glossário da resolução (Anexo I, verbete 87) sujeita o uso individual à declaração quando exigida e veda expor dados pessoais de terceiros, o que vale também para o histórico que você entregar.',
  'disp+': [G87]},
 'sup_retroativo': {'motivo+': DECLARAR_46, 'disp+': ['Art. 46, caput']},
 'sup_regimento': {
  'motivo+': ' As instituições têm doze meses, contados da publicação, para adequar regimentos e políticas (art. 46); a regra escrita pode ainda não ter sido revista.',
  'disp+': ['Art. 46, caput']},
 'pos_autoria': {
  'motivo+': ' O Glossário da resolução (Anexo I, verbete 19) define autoria intelectual como atribuição a pessoa natural ou grupo de pessoas.',
  'disp+': [G19], 'peso': 14, 'exclui+': ' ferramenta_imposta coautor_usou texto_alheio'},
 'pos_suspeita': dict(
  resposta='Peça que indiquem o fato, a regra e a evidência; resultado de detector não deve fundamentar sanção.',
  motivo='Detectores são admitidos apenas como elemento auxiliar de apuração (art. 40, § 1º, IX), e é vedada sanção fundada exclusivamente em seu resultado (art. 41, X). O Glossário da resolução (Anexo I, verbete 34) vai além: por causa de falsos positivos e falsos negativos, o detector não deve fundamentar sanções. Em avaliação e sanção, a dúvida se resolve pela interpretação mais protetiva (Anexo II). Você tem direito a explicação e a contestação com revisão humana (art. 40, § 2º, V e VI). A autoria e a responsabilidade continuam com você (art. 28, parágrafo único), então vale mostrar a sua contribuição.',
  exclui='professor_usou avaliado_por_ia',
  disp=['Art. 41, caput, inciso X', 'Art. 40, § 1º, inciso IX', G34, GUIA, 'Art. 40, § 2º, inciso V', 'Art. 40, § 2º, inciso VI', 'Art. 28, Parágrafo único']),
 'sup_sancao': dict(
  resposta='Uma sanção precisa de regra, fato e prova; resultado de detector não deve fundamentá-la, e ela não pode ser decidida só por um sistema.',
  motivo='A resolução veda sanção acadêmica ou disciplinar fundada exclusivamente em detector de IA (art. 41, X), e o Glossário (Anexo I, verbete 34) diz que o detector não deve fundamentar sanções. São vedadas também as decisões exclusivamente automatizadas sobre desligamento ou sanção (art. 41, V). Decisões relevantes exigem responsável humano, fundamentação, registro e possibilidade de revisão (art. 40, § 3º). A conduta proibida em si é definida pela política da instituição (art. 27).',
  disp=['Art. 41, caput, inciso X', G34, 'Art. 41, caput, inciso V', 'Art. 40, § 3º', 'Art. 27, caput']),
 'pos_nota': dict(
  motivo='É vedado atribuir nota, conceito ou mérito a texto autoral exclusivamente por sistema de IA ou sem correção humana (art. 41, IX), e essa vedação vale desde a publicação (art. 46). A correção humana exige leitura integral do seu texto e garante revisão por avaliador humano; não valem a homologação tácita, a validação em bloco nem a mera ratificação do que o sistema sugeriu (art. 40, § 4º). Também são vedadas decisões exclusivamente automatizadas com impacto relevante sobre a trajetória acadêmica (art. 29, parágrafo único). Um aviso que só orienta a revisão do trabalho, sem efeito sobre nota ou prazo, é devolutiva formativa e é admitido (art. 39, § 1º, II).',
  conferir='A saída do sistema alterou nota, prazo ou possibilidade de entregar? Alguma pessoa leu o seu texto por inteiro? Qual é o canal de revisão do programa?',
  disp=['Art. 41, caput, inciso IX', 'Art. 40, § 4º, inciso II', 'Art. 46, caput', 'Art. 29, Parágrafo único', 'Art. 39, § 1º, inciso II']),
 'pos_dados': dict(
  resposta='Em plataforma externa, não, se houver dados de pessoas; em ferramenta da instituição, só conforme o projeto aprovado e o termo de consentimento.',
  motivo='O Glossário da resolução (Anexo I, verbete 87) veda inserir em plataformas externas dados pessoais de estudantes, colegas ou terceiros, e o texto não abre exceção para o consentimento. Voz e fala transcrita de participantes são dados pessoais, e a resolução assegura a sua proteção (art. 10, § 2º). Em ferramenta contratada pela instituição, o tratamento segue o protocolo aprovado e o consentimento, que não pode ser genérico nem presumido (verbete 27). Na pesquisa, valem integridade e transparência metodológica (art. 28).',
  conferir='A ferramenta é externa (conta pessoal) ou contratada pela instituição? Os participantes são identificáveis pelo nome, pela voz ou pelo contexto? O termo de consentimento e o comitê de ética previram esse tratamento?',
  acao='Não envie o material a ferramenta externa. Se a instituição oferecer ferramenta própria, confira o protocolo e o termo. Anonimize os dados e registre a ferramenta e a etapa.',
  disp=[G87, 'Art. 10, § 2º', G27, 'Art. 28, caput']),
 'pos_dados_sensiveis': dict(
  motivo='O Glossário da resolução (Anexo I, verbete 87) veda inserir em plataformas externas dados pessoais de terceiros. Dados de saúde são dados pessoais sensíveis, que a resolução trata no nível de alto risco (art. 40, § 1º, V), e todo uso de IA deve ser examinado à luz da proteção de dados (art. 3º). Na pesquisa, valem a integridade científica e a responsabilidade de quem pesquisa (art. 28). O sigilo dos participantes decorre também da LGPD, do termo de consentimento e do comitê de ética, que vão além desta resolução. Declarar o uso depois não resolve a exposição dos dados.',
  disp=[G87, 'Art. 40, § 1º, inciso V', 'Art. 3, caput', 'Art. 28, caput']),
 'sup_assistiva': {
  'motivo+': ' Recursos com personalização ou tratamento sistemático de informações passam ao risco moderado, o que aumenta os deveres da instituição, não os seus (art. 39, § 1º, VII).',
  'disp+': ['Art. 39, § 1º, inciso VII']},
 'ori_parecerista': {
  'resposta': 'A resolução não rege periódicos; siga a política da revista e não envie manuscrito inédito a ferramenta externa.',
  'motivo+': ' O Glossário da resolução (Anexo I, verbete 87) veda inserir produções alheias em plataformas externas quando o uso se dá em contexto acadêmico; o texto não diz se a avaliação para uma revista entra nesse contexto, mas a cautela é a mesma.',
  'disp+': [G87]},
}

def F(id, nucleo, sinal, tema, pergunta, resposta, motivo, conferir, acao, disp, exige, reforca='', exclui='', peso=0, destaque=0, modelo=''):
    return dict(id=id, nucleo=nucleo, perfis=[POS], tema=tema, pergunta=pergunta, resposta=resposta, motivo=motivo, conferir=conferir,
                acao=acao, disp=disp, exige=exige, reforca=reforca, exclui=exclui, peso=peso, destaque=destaque, sinal=sinal, modelo=modelo)

SITUACOES = [
 # --- Posso usar IA? ---
 F('pos_ferramenta', 'ferramenta_imposta', Z, 'Ferramenta exigida pelo orientador',
   'Meu orientador exige ou recomenda uma ferramenta de IA. Quem responde por ela?',
   'Quando um docente exige ou recomenda a ferramenta no exercício da função, o uso conta como institucional, e a instituição responde junto.',
   'O Glossário da resolução (Anexo I, verbete 88) equipara ao uso institucional, para fins de responsabilidade, a recomendação ou a exigência de ferramenta externa por docente, no exercício de suas funções e com anuência ou tolerância institucional. O uso institucional atrai deveres reforçados de governança, transparência, formação e responsabilidade, e deve ser comunicado de forma clara aos estudantes (art. 13). A resolução distingue esse uso do que você faz por conta própria (art. 1º, § 4º). Ela não diz quem paga a ferramenta nem se você pode recusar.',
   'A exigência está escrita no plano de ensino, no regulamento ou em mensagem do orientador? A ferramenta vai receber dados de participantes ou textos de outras pessoas? Há alternativa para quem não pode pagar ou não quer criar conta?',
   'Peça a orientação por escrito, com a finalidade do uso. Pergunte à coordenação se a ferramenta foi avaliada pela instituição. Se ela for paga ou pedir dados seus, peça alternativa.',
   [G88, 'Art. 13, caput', 'Art. 1, § 4º'], 'ferramenta_imposta', exclui='declarar nao_declarei', peso=18),
 F('pos_assistente', 'assistente_ies', Z, 'Ferramenta oferecida pela instituição',
   'A universidade oferece um assistente de IA para escrita ou pesquisa. O que ela me deve?',
   'Aviso de que é IA, informação sobre finalidade, limites e responsáveis, e um canal para esclarecer e contestar. Conferir o que ele produz continua com você.',
   'Ferramentas de apoio à produção textual e à pesquisa adotadas pela instituição são aplicações de risco moderado (art. 39, § 1º, IV). A instituição deve comunicar o uso, as finalidades, os limites e os responsáveis, monitorar erros e manter canal de esclarecimento e contestação (art. 39, § 2º, I, IV e VI), e não pode usar os seus dados para treinar modelos de terceiros sem autorização específica e revogável (art. 39, § 2º, V). O Guia de Risco (Anexo II) acrescenta a identificação clara da interação automatizada e o monitoramento de alucinações. A responsabilidade pelo conteúdo que você apresenta continua sua (art. 10, § 1º), e o uso relevante na pesquisa deve ser declarado (art. 28).',
   'A instituição informou para que serve a ferramenta e quem responde por ela? Há um canal para relatar erros? Os seus textos e conversas ficam guardados ou são reutilizados?',
   'Leia o aviso de uso da ferramenta. Confira nas fontes tudo o que ela produzir. Se faltar informação sobre dados ou responsáveis, pergunte à coordenação ou à biblioteca.',
   ['Art. 39, § 1º, inciso IV', 'Art. 39, § 2º, inciso I', 'Art. 39, § 2º, inciso IV', 'Art. 39, § 2º, inciso V', 'Art. 39, § 2º, inciso VI', QUADRO, 'Art. 10, § 1º', 'Art. 28, caput'],
   'ferramenta_ies', exclui='alimentar_empresa treinar_modelo', peso=20),
 F('pos_disciplina', 'uso_disciplina', A, 'Uso de IA em disciplina',
   'Posso usar IA num trabalho de disciplina da pós?',
   'Como apoio, conforme o plano de ensino e a política da instituição; o trabalho e a responsabilidade continuam seus.',
   'Na educação superior, a IA pode ser objeto de estudo e recurso de apoio ao ensino, de forma planejada (art. 25), e cabe à instituição definir a política de uso (art. 27). A resolução não decide o que cada disciplina admite. Quem apresenta o trabalho responde pelo conteúdo, e a autoria deve corresponder à contribuição humana efetiva (art. 10, § 1º). Se o trabalho for aproveitado na pesquisa, vale a declaração do art. 28.',
   'O plano de ensino ou o professor disseram o que é permitido? A IA vai apoiar ou vai produzir o que será avaliado? O trabalho vai virar artigo ou capítulo da tese?',
   'Leia o plano de ensino. Na dúvida, pergunte ao professor antes de começar e guarde as suas versões.',
   ['Art. 25, caput', 'Art. 27, caput', 'Art. 10, § 1º', 'Art. 28, caput'], 'ia+disciplina+permissao', exclui='ferramenta_imposta', peso=3),
 F('pos_prova', 'prova_pos', Z, 'Seleção, proficiência e qualificação',
   'Posso usar IA na prova de seleção, de proficiência ou no exame de qualificação?',
   'A resolução não decide isso: vale o edital ou o regulamento do programa.',
   'A resolução deixa às instituições de educação superior definir as regras de uso de IA no ensino e na pesquisa (art. 27) e não trata de provas e exames específicos. O que ela fixa é que você responde pelo que apresenta e que a autoria deve corresponder à sua contribuição (art. 10, § 1º). Se a prova for monitorada por IA, valem os limites do monitoramento em avaliações (art. 40, § 1º, II). No texto de qualificação, que é parte da pesquisa, a contribuição relevante da IA deve ser declarada (art. 28).',
   'O edital ou o regulamento dizem o que pode ser consultado? A prova avalia justamente o que a ferramenta faria por você? O texto de qualificação já traz a declaração de uso?',
   'Leia o edital ou o regulamento. Se não disser nada, pergunte por escrito à comissão antes da prova.',
   ['Art. 27, caput', 'Art. 10, § 1º', 'Art. 40, § 1º, inciso II', 'Art. 28, caput'], 'prova_pos+permissao+ia', exclui='camera', peso=6),
 F('pos_melhor', 'melhor_ferramenta', Z, 'Escolha de ferramenta',
   'Qual é a melhor IA para a pesquisa ou para escrever a tese?',
   'Este app não recomenda ferramentas; ele explica as regras de uso.',
   'A resolução não indica produtos. Na educação superior, cada instituição define a sua política (art. 27). Se o programa ou o orientador indicarem uma ferramenta, o uso passa a contar como institucional (Glossário, Anexo I, verbete 88). Em qualquer ferramenta externa, não entram dados de outras pessoas, textos alheios nem informações sigilosas (verbete 87).',
   'A instituição oferece ou indica alguma ferramenta? O que você pretende enviar a ela?',
   'Pergunte à coordenação ou à biblioteca se há ferramenta contratada pela instituição e para qual uso.',
   ['Art. 27, caput', G88, G87], 'melhor_ferramenta', exclui='ferramenta_imposta', peso=20),
 # --- Avisar ou declarar o uso ---
 F('pos_nao_declarei', 'nao_declarei', Z, 'Uso não declarado',
   'Usei IA na pesquisa e não declarei. O que pode acontecer?',
   'A resolução não prevê punição para quem não declarou; a consequência, se houver, vem das regras da instituição. Dá para regularizar.',
   'O art. 28 exige declarar a contribuição relevante da IA, mas a resolução não fixa sanção para o descumprimento. O Glossário da resolução (Anexo I, verbete 87) sujeita o uso individual às normas institucionais e aos deveres de integridade acadêmica e científica; a conduta e a sanção são definidas pelo regimento e pela política da instituição (art. 27). Uma sanção não pode se fundar só em detector de IA (art. 41, X).',
   'A contribuição da IA foi relevante para o texto, os dados ou o código? O trabalho já foi defendido ou publicado? O regimento do programa trata de declaração de uso?',
   'Reúna as versões e descreva o que a IA fez. Conte ao orientador e apresente a declaração pelo procedimento do programa. Se o trabalho já foi publicado, consulte o editor sobre como registrar.',
   ['Art. 28, caput', G87, 'Art. 27, caput', 'Art. 41, caput, inciso X'], 'nao_declarei+ia', reforca='pesquisa', exclui='ordem incompleta coautor_usou retroativo', peso=14),
 F('pos_disc_declarar', 'declarar_disciplina', Z, 'Declaração em disciplina',
   'Usei IA num trabalho de disciplina da pós. Tenho que declarar?',
   'Em trabalho de disciplina, a resolução não exige por si; vale a regra do professor e da instituição. Na dúvida, declare em uma linha.',
   'A declaração obrigatória do art. 28 é a da pesquisa científica. Para atividades de ensino, as instituições podem definir formas de declaração (art. 27, § 2º), e a resolução pede transparência quanto ao uso (art. 10, § 1º). Se o trabalho da disciplina virar artigo, capítulo ou projeto, passa a valer o art. 28.',
   'O plano de ensino pede que o uso seja informado? O que a IA mudou no trabalho? O texto vai ser aproveitado na dissertação ou na tese?',
   'Confira o plano de ensino. Se não houver regra, informe em uma linha o que a IA fez e guarde a versão anterior.',
   ['Art. 28, caput', 'Art. 27, § 2º', 'Art. 10, § 1º'], 'ia+disciplina+usei|declarar', reforca='declarar', exclui='ferramenta_imposta', peso=4),
 # --- Trabalho feito com IA ---
 F('pos_coautor', 'coautor', Z, 'Coautoria',
   'Um coautor usou IA no artigo sem me dizer. Respondo por isso?',
   'A resolução deixa a responsabilidade com as pessoas pesquisadoras, sem repartir entre coautores: quem assina responde pelo conjunto.',
   'O uso de IA não transfere à tecnologia a autoria nem a responsabilidade pelos resultados, que permanecem integralmente com as pessoas pesquisadoras (art. 28, parágrafo único). A contribuição relevante da IA deve ser declarada (art. 28), e cada pesquisador responde pela veracidade e pela consistência do que apresenta (art. 10, § 1º). A resolução não diz como dividir a responsabilidade entre coautores; isso segue as regras de integridade da instituição e da revista.',
   'O que a IA fez no trabalho? O artigo já foi submetido ou publicado? A revista ou o programa exigem declaração de uso?',
   'Peça ao coautor que descreva o que a IA fez. Confira esse trecho nas fontes e nos dados. Combinem a declaração antes de submeter; se já foi publicado, consultem o editor.',
   ['Art. 28, Parágrafo único', 'Art. 28, caput', 'Art. 10, § 1º'], 'coautor_usou', reforca='responsavel', exclui='ordem', peso=24),
 # --- Nota ou correção por IA ---
 F('pos_parecer_ia', 'nota_estudante', Z, 'Parecer ou nota sem leitura',
   'Desconfio que o parecer da banca foi escrito por IA, sem leitura do meu texto. O que posso pedir?',
   'Peça a confirmação de que o seu texto foi lido por inteiro por um avaliador e, se não foi, a revisão humana.',
   'O avaliador pode usar IA como apoio preparatório, mas a nota de texto autoral exige leitura integral e apreciação direta por pessoa, com direito a revisão por avaliador humano; não valem a homologação tácita, a validação em bloco nem a mera ratificação do que o sistema sugeriu (art. 40, § 1º, X, e § 4º). Nota ou mérito atribuídos só por IA são vedados (art. 41, IX). A suspeita, sozinha, não prova que não houve leitura: o caminho é pedir esclarecimento.',
   'O parecer trata de pontos específicos do seu texto ou é genérico? A nota já produziu efeito (aprovação, reprovação, prazo)? O programa tem canal de revisão ou recurso?',
   'Anote o que no parecer levanta a dúvida. Peça ao avaliador ou à coordenação, por escrito, que confirmem a leitura integral e expliquem a nota. Se couber, peça revisão por outro avaliador.',
   ['Art. 40, § 1º, inciso X', 'Art. 40, § 4º, inciso II', 'Art. 41, caput, inciso IX'], 'avaliado_por_ia', exclui='detector parecerista docencia', peso=22,
   modelo='Solicito a confirmação de que [o texto] foi lido integralmente por avaliador humano e a fundamentação de [nota ou parecer]. Caso a avaliação tenha se apoiado em sistema de IA, solicito revisão por avaliador humano, nos termos do art. 40, § 4º, da Resolução CNE/CP nº 1/2026.'),
 # --- Decisão ou previsão automática ---
 F('pos_selecao', 'decisao_estudante', R_, 'Seleção, bolsas e desligamento',
   'Um sistema de IA classificou candidatos na seleção, distribuiu bolsas ou decidiu um desligamento. Vale?',
   'Seleção, bolsa, sanção e desligamento não podem ser decididos só pela máquina: precisam de uma pessoa responsável, antes, e de possibilidade de revisão.',
   'São vedadas as decisões exclusivamente automatizadas com efeitos relevantes sobre seleção, benefícios, permanência, sanção ou desligamento (art. 41, V; art. 29, parágrafo único), e essa vedação vale desde a publicação (art. 46). Sistemas ligados a seleção, concessão de benefícios e análise disciplinar são de alto risco: a decisão fica com profissional ou instância competente, com fundamentação, registro e revisão (art. 40, § 1º, IV, e § 3º), e você tem direito a explicação e contestação (art. 40, § 2º, V e VI). O Guia de Risco (Anexo II) inclui as triagens e os ranqueamentos que condicionam de fato a decisão humana e equipara à decisão automatizada a supervisão meramente formal.',
   'Uma pessoa ou comissão analisou cada caso antes de o resultado valer? O edital informou o uso do sistema e o critério? Há canal de recurso?',
   'Peça por escrito quem validou o resultado e com que critério. Solicite revisão do seu caso por uma pessoa ou comissão. Guarde o edital e as mensagens.',
   ['Art. 41, caput, inciso V', 'Art. 29, Parágrafo único', 'Art. 46, caput', 'Art. 40, § 1º, inciso IV', 'Art. 40, § 3º', 'Art. 40, § 2º, inciso V', 'Art. 40, § 2º, inciso VI', QUADRO],
   'decisao_auto|selecao_bolsa', reforca='ia sistema decidir', exclui='panorama proibir_tudo fomento', peso=20),
 F('pos_predicao', 'predicao_estudante', Z, 'Sistema que prevê desempenho',
   'Um sistema previu que eu ia reprovar ou abandonar o curso e perdi uma oportunidade. Pode?',
   'A previsão pode servir para oferecer apoio; não pode, sozinha, tirar de você bolsa, vaga ou atividade, e você tem direito a explicação e revisão.',
   'Predição de desempenho ou evasão é aplicação de alto risco (art. 40, § 1º, VI): exige explicação acessível e possibilidade efetiva de contestação e revisão humana (art. 40, § 2º). São vedados os sistemas que produzam exclusão de estudantes com base em inferências automatizadas sobre desempenho (art. 41, VIII) e a perfilização para restringir oportunidades educacionais (art. 41, IV). Benefícios e permanência ficam sob decisão de pessoa ou instância competente (art. 40, § 3º).',
   'Alguém do programa analisou o seu caso antes da decisão? Explicaram o critério? O que você perdeu: bolsa, vaga, atividade?',
   'Peça à coordenação, por escrito, o critério usado, quem validou a decisão e a revisão do seu caso por uma pessoa.',
   ['Art. 40, § 1º, inciso VI', 'Art. 40, § 2º', 'Art. 41, caput, inciso IV', 'Art. 41, caput, inciso VIII', 'Art. 40, § 3º'], 'predicao', peso=27),
 # --- Câmeras, dados e imagens ---
 F('pos_textos', 'textos_alheios', A, 'Textos de outras pessoas e documentos internos',
   'Posso colar numa IA o texto de um colega, um artigo de outro autor ou um documento interno do laboratório?',
   'Texto inédito de outra pessoa e documento sigiloso, não. Para obra já publicada, a resolução não distingue: prefira ferramenta da instituição.',
   'O Glossário da resolução (Anexo I, verbete 87) veda inserir em plataformas externas produções alheias e informações institucionais sigilosas, além de dados pessoais de terceiros. A regra vale para o uso por conta própria em contexto acadêmico. O texto não separa obra inédita de obra publicada: para um artigo já publicado o risco é menor, mas a resolução não abre a exceção, e os direitos autorais e a licença da obra continuam valendo. Você responde pelo que faz com o material (art. 10, § 1º).',
   'O texto é inédito (rascunho, capítulo, manuscrito, projeto) ou já foi publicado? O autor autorizou? A ferramenta guarda ou reutiliza o que recebe? A instituição oferece ferramenta própria?',
   'Não envie texto inédito de outra pessoa nem documento interno a ferramenta externa. Para obra publicada, use de preferência ferramenta contratada pela instituição e respeite a licença. Na dúvida, peça autorização ao autor.',
   [G87, 'Art. 10, § 1º'], 'texto_alheio', reforca='ia', exclui='parecerista inventar coautor_usou', peso=24),
 F('pos_treinar', 'treinar_pesquisa', A, 'Treinar modelo com dados de alunos',
   'Posso treinar ou ajustar um modelo com redações, notas ou dados de alunos coletados na pesquisa?',
   'Com dados de crianças e adolescentes, não, se o modelo for de terceiros; nos demais casos, só com base legal, autorização específica e aprovação ética.',
   'É vedado usar dados educacionais de crianças e adolescentes para treinar modelos de IA de terceiros (art. 41, XI), e os conteúdos produzidos por eles não admitem nem a ressalva da autorização (art. 15, parágrafo único). Para conteúdos de docentes e de estudantes adultos, o uso em modelos de terceiros depende de autorização específica (art. 15). O Glossário da resolução (Anexo I, verbete 86) inclui o ajuste fino no conceito de treinamento e exige base legal, finalidade legítima, minimização e segurança. A resolução não diz se o modelo que você mesmo treina, dentro da instituição, é de terceiros: se ele roda no serviço de uma empresa, trate como tal.',
   'Os dados são de crianças ou adolescentes? O modelo roda em infraestrutura da instituição ou no serviço de uma empresa? O comitê de ética e o termo de consentimento previram o treinamento?',
   'Descreva o treinamento no projeto e no termo de consentimento. Anonimize os dados e prefira infraestrutura da instituição. Com dados de menores, não use serviço de terceiros.',
   ['Art. 41, caput, inciso XI', 'Art. 15, Parágrafo único', 'Art. 15, caput', G86], 'treinar_modelo|ajuste_fino', reforca='dados_pesq', peso=22),
 F('pos_meus_textos', 'conteudo_treino', R_, 'Meus textos usados para treinar IA',
   'Minha dissertação ou meus textos vão alimentar o sistema de IA de uma empresa. Pode, sem me perguntar?',
   'Sem a sua autorização específica, é vedado usar conteúdos de estudantes para treinar modelos de IA de terceiros.',
   'A resolução veda utilizar conteúdos produzidos por docentes e estudantes para treinar modelos de IA de terceiros, salvo autorização específica (art. 15). Para dados educacionais em geral, a autorização precisa ser específica e revogável, com finalidade legítima e transparência (art. 39, § 2º, V). Os contratos da instituição devem prever governança e responsabilização dos fornecedores (art. 5º). O consentimento não pode ser genérico nem presumido (Glossário, Anexo I, verbete 27): um aviso geral ou um termo aceito na matrícula não é autorização específica.',
   'O que exatamente será enviado: textos, dados de uso, conversas? Você assinou autorização específica para isso? Dá para revogar?',
   'Peça à coordenação ou ao encarregado de dados, por escrito, o que é enviado ao fornecedor e com que base. Se não autorizou, diga que não autoriza e peça a exclusão.',
   ['Art. 15, caput', 'Art. 39, § 2º, inciso V', 'Art. 5, caput', G27], 'alimentar_empresa', peso=26),
 F('pos_emocoes', 'pesquisa_emocoes', A, 'Pesquisa com emoções ou biometria',
   'Minha pesquisa usa reconhecimento de emoções ou biometria de estudantes. Pode?',
   'Só como pesquisa aprovada por comitê de ética, e sem nenhum efeito sobre nota, disciplina ou seleção dos participantes.',
   'O reconhecimento e a inferência de emoções de estudantes são vedados (art. 41, II), mas a vedação não alcança a pesquisa científica aprovada por comitê de ética em pesquisa, desde que não haja qualquer repercussão avaliativa, disciplinar ou seletiva (art. 41, § 2º). A exceção é só para o inciso II: a vigilância biométrica contínua e o monitoramento permanente continuam vedados (art. 41, VI). O consentimento dos participantes não pode ser genérico nem presumido (Glossário, Anexo I, verbete 27).',
   'O projeto foi aprovado pelo comitê de ética com essa coleta descrita? Os resultados chegam a professores ou à gestão de forma identificada? A coleta é pontual ou contínua?',
   'Descreva a coleta no protocolo e no termo de consentimento. Garanta que nenhum resultado individual chegue à avaliação ou à disciplina dos participantes. Limite a coleta ao tempo do estudo.',
   ['Art. 41, caput, inciso II', 'Art. 41, § 2º', 'Art. 41, caput, inciso VI', G27], 'emocao|camera+minha_pesquisa', peso=14),
 F('pos_camera', 'camera_estudante', A, 'Câmera e monitoramento em prova',
   'A instituição quer me filmar ou me monitorar com IA durante uma prova ou defesa. Pode?',
   'Só como verificação pontual, com salvaguardas e alternativa não biométrica; vigilância contínua, leitura de emoções e devassa do ambiente de casa são vedadas.',
   'Sistemas de monitoramento em avaliações são de alto risco e exigem transparência, supervisão humana, possibilidade de contestação e a alternativa menos invasiva disponível (art. 40, § 1º, II, e § 2º). O Guia de Risco (Anexo II) limita esse monitoramento a verificações pontuais, com alternativa não biométrica assegurada, e põe no risco excessivo o monitoramento invasivo, com devassa do ambiente íntimo. A vigilância biométrica contínua, o monitoramento permanente e o reconhecimento de emoções são vedados (art. 41, II e VI). Punir automaticamente pelo que o sistema marcou, sem que uma pessoa examine o caso, é decisão exclusivamente automatizada, também vedada (art. 41, V).',
   'O monitoramento é pontual ou dura a prova inteira? Ele filma o cômodo onde você está? Ofereceram alternativa sem biometria? Explicaram como contestar um resultado?',
   'Peça à coordenação, por escrito, a finalidade, o que é gravado, quem analisa e qual é a alternativa não biométrica. Se o sistema apontar irregularidade, peça que uma pessoa examine antes de qualquer efeito.',
   ['Art. 40, § 1º, inciso II', 'Art. 40, § 2º, inciso IX', QUADRO, 'Art. 41, caput, inciso II', 'Art. 41, caput, inciso VI', 'Art. 41, caput, inciso V', 'Art. 41, § 1º'],
   'camera+prova|prova_pos', reforca='decisao_auto', exclui='minha_pesquisa', peso=14),
 F('pos_vigilancia', 'vigilancia_estudante', R_, 'Câmera que mede atenção ou emoção',
   'Vão instalar câmera ou sensor que mede atenção, cansaço ou emoção em sala ou no laboratório. Pode?',
   'Medir atenção ou emoção e vigiar de forma contínua são práticas vedadas.',
   'A resolução veda a vigilância emocional e o reconhecimento ou a inferência de emoções de estudantes (art. 41, II), a perfilização comportamental para classificar ou disciplinar (art. 41, IV) e a vigilância biométrica contínua ou o monitoramento permanente (art. 41, VI). Essas vedações valem desde a publicação (art. 46). O Guia de Risco (Anexo II) diz que a vedação não se convalida por consentimento.',
   'O sistema observa as pessoas de forma contínua? Ele informa quem está distraído, cansado ou triste?',
   'Peça à coordenação ou à ouvidoria que explique por escrito o que o sistema faz, citando o art. 41.',
   ['Art. 41, caput, inciso II', 'Art. 41, caput, inciso IV', 'Art. 41, caput, inciso VI', 'Art. 46, caput', QUADRO], 'emocao|camera', exclui='prova prova_pos identidade', peso=22),
 F('pos_gravar', 'gravar_aula', A, 'Gravar a aula',
   'Posso gravar a aula e jogar na IA pra fazer resumo?',
   'Gravar, só com autorização do professor; e voz e imagem de outras pessoas não entram em plataforma externa.',
   'A resolução assegura a proteção da imagem, da voz e dos dados de profissionais da educação e estudantes diante da IA (art. 10, § 2º). O Glossário da resolução (Anexo I, verbete 87) veda inserir em plataformas externas dados pessoais de terceiros, e a voz do professor e dos colegas é dado pessoal. A resolução não regula a gravação de aulas em si; isso depende da regra da instituição.',
   'O professor e os colegas aparecem ou falam na gravação? A instituição tem regra sobre gravar aulas? Há ferramenta de transcrição oferecida pela instituição?',
   'Peça autorização ao professor e diga para que vai usar. Prefira ferramenta da instituição. Se precisar só de um resumo, use as suas anotações em vez do áudio.',
   ['Art. 10, § 2º', G87], 'gravar_aula', peso=19),
 # --- Professor e IA ---
 F('pos_estagio', 'estagio_docente', A, 'Estágio docente',
   'No estágio docente, posso usar IA para preparar aula ou corrigir trabalhos?',
   'Para preparar, sim, informando o uso e conferindo o conteúdo. Para corrigir texto autoral, só como apoio: a leitura e a nota são de uma pessoa.',
   'O uso de IA para elaborar materiais e atividades deve ser informado de forma clara e não afasta a responsabilidade de quem prepara pela verificação do conteúdo (art. 14, § 2º); cabe à mediação docente a interpretação crítica do que a IA produz (art. 8º, § 1º). Na correção de textos autorais, a IA só entra como etapa preparatória: a nota exige leitura integral e correção humana, e são vedadas a validação em bloco e a mera ratificação do que o sistema sugeriu (art. 40, § 4º; art. 41, IX). A resolução veda substituir a atuação docente por sistemas automatizados (art. 14). No estágio, a nota é responsabilidade do professor da disciplina.',
   'O professor supervisor sabe e concorda com o uso? Os trabalhos dos alunos vão para ferramenta externa? Quem lê cada texto antes da nota?',
   'Combine o uso com o professor supervisor. Informe aos alunos quando o material tiver apoio de IA e confira tudo antes da aula. Não envie trabalhos de alunos a ferramenta externa: são produções alheias (Glossário, Anexo I, verbete 87).',
   ['Art. 14, § 2º', 'Art. 8, § 1º', 'Art. 40, § 4º, inciso II', 'Art. 41, caput, inciso IX', 'Art. 14, caput', G87], 'estagio|docencia+ia', peso=16),
 # --- Revistas e publicações ---
 F('pos_fomento', 'fomento', Z, 'Agências de fomento',
   'A agência de fomento aceita projeto ou relatório feito com IA?',
   'Isso depende da agência: a resolução vale para sistemas e instituições de ensino e não alcança as agências de fomento.',
   'A resolução se dirige aos sistemas de ensino e às instituições educacionais (art. 1º). Agências de fomento têm regras próprias, que podem exigir declaração ou proibir o uso em certas etapas. O que a resolução exige de você na pesquisa continua valendo: declarar a contribuição relevante da IA e responder pelo conteúdo (art. 28).',
   'O edital ou o manual da agência falam de IA? O que a IA fez no projeto ou no relatório?',
   'Leia o edital e o manual da agência. Se não disserem nada, declare o uso relevante e, na dúvida, consulte a agência por escrito.',
   ['Art. 1, caput', 'Art. 28, caput', 'Art. 28, Parágrafo único'], 'fomento', peso=28),
 # --- Sobre a resolução ---
 F('pos_panorama', 'panorama', Z, 'O que muda na pós-graduação',
   'O que a resolução permite e o que ela proíbe na pós-graduação?',
   'Ela não proíbe a IA na pós: manda a instituição ter política, exige declarar o uso relevante na pesquisa e fixa o que não vai para plataforma externa.',
   'Três regras alcançam você diretamente. A instituição deve estabelecer política própria de IA para ensino, pesquisa e gestão (art. 27), em até doze meses (art. 46). Na pesquisa, a contribuição relevante da IA deve ser declarada, e a autoria e a responsabilidade são suas (art. 28). No uso por conta própria, não entram em plataformas externas dados pessoais de terceiros, produções alheias nem informações sigilosas (Glossário, Anexo I, verbete 87). Valem desde já as vedações do art. 41, como nota de texto autoral dada só por IA e sanção fundada só em detector.',
   'O seu programa já tem política de IA? A sua dúvida é sobre usar, declarar, dados ou avaliação?',
   'Escolha o assunto na lista para ver a ficha do seu caso.',
   ['Art. 27, caput', 'Art. 46, caput', 'Art. 28, caput', G87, 'Art. 41, caput, inciso IX', 'Art. 41, caput, inciso X'], 'panorama', reforca='ia', peso=15),
 F('pos_prazo', 'prazo', Z, 'Programa sem política de IA',
   'Meu programa ainda não tem política de IA. O que vale até lá?',
   'A instituição tem até novembro de 2027 para criar a política. Até lá, valem as regras que o programa já tem, as vedações do art. 41 e o que a resolução pede de quem pesquisa.',
   'As instituições de educação superior devem estabelecer políticas próprias de IA (art. 27) e têm doze meses, contados da publicação, para adequar políticas, práticas e contratos; as vedações do art. 41 se aplicam de imediato (art. 46). A resolução está em vigor desde a publicação (art. 47), e o que ela pede de quem pesquisa não depende da política: declarar a contribuição relevante da IA (art. 28) e responder pelo conteúdo (art. 10, § 1º). Ela não diz, com todas as letras, se esses deveres individuais também esperam os doze meses; o caminho seguro é cumpri-los desde já.',
   'O regimento ou o plano de ensino já dizem algo sobre IA? O seu orientador combinou alguma regra? O que você pretende fazer com a IA?',
   'Pergunte à coordenação se há regra provisória. Combine o uso por escrito com o orientador. Declare desde já o uso relevante na pesquisa.',
   ['Art. 27, caput', 'Art. 46, caput', 'Art. 47, caput', 'Art. 28, caput', 'Art. 10, § 1º', 'Art. 41, caput'], 'sem_politica|prazo', reforca='politica', peso=20),
]
