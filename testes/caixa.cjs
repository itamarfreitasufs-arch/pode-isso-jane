// uso: node caixa.cjs <pasta dist> <perguntas.json> <saida.json>
// Caixa "Consultar a norma": chama consultarCaixa (v5.8); nas versões anteriores, reproduz o que a tela fazia (só buscarNorma).
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const [dist,input,out]=process.argv.slice(2).map(p=>path.resolve(p));
const perguntas=JSON.parse(fs.readFileSync(input,'utf8'));
const initSqlJs=()=>require(path.join(dist,'sql-wasm.js'))({locateFile:f=>path.join(dist,f)});
const fetch=async p=>({ok:true,arrayBuffer:async()=>fs.readFileSync(path.join(dist,p.split('?')[0]))});
const code=['motor','triagem'].map(n=>fs.readFileSync(path.join(dist,n+'.js'),'utf8')).join('\n');
vm.runInNewContext(code+`
(async()=>{
 const nome=u=>u.secao==='Anexo I'?'Glossário (Anexo I) · '+u.localizador.replace(/^Item /,'verbete '):u.secao==='Anexo II'?'Guia de Risco (Anexo II) · '+u.localizador:u.secao+' · '+u.localizador;
 const res=[];
 for(const {id,perfil,q} of perguntas){
  let erro=null,partes=[],apoio=false;
  try{
   if(typeof consultarCaixa==='function'){
    const r=await consultarCaixa(q,perfil);apoio=!!r.apoio;
    partes=[...r.avisos.map(a=>a.mensagem),r.status,...(r.candidatas||[]).map(c=>'FICHA: '+c.situacao.pergunta+' ;'),...(r.linhas||[]).map(u=>'LINHA: '+nome(u)+' ;')];
   }else{
    const linhas=await buscarNorma(q.trim());
    partes=linhas.length?linhas.map(u=>'LINHA: '+nome(u)+' ;'):['Sem correspondência. Busque um termo mais curto ou o número do artigo.'];
   }
  }catch(e){erro=String(e.stack||e)}
  res.push({id,perfil,q,status:partes.filter(Boolean).join('\\n'),fichas:[],erro,apoio});
 }
 __fs.writeFileSync(__out,JSON.stringify(res,null,1));
})().catch(e=>{console.error(e);process.exitCode=1});
`,{URL,perguntas,console,process,initSqlJs,fetch,__fs:fs,__out:out});
