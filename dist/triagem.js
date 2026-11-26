// Triagem da Jane v2. Função pura: recebe o texto, o perfil selecionado e a base carregada do SQLite.
const estudantes = ['basico', 'iniciais', 'finais', 'medio', 'graduacao', 'pos'];
const docentesNovos = ['profBasico', 'profSuperior'];
const docentesAntigos = ['docenteFundamental', 'docenteMedio', 'docenteSuperior'];
const docentes = [...docentesNovos, ...docentesAntigos];
// Perfis de professor da v5.13: temas que entram no escopo mesmo sem a palavra IA.
const temasDocente = ['pf_cst', 'licenciatura', 'pf_ref_falsas', 'pf_autocorrige', 'pf_proctoring', 'pf_vigia_prof', 'pf_evasao', 'sem_politica', 'prazo'];
const adultos = [...docentes, 'orientador', 'gestor', 'familia', 'gestorEscolar', 'responsavel'];
// Perfis da v5.17: quem se apresenta como gestor ou como família vai para o perfil novo quando o antigo está fora do ar.
const perfilNovo = {gestor: 'gestorEscolar', familia: 'responsavel'};
const destinoDoPapel = (p, base) => p && perfilNovo[p.perfil] && !(p.perfil in base.perfis) && perfilNovo[p.perfil] in base.perfis ? {...p, perfil: perfilNovo[p.perfil]} : p;
const familias = ['familia', 'responsavel'];
// Temas que entram no escopo desses perfis mesmo sem a palavra IA.
const temasGestor = ['ge_fiscaliza', 'ge_panorama', 'ge_privada', 'ge_risco', 'ge_alto_risco', 'gf_proctoring', 'gf_vigencia'];
const temasResponsavel = ['gf_proctoring', 'gf_vigencia', 'fa_panorama'];
const grupoComplemento = {
 '*estudante_basico': ['basico', 'iniciais', 'finais', 'medio'],
 '*gestor': ['gestor', 'gestorEscolar'],
 '*todos': [...estudantes, ...adultos]
};
// Fichas que já tratam da etapa: não recebem o lembrete geral sobre anos iniciais.
const nucleosDeEtapa = ['uso_iniciais', 'uso_iniciais_turma', 'etapa_iniciais', 'turma_chatbot', 'infantil', 'uso_casa', 'casa_familia'];

// Abreviações comuns de mensagens: expandidas antes de qualquer comparação.
const abreviacoes = {q: 'que', pq: 'porque', vc: 'voce', vcs: 'voces', n: 'nao', nn: 'nao', tb: 'tambem', tbm: 'tambem', oq: 'o que', ngm: 'ninguem', td: 'tudo', mt: 'muito', hj: 'hoje', dps: 'depois', qdo: 'quando', qd: 'quando', cmg: 'comigo', profe: 'professora', pro: 'pro', facul: 'faculdade', tou: 'to', eh: 'e'};
function expandir(texto) {
 // "eu ia fazer", "ia ser melhor": verbo ir, não inteligência artificial.
 texto = texto.replace(/(^|\b(?:eu|ele|ela|voce|gente|q|que|se|nao|n|ja|so|tambem|hoje|hj|ontem|quando|acho) )ia (?=(?:\w+ ){0,1}\w+(?:ar|er|ir|or)\b)/g, '$1iria ');
 texto = texto.replace(/(^|[?.!,;] ?)ia (?=\w+(?:ar|er|ir|or)\b)/g, '$1iria ');
 return texto.replace(/\bi\.a\.?(?=\s|$)/g, 'ia').replace(/[a-z]+/g, p => abreviacoes[p] ?? p);
}

// Erros de digitação ("teze", "profesor", "trabaio", "detetor", "usr"): a palavra que as fichas não conhecem é trocada
// pela palavra conhecida que soa igual; nas palavras longas, também pela que difere em uma letra.
function som(p) {
 return p.replace(/w/g, 'u').replace(/y/g, 'i').replace(/k/g, 'c').replace(/lh/g, 'i').replace(/ch/g, 'x').replace(/sc(?=[ei])/g, 's').replace(/c(?=[ei])/g, 's').replace(/g(?=[ei])/g, 'j')
  .replace(/z/g, 's').replace(/h/g, '').replace(/ct/g, 't').replace(/(.)\1+/g, '$1').replace(/u$/, 'o');
}
const alvosDeLetra = 'professor professora orientador orientadora dissertacao trabalho detector chatgpt declarar pesquisa inteligencia artificial mestrado doutorado faculdade universidade resolucao plagio redacao estagio ferramenta avaliacao monografia coordenador coordenacao reprovado relatorio resumo artigo projeto crianca criancas corrigir alunos'.split(' ');
const alvosSemVogal = 'usar usei posso pode tese prova nota aula'.split(' ');
function umaLetra(a, b) {
 if (Math.abs(a.length - b.length) > 1) return false;
 let i = 0;
 while (i < a.length && a[i] === b[i]) i++;
 const [ra, rb] = [a.slice(i), b.slice(i)];
 return ra.slice(1) === rb.slice(1) || ra.slice(1) === rb || ra === rb.slice(1) || (ra[0] === rb[1] && ra[1] === rb[0] && ra.slice(2) === rb.slice(2));
}
function vocabulario(base) {
 if (base.vocabulario) return base.vocabulario;
 const conta = new Map();
 const soma = (texto, peso) => (normalizar(texto).match(/[a-z]{3,}/g) ?? []).forEach(p => conta.set(p, (conta.get(p) ?? 0) + peso));
 base.situacoes.forEach(s => soma([s.pergunta, s.tema, s.resposta, s.motivo, s.conferir, s.acao].join(' '), 1));
 Object.values(base.conceitos).forEach(re => soma(re.source.replace(/\\[a-zA-Z]/g, ' '), 0));
 soma('mestrando mestranda mestrandos mestrandas doutorando doutoranda residente residencia especializacao', 0);
 base.portoes.forEach(p => soma(p.re.source.replace(/\\[a-zA-Z]/g, ' '), 0));
 Object.entries(abreviacoes).forEach(([a, b]) => soma(a + ' ' + b, 0));
 const porSom = new Map();
 [...conta].filter(([, n]) => n > 0).sort((a, b) => b[1] - a[1]).forEach(([p]) => porSom.has(som(p)) || porSom.set(som(p), p));
 return base.vocabulario = {conhecidas: new Set(conta.keys()), porSom};
}
function corrigir(texto, base) {
 const {conhecidas, porSom} = vocabulario(base);
 return texto.replace(/[a-z]{3,}/g, p => {
  if (conhecidas.has(p)) return p;
  return porSom.get(som(p))
   ?? (p.length >= 6 ? alvosDeLetra.find(a => umaLetra(p, a)) : undefined)
   ?? (!/[aeiou].*[aeiou]/.test(p) || p.length === 3 ? alvosSemVogal.find(a => a.length === p.length + 1 && umaLetra(p, a) && a.replace(/[aeiou]/g, '') === p.replace(/[aeiou]/g, '')) : undefined)
   ?? p;
 });
}

// Etapa que a própria pessoa declara no texto ("to no 7 ano", "tenho 15 anos", "faço pedagogia").
function etapaDeclarada(texto) {
 if (/\b(to|estou|sou|curso|faco) (n[oa]|d[oa]|o|a)? ?\d ?[ºo°]? (ano|serie) do (ensino )?medio\b|\b(to|estou|sou) (no|do) (ensino )?medio\b|\btecnico (em \w+ )?integrado\b/.test(texto)) return 'medio';
 if (/\bsou alun[oa] d[oe] (sexto|setimo|oitavo|nono)\b/.test(texto)) return 'finais';
 if (/\bsou alun[oa] d[oe] (quarto|quinto)\b/.test(texto)) return 'iniciais';
 const ano = texto.match(/\b(?:to|estou|sou) (?:n[oa]|d[oa]|alun[oa] d[oe]) (\d) ?[ºo°]? ano\b/);
 // 1º, 2º e 3º ano existem no fundamental e no médio: sozinhos, não decidem a etapa.
 if (ano && +ano[1] >= 4) return +ano[1] <= 5 ? 'iniciais' : 'finais';
 const idade = texto.match(/\btenho (\d{1,2}) anos\b/);
 if (idade && +idade[1] >= 6 && +idade[1] <= 17) return +idade[1] <= 10 ? 'iniciais' : +idade[1] <= 14 ? 'finais' : 'medio';
 if (/\b(to|estou|faco|entrei)( no| o| meu)? (mestrado|doutorado)\b|\bsou (mestrand|doutorand)\w+\b/.test(texto)) return 'pos';
 if (/\b\d{1,2} ?[ºo°]? (periodo|semestre) d[aeo]\b|\b(faco|curso|to cursando|estou cursando) (pedagogia|faculdade|engenharia|direito|medicina|enfermagem|letras|historia|psicologia|administracao|licenciatura|tecnologo\w*|graduacao|\w+ na (faculdade|universidade))\b|\b(to|estou) na (faculdade|graduacao|universidade)\b|\bcurso tecnologo\b/.test(texto)) return 'graduacao';
 if (/\bsou (estudante|alun[oa]) d[eoa] (mestrado|doutorado|pos|pos-?graduacao|especializacao|residencia|mba)\b|\bsou (mestrand|doutorand|pos-?graduand|pos-?doutorand)\w+\b|\bsou (medic[oa] |enfermeir[oa] )?residente( (de|em|do|da) (medicina|enfermagem|saude|psicologia|odontologia|farmacia|fisioterapia|nutricao|clinica|cirurgia|pediatria|\w+ multiprofissional))?$|\bsou residente (de|em|do|da) (medicina|enfermagem|saude|psicologia|odontologia|farmacia|fisioterapia|nutricao|clinica|cirurgia|pediatria|\w+ multiprofissional)\b|\b(faco|to fazendo|estou fazendo|curso|to cursando|estou cursando) (uma |a |minha )?(residencia|especializacao|pos|pos-?graduacao|mba)\b/.test(texto)) return 'pos';
 if (/\bsou (estudante|alun[oa]) d[oe] (ensino )?medio\b/.test(texto)) return 'medio';
 if (/\bsou (estudante|alun[oa]) d[oe] (ensino )?fundamental\b/.test(texto)) return 'finais';
 if (/\bsou (universitari[oa]|graduand[oa]|calour[oa])\b|\bsou (estudante|alun[oa]|academic[oa]|formand[oa]) (de|do curso( superior)? de) (?!escola|colegio|ensino|rede|uma?\b|ia\b|\d|inteligencia)[a-z]{4,}/.test(texto)) return 'graduacao';
 return '';
}

// Perfil único da educação básica: a etapa que a pessoa escreve vira conceito (eb_iniciais, eb_finais, eb_medio),
// porque só em "Posso usar IA?" a norma responde diferente por etapa. "1º ano", "2º ano" e "3º ano" sozinhos não decidem.
function etapaBasica(texto) {
 if (/\b(ensino medio|no medio|do medio|[1-3] ?[ºo°]? ?(ano|serie|serie do|ano do) (do )?(ensino )?medio|(primeiro|segundo|terceiro) (ano )?do (ensino )?medio|tecnico integrado|curso tecnico|novo ensino medio|enem|vestibular)\b/.test(texto)) return 'medio';
 if (/\b[6-9] ?[ºo°]? ?(ano|serie)\b|\b(sexto|setimo|oitavo|nono) ano\b|\banos finais\b|\bfundamental (2|ii)\b|\b6 ?[ºo°]? ao 9/.test(texto)) return 'finais';
 if (/\b[45] ?[ºo°]? ?(ano|serie)\b|\b(quarto|quinto) ano\b|\banos iniciais\b|\bfundamental (1|i)\b|\b1 ?[ºo°]? ao 5/.test(texto)) return 'iniciais';
 const idade = texto.match(/\b(?:tenho|com|de) (\d{1,2}) anos\b/);
 if (idade && +idade[1] >= 6 && +idade[1] <= 17) return +idade[1] <= 10 ? 'iniciais' : +idade[1] <= 14 ? 'finais' : 'medio';
 if (/\b[1-3] ?[ºo°]? ?(ano|serie) do (ensino )?fundamental\b|\b(primeiro|segundo|terceiro) ano do (ensino )?fundamental\b/.test(texto)) return 'iniciais';
 return '';
}

function perfisCandidatos(texto, selecionado, base) {
 // Versão com perfis desativados: quem se apresenta em perfil inativo recebe o aviso, não a ficha de outro perfil.
 const ativo = p => p in base.perfis;
 const parcial = !['medio', 'docenteSuperior', 'familia'].every(ativo);
 let papel = destinoDoPapel(base.papeis.find(p => p.re.test(texto) && (p.forte || !selecionado || estudantes.includes(selecionado) || familias.includes(selecionado))), base);
 if (papel && perfilNovo[papel.perfil] === selecionado) papel = {...papel, perfil: selecionado};
 let inferido = '';
 // Quem escolheu um perfil de estudante e só menciona "meus alunos" ou "dou aula" (monitor, estagiário, aula particular) continua no perfil escolhido.
 if (papel && !papel.forte && papel.perfil === 'docente' && !ativo('docenteMedio') && estudantes.includes(selecionado)) papel = undefined;
 // Quem já escolheu o perfil de professor do superior e fala de orientação continua nele.
 if (papel && papel.perfil === 'orientador' && selecionado === 'profSuperior') papel = undefined;
 // Orientador: enquanto o perfil próprio não existe, as fichas de orientação estão no perfil do professor do superior.
 if (papel && papel.perfil === 'orientador' && !ativo('orientador') && ativo('profSuperior') && (papel.forte || !selecionado)) {
  if (selecionado === 'profSuperior') return {perfis: [selecionado], nota: '', trocou: false};
  return {perfis: ['profSuperior'], nota: selecionado ? 'Pelo que você escreveu, respondi com as fichas de ' + base.perfis.profSuperior.toLowerCase() + '. ' : '', trocou: true};
 }
 if (parcial && papel) {
  const destinos = papel.perfil === 'docente' ? docentes : [papel.perfil];
  if (!destinos.some(ativo)) {
   if (papel.forte || papel.perfil === 'familia') return {inativo: true};
   papel = undefined;
  }
 }
 if (papel) {
  if (papel.perfil === 'docente') {
   if (!docentes.includes(selecionado)) inferido = /\b(ensino medio|medio)\b/.test(texto) ? 'docenteMedio'
    : /\b(faculdade|universidade|universitari\w+|graduacao|pos-?graduacao|mestrado|doutorado|licenciatura|tcc|ensino superior|curso superior)\b/.test(texto) ? 'docenteSuperior'
    : /\b(fundamental|criancas|\d ?[ºo°]? ano)\b/.test(texto) ? 'docenteFundamental' : 'docente';
   // Com os perfis antigos de professor fora do ar, o destino é o perfil novo do mesmo nível.
   const novo = {docenteFundamental: 'profBasico', docenteMedio: 'profBasico', docenteSuperior: 'profSuperior'}[inferido];
   if (novo && !ativo(inferido) && ativo(novo)) inferido = novo;
  } else if (papel.perfil !== selecionado) inferido = papel.perfil;
 }
 let etapa = (inferido || papel) ? '' : etapaDeclarada(texto);
 if (['iniciais', 'finais', 'medio'].includes(etapa) && (selecionado === 'basico' || (!ativo(etapa) && ativo('basico')))) etapa = 'basico';
 if (etapa && !ativo(etapa)) return {inativo: true};
 if (etapa && etapa !== selecionado && !(selecionado === 'pos' && etapa === 'graduacao')) {
  return {perfis: [etapa], nota: selecionado ? 'Pelo que você escreveu, respondi com as fichas de ' + base.perfis[etapa].toLowerCase() + '. ' : '', trocou: true};
 }
 if (inferido === 'docente') return {perfis: ativo('docenteMedio') ? docentesAntigos : docentesNovos.filter(ativo), nota: 'Você escreveu como docente; respondi com as fichas de professor. ', trocou: true};
 if (inferido) return {perfis: [inferido], nota: selecionado ? 'Pelo que você escreveu, respondi com as fichas de ' + base.perfis[inferido].toLowerCase() + '. ' : '', trocou: true};
 if (selecionado) return {perfis: [selecionado], nota: '', trocou: false};
 return {perfis: (ativo('medio') ? ['medio', 'finais', 'graduacao', 'pos'] : ['basico', 'graduacao', 'pos']).filter(ativo), nota: '', trocou: false, semPerfil: !parcial};
}

function pontuar(situacao, presentes) {
 if (situacao.exclusoes.some(c => presentes.has(c))) return 0;
 if (!situacao.grupos.every(grupo => grupo.some(c => presentes.has(c)))) return 0;
 return 10 * situacao.grupos.length + 2 * situacao.reforcos.filter(c => presentes.has(c)).length + situacao.peso;
}
function conceitosPresentes(texto, base) {
 const presentes = new Set(Object.entries(base.conceitos).filter(([, re]) => re.test(texto)).map(([nome]) => nome));
 const etapa = etapaBasica(texto);
 if (etapa) presentes.add('eb_' + etapa);
 return presentes;
}
function melhores(texto, perfis, base, herdados = []) {
 const presentes = conceitosPresentes(texto, base);
 herdados.forEach(c => presentes.add(c));
 const vistos = new Set();
 return base.situacoes
  .filter(s => s.perfis.some(p => perfis.includes(p)))
  .map(s => ({s, pontos: pontuar(s, presentes), ordemPerfil: Math.min(...s.perfis.map(p => perfis.indexOf(p)).filter(i => i >= 0))}))
  .filter(x => x.pontos > 0)
  .sort((a, b) => b.pontos - a.pontos || a.ordemPerfil - b.ordemPerfil || a.s.ordem - b.s.ordem)
  .filter(x => !vistos.has(x.s.nucleo) && vistos.add(x.s.nucleo));
}

// Nome do perfil como aparece na lista da tela.
const rotuloDeTela = {basico: 'Estudante · fundamental e médio', graduacao: 'Estudante · graduação', pos: 'Estudante · pós-graduação', profBasico: 'Professor · fundamental e médio', profSuperior: 'Professor · graduação e pós-graduação', gestorEscolar: 'Gestor escolar', responsavel: 'Pai, mãe ou responsável'};
const portoesDeCuidado = ['vida', 'autolesao', 'aliciamento', 'assedio', 'imagem_intima', 'violencia', 'humilhacao', 'aflicao'];
const cuidadoInteiro = ['vida', 'autolesao', 'aliciamento', 'assedio', 'imagem_intima', 'violencia'];
// "Minha mãe disse que vai me matar": ameaça vinda de outra pessoa é violência, e não risco de suicídio.
const ameacaDeOutro = /\b(vai|vao|quer|querem|ia|iam|ameac\w+|jurou|juraram|prometeu|tentou|tentaram) (que (vai|ia) )?me matar\b|\b(disse|falou|diz|fala|gritou|escreveu|avisou|disseram|falaram) (que )?(vai |ia |quer |vao )?(me mat\w+|acabar comigo)\b|\bme mata de (pancada|porrada|tanto bater)\b/g;
// "Minha mãe vai me matar se souber": força de expressão, não entra nos portões de risco à vida nem de violência.
const ameacaFigurada = /\b(tcc|tese|dissertacao|provas?|trabalhos?|materia|curso|faculdade|mestrado|doutorado|ia|chatgpt|aulas?|calor|sono|fome|ansiedade|saudade|curiosidade|estagio|prazo|rotina|semana|semestre|vestibular|enem) (ainda )?(vai|vao|ia|quer) (me matar|acabar comigo)\b|\bme mat\w+ de (rir|vergonha|tanto (rir|estudar|trabalhar)|estudar|trabalhar|raiva|susto|tedio|cansaco|saudade|curiosidade)\b|\b(vai|vao|ia|iria|iam) me matar (se|quando) (souber\w*|descobrir\w*|ver|vir|virem|eu (tirar|reprovar|chegar|contar|perder|levar|ficar|nao|for|usar|tiver))\b|\bme mata(m)? (se|quando) (souber\w*|descobrir\w*|eu (tirar|reprovar|chegar|contar|perder|levar|ficar|nao|for|usar|tiver))\b/g;
// Quem sofre: a pessoa que escreve, ou alguém de quem ela fala? "Me contou" e "me disse" não fazem de quem escreve a vítima.
const terceiraPessoa = /\b(alun[oa]s?|estudantes?|orientand[oa]s?|colegas?|amig[oa]s?|filh[oa]s?|net[oa]s?|sobrinh[oa]s?|entead[oa]s?|irma|irmao|menin[oa]s?|garot[oa]s?|criancas?|mae|pai|prim[oa]s?|namorad[oa]|marido|esposa|vizinh[oa]s?|el[ea]s?|del[ea]s?|nel[ea]s?)\b/;
const meRelato = /\bme (contou|contaram|disse|disseram|falou|falaram|procurou|procuraram|mostrou|relatou|pediu|avisou|avisaram|escreveu|confessou|confidenciou|mandou mensagem)\b/g;
const vitimaPropria = /\b(me|mim|comigo|fui|minha cara|(estou|to|sou|vivo) (sendo )?(zoad|xingad|humilhad|excluid|chamad|isolad|ridiculariz|perseguid)\w*|sofro|sofri)\b/;
// Adultos de quem um gestor, um colega ou um familiar pode estar falando (v5.18).
const outroAdulto = /\b(professor\w*|funcionari\w+|coordenador\w*|diretor\w*|servidor\w*|merendeir\w+|porteir\w+|secretari[oa]|inspetor\w*|estagiari\w+|tecnic[oa]|monitor[a]?|espos[oa]|companheir[oa]|sogr[oa]|ti[oa]|avo|mulher)\b/;
// Violência doméstica (v5.18): cônjuge ou companheiro como agressor; vítima adulta ou menor no relato; agressão vista pela criança.
const conjuge = /\b(marido|espos[oa]|companheir[oa]|noiv[oa]|ex[- ]?marido|ex[- ]?mulher|ex[- ]?espos[oa]|ex[- ]?companheir[oa]|pai d[oa]s? (meus?|minhas?) filh\w+)\b/;
const parceiro = /\b(namorad[oa]|ex[- ]?namorad[oa]|parceir[oa]|(meu|minha) ex)\b/;
const vitimaAdulta = /\b(mae|professor\w*|funcionari\w+|colega|amig[oa]|vizinh[oa]|irma|mulher|servidor\w*|merendeira|diretor\w*|coordenador\w*)\b/;
const vitimaMenor = /\b(alun[oa]s?|criancas?|menin[oa]s?|garot[oa]s?|adolescentes?|filh[oa]s?)\b/;
const violenciaEmCasa = /\b(fugi|vou fugir|quero fugir|penso em fugir|pensando em fugir|vontade de fugir) de casa\b|\bmedo d[oa] (meu|minha) (pai|mae|padrasto|madrasta|tio|tia|avo|vo|irmao|irma)\b|\b(pai|mae|padrasto|madrasta|tio|avo|irmao) .{0,25}\b(fica|e|esta|ta|anda) (muito )?(violent[oa]|agressiv[oa])\b|\b(pais?|mae|padrasto|madrasta|em casa|la em casa)\b.{0,45}\b(quebr\w+ (tudo|as coisas|a casa|os moveis|a tv|a televisao|a porta|os pratos)|se (batem|agridem|espancam)|sae?m? (no|na) (tapa|soco|porrada))\b|\b(pai|mae|padrasto|madrasta|tio|avo) .{0,20}\b(cheg\w+|fic\w+|vive|esta|ta|volta) (bebad[oa]|drogad[oa]|alcoolizad[oa])\b|\b(bate|bateu|batia|batendo|agride|agrediu|agredindo|espanc\w+|ameac\w+) .{0,6}\b(n[oa]|em|a|o)? ?(minha|meu) (mae|pai|irma|irmao|avo|madrasta)\b|\b(minha mae|minha irma|minha avo|minha madrasta) (apanha|apanhou|apanhava|e agredida|foi agredida)\b/;
// v5.19: fome em casa, violência entre adultos da casa, sinais de negligência e agressor da família.
const fomeEmCasa = /\b(nao tem|nao tinha|falta|faltando|acabou a|nunca tem) (o que comer|comida|nada (pra|para) comer)\b.{0,20}\b((la )?em casa|na minha casa)\b|\b((la )?em casa|na minha casa) .{0,15}\bnao tem (o que comer|comida|nada (pra|para) comer)\b|\b(to|estou|fico|ando|fiquei|vou|durmo|vim|venho) sem comer porque nao (tem|tinha)\b|\b(passo|passando|passamos|passei) fome(?! de (conhecimento|aprender|saber|ia|leitura|ler|estudar|novidade))\b/;
const violenciaNoLar = /\b(pais?|mae|padrasto|madrasta|marido|espos[oa]|companheir[oa]|em casa|la em casa)\b.{0,45}\b(quebr\w+ (tudo|as coisas|a casa|os moveis|a tv|a televisao|a porta|os pratos)|se (batem|agridem|espancam)|sae?m? (no|na) (tapa|soco|porrada))\b|\b(pai|mae|padrasto|madrasta|tio|avo) .{0,20}\b(cheg\w+|fic\w+|vive|esta|ta|volta) (bebad[oa]|drogad[oa]|alcoolizad[oa])\b.{0,40}\b(quebr\w+|bate|grit\w+|agrid\w+|ameac\w+|briga\w*|violent\w+)\b|\b(pai|padrasto|marido|namorado|companheiro|avo|tio) (del[ea] )?.{0,10}\b(bate|bateu|batia|agride|agrediu|espanc\w+|ameac\w+|enforc\w+) .{0,6}\b(na|a|sua|a sua|na sua) (mae|esposa|mulher|madrasta|avo|irma)\b|\b(pai|mae|padrasto|madrasta|tio|avo|irmao|marido|companheiro) .{0,25}\b(fica|e|esta|ta|anda) (muito )?(violent[oa]|agressiv[oa])\b|\b(mae|madrasta|avo|irma) (del[ea] )?(apanha|apanhou|apanhava|e agredida|foi agredida)\b/;
const negligencia = /\b(alun[oa]s?|criancas?|menin[oa]s?|garot[oa]s?|estudantes?|el[ea]s?) .{0,45}\b(nao come (ha|faz)|sem comer|pass\w+ fome|com fome(?! de (aprender|saber|conhecimento|ia|leitura|ler|estudar|novidade))|sem lanche|sem agasalho|sem casaco|sem sapato|descalc\w+|desmai\w+ de fome|nao tem (o que comer|comida)|sem ter o que comer|com a mesma roupa|roupas? suj\w+|suj\w+ e (com|sem|machucad)\w*|sem (tomar )?banho|fic\w+ sozinh\w+ em casa|dorm\w+ na rua|viv\w+ largad\w+|largad\w+ (na rua|em casa|pel[oa]s?)|machucad\w+ (toda|todo|sempre|quase|de novo|com frequencia)|abandonad\w+ (pel[oa]s? (pais?|mae|familia|responsave\w+)|em casa|na rua|a propria sorte)|negligenciad\w+|desnutrid\w+)\b|\b(pais|mae|pai|familia|responsave(l|is)) .{0,35}\b(abandon\w+ (el[ea]s?|a crianca|o menino|a menina|[oa]s? alun[oa]s?|[oa]s? filh[oa]s?)|negligenci\w+|deix\w+ (el[ea] |a crianca |o menino |a menina )?sozinh\w+|nao cuid\w+ (del[ea]s?|d[oa] (menin[oa]|crianca|alun[oa]|filh[oa])|direito))\b|\bninguem cuida (del[ea]s?|(de|dess[ea]|d[oa]) (um |uma )?(alun|crianc|menin|garot)\w+)\b|\b(criancas?|menin[oa]s?|\w+ de ([4-9]|1[0-5]) anos) .{0,30}\b(cuida\w* sozinh\w+ d[oa]s? irm\w+|(trabalha\w*|esta trabalhando|vend\w+|ped\w+) (vendendo|na rua|no sinal|no semaforo|na roca|na feira|na obra|(pra|para) sustentar|balas?|doces?|esmolas?|dinheiro n[oa]))\b/;
const agressao = /\b(bat\w+|apanh\w+|agrid\w+|agred\w+|espanc\w+|ameac\w+|machuc(a|ou|am|aram)|machucad\w+|queim\w+|surra|cintad\w+|hematomas?|marcas? de)\b/;
const agressorFamiliar = /\b(meu|minha) (pai|mae|padrasto|madrasta|irmao|irma|tio|avo|filh[oa]|sogr[oa]|cunhad[oa]|genro|nora)\b/;
const menorNoTexto = /\b(crianc\w+|menin[oa]s?|adolescentes?|menor(es)?|filh[oa]s?|net[oa]s?|sobrinh[oa]s?|entead[oa]s?|irma|irmao|([1-9]|1[0-7]) anos)\b/;
function relatoDeOutro(nome, texto, trecho, sobreOutro) {
 const semRelato = texto.replace(meRelato, ' ');
 if (nome === 'vida') {
  // "Uma mãe me contou que a filha quer morrer": o verbo na terceira pessoa indica relato. "Me mandaram se matar" é com quem escreve.
  if (/\b(eu|me|mim|minha|meu|prefiro|quero|aguento|consigo|deixei|cansei|penso|tenho|to|estou|ando|vejo|sei)\b/.test(trecho)) return false;
  if (/\bme (mand\w+|diss\w+|fal\w+|escrev\w+) .{0,20}\b(se|me) mat/.test(texto)) return false;
  if (/\b(quer|prefere|pensa|nao aguenta|se mat\w*|se cort\w+|se machuc\w+)\b/.test(trecho) && (terceiraPessoa.test(semRelato) || outroAdulto.test(semRelato))) return true;
  // "A coordenadora comentou que pensa em tirar a própria vida": o verbo de relato vem antes do trecho.
  if (/\b(disse|falou|comentou|contou|escreveu|postou|avisou|confessou|anda dizendo|vive dizendo) que (vai|quer|pensa|ia|queria|pretende|nao aguenta|prefere)\b/.test(semRelato) && (terceiraPessoa.test(semRelato) || outroAdulto.test(semRelato))) return true;
  return null;
 }
 if (nome === 'aliciamento') return !/\b(me|mim|comigo|eu|minhas?|meus?|fui|sou|estou|to|conheci|recebi|mandei)\b/.test(semRelato.replace(/\b(minha|meu|minhas|meus) (filh[oa]s?|net[oa]s?|alun[oa]s?|entead[oa]s?|sobrinh[oa]s?|irma|irmao|amig[oa]s?|colegas?|turma|escola)\b/g, ' ')) && terceiraPessoa.test(semRelato);
 if (nome === 'violencia' || nome === 'assedio') {
  // "Uma aluna vive com hematomas", "uma aluna me procurou dizendo que foi assediada": relato de quem viu ou ouviu.
  if (/\b(me|mim|comigo|eu|apanhei|apanho|fui|sou|estou|to|sofri|sofro|moro|tenho)\b/.test(semRelato)) return false;
  return terceiraPessoa.test(semRelato) ? true : null;
 }
 if (nome === 'autolesao') return /\bse (cort|mutil|automutil|machuc|fer|arranh|queim|bat|mord|soc|esmurr|belisc|estape)/.test(texto) || (!/\b(me|mim|eu|bato|batendo|arranco|arrancando|soco|esmurro|dou|mordo|queimo|corto|machuco|firo|arranho)\b|\b(meu|minha|meus|minhas) (bracos?|pulsos?|pernas?|coxas?|pele|corpo)\b/.test(semRelato) && terceiraPessoa.test(texto));
 if (nome === 'humilhacao') return !vitimaPropria.test(semRelato) && terceiraPessoa.test(texto.replace(/\b(pel[oa]s?|d[oa]s?|com (os|as)|meus|minhas|os|as) (colegas|alunos|alunas|meninos|meninas|garotos|garotas|amigos|amigas|outros|outras)\b/g, ' '));
 if (nome === 'aflicao') return /\b(del[ea]|el[ea]|alun[oa]|estudante|colega|amig[oa]|filh[oa]|menin[oa]|garot[oa]|orientand[oa]|crianca)\b/.test(trecho);
 return null;
}
// Quem pede para fazer ou espalhar montagem de outra pessoa recebe recusa; quem relata que fizeram recebe o acolhimento.
const querMontagem = /\b(vou|vamos|quero|queria|posso|podemos|pode|da (pra|para)|tem como|como (eu |que eu |se |a gente )?(faco|fazer|faz|crio|criar|cria|gero|gerar|gera|monto|montar|monta|espalho|espalhar|coloco|colocar|coloca|ponho|por|boto|botar|troco|trocar|uso|usar|imito|imitar|clono|clonar)|ajuda\w*( a)?|ensina\w*( a)?|qual|quais) .{0,45}\b(deepfake\w*|montage(m|ns)|nudes?|(foto|video|imagem|audio)s? fals\w+|tira\w* a roupa|sem roupa|pelad\w+|clonar a voz|imitar a voz|trocar o rosto|colocar o rosto|(o |a )?(rosto|cara|voz) d[eoa]s? (uma? |meu |minha |ess[ea] |aquel[ea] )?(colegas?|professor\w*|alun[oa]s?|menin[oa]s?|garot[oa]s?|amig[oa]s?|diretor\w*|coordenador\w*) .{0,15}\b(n[oa]|num|numa|em um|em uma) (videos?|fotos?|audios?|corpo|filmes?|memes?|montage\w+|cenas?)|(foto|video|imagem|audio)s? (editad|adulterad|manipulad|alterad|modificad|montad|fake)\w*|(perfil|conta) (fals[oa]|fake)|memes?|figurinhas?|stickers?)\b/;
const alvoDeMontagem = /\b(d[eoa]s?|com|n[oa]s?|zoando|sacaneando|humilhando) (uma? |meu |minha |meus |minhas |noss[oa] |ess[ea] |aquel[ea] |outr[oa] |a |o )?(colegas?|professor\w*|prof|alun[oa]s?|menin[oa]s?|garot[oa]s?|amig[oa]s?|diretor\w*|coordenador\w*|namorad[oa]|ex|alguem|pessoas?|el[ea]s?|famos\w*|celebridade\w*|mulher\w*|vizinh\w*|irma|irmao|prima|primo)\b|\bdel[ea]s?\b|\b(pelad\w+|sem roupa|nudes?|tira\w* a roupa)\b/;
const relatoDeMontagem = /\b(fizeram|fez|criaram|criou|espalh(ou|aram)|descobri|recebi|vaz(ou|aram)|me mandaram|circul\w+|o que (eu )?(faco|fazer|devo)|como (agir|lidar|proceder|denunciar|ajudar|proteger|evitar|impedir|identificar|orientar|saber se|remover|tirar do ar)|autoriz\w+|consentimento)\b/;
const terceiro = /\b(meu filho|minha filha|meu menino|minha menina|meu neto|minha neta|meu enteado|minha enteada|meu irmao|minha irma|(um|uma|meu|minha|o|a) (alun[oa]|orientand[oa]|colega|amig[oa])) .{0,160}\b(escreveu|disse|diz|falou|fala|contou|quer|queria|prefere|apanh\w*|pensa\w*|anda|esta|ta|fica)\b/;
// Montagem ou imagem íntima: quem escreve é a vítima, ou relata o que fizeram com outra pessoa?
const imagemPropria = /\b(de mim|comigo|sou (a |o )?vitima|me (filmaram|gravaram|fotografaram)|com (o )?meu nome|com (a )?minha (foto|cara|imagem)|se pass\w+ por mim|(foto|fotos|video|montagem|imagem|nude|nudes|deepfake|rosto|cara|corpo|voz|figurinha|perfil|conta|meme|memes) (fals[oa] |fake )?(minha|meu|minhas|meus)|(minha|meu|minhas|meus) (foto|fotos|video|imagem|nude|nudes|rosto|cara|corpo|voz)|(uma?|a|o) (minha|meu)\b.{0,12}\b(sem roupa|pelad\w+|nua?|intim\w+)|eu (pelad\w+|nua?|sem roupa)|me (expos|expuseram|mostra|mostrando))\b/;
const imagemDeOutro = /\b(d[eao]s?|com (a |o )?) ?(uma? |outr[oa] |minha |meu |noss[oa] |ess[ea] |aquel[ea] )?(colegas?|alun[oa]s?|menin[oa]s?|garot[oa]s?|estudantes?|criancas?|professor\w*|amig[oa]s?|filh[oa]s?|irma|irmao|sobrinh[oa]|net[oa]|mulher|namorad[oa])\b|\b((um|uma|meu|minha|meus|minhas|os|as|o|a) )?(alun[oa]s?|estudantes?|colegas?|menin[oa]s?|filh[oa]s?|amig[oa]s?|irma|irmao|professor\w*) .{0,30}\b(foi|e|esta sendo|estao sendo|foram|sofreu|virou) (vitimas?|alvos?|expost\w+)\b|\b(um|uma|meu|minha|meus|minhas|os|as|o|a) (alun[oa]s?|estudantes?|colegas?|menin[oa]s?) .{0,60}\b(fez|fizeram|criou|criaram|montou|montaram|gerou|geraram|espalh\w+|compartilh\w+|divulg\w+|mandou|mandaram|postou|postaram)\b/;
// "Posso colar na prova com IA?" é pergunta de permissão: vai para a ficha da prova, e não para a recusa.
const colaPermissao = /^(eu |a gente |nos )?(posso|pode|podemos|e permitido|permitido|ta liberado|e liberado|tem problema|e errado)\b/;
const colaComo = /\b(como|melhor|ensina\w*|ajuda\w*|jeito|truque|dica\w*|sem (o |a |que )?\w+ (perceb\w*|saib\w*|saber|descobr\w*|notar|ver|sacar|pegar))\b/;
const soCola = /\b(colar|cola|colo) (na prova|no exame|com (a )?ia)\b/;
const perguntaDeAdultoSobreBurla = /\b(evitar|impedir|prevenir|coibir|identificar|descobrir se|perceber se|lidar com|o que (eu )?(faco|fazer) (com|quando|se)|meus alunos|alunos estao|aluno (colou|burlou|tentou))\b/;
const riso = /^(k{2,}|(ha|he|hi|hua|rs|kk)+h?|lol)$/;
const ingles = new Set('the what can with my university school how use using should is are does do you your teacher student homework'.split(' '));
const espanhol = new Set('puedo puede tarea escuela deberes como usar mi mis en el la los las una profesor maestra hacer usted'.split(' '));
function idioma(original, palavras) {
 if (/[¿¡]/.test(original)) return true;
 const en = palavras.filter(p => ingles.has(p)).length;
 const es = palavras.filter(p => espanhol.has(p)).length;
 return (en >= 3 && en >= palavras.length * 0.4) || (/\b(puedo|tarea|deberes|usted)\b/.test(palavras.join(' ')) && es >= 2);
}

// Situações parecidas pelas palavras: usadas para completar a lista "Você quis dizer".
function parecidas(texto, perfis, base, fora = []) {
 const termos = radicais(texto).filter(t => t.length > 3);
 if (termos.length < 2) return [];
 return base.situacoes.filter(s => s.perfis.some(p => perfis.includes(p)) && !fora.includes(s.nucleo))
  .map(s => {
   s.termos ??= new Set(radicais(s.pergunta + ' ' + s.tema).filter(t => t.length > 3));
   return {s, pontos: termos.filter(t => s.termos.has(t)).length};
  })
  .filter(x => x.pontos >= 2).sort((a, b) => b.pontos - a.pontos || a.s.ordem - b.s.ordem);
}

function triar(original, selecionado, base) {
 const m = base.mensagens;
 const digitado = expandir(normalizar(original).replace(/\s+/g, ' ').trim());
 const saida = {tipo: '', avisos: [], status: '', fichas: [], perfil: selecionado};
 if (!digitado) return {...saida, tipo: 'vazio', status: m.vazio};
 const texto = corrigir(digitado, base);

 // 1. Cuidado, burla e limites: vêm antes de qualquer ficha. Os de cuidado se acumulam.
 const papelAdulto = adultos.includes(selecionado) || ['graduacao', 'pos'].includes(selecionado) || /\b(faculdade|campus|tcc|mestrado|doutorado|universidade)\b/.test(texto) || base.papeis.some(p => p.forte && p.re.test(texto));
 const sobreOutro = terceiro.test(texto);
 if (querMontagem.test(texto) && alvoDeMontagem.test(texto) && !relatoDeMontagem.test(texto) && !imagemPropria.test(texto) && m.montagem_dano) return {...saida, tipo: 'montagem_dano', status: m.montagem_dano};
 const semFigura = texto.replace(ameacaFigurada, ' ');
 const reDano = base.portoes.find(p => p.nome === 'dano')?.re;
 for (const portao of base.portoes) {
  const alvoTexto = ['vida', 'violencia'].includes(portao.nome) ? semFigura : texto;
  if (!portao.re.test(alvoTexto)) continue;
  if (portao.nome === 'vida' && ameacaDeOutro.test(alvoTexto) && !portao.re.test(alvoTexto.replace(ameacaDeOutro, ' '))) continue;
  if (['assedio', 'aliciamento'].includes(portao.nome) && reDano?.test(texto)) continue;
  if (['assedio', 'imagem_intima'].includes(portao.nome) && saida.avisos.some(a => a.nome === 'aliciamento')) continue;
  if (portao.nome === 'violencia' && /hematoma|rox|marcas? de|machucados/.test(alvoTexto.match(portao.re)[0]) && /\b(educacao fisica|na quadra|no recreio|jogando|no futebol|no treino|de bicicleta|acidente\w*|no parquinho)\b/.test(texto)) continue;
  if (portao.nome === 'imagem_intima' && saida.avisos.some(a => a.nome === 'assedio') && !/\b(fotos?|videos?|imagem|imagens|montage\w+|deepfake\w*|nudes?|audios?|prints?|perfil|meme\w*)\b/.test(texto)) continue;
  if (portoesDeCuidado.includes(portao.nome)) {
   if (portao.nome === 'aflicao' && saida.avisos.length) continue;
   if (portao.nome === 'autolesao' && saida.avisos.some(a => a.nome === 'vida')) continue;
   // "Quero fazer uma montagem para o trabalho de artes": pedido sem pessoa atingida não é relato de vítima.
   if (portao.nome === 'imagem_intima' && querMontagem.test(texto) && !relatoDeMontagem.test(texto) && !portao.re.test(texto.replace(/\b(deepfake\w*|montage(m|ns)|(foto|video|imagem|audio)s? fals\w+|memes?|figurinhas?|stickers?|(perfil|conta) (fals[oa]|fake)|(foto|video|imagem|audio)s? (editad|adulterad|manipulad|alterad|modificad)\w+)\b/g, ' '))) continue;
   if (portao.nome === 'humilhacao' && saida.avisos.some(a => a.nome === 'imagem_intima')) continue;
   const trecho = alvoTexto.match(portao.re)[0];
   const proprio = /\b(me|eu|mim|moro|minha|meu|prefiro|quero|aguento|consigo|deixei)\b/.test(trecho);
   const relato = relatoDeOutro(portao.nome, texto, trecho, sobreOutro);
   const deOutro = portao.nome === 'imagem_intima' ? !imagemPropria.test(texto) && (sobreOutro || imagemDeOutro.test(texto)) : relato ?? (sobreOutro && !proprio);
   let chave = (deOutro && m[portao.nome + '_outro']) ? portao.nome + '_outro' : (papelAdulto && m[portao.nome + '_adulto']) ? portao.nome + '_adulto' : '';
   if (portao.nome === 'violencia' && m.violencia_domestica) {
    // "Meu marido me bate": não é assunto para a escola, e sim para o Ligue 180 e o 190.
    const domestica = conjuge.test(texto) || (papelAdulto && parceiro.test(texto));
    if (deOutro) { if (domestica && vitimaAdulta.test(texto) && !vitimaMenor.test(texto)) chave = 'violencia_domestica_outro'; else if ((familias.includes(selecionado) || /\b(meu|minha) (ex[- ]?)?(marido|espos[oa]|companheir[oa])\b/.test(texto)) && vitimaMenor.test(texto)) chave = 'violencia_outro_familia'; else if (!papelAdulto && violenciaEmCasa.test(texto)) chave = 'violencia_em_casa'; }
    else if (domestica) chave = 'violencia_domestica';
    else if (!papelAdulto && violenciaEmCasa.test(texto)) chave = 'violencia_em_casa';
   }
   // "A escola pode usar IA para identificar alunos com fome?" é pergunta sobre a regra, e não relato.
   if (portao.nome === 'violencia' && negligencia.test(trecho) && /\b(pode|podemos|posso|devo|deve) usar\b|\b(ia|inteligencia artificial|sistema|algoritmo) (para|pra) (identificar|detectar|prever|mapear|monitorar|apontar)\b/.test(texto)) continue;
   if (portao.nome === 'violencia' && m.negligencia_outro) {
    // v5.19: fome, negligência e violência entre os adultos da casa pedem textos próprios.
    if (deOutro && conjuge.test(texto) && violenciaNoLar.test(texto) && !vitimaMenor.test(texto) && (familias.includes(selecionado) || /\b(meu|minha) (ex[- ]?)?(marido|espos[oa]|companheir[oa])\b/.test(texto))) chave = 'violencia_domestica';
    else if (deOutro && negligencia.test(texto) && !agressao.test(texto)) chave = 'negligencia_outro';
    else if (deOutro && papelAdulto && !familias.includes(selecionado) && vitimaMenor.test(texto) && violenciaNoLar.test(texto)) chave = 'violencia_casa_relato';
    else if (!deOutro && fomeEmCasa.test(texto) && !agressao.test(texto)) chave = papelAdulto ? 'fome_adulto' : 'fome_em_casa';
    else if (!deOutro && papelAdulto && chave === 'violencia_adulto' && agressorFamiliar.test(texto)) chave = 'violencia_domestica';
   }
   // Na graduação e na pós, relato sobre adultos ("uma aluna namora um homem mais velho") não é aliciamento de criança.
   if (portao.nome === 'aliciamento' && deOutro && ['graduacao', 'pos', 'profSuperior'].includes(selecionado) && !menorNoTexto.test(texto)) continue;
   if (portao.nome === 'aliciamento' && !deOutro && papelAdulto && !vitimaMenor.test(texto) && !/\b(fotos?|nudes?|videos?|ameac\w+|chantag\w+|extor\w+|dinheiro|pix|camera|segredo|sem roupa|pelad\w+|intim\w+|alici\w+|sextors\w+|espalh\w+|vaz\w+)\b/.test(texto)) continue;
   saida.avisos.push({nome: portao.nome, mensagem: chave ? m[chave] : portao.mensagem, variante: chave});
   saida.tipo = saida.tipo || portao.nome;
   continue;
  }
  if (saida.avisos.length) continue;
  if (portao.nome === 'burla' && papelAdulto && perguntaDeAdultoSobreBurla.test(texto)) continue;
  if (portao.nome === 'burla' && colaPermissao.test(texto) && !colaComo.test(texto) && soCola.test(texto) && !portao.re.test(texto.replace(soCola, ' '))) continue;
  return {...saida, tipo: portao.nome, status: portao.mensagem};
 }
 const cuidado = saida.avisos.length > 0;
 // Risco à vida, imagem íntima e violência: o acolhimento é a resposta inteira.
 if (saida.avisos.some(a => cuidadoInteiro.includes(a.nome))) return {...saida, status: m.cuidado_depois};

 // 2. Ruído, saudação e outra língua.
 const palavras = (texto.match(/[a-z]{2,}/g) ?? []);
 if (!cuidado) {
  if (/^(oi+|ola|opa|e ai|bom dia|boa tarde|boa noite|hello|hi|hey|oie)[ !.?]*$/.test(texto)) return {...saida, tipo: 'saudacao', status: m.saudacao};
  if (!palavras.length || palavras.every(p => riso.test(p)) || /<\/?[a-z]+[^>]*>/.test(original)) return {...saida, tipo: 'ruido', status: m.ruido};
  if (idioma(original, palavras)) return {...saida, tipo: 'lingua', status: m.lingua};
 }

 // 3. Consulta direta à norma: artigo ou definição.
 if (/^(o que diz (o )?)?art(igo)?s?\.?\s*\d{1,2}\b/.test(texto) && palavras.length <= 8) return {...saida, tipo: 'artigo', consulta: texto};
 if (/\b(o que e|o que significa|que significa|o que sao|definicao de|conceito de|significado de)\b/.test(texto) && palavras.length <= 10) saida.definicao = true;

 // 4. Escopo: precisa haver IA ou sistema na pergunta.
 const presentes = conceitosPresentes(texto, base);
 const temIA = ['ia', 'detector', 'camera', 'pontuacao_social', 'prof_ia', 'disse_resolucao', 'melhor_ferramenta', 'emocao', 'identidade', 'decisao_auto', 'provar_autoria', 'montagem'].some(c => presentes.has(c));
 const temSistema = presentes.has('sistema');
 const temEscola = /\b(escola\w*|aula\w*|prof\w*|alun\w*|estudante\w*|turma\w*|prova\w*|nota\w*|trabalho\w*|licao|tarefa\w*|faculdade|universidade|tcc|tese|disserta\w*|orientand\w*|resolucao|cne|mec|curso\w*|redac\w*|crianca\w*|coordenador\w*|diretor\w*|reprov\w*|aprov\w*|matricul\w*|ensino|pedagog\w*|educa\w*|bolsa\w*|evasao|pesquisa\w*|artigo\w*|banca)\b/.test(texto);
 if (saida.definicao && !temIA && !temSistema) return {...saida, tipo: 'definicao'};
 const citaNorma = /\b(resolucao|cne|diretrizes)\b/.test(texto);
 const alunoFalando = adultos.includes(selecionado) && !familias.includes(selecionado) && /\b(meu|minha) (prof\w*|fessor\w*|orientador\w*)\b.{0,80}\b(me deu|minha nota|meu trabalho|me zerou|me reprovou)\b/.test(texto);
 const temTema = ['assistiva', 'politica', 'formacao', 'treinar_modelo', 'predicao', 'substituir', 'ead', 'atendimento', 'panorama'].some(c => presentes.has(c))
  || (presentes.has('prazo') && citaNorma) || (docentesNovos.includes(selecionado) && temasDocente.some(c => presentes.has(c))) || (presentes.has('infantil') && (temSistema || citaNorma || presentes.has('conversar'))) || (presentes.has('publicidade') && temSistema)
  || ('gestorEscolar' in base.perfis && (selecionado === 'gestorEscolar' || (!selecionado && base.papeis.some(p => p.perfil === 'gestor' && p.re.test(texto)))) && (temasGestor.some(c => presentes.has(c)) || (presentes.has('ge_pequena') && /\bcumprir\b/.test(texto))))
  || ('responsavel' in base.perfis && (selecionado === 'responsavel' || (!selecionado && base.papeis.some(p => p.perfil === 'familia' && p.re.test(texto)))) && (temasResponsavel.some(c => presentes.has(c)) || (citaNorma && presentes.has('fa_reclamar'))));
 if (!temIA && !(temSistema && (temEscola || selecionado)) && !temTema) {
  if (cuidado) return saida;
  // Quem se apresenta como gestor ou família, sem dizer a dúvida, fica sabendo que o perfil ainda não está disponível.
  const apresentado = destinoDoPapel(base.papeis.find(p => p.forte && p.re.test(texto)), base);
  if (apresentado && ['gestor', 'familia'].includes(apresentado.perfil) && !(apresentado.perfil in base.perfis) && m.perfil_inativo) return {...saida, tipo: 'perfil_inativo', status: m.perfil_inativo};
  // Quem só se apresenta ("sou orientadora de mestrado", "sou professora") fica sabendo qual perfil usar.
  if ((apresentado || etapaDeclarada(texto)) && palavras.length <= 9 && m.apresentacao) {
   const c = perfisCandidatos(texto, '', base);
   const destino = c.perfis?.length === 1 ? c.perfis[0] : apresentado && apresentado.perfil in base.perfis ? apresentado.perfil : '';
   if (destino) return {...saida, tipo: 'apresentacao', status: m.apresentacao.replace('{perfil}', rotuloDeTela[destino] ?? base.perfis[destino])};
   if (apresentado?.perfil === 'docente') return {...saida, tipo: 'apresentacao', status: m.apresentacao_docente};
  }
  if (palavras.length <= 2 && presentes.has('permissao')) return {...saida, tipo: 'ruido', status: m.ruido};
  if (temEscola && selecionado) {
   const lista = parecidas(texto, [selecionado], base).slice(0, 3);
   if (lista.length) return {...saida, tipo: 'sem_ia', status: m.candidatas, candidatas: lista.map(({s}) => ({situacao: s, perfil: selecionado, complementos: []}))};
  }
  // Resposta sem saída: uma linha de apoio (CVV e Disque 100) acompanha, porque nenhuma regra reconhece todo pedido de ajuda.
  return {...saida, tipo: temEscola ? 'sem_ia' : 'fora', status: temEscola ? m.sem_ia : m.fora, apoio: true};
 }

 // 5. Perfil e fichas.
 const {perfis, nota, trocou, semPerfil, inativo} = perfisCandidatos(texto, alunoFalando ? '' : selecionado, base);
 if (inativo) return {...saida, tipo: 'perfil_inativo', status: m.perfil_inativo};
 const geral = melhores(texto, perfis, base);
 let escolhidas = geral.slice(0, 1);
 const partes = texto.split(/[?;.!]+|\b(?:e tambem|e ainda|alem disso|mas tambem|e quero|e queria|e depois)\b/).map(p => p.trim()).filter(p => p.split(' ').length >= 3);
 if (escolhidas.length && partes.length > 1) {
  // Segunda ficha: exigente por padrão; mais aberta quando a pessoa anuncia duas dúvidas.
  const variasPerguntas = /\?[^?]*[a-z]{3,}[^?]*\?/.test(texto) || /\b(duas|dois|2) (coisas|duvidas|perguntas|casos|pepinos|questoes|problemas)\b|\b(os dois|as duas|e outra|outra coisa|outra duvida|em cada caso)\b|\b1\) .*\b2\)/.test(texto);
  const herdados = ['ia', 'anos_iniciais', 'anos_finais', 'infantil', 'eb_iniciais', 'eb_finais', 'eb_medio'].filter(c => presentes.has(c));
  const outra = partes.map(parte => melhores(parte, perfis, base, herdados)[0])
   .filter(x => x && x.s.nucleo !== escolhidas[0].s.nucleo && x.s.nucleo !== 'panorama' && x.pontos >= (variasPerguntas ? 22 : 27) && !x.s.exclusoes.some(c => presentes.has(c)))
   .sort((a, b) => b.pontos - a.pontos)[0];
  if (outra) escolhidas.push(outra);
 }
 saida.perfil = trocou ? perfis[0] : selecionado;
 saida.perfisUsados = perfis;
 if (!escolhidas.length) {
  const lista = saida.definicao ? [] : parecidas(texto, perfis, base).slice(0, 3);
  if (lista.length) return {...saida, tipo: 'sem_ficha', status: nota + m.candidatas, candidatas: lista.map(({s}) => ({situacao: s, perfil: semPerfil && s.perfis.length >= 4 ? '' : s.perfis.find(p => perfis.includes(p)), complementos: []}))};
  return {...saida, tipo: saida.definicao ? 'definicao' : 'sem_ficha', status: nota + m.sem_ficha};
 }
 const montar = ({s, pontos}) => {
  const perfilFicha = s.perfis.find(p => perfis.includes(p));
  const semRotuloDePerfil = semPerfil && s.perfis.length >= 4;
  const complementos = base.complementos.filter(c => {
   const alvo = c.alvo === s.id || c.alvo === s.nucleo || ((grupoComplemento[c.alvo] ?? []).includes(perfilFicha) && !(c.alvo === '*todos' && (nucleosDeEtapa.includes(s.nucleo) || presentes.has('ensino_medio') || ['basico', 'medio', 'docenteMedio', 'graduacao', 'pos', 'docenteSuperior', 'orientador', 'profBasico', 'profSuperior', 'gestorEscolar', 'responsavel'].includes(perfilFicha))));
   return alvo && c.re.test(texto) && (!c.exige || presentes.has(c.exige));
  }).map(c => c.texto);
  return {situacao: s, pontos, perfil: semRotuloDePerfil ? '' : perfilFicha, complementos};
 };
 saida.fichas = escolhidas.map(montar);
 // Lista "Você quis dizer": a mais provável, a de outra parte da pergunta e as vizinhas, até três.
 // A ficha geral de declaração pontua em quase toda pergunta: só entra como vizinha quando fica perto da primeira.
 const usados = new Set(escolhidas.map(x => x.s.nucleo));
 const vizinhas = [...geral.filter(x => geral[0].pontos - x.pontos <= 10 && !usados.has(x.s.nucleo) && usados.add(x.s.nucleo)), ...parecidas(texto, perfis, base).filter(x => !(x.s.exclusoes ?? []).some(c => presentes.has(c)) && !usados.has(x.s.nucleo) && usados.add(x.s.nucleo))];
 saida.candidatas = [...escolhidas, ...vizinhas].slice(0, 3).map(montar);
 saida.tipo = saida.tipo || 'ficha';
 saida.status = (cuidado ? 'Sobre a regra de IA: ' : '') + nota + m.candidatas + (semPerfil ? m.sem_perfil : '');
 return saida;
}

// Caixa "Consultar a norma": aceita artigo, verbete, termo ou pergunta escrita com as palavras da pessoa.
// O acolhimento vem antes de qualquer busca; sem trecho da norma, a caixa oferece as fichas mais próximas.
const portoesDeLimite = ['burla', 'dano', 'penal', 'judicial', 'trabalhista'];
function fichasPorPalavra(texto, perfis, base) {
 const termos = radicais(texto, true).filter(t => t.length > 2);
 if (!termos.length || termos.length > 3) return [];
 return base.situacoes.filter(s => s.perfis.some(p => perfis.includes(p)))
  .map(s => {
   s.normalPergunta ??= normalizar(s.pergunta + ' ' + s.tema);
   s.normalCorpo ??= normalizar(s.resposta + ' ' + s.motivo);
   const naPergunta = termos.filter(t => contem(s.normalPergunta, t)).length;
   const noCorpo = termos.filter(t => contem(s.normalPergunta, t) || contem(s.normalCorpo, t)).length;
   return {s, naPergunta, noCorpo};
  })
  .filter(x => x.noCorpo === termos.length).sort((a, b) => b.naPergunta - a.naPergunta || a.s.ordem - b.s.ordem).slice(0, 4);
}
async function consultarCaixa(original, selecionado) {
 const base = await carregarBase();
 const m = base.mensagens;
 const t = triar(original, selecionado, base);
 const linhas = await buscarNorma(original);
 const saida = {avisos: [], status: '', linhas: [], candidatas: [], apoio: false};
 // Risco à vida e violência: o acolhimento é a resposta inteira. Os outros avisos saem quando a busca achou trechos
 // ("ambiente íntimo" é termo do Anexo II, não um pedido de ajuda).
 const graves = t.avisos.filter(a => ['vida', 'autolesao', 'violencia', 'assedio', 'aliciamento'].includes(a.nome));
 if (graves.length) return {...saida, avisos: t.avisos, status: m.cuidado_depois};
 if (t.avisos.length && (!linhas.length || (t.avisos.some(a => a.nome === 'imagem_intima') && (normalizar(original).match(/[a-z0-9]+/g) ?? []).length >= 4))) return {...saida, avisos: t.avisos, status: t.avisos.some(a => a.nome === 'imagem_intima') ? m.cuidado_depois : ''};
 if (linhas.ref) return {...saida, linhas, status: linhas.nota};
 // Humilhação e aflição contadas em frase: o acolhimento não some porque a busca achou palavras soltas na norma.
 if (t.avisos.length && !t.avisos.some(a => a.nome === 'imagem_intima') && (normalizar(original).match(/[a-z0-9]+/g) ?? []).length >= 3) return {...saida, avisos: t.avisos, candidatas: t.tipo === 'ficha' || t.fichas.length ? (t.candidatas ?? []).map(c => ({...c, doMenu: true})) : [], status: t.fichas.length ? t.status : ''};
 if (t.tipo === 'apresentacao') return {...saida, status: t.status};
 // Pedido de burla ou de dano: a recusa vem antes dos trechos da norma que só repetem palavras da pergunta.
 if (['burla', 'dano', 'montagem_dano'].includes(t.tipo)) return {...saida, status: t.status};
 const palavras = normalizar(original).match(/[a-z0-9]+/g) ?? [];
 const perfis = selecionado ? [selecionado] : Object.keys(base.perfis);
 const candidatas = lista => lista.map(c => ({...c, doMenu: true}));
 // Sem perfil escolhido (e sem etapa declarada no texto), a caixa não oferece ficha de um perfil qualquer: pede o perfil.
 const semPerfil = !selecionado && !(t.perfisUsados?.length === 1);
 const oferecer = lista => semPerfil ? {...saida, status: m.caixa_sem_perfil} : {...saida, candidatas: candidatas(lista), status: m.candidatas};
 if (t.tipo === 'ficha' && palavras.length >= 3) return oferecer(t.candidatas);
 if (linhas.length) return {...saida, linhas};
 if (portoesDeLimite.includes(t.tipo) || ['saudacao', 'lingua'].includes(t.tipo)) return {...saida, status: t.status};
 if (t.candidatas?.length) return oferecer(t.candidatas);
 const proximas = fichasPorPalavra(original, perfis, base);
 if (proximas.length) return semPerfil ? {...saida, status: m.caixa_sem_perfil} : {...saida, candidatas: proximas.map(({s}) => ({situacao: s, perfil: s.perfis.find(p => perfis.includes(p)), complementos: [], doMenu: true})), status: m.caixa_fichas};
 // Pergunta que não é sobre IA na educação: a caixa diz que foge do escopo, em vez de "sem correspondência".
 if (['fora', 'sem_ia', 'perfil_inativo'].includes(t.tipo) && palavras.length >= 3) return {...saida, status: t.status, apoio: !!t.apoio};
 return {...saida, status: m.caixa_vazia, apoio: palavras.length >= 4};
}
