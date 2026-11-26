// uso: node top3.cjs <dist> <perguntas.json>... — mede se o artigo esperado pelo redator aparece na 1ª candidata e nas 3.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const [dist,...arqs]=process.argv.slice(2);const d=path.resolve(dist);
const ctx={initSqlJs:()=>require(path.join(d,'sql-wasm.js'))({locateFile:f=>path.join(d,f)}),fetch:async p=>({ok:true,arrayBuffer:async()=>fs.readFileSync(path.join(d,p))}),console,arqs,fs,JSON};
vm.runInNewContext(['motor','triagem'].map(n=>fs.readFileSync(path.join(d,n+'.js'),'utf8')).join('\n')+`;(async()=>{const base=await carregarBase();
for(const a of arqs){const qs=JSON.parse(fs.readFileSync(a,'utf8')).filter(q=>['FICHA','LIVRE'].includes(q.classe));let n=0,t1=0,t3=0,lista=0,nada=0,k=0;
 for(const q of qs){const esp=new Set([...(q.dispositivo||'').matchAll(/art\\.? ?(\\d+)/gi)].map(m=>+m[1]));if(!esp.size)continue;n++;
  const r=triar(q.q.slice(0,600),q.perfil,base);const c=r.candidatas||[];if(c.length)lista++;else nada++;k+=c.length;
  const tem=f=>f.situacao.dispositivos.some(x=>esp.has(x.artigo));
  if(c[0]&&tem(c[0]))t1++;if(c.some(tem))t3++;}
 console.log(a.split('/').slice(-2,-1)[0],'| perguntas com artigo esperado',n,'| 1ª candidata tem o artigo',t1,'('+Math.round(100*t1/n)+'%) | alguma das 3 tem',t3,'('+Math.round(100*t3/n)+'%) | mostrou lista',lista,'| sem lista',nada,'| média de opções',(k/Math.max(lista,1)).toFixed(1));}
})()`,ctx);
