import {assess,InputError,MODEL} from './assessment.mjs';
import {html} from './page.mjs';
const windows=new Map();
let busy=0;
function json(status,data){return new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}})}
export default {async fetch(request,env){
  try{
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/pulse/api/config')return json(200,{configured:!!env.GROQ_API_KEY,model:MODEL});
    if(request.method==='POST'&&url.pathname==='/pulse/api/assess'){
      if(request.headers.get('Origin')!==url.origin)return json(403,{error:'Send your assessment from the Pulse page.'});
      if(!request.headers.get('Content-Type')?.startsWith('application/json'))return json(415,{error:'Use the assessment form.'});
      const reader=request.body?.getReader();if(!reader)return json(400,{error:'The assessment is empty.'});
      let bytes=0;const chunks=[];for(;;){const {value,done}=await reader.read();if(done)break;bytes+=value.byteLength;if(bytes>40000){await reader.cancel();return json(413,{error:'Your check-in is too long. Please shorten it.'})}chunks.push(value)}
      const buffer=new Uint8Array(bytes);let offset=0;for(const part of chunks){buffer.set(part,offset);offset+=part.byteLength}
      let input;try{input=JSON.parse(new TextDecoder().decode(buffer))}catch{return json(400,{error:'The assessment could not be read.'})}
      const now=Date.now(),id=request.headers.get('CF-Connecting-IP')||'private-owner';
      for(const [key,value]of windows)if(value.start<now-60000)windows.delete(key);
      const state=windows.get(id)||{start:now,count:0};
      if(busy>=4||state.count>=10||windows.size>=2000)return json(429,{error:'Please wait a minute before trying another assessment.'});
      state.count++;windows.set(id,state);busy++;
      try{const result=await assess(input,{apiKey:env.GROQ_API_KEY});return json(result.status,result.body)}finally{busy--}
    }
    if(request.method==='GET'&&['/pulse/','/pulse'].includes(url.pathname))return new Response(html,{headers:{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin'}});
    if(['GET','HEAD'].includes(request.method)&&!url.pathname.startsWith('/pulse/api/'))return env.ASSETS.fetch(request);
    return json(404,{error:'Not found.'});
  }catch(e){return json(e instanceof InputError?400:500,{error:e instanceof InputError?e.message:'The server could not complete this request.'})}
}};
