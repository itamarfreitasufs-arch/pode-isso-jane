# v5.23 (27/11/2026): correções do teste com graduandos (parecer de 26/11/2026, itens 1 a 10 do app).
GRA = 'graduacao'
V, R_, A, Z = 'verde', 'vermelho', 'amarelo', 'azul'

# Conceitos novos (texto normalizado: minúsculas, sem acento).
CONCEITOS = {
 'reescrevi': r'\b(reescrev\w*|parafrase\w*|parafrasea\w*|minhas (proprias )?palavras|outras palavras|(mud|troc)\w+ (as |umas |algumas )?palavras|adapt\w+ o texto)\b',
 'estudo_ia': r'\b(resumir|resumos? (de|do|da|dos|das) (texto|textos|livro|livros|capitulo|capitulos|artigo|artigos|materia|conteudo|aula)|fichament\w*|fichar|anotac\w+|anotar|mapas? menta\w*|flashcards?|cronograma de estud\w+|(pra|para) (eu )?estudar|estudar (pra|para) (a |as )?provas?|me explic\w+|explic\w+ (a |o )?(materia|conteudo|texto|assunto|exercicio))\b',
 'como_declarar': r'\bcomo (eu )?(devo |posso |tenho que |preciso |vou |faco pra |faco para )?(declar\w+|descrev\w+|escrev\w+|redig\w+|cit\w+|mencion\w+|informar|coloc\w+|fac\w+|fic\w+)\b.{0,40}\b(declarac\w+|uso|usei|ia|chat\w*|gpt|gemini|ferramenta|descrit\w+)\b|\b(modelo|exemplo|texto) d[ae] declarac\w+\b|\bcomo (pode|deve|devo|tem que|precisa) (estar |ser |ficar )?(descrit\w+|declarad\w+|escrit\w+)\b',
 'anulou': r'\b(anul\w+|zer\w+ (a |o |minha |meu )?(nota|trabalho|prova)|tiraram (a |minha )?nota|deu zero|levei zero|tirei zero)\b',
}
# "o professor deu minha nota usando IA" (item 8): "deu minha nota" não era reconhecido.
AMPLIA = {
 'autoria': r'\b(totalmente|completamente|integralmente|inteiramente) (feit|escrit|gerad|produzid)\w*\b|\b(feit|escrit|gerad|produzid)\w* (totalmente|completamente|integralmente|inteiramente)\b',
 'avaliado_por_ia': r'\b(professor\w*|avaliador\w*|tutor\w*) .{0,30}\b(deu|dar|da|lancou|atribuiu) (a |as |minha |minhas |meu )?(nota|notas|conceito) .{0,50}\b(com|pela|pelo|usando|na|no|por) (a |o )?(ia|chat\w*|gpt|inteligencia artificial)\b',
}

# Item 1 e 6: fichas "Em parte" da graduação abrem com Sim ou Não, em frases curtas.
AJUSTES = {
 'gr_disciplina': dict(resposta='Sim, como apoio, se o plano de ensino e a regra da instituição permitirem. O trabalho e a responsabilidade continuam sendo seus.'),
 'gr_tcc': dict(resposta='Sim, como apoio, declarando o que a IA fez de relevante. Mas dados de outras pessoas e textos de outros autores não podem ir para o ChatGPT ou outra IA aberta.'),
 'gr_ead': dict(sinal=R_, resposta='Não como substituto. A IA pode ajudar na tutoria, mas não substitui o professor nem o tutor que o curso é obrigado a oferecer.'),
 'gr_pratica': dict(resposta='Sim, como apoio, desde que você continue capaz de fazer e de decidir sem o aplicativo. A IA não pode tomar o lugar da prática que o curso ensina.'),
 'gr_estagio': dict(resposta='Sim, como apoio, se o supervisor souber e sem enviar dados de outras pessoas. Para dar nota a redação de aluno, não: isso exige a leitura e a correção de um professor.'),
 'gr_declarar': dict(resposta='Sim, se a IA ajudou de forma relevante no texto, nos dados, na revisão de literatura, no código ou em outra etapa. Na dúvida, declare.'),
 'gr_revisao': dict(resposta='Em geral, não: a resolução só exige declarar quando a ajuda da IA é relevante, e corrigir vírgulas, formatar ou traduzir costuma não ser. Mas a regra do curso ou do professor pode pedir. Na dúvida, declare em uma linha.'),
 'pos_gravar': dict(resposta='Não sem autorização do professor. E, mesmo com ela, a voz e a imagem de outras pessoas não podem ir para o ChatGPT ou outra IA aberta.'),
 'gr_camera': dict(resposta='Só para conferir a sua identidade num momento pontual, com cuidados e uma alternativa sem biometria. Filmar o tempo todo, ler suas emoções ou vasculhar a sua casa, não.'),
 'gr_textos': dict(resposta='Não, se for texto inédito de outra pessoa, como o trabalho de um colega ou o material do professor. Para artigo já publicado, a resolução não abre exceção: prefira a ferramenta da instituição.'),
 'sup_facial': dict(resposta='Conferir a sua identidade num momento pontual é permitido. Mas o rosto é dado sensível: só se for mesmo necessário e se não houver jeito menos invasivo.'),
 'gr_monitor': dict(resposta='Sim, para preparar material e tirar dúvidas, avisando que usou IA e conferindo tudo. Para corrigir listas, só como apoio: a nota é do professor, e o trabalho dos colegas não vai para IA aberta.'),
 # Item 4: exemplo de declaração também no trabalho de disciplina.
 'gr_disc_declarar': dict(modelo='Usei o [ChatGPT] para [revisar a redação e sugerir um roteiro]. Conferi o resultado e reescrevi o que aproveitei. O conteúdo do trabalho é de minha responsabilidade.'),
}

def F(id, nucleo, sinal, tema, pergunta, resposta, motivo, conferir, acao, disp, exige, reforca='', exclui='', peso=0, destaque=0, modelo=''):
    return dict(id=id, nucleo=nucleo, perfis=[GRA], tema=tema, pergunta=pergunta, resposta=resposta, motivo=motivo, conferir=conferir,
                acao=acao, disp=disp, exige=exige, reforca=reforca, exclui=exclui, peso=peso, destaque=destaque, sinal=sinal, modelo=modelo)

# Fichas novas, cada uma com a ficha depois da qual aparece no menu.
NOVAS = [
 # Item 10: a ficha das vírgulas também em "Posso usar IA?", logo depois do trabalho de disciplina.
 ('gr_disciplina', F('gr_revisar_usar', 'uso_disciplina', A, 'Revisão de vírgulas, ortografia e tradução',
   'Posso usar IA só para corrigir vírgulas, ortografia ou traduzir?',
   'Sim, para revisar a forma do seu texto, conferindo o resultado. Se precisa declarar depende da regra do curso; na dúvida, declare em uma linha.',
   'Na educação superior, a IA pode ser usada como apoio às atividades de ensino (art. 25), e cada instituição define a sua política de uso (art. 27). Quem entrega responde pelo texto final, inclusive pelo que a ferramenta mudou (art. 10, § 1º). A resolução só exige declarar, na pesquisa, a contribuição relevante da IA (art. 28), e revisar a forma costuma não ser relevante. Em trabalho de disciplina, se e como declarar fica com a regra da instituição (art. 27, § 2º).',
   'O plano de ensino ou o professor dizem algo sobre revisão com IA? A ferramenta mudou só a forma ou também as ideias? Você comparou a versão final com a sua?',
   'Compare o texto revisado com o seu e desfaça o que mudou o sentido. Confira a regra da disciplina. Na dúvida, declare em uma linha.',
   ['Art. 25, caput', 'Art. 27, caput', 'Art. 10, § 1º', 'Art. 28, caput', 'Art. 27, § 2º'], 'revisao_ling+ia|permissao', exclui='declarar nao_declarei', peso=27,
   modelo='Usei [ferramenta] para [revisar a redação, padronizar a formatação ou traduzir] o texto. Conferi a versão final com a original. O conteúdo é de minha responsabilidade.')),
 # Item 3: estudar com IA.
 ('gr_revisar_usar', F('gr_estudar', 'uso_disciplina', A, 'Estudar com IA',
   'Posso usar IA para resumir textos, fazer fichamento ou me explicar a matéria?',
   'Sim, para estudar, pode. Mas não cole na IA aberta o material do professor nem textos de colegas, e confira no original o que ela disser.',
   'Na educação superior, a IA pode ser usada como recurso de apoio ao ensino (art. 25). Quem usa responde pelo que aproveita, e a resposta da IA precisa ser conferida, porque ela pode errar ou inventar (art. 10, § 1º; art. 13, parágrafo único). A resolução proíbe colocar em plataformas externas produções de outras pessoas, como slides e apostilas do professor e trabalhos de colegas (Anexo I, verbete 87). Para textos já publicados, ela não abre exceção; por isso a ferramenta da instituição é a opção mais segura.',
   'O texto que você quer resumir é do professor, de um colega ou já foi publicado? Você conferiu o resumo no texto original? O resumo é só para estudar ou vai ser entregue?',
   'Use a IA para tirar dúvidas e testar o que entendeu. Peça explicações sobre o assunto em vez de colar o material do professor. Confira tudo no texto original. Se o resumo virar trabalho entregue, siga a regra da disciplina.',
   ['Art. 25, caput', 'Art. 10, § 1º', 'Art. 13, Parágrafo único', 'Glossário, verbete 87'], 'estudo_ia', exclui='gravar_aula autoria declarar melhor_ferramenta', peso=28)),
 # Item 4: como escrever a declaração.
 ('gr_disc_declarar', F('gr_como_declarar', 'declarar_disciplina', Z, 'Como escrever a declaração',
   'Como escrevo a declaração de uso de IA? Tem um exemplo?',
   'Em duas ou três frases: qual IA você usou, para quê, e o que conferiu e decidiu. Veja o exemplo abaixo e adapte.',
   'Na pesquisa, a resolução exige declarar a IA quando a contribuição dela for relevante para o texto, a análise de dados, a revisão bibliográfica, a programação ou outra etapa (art. 28). Em trabalho de disciplina, se e como declarar é definido pela política da instituição (art. 27, § 2º). Em qualquer caso, você continua respondendo pelo conteúdo (art. 10, § 1º). A resolução não traz modelo oficial: o exemplo só organiza o que ela pede.',
   'O curso ou o professor têm modelo próprio? Em que etapas a IA ajudou? O que você conferiu e mudou?',
   'Diga qual ferramenta usou, em que etapa e o que conferiu. Se o curso tiver modelo próprio, use o dele. Coloque a declaração onde o professor indicar, por exemplo no fim do trabalho ou na metodologia.',
   ['Art. 28, caput', 'Art. 27, § 2º', 'Art. 10, § 1º'], 'como_declarar', peso=32,
   modelo='Usei o [ChatGPT] para [sugerir um roteiro inicial e revisar a gramática]. Conferi as informações em [fontes consultadas] e reescrevi o texto com minhas palavras. As ideias, a análise e as conclusões são de minha responsabilidade.')),
 # Item 2: reescrevi com minhas palavras.
 ('gr_autoria', F('gr_reescrevi', 'autoria_superior', R_, 'Texto da IA reescrito com outras palavras',
   'A IA escreveu e eu reescrevi com minhas palavras. Posso entregar?',
   'Não, se as ideias, a ordem e os argumentos continuam sendo da IA: trocar as palavras não torna o texto seu. Pode entregar quando o pensamento for seu e a IA tiver sido só apoio.',
   'Usar IA não passa para a ferramenta a responsabilidade pelo conteúdo: quem entrega responde pela seleção, pela verificação e pela veracidade do que apresenta (art. 10, § 1º). Autoria é responder pela concepção, pela argumentação e pela análise do trabalho (Anexo I, verbete 19), e a formação deve ajudar você a entender o limite entre o apoio da tecnologia e a produção própria (art. 30, VII). Reescrever com outras palavras o que a IA pensou não muda quem concebeu o texto. No TCC e na iniciação científica, a contribuição relevante da IA precisa ser declarada (art. 28).',
   'As ideias, a ordem dos argumentos e os exemplos vieram de você ou da IA? Você consegue explicar e defender o texto sem a IA? O professor ou o plano de ensino dizem o que é permitido?',
   'Não entregue o texto só com as palavras trocadas. Use o que a IA trouxe como ponto de partida: leia as fontes, decida o que pensa e escreva a partir disso. Guarde as versões e declare o que a IA fez quando o professor pedir ou quando for TCC.',
   ['Art. 10, § 1º', 'Glossário, verbete 19', 'Art. 30, caput, inciso VII', 'Art. 28, caput'], 'ia|tarefa+reescrevi', peso=30)),
 # Item 5: professor proibiu e anulou.
 ('sup_sancao', F('gr_anulou', 'regimento_superior', Z, 'Trabalho anulado por uso de IA',
   'O professor proibiu IA e anulou meu trabalho. Pode?',
   'Se a proibição estava na regra da disciplina e há prova de que você usou, o professor pode aplicar a regra. Só por suspeita ou por detector, não: peça por escrito o fato, a regra e a prova.',
   'A resolução deixa cada instituição de educação superior definir a própria política de IA (art. 27), então uma proibição prevista na regra da disciplina ou no regimento vale. Mas é vedada sanção fundada só em detector de IA (art. 41, X), e o Glossário diz que o detector não deve fundamentar sanções (Anexo I, verbete 34). Decisões relevantes exigem responsável humano, fundamentação, registro e possibilidade de revisão (art. 40, § 3º).',
   'A proibição estava escrita no plano de ensino ou foi só dita em aula? Que prova foi apresentada além de um detector? Qual é o canal de recurso do curso?',
   'Peça ao professor, por escrito, a regra que foi aplicada e a prova do uso. Junte as suas versões e anotações. Se discordar, recorra pelo canal do curso ou à coordenação.',
   ['Art. 27, caput', 'Art. 41, caput, inciso X', 'Glossário, verbete 34', 'Art. 40, § 3º'], 'anulou+ia|proibir_tudo|pf_proibir|fa_proibe|ge_proibir', reforca='sancao', peso=30)),
]
