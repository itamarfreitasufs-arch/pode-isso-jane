# v5.22 (27/11/2026): ficha das entrevistas do TCC. No teste dos alunos (26/11), só 4 de 13 entenderam "não pode".
# O veredito passa a vermelho ("Não") e a primeira linha diz "Não."; a saída legítima vem depois.
G87_TXT = 'A resolução proíbe colocar em plataformas externas, como o ChatGPT, dados pessoais de colegas ou de outras pessoas (Anexo I, verbete 87).'
AJUSTES = {
 'gr_dados': dict(sinal='vermelho',
  resposta='Não. Entrevistas e questionários trazem dados de outras pessoas, e a resolução proíbe colocar esses dados no ChatGPT ou em outra IA que você usa por conta própria.',
  motivo=G87_TXT + ' Nome, voz, falas e respostas de quem participou da pesquisa são dados pessoais, e a resolução protege a voz e os dados de cada um (art. 10, § 2º). Pedir autorização aos participantes não muda essa proibição: a resolução não abre exceção para o consentimento, que além disso não pode ser genérico (verbete 27). Na pesquisa, vale também ser transparente sobre o método (art. 28).',
  conferir='A IA é de uso pessoal (sua conta no ChatGPT, no Gemini ou parecida) ou é uma ferramenta oferecida pela instituição? Dá para reconhecer alguém pelo nome, pela voz ou pelo que a pessoa conta? O projeto e o termo de consentimento falam desse uso?',
  acao='Não cole as entrevistas nem os questionários no ChatGPT ou em outra IA aberta. Se precisar de ajuda para transcrever ou analisar, pergunte ao orientador se a instituição tem ferramenta própria e se o projeto e o termo de consentimento preveem esse uso. Mesmo nela, tire os nomes e o que identifique as pessoas, e registre a ferramenta usada.'),
 'pos_dados': dict(sinal='vermelho',
  resposta='Não. Entrevistas, áudios e transcrições trazem dados de outras pessoas, e a resolução proíbe colocar esses dados no ChatGPT ou em outra IA que você usa por conta própria.',
  motivo=G87_TXT + ' Voz e fala transcrita de participantes são dados pessoais, e a resolução protege a voz e os dados de cada um (art. 10, § 2º). O consentimento dos participantes não muda essa proibição: a resolução não abre exceção para ele, que além disso não pode ser genérico nem presumido (verbete 27). Na pesquisa, valem integridade e transparência metodológica (art. 28).',
  conferir='A IA é de uso pessoal (sua conta no ChatGPT, no Gemini ou parecida) ou é uma ferramenta contratada pela instituição? Dá para reconhecer os participantes pelo nome, pela voz ou pelo contexto? O projeto aprovado e o termo de consentimento preveem esse uso?',
  acao='Não envie o material a uma IA aberta. Se a instituição oferecer ferramenta própria, confira com o orientador se o projeto aprovado e o termo de consentimento preveem esse uso. Mesmo nela, tire os identificadores e registre a ferramenta e a etapa.'),
 'ps_dados_pesquisa': dict(sinal='vermelho',
  resposta='Não, em ferramenta aberta como o ChatGPT: dados de participantes não podem ir para plataformas externas. Só sem identificação e em ferramenta aprovada pela instituição.'),
}
