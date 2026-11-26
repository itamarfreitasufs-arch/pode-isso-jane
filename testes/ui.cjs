// Teste de tela da v5.8: histórico, caixa de busca, acolhimento, quadro do Anexo II. Uso: node ui.cjs <pasta de saída> [perfil]
const {chromium} = require('playwright');
(async () => {
 const out = process.argv[2], perfil = process.argv[3] || 'pos';
 const b = await chromium.launch();
 const p = await b.newPage({viewport: {width: 360, height: 800}, deviceScaleFactor: 1});
 const errs = [];
 p.on('pageerror', e => errs.push(String(e)));
 p.on('console', m => m.type() === 'error' && errs.push(m.text()));
 const ok = (nome, cond, extra = '') => console.log((cond ? 'OK   ' : 'FALHA') + ' ' + nome + (extra ? ' | ' + extra : ''));
 await p.goto('http://localhost:8765/');
 await p.waitForSelector('#level');
 console.log('opcoes:', (await p.$$eval('#level option', o => o.map(x => x.textContent + (x.disabled ? ' [off]' : '') + (x.selected ? ' [sel]' : '')))).join(' / '));
 if (!(await p.$('#assuntos button'))) await p.selectOption('#level', perfil);
 await p.waitForSelector('#assuntos button');
 // abre todas as fichas pelo menu
 let total = 0;
 const n = await p.$$eval('#assuntos button', x => x.length);
 for (let i = 0; i < n; i++) {
  await (await p.$$('#assuntos button'))[i].click();
  const m = await p.$$eval('#level-examples button', x => x.length);
  if (m === 0) { total += (await p.$('#results article')) ? 1 : 0; continue; }
  for (let j = 0; j < m; j++) { await (await p.$$('#level-examples button'))[j].click(); if (await p.$('#results article')) total++; }
 }
 console.log('fichas abertas pelo menu:', total);
 // Voltar: da ficha para a lista de situações
 await p.goto('http://localhost:8765/');
 if (!(await p.$('#assuntos button'))) await p.selectOption('#level', perfil);
 await p.waitForSelector('#assuntos button');
 await (await p.$$('#assuntos button'))[0].click();
 await (await p.$$('#level-examples button'))[1].click();
 const pergunta = await p.$eval('#results .asked', e => e.textContent);
 const url = p.url();
 await p.goBack();
 await p.waitForTimeout(300);
 ok('Voltar fecha a ficha e mantém a lista', !(await p.$('#results article')) && (await p.$$eval('#level-examples button', x => x.length)) > 1, p.url());
 await p.goForward(); await p.waitForTimeout(300);
 ok('Avançar reabre a ficha', (await p.$eval('#results .asked', e => e.textContent).catch(() => '')) === pergunta);
 await p.reload(); await p.waitForSelector('#results article');
 ok('Recarregar mantém a ficha', (await p.$eval('#results .asked', e => e.textContent)) === pergunta && p.url() === url, url);
 await p.goBack(); await p.waitForTimeout(300); await p.goBack(); await p.waitForTimeout(300);
 ok('Dois Voltar: lista de assuntos sem situações', (await p.$$eval('#level-examples button', x => x.length)) === 0 && (await p.$$eval('#assuntos button', x => x.length)) > 5, p.url());
 // caixa
 const buscar = async q => { await p.fill('#query', q); await p.click('#search button'); await p.waitForFunction(() => !document.querySelector('#legal-results').textContent.includes('Buscando')); return p.$eval('#legal-results', e => e.innerText); };
 let t = await buscar('quero me matar');
 ok('acolhimento na caixa', /188/.test(t) && !/Sem correspond/.test(t) && !!(await p.$('#legal-results .care a[href="tel:188"]')));
 await p.screenshot({path: out + '/caixa-acolhimento.png', fullPage: true});
 t = await buscar({gestorEscolar: 'posso proibir a ia na escola inteira?', responsavel: 'a escola acusou meu filho de usar ia'}[perfil] || 'posso usar chatgpt na minha tese');
 ok('pergunta na caixa oferece fichas', (await p.$$eval('#legal-results .examples button', x => x.length)) >= 1, t.slice(0, 120).replace(/\n/g, ' / '));
 await p.click('#legal-results .examples button');
 await p.waitForSelector('#results article');
 ok('ficha aberta pela caixa', /#\w+\/\w+\/\w+/.test(p.url()), p.url());
 await p.goBack(); await p.waitForTimeout(300);
 ok('Voltar depois da ficha da caixa', !(await p.$('#results article')));
 t = await buscar('anexo II');
 await p.click('#legal-results details:nth-of-type(2) > summary');
 const larg = await p.$eval('#legal-results .quadro', e => [e.scrollWidth, e.clientWidth, e.querySelectorAll('h4').length, e.offsetHeight]);
 ok('quadro do Anexo II cabe na tela', larg[0] <= larg[1] && larg[2] === 4, JSON.stringify(larg));
 await p.screenshot({path: out + '/quadro.png', fullPage: true});
 t = await buscar('art. 100'); ok('art. 100', /47 artigos/.test(t) && !/Art\. 10/.test(t));
 t = await buscar('verbete 87'); ok('verbete 87', /verbete 87/.test(t));
 t = await buscar('5'); ok('número 5', /Art\. 5/.test(t) && /verbete 5/.test(t));
 await p.selectOption('#level', '');
 ok('sem perfil avisa', /Selecione o seu perfil/.test(await p.$eval('#status', e => e.textContent)));
 console.log('largura da página:', await p.evaluate(() => document.documentElement.scrollWidth));
 console.log('erros:', errs);
 await b.close();
})();
