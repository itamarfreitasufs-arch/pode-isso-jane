// uso: node rodar.cjs <pasta dist> <perguntas.json> <saida.json>
// Executa o envio real (app.js) com uma página simulada e o SQLite verdadeiro.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const [dist,input,out]=process.argv.slice(2).map(p=>path.resolve(p));
const perguntas=JSON.parse(fs.readFileSync(input,'utf8'));
function el(){return {value:'',textContent:'',hidden:false,open:false,children:[],dataset:{},append(...x){this.children.push(...x)},replaceChildren(...x){this.children=x},focus(){},setAttribute(){},addEventListener(){},querySelectorAll(){return[]}}}
const nodes={};const document={body:{dataset:{}},createElement:el,querySelector:k=>nodes[k]??=el(),querySelectorAll:()=>[]};
const initSqlJs=()=>require(path.join(dist,'sql-wasm.js'))({locateFile:f=>path.join(dist,f)});
const fetch=async p=>({ok:true,arrayBuffer:async()=>fs.readFileSync(path.join(dist,p.split('?')[0]))});
const code=['motor','triagem','app'].map(n=>fs.readFileSync(path.join(dist,n+'.js'),'utf8')).join('\n');
vm.runInNewContext(code+`
(async()=>{
 const texto=x=>[x.textContent,...x.children.map(texto)].filter(Boolean).join(' | ');
 const base=await carregarBase();const res=[];
 for(const {id,perfil,q} of perguntas){
  let erro=null,t=null;
  try{ nivelSelecionado.value=perfil; await atualizarNivel();
   document.querySelector('#message').value=q;
   await document.querySelector('#question').onsubmit({preventDefault(){}});
   t=triar(q,perfil,base);
   // A tela agora pede confirmação ("Você quis dizer"); o teste do motor abre direto as fichas escolhidas.
   if(t.fichas.length) t.fichas.forEach((f,i)=>mostrarFicha(base,f,i>0));
  }catch(e){erro=String(e.stack||e)}
  res.push({id,perfil,q,tipo:t&&t.tipo,ids:t?t.fichas.map(f=>f.situacao.id):[],status:[cuidado.children.map(texto).join(' '),status.textContent].filter(Boolean).join(' '),fichas:resultArea.children.map(texto),erro});
 }
 __fs.writeFileSync(__out,JSON.stringify(res,null,1));
})().catch(e=>{console.error(e);process.exitCode=1});
`,{URL,document,nodes,perguntas,console,process,initSqlJs,fetch,__fs:fs,__out:out});
