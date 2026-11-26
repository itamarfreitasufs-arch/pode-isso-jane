// Teste de tela do reteste (v5.9): acolhimento na caixa, endereços inválidos, texto da caixa depois de Voltar. Uso: node ui2.cjs
const {chromium} = require('playwright');
(async () => {
 const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 360, height: 800}});
 const errs = []; p.on('pageerror', e => errs.push(String(e)));
 const ok = (nome, cond, extra = '') => console.log((cond ? 'OK   ' : 'FALHA') + ' ' + nome + (extra ? ' | ' + String(extra).slice(0, 160).replace(/\n/g, ' / ') : ''));
 const U = 'http://localhost:8765/';
 const buscar = async q => { await p.fill('#query', q); await p.click('#search button'); await p.waitForFunction(() => !document.querySelector('#legal-results').textContent.includes('Buscando')); return p.$eval('#legal-results', e => e.innerText); };
 // N5
 await p.goto(U + '#pos/usar/pos_uso'); await p.waitForSelector('#results article');
 let t = await buscar('sou vítima de deepfake nude');
 ok('N5 ficha anterior some ao acolher', !(await p.$('#results article')));
 const [h, par] = await p.$eval('#legal-results .care', e => [e.querySelector('h2').textContent, e.querySelector('p').textContent]);
 ok('N5 título não se repete na primeira frase', !par.startsWith(h.replace(/[.!]$/, '')), h + ' || ' + par.slice(0, 50));
 // N6
 await p.goto('about:blank'); await p.goto(U + '#familia'); await p.waitForTimeout(600);
 ok('N6 perfil desativado avisa', /em breve|por enquanto|selecione/i.test(await p.$eval('#status', e => e.textContent)), await p.$eval('#status', e => e.textContent));
 await p.goto('about:blank'); await p.goto(U + '#pos/xxx/yyy'); await p.waitForTimeout(600);
 ok('N6 ficha inexistente avisa e mostra assuntos', /não encontrei|nao encontrei/i.test(await p.$eval('#status', e => e.textContent)) && (await p.$$eval('#assuntos button', x => x.length)) > 5, await p.$eval('#status', e => e.textContent));
 await p.goto('about:blank'); await p.goto(U + '#pos/usar/naoexiste'); await p.waitForTimeout(600);
 ok('N6 ficha inexistente em assunto válido avisa', /não encontrei|nao encontrei/i.test(await p.$eval('#status', e => e.textContent)) && (await p.$$eval('#level-examples button', x => x.length)) > 1);
 // N1 na tela
 await p.goto('about:blank'); await p.goto(U); await p.waitForSelector('#level');
 t = await buscar('usei IA na dissertação');
 ok('N1 sem perfil pede o perfil', /selecione o seu perfil/i.test(t) && !(await p.$('#legal-results .examples button')), t);
 // item 10
 t = await buscar('art. 28');
 await p.goto('about:blank'); await p.goBack(); await p.waitForTimeout(800);
 const v = await p.$eval('#query', e => e.value), r = await p.$eval('#legal-results', e => e.innerText);
 ok('item 10: depois de Voltar, caixa e resultado coerentes', (v === '' && r.trim() === '') || (v !== '' && /Art\. 28/.test(r)), JSON.stringify([v, r.slice(0, 40)]));
 console.log('erros:', errs); await b.close();
})();
