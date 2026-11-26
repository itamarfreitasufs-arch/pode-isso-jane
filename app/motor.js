// Banco (SQLite no navegador), busca na norma e carga da base de triagem.
function normalizar(valor) {
 return String(valor).toLowerCase().normalize('NFKD').replace(/\p{M}/gu, '');
}
let carregamento;
async function banco() {
 if (!carregamento) {
  carregamento = Promise.all([
   initSqlJs({locateFile: nome => nome}),
   fetch('norma.sqlite?v=5.14').then(r => {
    if (!r.ok) throw new Error('Banco indisponível.');
    return r.arrayBuffer();
   })
  ]).then(([SQL, bytes]) => new SQL.Database(new Uint8Array(bytes))).catch(erro => {
   carregamento = undefined;
   throw erro;
  });
 }
 return carregamento;
}
function consultar(db, sql, parametros = []) {
 const consulta = db.prepare(sql);
 try {
  consulta.bind(parametros);
  const saida = [];
  while (consulta.step()) saida.push(consulta.getAsObject());
  return saida;
 } finally {
  consulta.free();
 }
}

// Base de triagem: lida uma vez e mantida em memória.
let baseCarregada;
async function carregarBase() {
 if (!baseCarregada) {
  baseCarregada = banco().then(db => {
   const re = padrao => new RegExp(padrao);
   const conceitos = Object.fromEntries(consultar(db, 'SELECT nome, padrao FROM conceito').map(c => [c.nome, re(c.padrao)]));
   const situacoes = consultar(db, 'SELECT * FROM situacao ORDER BY ordem');
   const porId = Object.fromEntries(situacoes.map(s => [s.id, s]));
   situacoes.forEach(s => {
    s.perfis = [];
    s.dispositivos = [];
    s.grupos = s.exige.split('+').map(g => g.split('|'));
    s.reforcos = s.reforca.split(' ').filter(Boolean);
    s.exclusoes = s.exclui.split(' ').filter(Boolean);
   });
   consultar(db, 'SELECT situacao_id, perfil FROM situacao_perfil').forEach(r => porId[r.situacao_id].perfis.push(r.perfil));
   consultar(db, 'SELECT d.situacao_id, u.* FROM situacao_dispositivo d JOIN unidade u ON u.id = d.unidade_id ORDER BY d.situacao_id, d.ordem')
    .forEach(r => porId[r.situacao_id].dispositivos.push(r));
   const unidades = consultar(db, "SELECT * FROM unidade WHERE tipo != 'contexto' ORDER BY id");
   unidades.forEach(u => u.normal = normalizar(u.texto));
   // Guia de Risco (Anexo II): o quadro e os textos que o acompanham, para a busca por "anexo II".
   const anexoII = consultar(db, "SELECT * FROM unidade WHERE secao = 'Anexo II' AND localizador != 'REFERÊNCIAS' ORDER BY CASE localizador WHEN 'Critérios gerais do guia' THEN 0 WHEN 'Quadro de classificação de risco' THEN 1 WHEN 'Disposições finais' THEN 2 ELSE 3 END");
   return {
    conceitos, situacoes, porId, unidades, anexoII,
    assuntos: consultar(db, 'SELECT chave, rotulo FROM assunto ORDER BY ordem'),
    perfis: Object.fromEntries(consultar(db, 'SELECT chave, nome FROM perfil').map(p => [p.chave, p.nome])),
    portoes: consultar(db, 'SELECT * FROM portao ORDER BY ordem').map(p => ({...p, re: re(p.padrao)})),
    papeis: consultar(db, 'SELECT * FROM papel ORDER BY id').map(p => ({...p, re: re(p.padrao)})),
    complementos: consultar(db, 'SELECT * FROM complemento ORDER BY id').map(c => ({...c, re: re(c.padrao)})),
    mensagens: Object.fromEntries(consultar(db, 'SELECT chave, texto FROM mensagem').map(m => [m.chave, m.texto]))
   };
  }).catch(erro => {
   baseCarregada = undefined;
   throw erro;
  });
 }
 return baseCarregada;
}

const vazias = new Set('a o as os um uma uns umas de da do das dos em no na nos nas e ou que se com por para pra pro pela pelo ao aos como mais mas nao sim eu me meu minha meus minhas seu sua voce ele ela isso isto esse essa este esta e eh foi ser sao ter tem tenho pode posso podem sobre qual quais quando onde quem diz dizer artigo art resolucao norma ia usar uso usei escola aluno alunos professor professora faz fazer fiz ja so tambem muito entao ai la aqui the of'.split(' '));
function radical(termo) {
 return termo.length > 4 ? termo.replace(/(coes|soes|oes|aes|ais|eis|ns|cao|sao|ao|as|os|es|a|o|e|s)$/, '') : termo;
}
const conectivos = new Set('a o as os um uma de da do das dos em no na nos nas e ou que se com por para pra ao aos'.split(' '));
// Palavras do dia a dia que a norma escreve de outro jeito ("detector" → "detecção").
const equivalentes = {detector: 'detecc', detectores: 'detecc', antiplagio: 'detecc', chatbot: 'conversacional', chatbots: 'conversacional', camera: 'vigilancia', cameras: 'vigilancia', creche: 'educacao infantil', cola: 'honestidade academica',
 plagio: 'integridade academica', plagios: 'integridade academica', chatgpt: 'generativa', gpt: 'generativa', gemini: 'generativa', copilot: 'generativa', lgpd: 'dados pessoais', tese: 'pesquisa cientifica', teses: 'pesquisa cientifica', dissertacao: 'pesquisa cientifica', tcc: 'pesquisa cientifica', prova: 'avaliacoes', provas: 'avaliacoes', pos: '', graduacao: 'educacao superior', faculdade: 'educacao superior', universidade: 'educacao superior', cne: 'conselho nacional educacao', mec: 'ministerio educacao'};
function radicais(texto, paraBusca = false) {
 const fora = paraBusca ? conectivos : vazias;
 const palavras = (normalizar(texto).match(/[a-z0-9]+/g) ?? []).flatMap(t => paraBusca && equivalentes[t] ? equivalentes[t].split(' ') : [t]);
 return [...new Set(palavras.filter(t => !fora.has(t) && t.length > 1).map(t => t === 'detecc' ? t : radical(t)))].slice(0, 12);
}
// O radical precisa começar uma palavra: "emoc" acha "emoções", não "promoção".
const noInicio = {};
function contem(textoNormal, termo) {
 return (noInicio[termo] ??= new RegExp('\\b' + termo)).test(textoNormal);
}
const romanos = /^(x{0,2})(ix|iv|v?i{0,3})$/;
const TOTAL_ARTIGOS = 47;
// Busca na norma: "art. 41", "art. 41, X", "art. 40 § 4", "verbete 87", "anexo II", um número ou termos, ordenados por relevância.
// A lista devolvida pode trazer .nota (aviso para a tela) e .ref (a busca citou um dispositivo pelo nome ou número).
async function buscarNorma(busca) {
 const base = await carregarBase();
 const texto = normalizar(busca).replace(/\s+/g, ' ').trim();
 if (!texto) return [];
 const ref = (linhas, nota = '') => Object.assign(linhas, {ref: true, nota});
 const verbetes = base.unidades.filter(u => u.secao === 'Anexo I' && u.tipo === 'verbete');
 const semArtigo = 'Não encontrei esse artigo. A resolução tem ' + TOTAL_ARTIGOS + ' artigos.';
 const semVerbete = 'Não encontrei esse verbete. O Glossário (Anexo I) tem ' + verbetes.length + ' verbetes.';
 const doArtigo = n => base.unidades.filter(u => u.secao === 'Resolução' && u.artigo === n);
 const doVerbete = n => verbetes.filter(u => u.localizador === 'Item ' + n);
 const pedeVerbete = texto.match(/^(?:glossario|anexo (?:i|1))?[ ,·:-]*(?:verbete|item)? ?(?:n[ºo°.]* ?)?(\d{1,4})$/);
 if (pedeVerbete && /[a-z]/.test(texto)) {
  const linhas = doVerbete(Number(pedeVerbete[1]));
  return ref(linhas, linhas.length ? '' : semVerbete);
 }
 if (/^(o )?(glossario|anexo (i|1))( da resolucao)?$/.test(texto)) return ref([], 'O Glossário (Anexo I) tem ' + verbetes.length + ' verbetes. Busque pelo termo (ex.: detector) ou pelo número (ex.: verbete 87).');
 if (/^(o )?(anexo (ii|2)|guia de (interpretacao|risco)( da classificacao de risco)?|quadro de (classificacao de )?risco|classificacao de risco)$/.test(texto)) return ref([...base.anexoII]);
 // Número solto: o artigo e o verbete de mesmo número.
 if (/^\d{1,4}$/.test(texto)) {
  const linhas = [...doArtigo(Number(texto)), ...doVerbete(Number(texto))];
  return ref(linhas, linhas.length ? '' : semArtigo);
 }
 const artigo = texto.match(/^(?:o que diz (?:o )?)?art(?:igo)?s?\.? ?(\d+) ?[ºo°]? ?[,;]? ?(.*)$/);
 if (artigo) {
  let linhas = doArtigo(Number(artigo[1]));
  if (!linhas.length) return ref([], semArtigo);
  const resto = artigo[2].replace(/\binciso\b|\bcaput\b|[?.!]/g, '').trim();
  const paragrafo = resto.match(/(?:§|paragrafo)\s*(\d+|unico)/);
  const inciso = resto.replace(/(?:§|paragrafo)\s*(\d+|unico)\s*[ºo°]?/, '').replace(/[, ]+/g, '').toUpperCase();
  if (paragrafo) linhas = linhas.filter(u => normalizar(u.localizador).includes(paragrafo[1] === 'unico' ? 'paragrafo unico' : '§ ' + paragrafo[1]));
  if (inciso && romanos.test(inciso.toLowerCase())) {
   const comInciso = linhas.filter(u => u.localizador.endsWith('inciso ' + inciso));
   if (comInciso.length) linhas = comInciso;
  }
  return ref(linhas);
 }
 const termos = radicais(texto, true);
 if (!termos.length) return [];
 const minimo = termos.length <= 3 ? termos.length : Math.ceil(termos.length * 0.6);
 return base.unidades.map(u => ({u, n: termos.filter(t => contem(u.normal, t)).length}))
  .filter(x => x.n >= minimo).sort((a, b) => b.n - a.n || a.u.id - b.u.id).slice(0, 20).map(x => x.u);
}
// Trechos da resolução que compartilham termos raros com a pergunta (usado quando não há ficha).
async function sugerirDispositivos(pergunta) {
 const base = await carregarBase();
 const corpo = base.unidades.filter(u => u.secao === 'Resolução');
 const termos = radicais(pergunta).filter(t => t.length > 3);
 const peso = Object.fromEntries(termos.map(t => {
  const df = corpo.filter(u => contem(u.normal, t)).length;
  return [t, df && df <= 25 ? Math.log(corpo.length / df) : 0];
 }));
 return corpo.map(u => ({u, p: termos.reduce((s, t) => s + (contem(u.normal, t) ? peso[t] : 0), 0), n: termos.filter(t => peso[t] && contem(u.normal, t)).length}))
  .filter(x => x.n >= 2 || x.p >= 3.4).sort((a, b) => b.p - a.p || a.u.id - b.u.id).slice(0, 3).map(x => x.u);
}
// Verbete do glossário (Anexo I) cujo termo aparece na pergunta.
async function verbete(pergunta) {
 const base = await carregarBase();
 const termos = radicais(pergunta.replace(/^.*?\b(o que e|o que significa|que significa|o que sao|definicao de|conceito de|significado de)\b/, ''));
 if (!termos.length) return null;
 const candidatos = base.unidades.filter(u => u.secao === 'Anexo I' && u.tipo === 'verbete').map(u => {
  const titulo = radicais((u.texto.match(/^\d+\.\s*([^:]+):/) ?? [,''])[1]);
  const comuns = titulo.filter(t => termos.includes(t)).length;
  return {u, comuns, cobertura: titulo.length ? comuns / titulo.length : 0};
 }).filter(x => x.comuns && x.cobertura >= 0.5).sort((a, b) => b.cobertura - a.cobertura || b.comuns - a.comuns);
 return candidatos[0]?.u ?? null;
}
