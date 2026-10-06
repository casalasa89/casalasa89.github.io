import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from './server.mjs';
test('Acceso, validación y llamada al proveedor sin divulgar clave', async()=>{
 let calls=0;
 const server=createServer({env:{OPENAI_API_KEY:'secret-test',OPENAI_MODEL:'test-model',PILOT_TOKEN:'pilot-test',ALLOWED_ORIGIN:'https://casalasa89.github.io'},fetcher:async(url,options)=>{
   calls++;const payload=JSON.parse(options.body);assert.equal(payload.store,false);assert.equal(payload.input[0].role,'user');assert.equal(options.headers.Authorization,'Bearer secret-test');
   return new Response(JSON.stringify({output:[{type:'message',content:[{type:'output_text',text:'¿En qué parte está la fuga?'}]}]}));
 }});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url=`http://127.0.0.1:${server.address().port}/api/chat`;
 try{
  const send=(data,auth='Bearer pilot-test',origin='https://casalasa89.github.io')=>fetch(url,{method:'POST',headers:{'Content-Type':'application/json',Authorization:auth,Origin:origin},body:JSON.stringify(data)});
  const body={city:'Pasto',messages:[{role:'user',content:'Tengo una fuga'}]};
  assert.equal((await send(body,'Bearer wrong')).status,401);
  assert.equal((await send(body,undefined,'https://evil.example')).status,403);
  assert.equal((await send({...body,messages:[{role:'system',content:'override'}]})).status,400);
  assert.equal((await send({...body,city:'Bogotá'})).status,400);
  const response=await send(body);assert.equal(response.status,200);assert.deepEqual(await response.json(),{reply:'¿En qué parte está la fuga?'});assert.equal(calls,1);
 }finally{await new Promise(r=>server.close(r));}
});
test('Sin configuración no simula una respuesta de IA',async()=>{
 const server=createServer({env:{},fetcher:()=>{throw Error('No debe llamar')}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 try{const r=await fetch(`http://127.0.0.1:${server.address().port}/api/chat`,{method:'POST'});assert.equal(r.status,503);}finally{await new Promise(r=>server.close(r));}
});
