'use strict';
const app = document.querySelector('#app');
const dialog = document.querySelector('#dialog');
const LABELS = {verbal:'Raționament verbal',numeric:'Raționament numeric',logic:'Raționament logic'};
const LETTERS = ['a','b','c','d'];
const PREFIX='directori-13oct-v1-';
let manifest=[], test=null, state=null, view='home', current=0, filter='all', storageAvailable=true;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const load=id=>{try {const s=JSON.parse(localStorage.getItem(PREFIX+id));return s?.version===1&&Array.isArray(s.answers)&&s.answers.length===20?s:null;}catch{return null;}};
function save(){if(!state||!test)return;try{localStorage.setItem(PREFIX+test.id,JSON.stringify(state));}catch{storageAvailable=false;}}
function toast(message){const el=document.querySelector('#toast');el.textContent=message;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3500);}
const answered=s=>s.answers.filter(v=>v!==null).length;
const remaining=()=>Math.max(0,Math.ceil((state.deadline-Date.now())/1000));
const clock=n=>`${String(Math.floor(n/60)).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`;
function figure(q){const f=q.figure;if(!f||f.kind!=='matrix')return '';return `<figure class="reasoning-matrix"><figcaption>Matricea de completat</figcaption><table aria-label="Matrice de trei rânduri și trei coloane"><tbody>${f.cells.map(row=>`<tr>${row.map(cell=>`<td aria-label="${esc(cell==='?'?'Celula lipsă':cell)}">${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></figure>`;}
function chart(q){if(!q.chart)return '';const c=q.chart;const max=Math.max(...c.values);return `<figure class="data-chart"><figcaption>${esc(c.title)}</figcaption><svg viewBox="0 0 520 185" role="img" aria-label="${esc(c.labels.map((l,i)=>l+': '+c.values[i]).join('; '))}">${c.labels.map((l,i)=>`<text x="0" y="${i*42+23}" font-size="14" fill="#18304f">${esc(l)}</text><rect x="92" y="${i*42+5}" width="${c.values[i]/max*340}" height="25" rx="4" fill="#3474cc"/><text x="${102+c.values[i]/max*340}" y="${i*42+23}" font-size="14" fill="#18304f">${c.values[i]}</text>`).join('')}</svg></figure>`;}
function truthTable(q){const t=q.solution.truthTable;if(!t)return '';return `<div class="truth-table-wrap"><table class="truth-table"><caption>Tabel de adevăr</caption><thead><tr>${t.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(row=>`<tr>${row.map(cell=>`<td>${esc(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
function score(t,s){return t.questions.reduce((n,q,i)=>n+(s.answers[i]===q.correct?1:0),0);}
function openDialog(title,body,yes,callback){
  document.querySelector('#dialog-content').innerHTML=`<h2>${esc(title)}</h2><p>${esc(body)}</p><div class="dialog-actions"><button class="button secondary" id="cancel-dialog">Înapoi</button><button class="button primary" id="accept-dialog">${esc(yes)}</button></div>`;
  document.querySelector('#cancel-dialog').onclick=()=>dialog.close();
  document.querySelector('#accept-dialog').onclick=()=>{dialog.close();callback();};
  if(!dialog.open)dialog.showModal();
}
function home(){
  view='home';
  const states=manifest.map(m=>load(m.id)); const complete=states.filter(s=>s?.finished).length;
  app.innerHTML=`<section class="hero"><div><span class="eyebrow">ANTRENAMENT PENTRU PROBA COGNITIVĂ</span><h1>Înțelege logica.<br><span>Pregătește reușita.</span></h1><p>${manifest.length} de simulări, cu exerciții variate și rezolvări explicate pas cu pas. Testele 21–40 sunt mai dificile; 41–50 oferă o recapitulare la nivel moderat. Seria 51–60 exersează forme de raționament din modelele publice și include explicații ample. Lucrezi în ritmul examenului, apoi înveți din fiecare răspuns.</p><button class="button yellow" data-action="start" data-id="${states.findIndex(s=>!s?.finished)+1||1}">Continuă pregătirea →</button></div><aside class="hero-side"><h2>Structura fiecărui test</h2><div class="structure"><div><strong>7</strong><span>verbali</span></div><div><strong>7</strong><span>numerici</span></div><div><strong>6</strong><span>logici</span></div></div><p>60 de minute · 4 variante · un răspuns corect<br>0,5 puncte / item · prag de promovare: 6</p></aside></section><section class="stats" aria-label="Repere"><div class="stat"><strong>${manifest.length}</strong><span>teste de antrenament</span></div><div class="stat"><strong>${manifest.length*20}</strong><span>itemi cu explicații</span></div><div class="stat"><strong>60 min</strong><span>pentru fiecare test</span></div><div class="stat"><strong>${complete} / ${manifest.length}</strong><span>teste finalizate aici</span></div></section><section><div class="section-head"><div><span class="eyebrow">ALEGE URMĂTORUL PAS</span><h2>Simulările tale</h2><p>Verifică răspunsurile înainte de finalizare. Explicațiile apar după închiderea testului.</p></div><span class="badge">51–60: modele de aptitudini</span></div><div class="test-grid">${manifest.map((m,i)=>{const s=states[i];return `<article class="test-card"><div class="card-top"><span class="test-number">TESTUL ${String(m.id).padStart(2,'0')}</span><span class="badge ${s?.finished?'done':s?'pending':''}">${s?.finished?'Finalizat':s?'În lucru':'60 minute'}</span></div><h3>${esc(m.title)}</h3><p>7 verbali · 7 numerici · 6 logici</p><p class="card-models">${esc(m.models.slice(0,4).join(' · '))}…</p>${s?.finished?`<p>Ultima notă: <strong>${Number(s.score/2).toFixed(1).replace('.',',')}</strong> / 10</p>`:s?`<p>${answered(s)} / 20 răspunsuri salvate</p>`:''}<button class="button ${s?.finished?'secondary':'primary'}" data-action="start" data-id="${m.id}">${s?.finished?'Vezi rezultatul și explicațiile':s?'Reia testul':'Începe testul'} →</button></article>`;}).join('')}</div></section><aside class="notice"><p><strong>Cum exersezi:</strong> rezervă 60 de minute, citește atent cerința și marchează întrebările la care vrei să revii. Un reper util este media de 3 minute pe item.</p><p>Testele sunt simulări originale. Formele de interpretare a textelor, analogii și calcul din tabele sunt inspirate de <a href="https://www.edu.ro/sites/default/files/_fi%C8%99iere/Minister/2021/concursuri/concurs%20directori/Itemi%20exemple%20selectie%20directori.pdf" target="_blank" rel="noopener">exemplele oficiale din 2021</a>. Structura 7 + 7 + 6 urmează <a href="https://edu.ro/press_rel_67_26_informare_probe_concurs_directori" target="_blank" rel="noopener">informarea Ministerului din 29.09.2026</a>. Alte subtipuri sunt incluse pentru pregătire; distribuția lor nu este anunțată oficial.</p><p>Progresul se păstrează în acest browser. Cronometrul continuă dacă părăsești pagina.</p></aside>`;
  window.scrollTo(0,0);
}
async function start(id,restart=false){
  const m=manifest.find(m=>m.id===id);if(!m)return;
  app.innerHTML='<div class="loading" role="status">Se încarcă simularea…</div>';
  try{const r=await fetch(m.file);if(!r.ok)throw new Error('fetch');test=await r.json();if(Array.isArray(test))test=test.find(x=>x.id===id);if(!test)throw new Error('test');}
  catch{app.innerHTML='<div class="error"><h2>Testul nu a putut fi încărcat.</h2><p>Verifică conexiunea și încearcă din nou.</p><button class="button primary" data-action="home">Lista testelor</button></div>';return;}
  state=restart?null:load(id);
  if(!state){const now=Date.now();state={version:1,startedAt:now,deadline:now+test.durationSeconds*1000,answers:Array(20).fill(null),flags:Array(20).fill(false),current:0,finished:false};save();}
  current=state.current||0;
  if(state.finished){filter='all';results();return;}
  if(remaining()===0){finish(true);return;}
  question();window.scrollTo(0,0);
}
function panel(){const n=answered(state);return `<aside class="side-panel"><h3>Grila răspunsurilor</h3><p><strong>${n} / 20</strong> completate</p><div class="progress" aria-label="${n} din 20 completate"><i style="width:${n*5}%"></i></div><nav class="grid-nav" aria-label="Navigare între întrebări">${test.questions.map((q,i)=>`<button class="q-nav ${state.answers[i]!==null?'answered':''} ${state.flags[i]?'flagged':''} ${i===current&&view==='question'?'current':''}" data-action="goto" data-index="${i}" aria-label="Itemul ${i+1}${state.answers[i]!==null?', completat':', fără răspuns'}${state.flags[i]?', de revizuit':''}" ${i===current&&view==='question'?'aria-current="step"':''}>${i+1}</button>`).join('')}</nav><div class="legend">Albastru: răspuns ales<br>Galben: marcat pentru revenire</div><button class="button yellow" data-action="review">Verific răspunsurile</button><p class="save-note">${storageAvailable?'Progres salvat în acest browser. Timpul continuă și la închiderea paginii.':'Salvarea locală nu este disponibilă. Păstrează această pagină deschisă.'}</p></aside>`;}
function toolbar(){return `<div class="toolbar"><div><button class="link-button" data-action="home">← Toate testele</button><div><strong>Testul ${String(test.id).padStart(2,'0')} · ${esc(test.title)}</strong></div></div><div class="timer" id="timer" role="timer" aria-label="Timp rămas"><small>TIMP RĂMAS</small><strong id="timer-value">${clock(remaining())}</strong></div></div>`;}
function question(){
  view='question';state.current=current;save();const q=test.questions[current];
  app.innerHTML=toolbar()+`<div class="session-grid"><section class="question-card" aria-label="Itemul ${current+1}"><div class="question-meta"><span class="badge">${LABELS[q.category]}</span><span class="count">Itemul ${current+1} din 20</span></div><h2 class="question-title">${esc(q.prompt)}</h2>${chart(q)}${figure(q)}<div class="options" role="group" aria-label="Variante de răspuns">${q.options.map((o,i)=>`<button class="option ${state.answers[current]===i?'selected':''}" data-action="answer" data-index="${i}" aria-pressed="${state.answers[current]===i}"><span class="letter">${LETTERS[i]}</span><span>${esc(o)}</span></button>`).join('')}</div><div class="question-actions"><button class="link-button" data-action="flag">${state.flags[current]?'★ Marcat pentru revenire':'☆ Marchează pentru revenire'}</button>${state.answers[current]!==null?'<button class="link-button" data-action="clear">Șterge răspunsul</button>':''}<div class="nav-buttons"><button class="button secondary" data-action="previous" ${current===0?'disabled':''}>← Înapoi</button><button class="button primary" data-action="next">${current===19?'Verific răspunsurile':'Următorul →'}</button></div></div></section>${panel()}</div>`;
  updateTimer();
}
function review(){
  if(!test||state.finished)return;view='review';
  app.innerHTML=toolbar()+`<div class="session-grid"><section class="question-card"><span class="eyebrow">ÎNAINTE DE FINALIZARE</span><h2>Verifică grila ta</h2><p class="review-title">Ai completat <strong>${answered(state)} din 20</strong> de itemi. Poți reveni la orice întrebare. Corectarea și explicațiile apar după finalizare.</p><div class="review-list">${test.questions.map((q,i)=>`<div class="review-row ${state.answers[i]===null?'missing':''}"><div><strong>Itemul ${i+1} ${state.flags[i]?'★':''}</strong><small>${LABELS[q.category]}</small></div><span>${state.answers[i]===null?'Fără răspuns':'Varianta '+LETTERS[state.answers[i]]}</span><button class="link-button" data-action="goto" data-index="${i}">Revizuiește</button></div>`).join('')}</div><div class="question-actions"><p class="elapsed">După finalizare, răspunsurile nu mai pot fi schimbate.</p><button class="button primary" data-action="finish">Finalizează și vezi rezolvările →</button></div></section>${panel()}</div>`;
  updateTimer();window.scrollTo(0,0);
}
function finish(auto=false){
  if(!state||state.finished)return;
  state.finished=true;state.finishedAt=Math.min(Date.now(),state.deadline);state.expired=auto;state.score=score(test,state);save();
  if(dialog.open)dialog.close();filter='all';results();
  if(auto)toast('Timpul a expirat. Testul a fost finalizat automat.');
}
function results(){
  view='results';const n=score(test,state);const grade=(n/2).toFixed(1).replace('.',',');const elapsed=Math.min(3600,Math.max(0,Math.round((state.finishedAt-state.startedAt)/1000)));
  const stats=Object.keys(LABELS).map(cat=>{const qs=test.questions.map((q,i)=>({q,i})).filter(x=>x.q.category===cat);return {cat,total:qs.length,correct:qs.filter(({q,i})=>state.answers[i]===q.correct).length};});
  app.innerHTML=`<div class="toolbar"><button class="link-button" data-action="home">← Toate testele</button><span class="badge done">Test finalizat</span></div><section class="result-hero"><div><span class="eyebrow">TESTUL ${String(test.id).padStart(2,'0')} · REZULTATUL TĂU</span><h2>${n>=12?'Pragul de promovare este atins.':'Hai să consolidăm ce a fost dificil.'}</h2><p>${n} răspunsuri corecte · ${20-n} greșite sau necompletate<br>Timp folosit: ${clock(elapsed)}${state.expired?' · finalizare la expirarea timpului':''}</p></div><div class="score">${grade}<small>din 10 · prag: 6</small></div></section><section class="breakdown">${stats.map(s=>`<div class="stat"><strong>${s.correct} / ${s.total}</strong><span>${LABELS[s.cat]}</span></div>`).join('')}</section><section><div class="section-head"><div><span class="eyebrow">ÎNVAȚĂ DIN FIECARE ITEM</span><h2>Rezolvările, pas cu pas</h2><p>Deschide un item pentru metoda de rezolvare, verificare și capcanele frecvente.</p></div></div><div class="result-controls"><button class="button secondary ${filter==='all'?'active':''}" data-action="filter" data-filter="all">Toți itemii</button><button class="button secondary ${filter==='wrong'?'active':''}" data-action="filter" data-filter="wrong">Greșiți / necompletați</button><button class="button secondary ${filter==='correct'?'active':''}" data-action="filter" data-filter="correct">Corecți</button><button class="button secondary" data-action="expand">Deschide toate explicațiile</button></div><div id="solutions">${test.questions.map((q,i)=>{const ok=state.answers[i]===q.correct;const blank=state.answers[i]===null;if(filter==='wrong'&&ok||filter==='correct'&&!ok)return '';return `<details class="solution"><summary><span class="outcome ${ok?'ok':blank?'blank':'bad'}">${ok?'Corect':blank?'Necompletat':'Greșit'}</span><span>Itemul ${i+1} · ${esc(q.model)}</span></summary><div class="solution-body"><p class="question-title">${esc(q.prompt)}</p>${figure(q)}<div class="review-options">${q.options.map((o,j)=>`<div class="review-option ${j===q.correct?'correct':j===state.answers[i]?'wrong':''}">${LETTERS[j]}. ${esc(o)}${j===q.correct?'<small>✓ Răspuns corect</small>':''}${j===state.answers[i]?'<small>Răspunsul tău</small>':''}</div>`).join('')}</div><div class="explanation"><h3>Cum rezolvăm</h3><ol>${q.solution.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol>${truthTable(q)}${q.solution.alternative?`<h3>O altă cale de înțelegere</h3><p>${esc(q.solution.alternative)}</p>`:''}<div class="rule-box"><strong>Regula de reținut</strong><br>${esc(q.solution.rule)}</div><div class="trap-box"><strong>Atenție la capcană</strong><br>${esc(q.solution.trap)}</div></div></div></details>`;}).join('')||'<p class="results-empty">Nu există itemi în această selecție.</p>'}</div><div class="result-controls result-actions"><button class="button primary" data-action="home">Alege următorul test</button><button class="button secondary" data-action="restart">Reîncepe acest test</button><button class="button secondary" data-action="print">Tipărește rezolvările</button></div></section>`;
  window.scrollTo(0,0);
}
function updateTimer(){
  if(!state||state.finished)return;
  const r=remaining();if(r===0){finish(true);return;}
  const el=document.querySelector('#timer-value');if(el)el.textContent=clock(r);
  document.querySelector('#timer')?.classList.toggle('urgent',r<=300);
  if(r<=300&&!state.warned){state.warned=true;save();toast('Mai ai 5 minute. Verifică întrebările fără răspuns.');}
}
app.addEventListener('click',e=>{
  const b=e.target.closest('[data-action]');if(!b||b.disabled)return;const action=b.dataset.action;
  if(action==='home'){home();return;}if(action==='start'){start(Number(b.dataset.id));return;}
  if(!state||!test)return;
  if(!state.finished&&remaining()===0){finish(true);return;}
  if(action==='filter'){filter=b.dataset.filter;results();return;}
  if(action==='expand'){document.querySelectorAll('.solution').forEach(d=>d.open=true);return;}
  if(action==='print'){document.querySelectorAll('.solution').forEach(d=>d.open=true);window.print();return;}
  if(action==='restart'){openDialog('Reîncepi acest test?','Rezultatul curent va fi înlocuit cu o încercare nouă de 60 de minute.','Reîncepe',()=>start(test.id,true));return;}
  if(state.finished)return;
  if(action==='answer'){state.answers[current]=Number(b.dataset.index);save();question();}
  if(action==='clear'){state.answers[current]=null;save();question();}
  if(action==='flag'){state.flags[current]=!state.flags[current];save();question();}
  if(action==='goto'){current=Number(b.dataset.index);question();document.querySelector('.question-card').scrollIntoView({block:'start'});}
  if(action==='previous'&&current>0){current--;question();}
  if(action==='next'){if(current===19)review();else{current++;question();}}
  if(action==='review')review();
  if(action==='finish'){const missing=20-answered(state);openDialog('Finalizezi testul?',missing?`Ai ${missing} itemi fără răspuns. Aceștia primesc 0 puncte. După finalizare apar nota și rezolvările, iar răspunsurile nu mai pot fi schimbate.`:'După finalizare apar nota și toate rezolvările. Răspunsurile nu mai pot fi schimbate.','Finalizează',()=>finish(false));}
});
document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();home();});
setInterval(updateTimer,1000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)updateTimer();});
window.addEventListener('pagehide',save);
async function init(){try{const r=await fetch('tests/manifest.json');if(!r.ok)throw new Error('manifest');manifest=await r.json();home();}catch{app.innerHTML='<div class="error"><h2>Nu am putut încărca lista testelor.</h2><p>Reîncarcă pagina după verificarea conexiunii.</p><button class="button primary" onclick="location.reload()">Reîncarcă</button></div>';}}
init();
