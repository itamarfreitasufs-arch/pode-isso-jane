# Pode isso, Jane? | IA na educação segundo a Resolução CNE/CP nº 1/2026

Aplicativo de **Itamar Freitas**, versão **5.22**, de 26 de novembro de 2026, preparado com assistência de IA.

O Jane responde a dúvidas práticas sobre o uso de inteligência artificial na escola e na universidade, com base na [Resolução CNE/CP nº 1, de 11 de novembro de 2026](https://www.in.gov.br/web/dou/-/resolucao-cne/cp-n-1-de-11-de-novembro-de-2026-744136563). A pessoa escolhe o perfil, o assunto e a situação, ou escreve a dúvida, e recebe uma ficha com o que a norma permite, exige ou proíbe, sempre com o artigo que fundamenta a resposta.

**O Jane não usa IA.** Funciona por regras escritas à mão e por um banco SQLite que roda no próprio navegador (WebAssembly). Nada do que a pessoa escreve sai do aparelho.

Versão em uso: https://iaeduca.online/jane/

## Perfis

Estudante (fundamental e médio, graduação, pós-graduação), professor (fundamental e médio; graduação e pós-graduação), gestor escolar e pai, mãe ou responsável. São 309 fichas no total.

## Experimente no seu computador

1. Baixe o repositório (botão **Code → Download ZIP**) e descompacte.
2. Abra um terminal na pasta `app/` e rode `python3 -m http.server 8000`.
3. Acesse http://localhost:8000/ no navegador.

A página precisa de um servidor local porque o navegador não carrega o banco e o WebAssembly abrindo o arquivo direto. Para hospedar, basta copiar o conteúdo de `app/` para qualquer servidor de páginas estáticas.

Veja [protocolo.md](protocolo.md) para o método de construção (como o app foi feito e como replicá-lo ou melhorá-lo) e [COMO_USAR.md](COMO_USAR.md) para reconstruir o banco, mudar os perfis ativos e rodar as baterias de teste.

## Situação dos textos

**Esta é uma versão em teste com alunos.** Os textos das fichas e os textos de acolhimento ainda estão em revisão por estudantes de pós-graduação. Esta é uma edição experimental. As fichas resumem a norma, mas não a substituem: em caso de dúvida, vale o texto da resolução e as regras da sua instituição.

O Jane reconhece por regras algumas situações de risco (violência, abuso, aliciamento, automutilação, risco à vida) e responde com orientação de proteção e canais de ajuda, como CVV 188 e Disque 100. Nenhuma regra reconhece todas as formas de pedir ajuda; por isso as respostas sem correspondência trazem a linha de apoio. O app não é serviço de atendimento.

## Testes

Cada correção foi testada em baterias de perguntas **congeladas antes da correção**, com hash SHA-256 registrado (`congelado/`). Resultados e limites estão em [AVALIACAO.md](AVALIACAO.md).

## Organização

| Pasta | Conteúdo |
|---|---|
| `app/` | Versão pronta para publicar (sete perfis). |
| `dist/` | Fontes da tela (HTML, JS, CSS) usadas para montar `app/` e rodar as baterias antigas. |
| `construir/` | Gerador do banco: texto da norma (`norma_origem.sqlite`) e fichas, conceitos e regras (`sit_*.py`, `base.py`). |
| `congelado/` | Baterias congeladas, hashes e o pontuador. |
| `testes/` | Executores das baterias e testes de tela. |
| `servidor/` | Contador de visitas opcional, em PHP. Não é necessário para o app funcionar. |
| `docs/` | Histórico detalhado das versões. |

## Autoria e reutilização

© 2026 Itamar Freitas. O código está sob a [licença MIT](LICENSE). As fichas, os textos de acolhimento, as baterias de perguntas e a documentação estão sob [CC BY 4.0](LICENSE-CONTEUDO.md). Componentes de terceiros e o texto da resolução estão descritos em [AVISOS_DE_TERCEIROS.md](AVISOS_DE_TERCEIROS.md). Como citar: [CITATION.cff](CITATION.cff).

Para conferir a integridade dos arquivos: `sha256sum -c SHA256SUMS.txt`.

## Relatar um problema

Se o canal Issues estiver disponível, informe a versão, o perfil escolhido, a pergunta exata e a resposta recebida, e o que você esperava. Não escreva dados pessoais nem relatos reais de violência no Issues.
