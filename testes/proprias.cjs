// Coerência interna: a pergunta-exemplo de cada situação, enviada em cada perfil dela, deve trazer a própria situação
// (ou outra do mesmo núcleo) como primeira ficha. Uso: node proprias.cjs <dist>
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const dist=path.resolve(process.argv[2]);
const initSqlJs=()=>require(path.join(dist,'sql-wasm.js'))({locateFile:f=>path.join(dist,f)});
const fetch=async p=>({ok:true,arrayBuffer:async()=>fs.readFileSync(path.join(dist,p.split('?')[0]))});
const code=['motor','triagem'].map(n=>fs.readFileSync(path.join(dist,n+'.js'),'utf8')).join('\n');
vm.runInNewContext(code+`
(async()=>{const base=await carregarBase();let ok=0,total=0;const falhas=[];
 for(const s of base.situacoes) for(const p of s.perfis){total++;
  const r=triar(s.pergunta,p,base);const f=r.fichas[0];
  if(f&&(f.situacao.id===s.id||f.situacao.nucleo===s.nucleo)) ok++; else falhas.push(s.id+'@'+p+' → '+(f?f.situacao.id:r.tipo));}
 console.log('exemplos próprios: '+ok+'/'+total);falhas.forEach(f=>console.log('  '+f));
 if(falhas.length) process.exitCode=1;
})()`,{console,process,initSqlJs,fetch,URL});
