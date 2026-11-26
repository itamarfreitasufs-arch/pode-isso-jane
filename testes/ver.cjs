// uso: node ver.cjs <dist> <perfil> "pergunta" ... — mostra conceitos presentes e a pontuação das fichas
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const [dist,perfil,...qs]=process.argv.slice(2);const d=path.resolve(dist);
const initSqlJs=()=>require(path.join(d,'sql-wasm.js'))({locateFile:f=>path.join(d,f)});
const fetch=async p=>({ok:true,arrayBuffer:async()=>fs.readFileSync(path.join(d,p))});
const code=['motor','triagem'].map(n=>fs.readFileSync(path.join(d,n+'.js'),'utf8')).join('\n');
vm.runInNewContext(code+`
(async()=>{const base=await carregarBase();
 for(const q of qs){const t=expandir(normalizar(q).replace(/\\s+/g,' ').trim());
  const r=triar(q,perfil,base);
  console.log('\\n'+q+'\\n  tipo '+r.tipo+' | '+[...conceitosPresentes(t,base)].join(' '));
  console.log('  '+melhores(t,[perfil],base).slice(0,6).map(x=>x.s.id+':'+x.pontos).join('  '));}
})()`,{console,process,initSqlJs,fetch,URL,qs,perfil});
