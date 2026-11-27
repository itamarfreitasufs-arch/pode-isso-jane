# Uso: python3 build.py <norma.sqlite de origem> <norma.sqlite de destino> [perfis ativos, separados por vírgula]
# Com o terceiro argumento, só os perfis indicados são publicados: as fichas dos demais ficam fora do banco
# e o index.html da pasta de destino tem as outras opções de perfil desativadas.
# Copia o banco da norma e acrescenta as tabelas de triagem, validando cada referência.
import sys, shutil, sqlite3, re
sys.path.insert(0, __import__('os').path.dirname(__file__))
import base, sit_estudantes, sit_profissionais, sit_novas, sit_pos, sit_gra, sit_bas, sit_prof, sit_ge, sit_fa
orig, dest = sys.argv[1:3]
ATIVOS = sys.argv[3].split(',') if len(sys.argv) > 3 else list(base.PERFIS)
assert all(p in base.PERFIS for p in ATIVOS), ATIVOS
base.CONCEITOS.update(sit_pos.CONCEITOS)
base.CONCEITOS.update(sit_gra.CONCEITOS)
for k, v in sit_gra.AMPLIA.items(): base.CONCEITOS[k] += '|' + v
base.CONCEITOS.update(sit_bas.CONCEITOS)
for k, v in sit_bas.AMPLIA.items(): base.CONCEITOS[k] += '|' + v
base.CONCEITOS.update(sit_prof.CONCEITOS)
for k, v in sit_prof.AMPLIA.items(): base.CONCEITOS[k] += '|' + v
base.CONCEITOS.update(sit_ge.CONCEITOS)
base.CONCEITOS.update(sit_fa.CONCEITOS)
base.MENSAGENS['perfil_inativo'] = sit_fa.MENSAGEM_INATIVO if 'responsavel' in ATIVOS else sit_prof.MENSAGEM_INATIVO if 'profBasico' in ATIVOS else sit_bas.MENSAGEM_INATIVO if 'basico' in ATIVOS else sit_gra.MENSAGEM_INATIVO if 'graduacao' in ATIVOS else sit_pos.MENSAGEM_INATIVO
shutil.copyfile(orig, dest)
db = sqlite3.connect(dest)
# Anexos: o quadro de risco vinha como texto de PDF em colunas e dois títulos vinham colados.
import anexos
anexos.corrigir(db)
db.executescript('''
DROP TABLE IF EXISTS assunto; DROP TABLE IF EXISTS conceito; DROP TABLE IF EXISTS situacao; DROP TABLE IF EXISTS situacao_perfil;
DROP TABLE IF EXISTS situacao_dispositivo; DROP TABLE IF EXISTS complemento; DROP TABLE IF EXISTS portao;
DROP TABLE IF EXISTS papel; DROP TABLE IF EXISTS mensagem; DROP TABLE IF EXISTS perfil;
CREATE TABLE perfil(chave TEXT PRIMARY KEY, nome TEXT NOT NULL);
CREATE TABLE conceito(nome TEXT PRIMARY KEY, padrao TEXT NOT NULL);
CREATE TABLE situacao(id TEXT PRIMARY KEY, ordem INTEGER, nucleo TEXT NOT NULL, tema TEXT NOT NULL, pergunta TEXT NOT NULL,
  resposta TEXT NOT NULL, motivo TEXT NOT NULL, conferir TEXT NOT NULL, acao TEXT NOT NULL,
  exige TEXT NOT NULL, reforca TEXT NOT NULL, exclui TEXT NOT NULL, peso INTEGER NOT NULL, destaque INTEGER NOT NULL, sinal TEXT NOT NULL, modelo TEXT NOT NULL, assunto TEXT NOT NULL);
CREATE TABLE assunto(chave TEXT PRIMARY KEY, ordem INTEGER, rotulo TEXT NOT NULL);
CREATE TABLE situacao_perfil(situacao_id TEXT REFERENCES situacao(id), perfil TEXT REFERENCES perfil(chave), PRIMARY KEY(situacao_id, perfil));
CREATE TABLE situacao_dispositivo(situacao_id TEXT REFERENCES situacao(id), ordem INTEGER, unidade_id INTEGER REFERENCES unidade(id), PRIMARY KEY(situacao_id, ordem));
CREATE TABLE complemento(id INTEGER PRIMARY KEY, alvo TEXT NOT NULL, padrao TEXT NOT NULL, exige TEXT NOT NULL, texto TEXT NOT NULL);
CREATE TABLE portao(ordem INTEGER PRIMARY KEY, nome TEXT UNIQUE, padrao TEXT NOT NULL, continua INTEGER NOT NULL, mensagem TEXT NOT NULL);
CREATE TABLE papel(id INTEGER PRIMARY KEY, perfil TEXT NOT NULL, forte INTEGER NOT NULL, padrao TEXT NOT NULL);
CREATE TABLE mensagem(chave TEXT PRIMARY KEY, texto TEXT NOT NULL);
''')
for k, v in base.PERFIS.items():
    if k in ATIVOS: db.execute('INSERT INTO perfil VALUES(?,?)', (k, v))
for k, v in base.CONCEITOS.items():
    re.compile(v); db.execute('INSERT INTO conceito VALUES(?,?)', (k, v))
sits = sit_estudantes.SITUACOES + sit_profissionais.SITUACOES
sits = sits + sit_novas.SITUACOES + sit_novas.SITUACOES2
for id_, campos in sit_novas.AJUSTES.items():
    alvo = [s for s in sits if s['id'] == id_]
    assert len(alvo) == 1, id_
    alvo[0].update(campos)
for id_, (cor, resposta, *pergunta) in sit_novas.CARTOES.items():
    alvo = [s for s in sits if s['id'] == id_]
    assert len(alvo) == 1, id_
    alvo[0]['resposta'] = resposta
    if pergunta: alvo[0]['pergunta'] = pergunta[0]
sits = [s for s in sits if s['id'] not in sit_novas.DESATIVADAS]
# Revisão do perfil Pós-graduação: fichas que saem do perfil, correções e fichas novas.
for id_ in sit_pos.SAI_DO_POS:
    alvo = [s for s in sits if s['id'] == id_]
    assert len(alvo) == 1 and 'pos' in alvo[0]['perfis'], id_
    alvo[0]['perfis'] = [p for p in alvo[0]['perfis'] if p != 'pos']
for id_, campos in sit_pos.ALTERA.items():
    alvo = [s for s in sits if s['id'] == id_]
    assert len(alvo) == 1, id_
    for k, v in campos.items():
        if k.endswith('+'): alvo[0][k[:-1]] = alvo[0][k[:-1]] + v
        else: alvo[0][k] = v
sits = sits + sit_pos.SITUACOES
# Perfil Graduação: fichas derivadas das da pós, fichas comuns ao ensino superior e fichas próprias.
sits = sit_gra.aplicar(sits, lambda i: sit_novas.CARTOES.get(i, (base.sinal(i),))[0], base.MODELOS)
# Perfil Estudante da educação básica: fichas próprias, uma só etapa separada em "Posso usar IA?".
sits = sit_bas.aplicar(sits)
# Perfis de professor: ensino fundamental e médio; graduação e pós-graduação.
sits = sit_prof.aplicar(sits)
# Perfis de gestor escolar e de pai, mãe ou responsável.
sits = sit_fa.aplicar(sits)
# v5.22: ficha das entrevistas do TCC e irmãs com veredito "Não" inequívoco.
import sit_v522
for id_, campos in sit_v522.AJUSTES.items():
    alvo = [s for s in sits if s['id'] == id_]
    assert len(alvo) == 1, id_
    alvo[0].update(campos)
todos_ids = {s['id'] for s in sits}; todos_nucleos = {s['nucleo'] for s in sits}
sits = [dict(s, perfis=[p for p in s['perfis'] if p in ATIVOS]) for s in sits if any(p in ATIVOS for p in s['perfis'])]
# Dispositivos fora do corpo da resolução: verbetes do Glossário (Anexo I) e o Guia de Risco (Anexo II).
def unidade(loc):
    m = re.fullmatch(r'Glossário, verbete (\d+)', loc)
    if m: return ('Anexo I', 'Item ' + m.group(1))
    if loc == 'Anexo II, quadro': return ('Anexo II', 'Quadro de classificação de risco')
    if loc == 'Anexo II, critérios gerais': return ('Anexo II', 'Critérios gerais do guia')
    return ('Resolução', loc)
erros = []
assunto_de = {n: chave for chave, _, nucleos in base.ASSUNTOS for n in (nucleos + ' ' + sit_pos.NUCLEOS.get(chave, '') + ' ' + sit_gra.NUCLEOS.get(chave, '') + ' ' + sit_bas.NUCLEOS.get(chave, '') + ' ' + sit_prof.NUCLEOS.get(chave, '') + ' ' + sit_ge.NUCLEOS.get(chave, '') + ' ' + sit_fa.NUCLEOS.get(chave, '')).split()}
for i, (chave, rotulo, _) in enumerate(base.ASSUNTOS): db.execute('INSERT INTO assunto VALUES(?,?,?)', (chave, i, rotulo))
nomes = set(base.CONCEITOS)
for n, s in enumerate(sits):
    for campo in ('exige', 'reforca', 'exclui'):
        for c in re.split(r'[+| ]+', s[campo]):
            if c and c not in nomes: erros.append(f"{s['id']}: conceito desconhecido «{c}» em {campo}")
    if s['nucleo'] not in assunto_de: erros.append(f"{s['id']}: núcleo «{s['nucleo']}» sem assunto")
    db.execute('INSERT INTO situacao VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (s['id'], n, s['nucleo'], s['tema'], s['pergunta'], s['resposta'],
               s['motivo'], s['conferir'], s['acao'], s['exige'], s['reforca'], s['exclui'], s['peso'], s['destaque'], s.get('sinal') or sit_novas.CARTOES.get(s['id'], (base.sinal(s['id']),))[0], s.get('modelo') or base.MODELOS.get(s['id'], ''), assunto_de.get(s['nucleo'], '')))
    for p in s['perfis']:
        if p not in base.PERFIS: erros.append(f"{s['id']}: perfil {p}")
        db.execute('INSERT INTO situacao_perfil VALUES(?,?)', (s['id'], p))
    for i, loc in enumerate(s['disp']):
        r = db.execute("SELECT id FROM unidade WHERE secao=? AND localizador=?", unidade(loc)).fetchall()
        if len(r) != 1: erros.append(f"{s['id']}: localizador «{loc}» encontrado {len(r)} vez(es)")
        else: db.execute('INSERT INTO situacao_dispositivo VALUES(?,?,?)', (s['id'], i, r[0][0]))
    # todo "art. N" citado no texto precisa existir entre os dispositivos da ficha
    corpo = s['resposta'] + ' ' + s['motivo'] + ' ' + s['acao']
    citados = set(int(x) for x in re.findall(r'art\. (\d+)', corpo))
    ligados = set(int(re.match(r'Art\. (\d+)', l).group(1)) for l in s['disp'] if l.startswith('Art.'))
    # o mesmo vale para os anexos: verbete citado e menção ao Anexo II precisam do dispositivo ligado
    verbetes = set(re.findall(r'verbete (\d+)', corpo)) - set(l.split()[-1] for l in s['disp'] if l.startswith('Glossário'))
    if verbetes: erros.append(f"{s['id']}: texto cita verbete {sorted(verbetes)} sem dispositivo ligado")
    if 'Anexo II' in corpo and not any(l.startswith('Anexo II') for l in s['disp']): erros.append(f"{s['id']}: texto cita o Anexo II sem dispositivo ligado")
    if any(l.startswith('Glossário') for l in s['disp']) and 'verbete' not in corpo: erros.append(f"{s['id']}: verbete ligado sem citação no texto")
    falta = citados - ligados
    if falta: erros.append(f"{s['id']}: texto cita art. {sorted(falta)} sem dispositivo ligado")
ids = {s['id'] for s in sits}; nucleos = {s['nucleo'] for s in sits}
for k, v in base.CUIDADO_VARIANTES.items(): base.MENSAGENS[k] = v
for alvo, padrao, exige, texto in base.COMPLEMENTOS:
    if not alvo.startswith('*') and alvo not in todos_ids | todos_nucleos: erros.append(f'complemento: alvo {alvo}')
    if not alvo.startswith('*') and alvo not in ids | nucleos: continue
    pad = base.CONCEITOS.get(padrao, padrao); re.compile(pad)
    if exige and exige not in nomes: erros.append(f'complemento: exige {exige}')
    db.execute('INSERT INTO complemento(alvo,padrao,exige,texto) VALUES(?,?,?,?)', (alvo, pad, exige, texto))
for i, (nome, padrao, continua, msg) in enumerate(base.PORTOES):
    re.compile(padrao); db.execute('INSERT INTO portao VALUES(?,?,?,?,?)', (i, nome, padrao, continua, msg))
for perfil, forte, padrao in base.PAPEIS:
    re.compile(padrao); db.execute('INSERT INTO papel(perfil,forte,padrao) VALUES(?,?,?)', (perfil, forte, padrao))
for k, v in base.MENSAGENS.items(): db.execute('INSERT INTO mensagem VALUES(?,?)', (k, v))
if len(ids) != len(sits): erros.append('ids de situação repetidos')
for k in set(base.MODELOS) - todos_ids: erros.append('modelo para situação inexistente: ' + k)
for k in base.SINAIS_IDS - todos_ids: erros.append('sinal para situação inexistente: ' + k)
if erros:
    print('\n'.join(erros)); sys.exit(1)
db.execute("INSERT OR REPLACE INTO fonte VALUES('triagem','Jane v2: situações, conceitos, portões e complementos')")
db.commit(); db.execute('VACUUM')
if len(sys.argv) > 3:
    # Tela: as opções dos perfis inativos ficam desativadas; com um perfil só, ele já vem escolhido.
    pagina = __import__('os').path.join(__import__('os').path.dirname(dest), 'index.html')
    html = open(pagina, encoding='utf8').read()
    def opcao(m):
        if m.group(1) not in ATIVOS: return '<option disabled value="%s">%s · em breve</option>' % m.groups()
        return m.group(0).replace('<option ', '<option selected ') if len(ATIVOS) == 1 else m.group(0)
    html, n = re.subn(r'<option value="(\w+)">([^<]*)</option>', opcao, html)
    assert n == len(base.PERFIS), n
    # Com o perfil único da educação básica no ar, as três opções antigas por etapa saem da lista.
    if 'basico' in ATIVOS:
        html = re.sub(r'<option disabled value="(iniciais|finais|medio)">[^<]*</option>\n?', '', html)
    # O mesmo vale para os perfis antigos de professor quando os novos estão no ar.
    if 'profBasico' in ATIVOS:
        html = re.sub(r'<option disabled value="(docenteFundamental|docenteMedio|docenteSuperior)">[^<]*</option>\n?', '', html)
    # O perfil de orientador não vai existir: as fichas de orientação estão no perfil do professor do superior.
    if 'orientador' not in ATIVOS:
        html = re.sub(r'<option disabled value="orientador">[^<]*</option>\n?', '', html)
    # Com os perfis novos de gestor escolar e de responsável no ar, as opções antigas saem da lista.
    if 'gestorEscolar' in ATIVOS:
        html = re.sub(r'<option disabled value="gestor">[^<]*</option>\n?', '', html)
    if 'responsavel' in ATIVOS:
        html = re.sub(r'<option disabled value="familia">[^<]*</option>\n?', '', html)
    open(pagina, 'w', encoding='utf8').write(html)
print('situações', len(sits), '| conceitos', len(base.CONCEITOS), '| portões', len(base.PORTOES), '| complementos', len(base.COMPLEMENTOS))
print('por perfil', db.execute('select perfil,count(*) from situacao_perfil group by 1').fetchall())
arts = sorted({r[0] for r in db.execute('select distinct u.artigo from situacao_dispositivo d join unidade u on u.id=d.unidade_id where u.artigo is not null')})
print('artigos cobertos', len(arts), arts)
print('incisos do art. 41', sorted(r[0] for r in db.execute("select distinct u.localizador from situacao_dispositivo d join unidade u on u.id=d.unidade_id where u.artigo=41")))
