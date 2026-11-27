const resultArea = document.querySelector('#results');
const status = document.querySelector('#status');
const apoio = document.querySelector('#apoio');

function element(tag, text, className) {
 const item = document.createElement(tag);
 if (text) item.textContent = text;
 if (className) item.className = className;
 return item;
}

// Nome do dispositivo como a pessoa o procura: artigo, verbete do Glossário ou Guia de Risco.
function nomeDispositivo(row) {
 if (row.secao === 'Anexo I') return 'Glossário (Anexo I) · ' + row.localizador.replace(/^Item /, 'verbete ');
 if (row.secao === 'Anexo II') return 'Guia de Risco (Anexo II) · ' + row.localizador;
 return [row.secao, row.localizador].join(' · ');
}
function rotuloFonte(d) {
 if (d.secao === 'Anexo I') return 'Glossário (verbete ' + d.localizador.replace(/^Item /, '') + ')';
 if (d.secao === 'Anexo II') return 'Anexo II';
 return 'art. ' + d.artigo;
}
function sourceDetails(row) {
 const details = element('details');
 const heading = nomeDispositivo(row);
 details.append(element('summary', heading));
 if (row.contexto) details.append(element('p', 'Dispositivo superior: ' + row.contexto));
 details.append(row.tipo === 'quadro' ? quadro(row.texto) : element('pre', row.texto, row.tipo === 'tabela' ? 'layout-table' : ''));
 return details;
}
// Quadro de classificação de risco (Anexo II): um bloco por nível, com as três colunas do quadro em sequência.
function quadro(texto) {
 const caixa = element('div', '', 'quadro');
 texto.split('\n\n').forEach(parte => {
  const [titulo, ...linhas] = parte.split('\n');
  const nivel = element('section');
  nivel.append(element('h4', titulo));
  linhas.forEach(linha => {
   const corte = linha.indexOf(': ');
   const p = element('p');
   p.append(element('strong', linha.slice(0, corte + 1)), element('span', ' ' + linha.slice(corte + 2)));
   nivel.append(p);
  });
  caixa.append(nivel);
 });
 return caixa;
}

const nivelSelecionado = document.querySelector('#level');
const exemplosNivel = document.querySelector('#level-examples');
const caixaExemplos = document.querySelector('#more');
const caixaAssuntos = document.querySelector('#assuntos');
const campo = document.querySelector('#message');
const cuidado = document.querySelector('#care');
let requestNumber = 0;

// Limite do relato: perguntas longas acionam fichas por acaso.
const LIMITE = 600;
const dica = document.querySelector('#hint');
const dicaPadrao = '';
function atualizarContador() {
 if (campo.value.length > LIMITE) campo.value = campo.value.slice(0, LIMITE);
 const resto = LIMITE - campo.value.length;
 dica.textContent = resto <= 0 ? 'Limite de ' + LIMITE + ' caracteres atingido. Resuma em uma ou duas frases.'
  : resto <= 120 ? 'Restam ' + resto + ' caracteres.' : dicaPadrao;
 dica.dataset.estado = resto <= 0 ? 'cheio' : resto <= 120 ? 'perto' : '';
}
campo.oninput = atualizarContador;

const sinais = {
 vermelho: 'Não',
 amarelo: 'Em parte',
 verde: 'Sim',
 azul: 'Como proceder'
};
const ajudas = {
 vida: {titulo: 'Você não precisa passar por isso sozinho', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188'], ['Conversar pelo chat do CVV', 'https://cvv.org.br/chat/']]},
 autolesao: {titulo: 'Você não precisa lidar com isso sozinho', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188'], ['Conversar pelo chat do CVV', 'https://cvv.org.br/chat/']]},
 autolesao_outro: {titulo: 'Esse sinal pede atenção hoje', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188']]},
 humilhacao_outro: {titulo: 'Aja para proteger quem está sendo atingido', acoes: []},
 humilhacao_adulto: {titulo: 'Isso não é aceitável', acoes: []},
 aflicao_outro: {titulo: 'Essa pessoa pode precisar de apoio', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188']]},
 imagem_intima: {titulo: 'Isso é sério e não é culpa sua', acoes: [['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Denunciar na SaferNet', 'https://new.safernet.org.br/denuncie'], ['Canal de ajuda da SaferNet', 'https://www.canaldeajuda.org.br/']]},
 assedio: {titulo: 'Isso é sério e não é culpa sua', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 assedio_adulto: {titulo: 'Isso é sério e não é culpa sua', acoes: [['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 assedio_outro: {titulo: 'Aja hoje para proteger essa pessoa', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Emergência: ligar 190', 'tel:190']]},
 aliciamento: {titulo: 'Isso é sério e não é culpa sua', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Denunciar na SaferNet', 'https://new.safernet.org.br/denuncie'], ['Canal de ajuda da SaferNet', 'https://www.canaldeajuda.org.br/'], ['Emergência: ligar 190', 'tel:190']]},
 aliciamento_adulto: {titulo: 'Isso é sério e não é culpa sua', acoes: [['Canal de ajuda da SaferNet', 'https://www.canaldeajuda.org.br/'], ['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 aliciamento_outro: {titulo: 'Aja hoje para proteger essa pessoa', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Denunciar na SaferNet', 'https://new.safernet.org.br/denuncie'], ['Emergência: ligar 190', 'tel:190']]},
 violencia_domestica: {titulo: 'Ninguém pode agredir nem ameaçar você', acoes: [['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 violencia_domestica_outro: {titulo: 'Como ajudar essa pessoa', acoes: [['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 violencia_outro_familia: {titulo: 'Aja hoje para proteger essa criança', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Emergência: ligar 190', 'tel:190']]},
 violencia_em_casa: {titulo: 'Você não precisa resolver isso sozinho', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Emergência: ligar 190', 'tel:190']]},
 fome_em_casa: {titulo: 'Você tem direito a se alimentar', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100']]},
 fome_adulto: {titulo: 'Você não precisa passar por isso sozinho', acoes: []},
 negligencia_outro: {titulo: 'Aja hoje para proteger essa criança', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 violencia_casa_relato: {titulo: 'Aja hoje para proteger essa criança', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Ligar 180 (grátis, 24 horas)', 'tel:180'], ['Emergência: ligar 190', 'tel:190']]},
 violencia: {titulo: 'Ninguém pode bater em você nem ameaçar você', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 humilhacao: {titulo: 'Você merece ser tratado com respeito', acoes: []},
 vida_outro: {titulo: 'Como ajudar essa pessoa agora', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188'], ['Conversar pelo chat do CVV', 'https://cvv.org.br/chat/']]},
 imagem_intima_outro: {titulo: 'Proteja quem foi atingido', acoes: [['Ligar 100 (Disque Direitos Humanos)', 'tel:100'], ['Denunciar na SaferNet', 'https://new.safernet.org.br/denuncie'], ['Canal de ajuda da SaferNet', 'https://www.canaldeajuda.org.br/']]},
 violencia_adulto: {titulo: 'Você não precisa enfrentar isso sozinho', acoes: [['Emergência: ligar 190', 'tel:190']]},
 violencia_outro: {titulo: 'Aja hoje para proteger essa pessoa', acoes: [['Ligar 100 (grátis, todos os dias)', 'tel:100'], ['Emergência: ligar 190', 'tel:190']]},
 aflicao: {titulo: 'Como você está?', acoes: [['Ligar 188 (CVV, grátis, 24 horas)', 'tel:188']]}
};

function blocosDeCuidado(avisos) {
 return avisos.map(({nome, mensagem, variante}) => {
  const ajuda = ajudas[variante] ?? ajudas[nome] ?? {titulo: 'Importante', acoes: []};
  const bloco = element('section', '', 'care');
  // O título já diz a primeira frase de alguns acolhimentos: ela não se repete no parágrafo.
  const corpo = mensagem.startsWith(ajuda.titulo + '. ') ? mensagem.slice(ajuda.titulo.length + 2) : mensagem;
  bloco.append(element('h2', ajuda.titulo), element('p', corpo));
  if (ajuda.acoes.length) {
   const linha = element('p', '', 'care-actions');
   ajuda.acoes.forEach(([rotulo, destino]) => {
    const link = element('a', rotulo);
    link.href = destino;
    linha.append(link);
   });
   bloco.append(linha);
  }
  return bloco;
 });
}
function mostrarCuidado(avisos) {
 cuidado.replaceChildren(...blocosDeCuidado(avisos));
 cuidado.hidden = !avisos.length;
}

// Divide um texto em frases, sem cortar em "art." ou "§ 1º.".
function frases(texto) {
 return texto.split(/(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕ])/).map(f => f.trim()).filter(Boolean);
}
function lista(tag, itens, classe) {
 const ul = element(tag, '', classe);
 itens.forEach(item => ul.append(element('li', item)));
 return ul;
}
function bloco(parent, titulo, conteudo) {
 const secao = element('section', '', 'entry');
 secao.append(element('h3', titulo), conteudo);
 parent.append(secao);
}

// Contador de usos (conta.php): manda só o tipo de evento, o perfil e o código da ficha.
// Nada do que a pessoa escreve sai do navegador; sem cookie, sem identificador.
const PERFIS_CONTADOS = ['basico', 'graduacao', 'pos', 'profBasico', 'profSuperior', 'gestorEscolar', 'responsavel'];
let ultimaFichaContada = '';
function contar(evento, perfil = '', ficha = '') {
 try {
  if (typeof navigator === 'undefined' || !navigator.sendBeacon || !/^https?:$/.test(location.protocol)) return;
  const dados = new URLSearchParams({e: evento});
  if (PERFIS_CONTADOS.includes(perfil)) dados.set('p', perfil);
  if (/^[a-z0-9_]{1,40}$/.test(ficha)) dados.set('f', ficha);
  navigator.sendBeacon('conta.php', dados);
 } catch (erro) {}
}
function contarFicha(perfil, id) {
 // Voltar, avançar ou recarregar a página não contam a mesma ficha de novo.
 try { ultimaFichaContada = sessionStorage.getItem('jane_ficha') ?? ultimaFichaContada; } catch (erro) {}
 if (ultimaFichaContada === perfil + '/' + id) return;
 ultimaFichaContada = perfil + '/' + id;
 try { sessionStorage.setItem('jane_ficha', ultimaFichaContada); } catch (erro) {}
 contar('ficha', perfil, id);
}

function mostrarFicha(base, ficha, adicionar = false, focar = true) {
 const s = ficha.situacao;
 const artigo = element('article', '', 'card result sinal-' + s.sinal);
 const veredito = element('div', '', 'verdict');
 const cartao = element('span', '', 'cartao');
 cartao.setAttribute('aria-hidden', 'true');
 const texto = element('div');
 texto.append(element('p', sinais[s.sinal], 'verdict-label'), element('h2', s.resposta));
 veredito.append(cartao, texto);
 // Pelo menu, a situação escolhida vem antes da resposta; no texto livre, o app mostra como entendeu.
 if (ficha.doMenu) artigo.append(element('p', s.pergunta, 'asked'));
 artigo.append(veredito);
 artigo.append(element('p', [base.perfis[ficha.perfil], s.tema].filter(Boolean).join(' · '), 'eyeline'));
 if (!ficha.doMenu) artigo.append(element('p', 'Entendi como: ' + s.pergunta, 'question'));
 (ficha.complementos ?? []).forEach(c => artigo.append(element('p', c, 'told')));
 const passos = frases(s.acao);
 bloco(artigo, 'O que fazer agora?', passos.length > 1 ? lista('ol', passos, 'steps') : element('p', s.acao));
 const perguntas = frases(s.conferir);
 bloco(artigo, 'Perguntas para conferir', lista('ul', perguntas.length ? perguntas : [s.conferir], 'checks'));
 if (s.modelo) {
  const caixa = element('div', '', 'modelo');
  const texto = element('p', s.modelo, 'draft');
  const copiar = element('button', 'Copiar texto', 'no-print');
  copiar.type = 'button';
  copiar.onclick = async () => {
   try {
    await navigator.clipboard.writeText(s.modelo);
    copiar.textContent = 'Texto copiado';
   } catch {
    copiar.textContent = 'Selecione o texto e copie';
   }
  };
  caixa.append(texto, copiar);
  bloco(artigo, 'Texto para adaptar', caixa);
 }
 bloco(artigo, 'Por quê?', element('p', s.motivo));
 if (s.dispositivos.length) {
  const fontes = element('details', '', 'norma');
  fontes.append(element('summary', 'Ler na resolução: ' + [...new Set(s.dispositivos.map(rotuloFonte))].join(', ')));
  s.dispositivos.forEach(row => fontes.append(sourceDetails(row)));
  artigo.append(fontes);
 }
 artigo.tabIndex = -1;
 if (adicionar) resultArea.append(artigo);
 else {
  resultArea.replaceChildren(artigo);
  if (focar) artigo.focus();
 }
}

// Texto livre: em vez de abrir uma ficha por conta própria, o app pede que a pessoa confirme a situação.
function mostrarCandidatas(base, candidatas) {
 const artigo = element('article', '', 'card result candidatas');
 artigo.append(element('h2', 'Você quis dizer:'));
 const lista = element('div', '', 'examples');
 candidatas.forEach(ficha => {
  const rotulo = ficha.situacao.pergunta;
  const botao = element('button', rotulo, 'cand');
  botao.type = 'button';
  botao.onclick = () => {
   ++requestNumber;
   status.textContent = '';
   mostrarFicha(base, {...ficha, doMenu: true});
   contarFicha(ficha.perfil || nivelSelecionado.value, ficha.situacao.id);
  };
  lista.append(botao);
 });
 const nenhuma = element('button', 'Nenhuma dessas', 'cand nenhuma');
 nenhuma.type = 'button';
 nenhuma.onclick = () => {
  ++requestNumber;
  resultArea.replaceChildren();
  status.textContent = nivelSelecionado.value ? 'Escolha o assunto na lista acima.' : 'Selecione o seu perfil e escolha o assunto na lista.';
  (nivelSelecionado.value ? caixaAssuntos.querySelector('button') ?? nivelSelecionado : nivelSelecionado).focus();
 };
 lista.append(nenhuma);
 artigo.append(lista);
 artigo.tabIndex = -1;
 resultArea.replaceChildren(artigo);
 artigo.focus();
}

function mostrarTrechos(titulo, linhas, explicacao) {
 const artigo = element('article', '', 'card result sinal-azul');
 artigo.append(element('p', 'Texto da resolução', 'eyeline'), element('h2', titulo));
 if (explicacao) artigo.append(element('p', explicacao));
 const caixa = element('div', '', 'norma');
 linhas.forEach(row => {
  const detalhe = sourceDetails(row);
  detalhe.open = linhas.length <= 3;
  caixa.append(detalhe);
 });
 artigo.append(caixa);
 artigo.tabIndex = -1;
 resultArea.replaceChildren(artigo);
 artigo.focus();
}

function limpar() {
 apoio.hidden = true;
 resultArea.replaceChildren();
 cuidado.replaceChildren();
 cuidado.hidden = true;
}

// Navegação: perfil, assunto e ficha ficam no endereço (#pos/usar/pos_uso), para o Voltar do navegador
// retornar à lista de situações e o Recarregar manter a ficha aberta.
const temHistorico = typeof history !== 'undefined' && typeof location !== 'undefined';
function lerEndereco() {
 if (!temHistorico) return {};
 const [p = '', a = '', sit = ''] = decodeURIComponent(location.hash.slice(1)).split('/');
 return {p, a, s: sit};
}
function navegar(estado) {
 if (temHistorico) {
  const destino = '#' + [estado.p, estado.a, estado.s].filter(Boolean).join('/');
  if (location.hash !== destino && (location.hash || destino !== '#')) history.pushState(null, '', destino === '#' ? location.pathname + location.search : destino);
 }
 return aplicar(estado, true);
}
async function aplicar(estado, focar) {
 const id = ++requestNumber;
 limpar();
 status.textContent = '';
 const opcao = [...(nivelSelecionado.options ?? [])].find(o => o.value === estado.p);
 const nivel = nivelSelecionado.options ? (opcao && !opcao.disabled ? estado.p : '') : estado.p;
 nivelSelecionado.value = nivel;
 document.body.dataset.perfil = nivel;
 exemplosNivel.replaceChildren();
 caixaAssuntos.replaceChildren();
 caixaExemplos.hidden = true;
 campo.placeholder = 'Ex.: usei IA no meu trabalho. Preciso contar?';
 // Endereço que não leva a lugar nenhum (perfil desativado, assunto ou ficha que não existe): a tela avisa e o endereço é corrigido.
 const corrigirEndereco = (aviso, valido) => {
  status.textContent = aviso;
  if (temHistorico) history.replaceState(null, '', valido.length ? '#' + valido.join('/') : location.pathname + location.search);
 };
 if (!nivel) {
  if (estado.p) corrigirEndereco(opcao ? 'O perfil deste endereço ainda não está disponível: na lista, ele aparece como "em breve". Selecione o seu perfil.' : 'Não encontrei esse endereço. Selecione o seu perfil.', []);
  return;
 }
 try {
  const base = await carregarBase();
  if (id !== requestNumber) return;
  // Menu: assuntos do perfil e, dentro de cada um, as situações que têm ficha.
  const doPerfil = base.situacoes.filter(s => s.perfis.includes(nivel));
  const destaque = doPerfil.find(s => s.destaque);
  if (destaque) campo.placeholder = 'Ex.: ' + destaque.pergunta;
  const assuntos = base.assuntos.filter(a => doPerfil.some(s => s.assunto === a.chave));
  caixaAssuntos.replaceChildren(...assuntos.map(a => {
   const botao = element('button', a.rotulo);
   botao.type = 'button';
   botao.setAttribute('aria-pressed', String(a.chave === estado.a));
   botao.onclick = () => navegar({p: nivel, a: a.chave});
   return botao;
  }));
  caixaExemplos.hidden = !doPerfil.length;
  caixaExemplos.open = true;
  const assunto = assuntos.find(a => a.chave === estado.a);
  if (!assunto) {
   if (estado.a) corrigirEndereco('Não encontrei essa ficha. Escolha o assunto na lista.', [nivel]);
   return;
  }
  const itens = doPerfil.filter(s => s.assunto === assunto.chave).sort((a, b) => b.destaque - a.destaque || a.ordem - b.ordem);
  // Assunto com uma situação só: abre a ficha direto, sem lista de um item.
  const escolhida = itens.length === 1 ? itens[0] : itens.find(s => s.id === estado.s);
  if (itens.length > 1) exemplosNivel.replaceChildren(...itens.map(s => {
   const botao = element('button', s.pergunta);
   botao.type = 'button';
   if (s === escolhida) botao.setAttribute('aria-current', 'true');
   botao.onclick = () => navegar({p: nivel, a: assunto.chave, s: s.id});
   return botao;
  }));
  if (estado.s && !escolhida) corrigirEndereco('Não encontrei essa ficha. Escolha a situação na lista.', [nivel, assunto.chave]);
  if (escolhida) {
   mostrarFicha(base, {situacao: escolhida, perfil: nivel, complementos: [], doMenu: true}, false, focar);
   contarFicha(nivel, escolhida.id);
  }
  // Leitor de tela e teclado: o foco vai para a primeira situação do assunto escolhido.
  else if (focar) exemplosNivel.firstElementChild?.focus({preventScroll: true});
 } catch (erro) {
  status.textContent = erro.message;
 }
}
function atualizarNivel() {
 return aplicar({p: nivelSelecionado.value}, false);
}
nivelSelecionado.onchange = async () => {
 contar('perfil', nivelSelecionado.value);
 await navegar({p: nivelSelecionado.value});
 // Sem perfil, a lista de assuntos some: a tela diz o que falta.
 if (!nivelSelecionado.value) status.textContent = 'Selecione o seu perfil para ver os assuntos.';
};
// Ao abrir: o endereço manda (ficha recarregada ou link); sem ele, vale o perfil que já vier escolhido.
const perfilInicial = nivelSelecionado.value;
const estadoDoEndereco = () => {
 const estado = lerEndereco();
 return estado.p ? estado : {p: perfilInicial};
};
if (estadoDoEndereco().p) aplicar(estadoDoEndereco(), false);
if (typeof window !== 'undefined') window.addEventListener('popstate', () => aplicar(estadoDoEndereco(), false));

document.querySelector('#question').onsubmit = async event => {
 event.preventDefault();
 const id = ++requestNumber;
 const pergunta = campo.value.slice(0, LIMITE);
 limpar();
 contar('escrita', nivelSelecionado.value);
 status.textContent = 'Lendo a sua pergunta…';
 try {
  const base = await carregarBase();
  if (id !== requestNumber) return;
  const r = triar(pergunta, nivelSelecionado.value, base);
  mostrarCuidado(r.avisos);
  if (r.tipo === 'artigo') {
   const linhas = await buscarNorma(r.consulta);
   if (id !== requestNumber) return;
   if (linhas.length) {
    status.textContent = 'Este é o texto da resolução.';
    mostrarTrechos('Texto da norma', linhas);
   } else status.textContent = 'Não encontrei esse artigo. A resolução tem 47 artigos.';
   return;
  }
  if (r.tipo === 'definicao') {
   const item = await verbete(normalizar(pergunta));
   if (id !== requestNumber) return;
   if (item) {
    status.textContent = 'Encontrei este verbete no glossário da resolução (Anexo I).';
    mostrarTrechos('Glossário da resolução', [item]);
    return;
   }
   if (!r.fichas.length) r.tipo = 'sem_ficha', r.status = r.status || base.mensagens.sem_ficha;
  }
  if (r.tipo === 'sem_ficha' && !r.candidatas) {
   const linhas = await sugerirDispositivos(pergunta);
   if (id !== requestNumber) return;
   if (linhas.length) {
    status.textContent = r.status.replace(base.mensagens.sem_ficha, base.mensagens.sem_ficha_sugestoes);
    mostrarTrechos('Trechos que mencionam a sua pergunta', linhas, 'Estes trechos foram escolhidos pelas palavras da pergunta. Eles não são uma orientação para o seu caso.');
   } else status.textContent = r.status;
   if (caixaAssuntos.children.length) caixaExemplos.open = true;
   return;
  }
  const noLimite = pergunta.length >= LIMITE && ['fora', 'sem_ia', 'ruido'].includes(r.tipo);
  status.textContent = r.status + (noLimite ? ' O seu texto chegou ao limite de ' + LIMITE + ' caracteres. Se a pergunta ficou de fora, apague o relato e escreva só ela.' : '');
  apoio.hidden = !r.apoio;
  if (r.candidatas?.length) mostrarCandidatas(base, r.candidatas);
  if (!r.avisos.length && caixaAssuntos.children.length) caixaExemplos.open = true;
 } catch (erro) {
  if (id === requestNumber) status.textContent = 'Não consegui carregar a base agora. ' + erro.message;
 }
};


// Caixa "Consultar a norma": artigo, verbete, termo ou pergunta. O acolhimento vem antes de qualquer busca.
const campoBusca = document.querySelector('#query');
const caixaBusca = document.querySelector('#legal-results');
async function buscar() {
 const query = campoBusca.value.trim();
 if (!query) {
  caixaBusca.replaceChildren(element('p', 'Digite um assunto, o número de um artigo ou a sua dúvida.'));
  return;
 }
 caixaBusca.replaceChildren(element('p', 'Buscando…'));
 contar('busca', nivelSelecionado.value);
 try {
  const r = await consultarCaixa(query, nivelSelecionado.value);
  const itens = blocosDeCuidado(r.avisos);
  // Acolhimento na caixa: a ficha que estava aberta sai da tela, para não disputar a atenção.
  if (r.avisos.length) {
   ++requestNumber;
   limpar();
  }
  if (r.status) itens.push(element('p', r.status));
  if (r.apoio) {
   const linha = element('p', 'Precisa de ajuda agora? ', 'notice ajuda');
   [['CVV 188', 'tel:188', ' (apoio emocional)'], ['Disque 100', 'tel:100', ' (violência ou abuso)']].forEach(([rotulo, destino, para], i) => {
    const link = element('a', rotulo);
    link.href = destino;
    const par = element('span', '', 'junto');
    par.append(link, para);
    const sep = element('span', ' · ', 'sep');
    sep.setAttribute('aria-hidden', 'true');
    linha.append(...(i ? [sep, par] : [par]));
   });
   itens.push(linha);
  }
  if (r.candidatas.length) {
   const lista = element('div', '', 'examples');
   r.candidatas.forEach(ficha => {
    const botao = element('button', ficha.situacao.pergunta);
    botao.type = 'button';
    botao.onclick = () => navegar({p: ficha.perfil || nivelSelecionado.value || ficha.situacao.perfis[0], a: ficha.situacao.assunto, s: ficha.situacao.id});
    lista.append(botao);
   });
   // v5.23: saída para quem não se reconhece em nenhuma das fichas sugeridas.
   const nenhuma = element('button', 'Nenhuma destas');
   nenhuma.type = 'button';
   nenhuma.className = 'nenhuma-destas';
   nenhuma.onclick = () => caixaBusca.replaceChildren(element('p', 'O Jane só responde às situações que estão nas fichas. Para essa dúvida, veja a regra do seu curso ou pergunte ao professor ou à coordenação. Você também pode procurar pelo assunto no menu acima.', 'nenhuma'));
   lista.append(nenhuma);
   itens.push(lista);
  }
  itens.push(...r.linhas.map(sourceDetails));
  caixaBusca.replaceChildren(...itens);
 } catch (error) {
  caixaBusca.replaceChildren(element('p', error.message));
 }
}
document.querySelector('#search').onsubmit = event => {
 event.preventDefault();
 return buscar();
};
// Ao voltar para a página, o navegador devolve o texto da caixa sem os resultados: a busca é refeita.
if (typeof window !== 'undefined') window.addEventListener('pageshow', () => {
 if (campoBusca.value.trim()) buscar();
});
// Visita: uma por aba aberta (recarregar a página não conta de novo).
if (typeof window !== 'undefined') {
 let nova = true;
 try {
  nova = !sessionStorage.getItem('jane_visita');
  sessionStorage.setItem('jane_visita', '1');
 } catch (erro) {}
 if (nova) contar('visita');
 // Número discreto no rodapé, ao lado de "Realização: IAEduca". Se o servidor não responder, nada aparece.
 setTimeout(() => {
  if (!/^https?:$/.test(location.protocol)) return;
  fetch('conta.php', {cache: 'no-store'}).then(r => r.ok ? r.text() : '').then(t => {
   const n = parseInt(t, 10);
   const alvo = document.querySelector('#visitas');
   if (!alvo || !(n > 0)) return;
   alvo.textContent = ' · ' + n.toLocaleString('pt-BR') + (n === 1 ? ' visita' : ' visitas');
   alvo.hidden = false;
  }).catch(() => {});
 }, 800);
}
