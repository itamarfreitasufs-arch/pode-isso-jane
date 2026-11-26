# Contador de visitas (opcional)

O app funciona sem esta pasta. Ela serve a quem hospeda o Jane num servidor com PHP e quer saber quantas pessoas usam o app.

## Instalação

Copie `conta.php`, `painel.php` e a pasta `contagem/` (com o `.htaccess`) para a mesma pasta de `app/`. O servidor precisa permitir que o PHP grave em `contagem/`.

## O que é gravado

`conta.php` soma, por dia, o tipo de uso (visita, perfil escolhido, ficha aberta, dúvida escrita, busca na norma), o perfil e o código da ficha, em `contagem/AAAA-MM.json`. **Não grava IP, navegador, hora, cookie nem nada do que a pessoa escreve.** Eventos e perfis fora da lista são recusados, e cada dia aceita no máximo 400 chaves. Uma visita é uma aba aberta; recarregar não conta de novo.

Por GET, `conta.php` devolve só o total de visitas, que o app mostra discreto no rodapé.

## Painel

`painel.php?k=CHAVE` mostra os totais por dia, por perfil e por ficha. A chave fica em `contagem/chave.txt`, que **você cria no servidor** com uma sequência aleatória de pelo menos 12 caracteres (por exemplo, a saída de `openssl rand -hex 16`). Nunca coloque esse arquivo no repositório; o `.gitignore` já o exclui. O `.htaccess` fecha a pasta `contagem/` ao navegador.
