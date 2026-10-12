const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const storage=new Map();
function setup(){
  const elements=new Map();
  const element=()=>({innerHTML:'',textContent:'',open:false,onclick:null,handlers:{},classList:{add(){},remove(){},toggle(){}},addEventListener(n,fn){this.handlers[n]=fn;},showModal(){this.open=true;},close(){this.open=false;},scrollIntoView(){}});
  for(const id of ['#app','#dialog','#dialog-content','#toast','#timer','#timer-value','.brand','#cancel-dialog','#accept-dialog','.question-card'])elements.set(id,element());
  const context=vm.createContext({console,Date,Math,JSON,Number,String,Array,Object,Error,Promise,
    document:{querySelector:s=>elements.get(s)||null,querySelectorAll:()=>[],addEventListener(){},hidden:false},
    localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
    window:{scrollTo(){},addEventListener(){},print(){}},
    setInterval(){},setTimeout(){},fetch:async file=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8'))})});
  vm.runInContext(fs.readFileSync(path.join(root,'app.js'),'utf8'),context);
  return {context,elements,run:s=>vm.runInContext(s,context),click(action,extra={}){elements.get('#app').handlers.click({target:{closest:()=>({dataset:{action,...extra},disabled:false})}});}};
}
async function main(){
  let env=setup();await new Promise(r=>setImmediate(r));
  assert.equal(env.run('manifest.length'),60);assert.match(env.elements.get('#app').innerHTML,/1200/);
  await env.run('start(1)');assert.equal(env.run('remaining()'),3600);
  assert(!env.elements.get('#app').innerHTML.includes('Cum rezolvăm'));
  env.click('answer',{index:'2'});assert.equal(env.run('state.answers[0]'),2);
  env.click('flag');assert.equal(env.run('state.flags[0]'),true);
  env.click('clear');assert.equal(env.run('state.answers[0]'),null);
  env.click('goto',{index:'19'});env.click('next');assert.equal(env.run('view'),'review');
  assert(!env.elements.get('#app').innerHTML.includes('Răspuns corect'));
  env.click('finish');assert.equal(env.elements.get('#dialog').open,true);
  env.elements.get('#cancel-dialog').onclick();assert.equal(env.run('state.finished'),false);
  env.run('state.answers=test.questions.map(q=>q.correct);save();');
  env.click('finish');env.elements.get('#accept-dialog').onclick();
  assert.equal(env.run('state.finished'),true);assert.equal(env.run('state.score'),20);
  assert.match(env.elements.get('#app').innerHTML,/10,0/);assert.match(env.elements.get('#app').innerHTML,/Cum rezolvăm/);
  const snapshot=env.run('JSON.stringify(state.answers)');env.click('answer',{index:'0'});assert.equal(env.run('JSON.stringify(state.answers)'),snapshot);
  env.click('filter',{filter:'wrong'});assert.match(env.elements.get('#app').innerHTML,/Nu există itemi/);
  env=setup();await new Promise(r=>setImmediate(r));await env.run('start(1)');assert.equal(env.run('view'),'results');assert.equal(env.run('state.score'),20);
  await env.run('start(2,true)');env.run('state.answers[0]=test.questions[0].correct;save();');
  const deadline=env.run('state.deadline');env=setup();await new Promise(r=>setImmediate(r));await env.run('start(2)');assert.equal(env.run('state.deadline'),deadline);assert.equal(env.run('answered(state)'),1);
  env.run('state.deadline=Date.now()-1000;updateTimer();');assert.equal(env.run('state.finished'),true);assert.equal(env.run('state.expired'),true);assert.equal(env.run('state.score'),1);
  assert.match(env.elements.get('#app').innerHTML,/0,5/);
  for(let id=1;id<=60;id++){
    await env.run(`start(${id},true)`);
    for(let i=0;i<20;i++){
      env.run(`current=${i};question();`);assert(!env.elements.get('#app').innerHTML.includes('Cum rezolvăm'));if(env.run(`!!test.questions[${i}].figure`))assert.match(env.elements.get('#app').innerHTML,/Matricea de completat/);
    }
    env.run('state.answers=test.questions.map((q,i)=>i<12?q.correct:null);finish();');if(id>=41){assert.match(env.elements.get('#app').innerHTML,/Tabel de adevăr/);}assert.equal(env.run('state.score'),12);assert.match(env.elements.get('#app').innerHTML,/Pragul de promovare este atins/);
  }
  console.log('OK: 60 teste, 1200 întrebări randate; punctaj, navigare, răspunsuri, marcaje, verificare, confirmare, blocare după finalizare, explicații ascunse înainte de finalizare.');
  console.log('OK: cronometru 60 min, expirare automată, progres și termen păstrate la reîncărcare, pragul 6/10, filtrarea rezultatelor.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
