import json, os
_ANT = json.load(open(os.path.join(os.path.dirname(__file__), 'fichas_antigas.json'), encoding='utf8'))
def M(perfil, i):
    return tuple(_ANT[perfil]['fichas'][i]['f'][:5])
def S(id, nucleo, perfis, tema, textos, disp, exige, reforca='', exclui='', peso=0, destaque=0):
    assert len(textos) == 5, id
    # Situação de um só conceito específico: vale mais que uma genérica de dois conceitos.
    if '+' not in exige and peso >= 5: peso += 12
    return dict(id=id, nucleo=nucleo, perfis=perfis, tema=tema, pergunta=textos[0], resposta=textos[1], motivo=textos[2],
                conferir=textos[3], acao=textos[4], disp=disp, exige=exige, reforca=reforca, exclui=exclui, peso=peso, destaque=destaque)
