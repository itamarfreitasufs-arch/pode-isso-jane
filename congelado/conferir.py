# Confere os hashes registrados no congelamento de cada bateria.
# Os arquivos SHA256_*.txt foram gravados em momentos diferentes, com caminhos em formatos diferentes;
# este script lê o hash e o nome de cada linha e procura o arquivo em congelado/ e em testes/.
# Uso (na raiz do repositório): python3 congelado/conferir.py
import hashlib, pathlib, re, sys
raiz = pathlib.Path(__file__).resolve().parent.parent
ok = falha = 0
for reg in sorted((raiz / 'congelado').glob('SHA256*.txt')):
    for linha in reg.read_text(encoding='utf8').splitlines():
        m = re.match(r'^([0-9a-f]{64})\s+\*?(.+?)\s*$', linha)
        if not m: continue
        h, nome = m.group(1), pathlib.Path(m.group(2).strip()).name
        alvo = next((p for p in (raiz / 'congelado' / nome, raiz / 'testes' / nome) if p.exists()), None)
        if alvo is None:
            print(f'AUSENTE  {reg.name}: {nome}'); continue
        if hashlib.sha256(alvo.read_bytes()).hexdigest() == h: ok += 1
        else: falha += 1; print(f'DIFERE   {reg.name}: {alvo.relative_to(raiz)} (o arquivo mudou depois do registro)')
print(f'{ok} conferidos, {falha} diferentes')
sys.exit(1 if falha else 0)
