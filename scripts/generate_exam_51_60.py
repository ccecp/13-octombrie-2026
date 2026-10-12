"""200 exerciții originale după forme publice 2016/2021/2022 și descrieri de aptitudini."""
import json,subprocess,itertools
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
def item(cat,model,prompt,answer,wrong,steps,rule,trap,alternative='',proof=None,table=None):
    assert len(set([answer]+wrong))==4
    q=dict(category=cat,model=model,prompt=prompt,options=[answer]+wrong,correct=0,
        solution=dict(steps=steps,rule=rule,trap=trap,alternative=alternative),hint='',proof=proof,historical=False)
    if table:q['solution']['truthTable']=table
    return q
def fmt(x):
    x=F(x)
    if x.denominator==1:return str(x.numerator)
    if 1000%x.denominator==0:return ('%.3f'%float(x)).rstrip('0').rstrip('.').replace('.',',')
    return str(x)

# Texte originale: A=afirmat de text, F=contrazis, N=nedeterminabil.
TEXTS=[
('Arhiva digitală','Arhiva digitală permite căutarea documentelor după titlu sau dată. În etapa pilot au fost incluse numai documentele din ultimii doi ani. Originalele pe hârtie sunt păstrate. Raportul arată reducerea timpului de căutare, dar nu precizează economiile financiare.',
 ['Se poate căuta după dată.','Originalele pe hârtie au fost distruse.','Proiectul a redus cheltuielile cu 30%.'],['A','F','N'],
 'Arhiva facilitează căutarea, păstrând originalele și având deocamdată o acoperire limitată',
 ['Arhiva cuprinde toate documentele din istoria instituției','Arhiva a eliminat obligatoriu orice document pe hârtie','Raportul demonstrează economii financiare precise'],
 ('Ce limită a proiectului este precizată?', 'Sunt incluse numai documentele din ultimii doi ani',['Căutarea după dată este imposibilă','Originalele nu mai există','Toți utilizatorii trebuie să plătească'], 'Limita privește perioada documentelor incluse, nu funcția de căutare sau păstrarea originalelor.')),
('Transportul școlar','Un traseu nou reduce distanța parcursă de o parte dintre elevi. Pentru ceilalți, distanța rămâne neschimbată. Frecvența curselor este aceeași ca înainte. Nu există în fragment date despre durata călătoriilor sau costurile transportului.',
 ['Toți elevii parcurg acum o distanță mai mică.','Frecvența curselor s-a păstrat.','Durata fiecărei călătorii a scăzut.'],['F','A','N'],
 'Traseul schimbă distanța pentru unii elevi, fără să modifice frecvența curselor',
 ['Noul traseu reduce timpul de călătorie pentru fiecare elev','Toate cursele au fost suspendate','Transportul este acum gratuit pentru toate persoanele'],
 ('Ce concluzie este susținută?', 'Cel puțin o parte dintre elevi parcurg o distanță mai mică',['Fiecare elev ajunge mai repede','Frecvența curselor s-a dublat','Prețul călătoriei a scăzut'], 'Reducerea distanței este confirmată pentru o parte dintre elevi; durata și prețul nu sunt precizate.')),
('Observarea vremii','Elevii înregistrează temperatura la aceeași oră în fiecare zi de școală. În vacanță nu se fac înregistrări. Datele sunt comparate la sfârșitul fiecărei luni. Fragmentul nu indică temperatura maximă observată.',
 ['Temperatura maximă observată a fost 35 de grade.','În vacanță nu se fac înregistrări.','Datele sunt comparate numai o dată pe an.'],['N','A','F'],
 'Elevii urmăresc temperatura în zilele de școală și compară datele lunar',
 ['Elevii fac înregistrări fără pauză în toate zilele anului','Textul oferă temperatura maximă și minimă','Toate comparațiile au loc zilnic'],
 ('De ce nu putem calcula media anuală din fragment?', 'Nu sunt oferite valorile temperaturilor',['Ora măsurării este aceeași','Elevii nu pot calcula o medie','Temperatura este întotdeauna constantă'], 'Pentru medie avem nevoie de valori și de numărul lor; descrierea procedurii nu oferă temperaturile.')),
('Înscrierea online','Formularul online poate fi completat de pe telefon sau calculator. După trimitere, solicitantul primește un mesaj de confirmare. Confirmarea arată primirea cererii, nu aprobarea ei. Decizia este comunicată ulterior. Textul nu precizează termenul deciziei.',
 ['Mesajul confirmă primirea cererii.','Decizia este comunicată în exact două zile.','Confirmarea înseamnă aprobarea cererii.'],['A','N','F'],
 'Formularul permite depunerea cererii, iar confirmarea primirii este distinctă de aprobare',
 ['Confirmarea aprobă automat fiecare cerere','Formularul poate fi folosit numai de pe calculator','Toate deciziile sunt comunicate înaintea depunerii'],
 ('Ce distincție trebuie păstrată?', 'Primirea cererii este diferită de aprobarea cererii',['Confirmarea este identică aprobării','Telefonul nu permite completarea','Termenul deciziei este cunoscut'], 'Textul separă explicit confirmarea depunerii de decizia ulterioară.')),
('Atelierul de teatru','Atelierul de teatru pune accent pe exprimare și cooperare. Participanții pot schimba rolurile între repetiții. Spectacolul final nu este obligatoriu pentru fiecare participant. Fragmentul nu conține rezultatele unui test de încredere în sine.',
 ['Fiecare participant este obligat să joace în spectacol.','Atelierul a dublat încrederea în sine a tuturor.','Rolurile se pot schimba între repetiții.'],['F','N','A'],
 'Atelierul exersează exprimarea și cooperarea, cu roluri flexibile și spectacol opțional',
 ['Spectacolul este obligatoriu pentru toate persoanele','Rolurile rămân obligatoriu identice la toate repetițiile','Fragmentul demonstrează creșteri măsurate ale încrederii în sine'],
 ('Care obiectiv este menționat explicit?', 'Exersarea exprimării și cooperării',['Clasificarea elevilor după inteligență','Eliminarea tuturor emoțiilor','Obținerea obligatorie a unui premiu'], 'Prima propoziție indică exprimarea și cooperarea, fără să promită premii sau dispariția emoțiilor.')),
('Buletinul informativ','Buletinul informativ este trimis săptămânal abonaților. Unele ediții includ anunțuri despre evenimente, iar altele prezintă resurse de studiu. Abonarea este voluntară. Nu este menționat câți abonați citesc efectiv fiecare ediție.',
 ['Toți abonații citesc fiecare ediție.','Abonarea este obligatorie.','Buletinul este trimis săptămânal.'],['N','F','A'],
 'Buletinul oferă săptămânal informații variate persoanelor abonate voluntar',
 ['Fiecare ediție este citită obligatoriu de toți destinatarii','Buletinul conține exclusiv anunțuri despre evenimente','Abonarea este impusă tuturor elevilor'],
 ('Care inferență trebuie evitată?', 'Trimiterea unei ediții dovedește că destinatarul a citit-o',['Abonarea este voluntară','Unele ediții prezintă resurse de studiu','Buletinul are o frecvență săptămânală'], 'Expedierea și lectura sunt fapte distincte. Textul confirmă expedierea, nu lectura fiecărui destinatar.')),
('Utilizarea energiei','În trei săli au fost instalate senzori care sting lumina când încăperea este goală. Consumul acestor săli a scăzut în luna următoare. În același timp, programul de folosire a sălilor a fost redus. Raportul nu separă efectele celor două schimbări.',
 ['Senzorii sting lumina când sala este goală.','Programul de folosire a rămas neschimbat.','Întreaga reducere a consumului este produsă exclusiv de senzori.'],['A','F','N'],
 'Consumul a scăzut după două schimbări, ale căror efecte nu sunt separate',
 ['Raportul dovedește că numai senzorii au redus consumul','Consumul a crescut în fiecare sală','Programul sălilor a fost prelungit'],
 ('Ce informație ar ajuta la izolarea efectului senzorilor?', 'Consumul unei săli comparabile cu același program, dar fără senzori',['Culoarea pereților din alte clădiri','Numele persoanei care citește raportul','Numărul ferestrelor unui depozit nefolosit'], 'O comparație cu același program ține constant acest factor și ajută la analizarea efectului senzorilor.')),
('Serviciul de împrumut','Elevii pot împrumuta instrumente de laborator pentru cel mult șapte zile. Prelungirea este posibilă dacă instrumentul nu a fost rezervat de alt elev. Unele instrumente sunt disponibile doar pentru utilizare în laborator. Textul nu arată câte cereri de prelungire au fost aprobate.',
 ['Toate instrumentele pot fi luate acasă.','Prelungirea depinde de existența unei rezervări.','Au fost aprobate zece cereri de prelungire.'],['F','A','N'],
 'Împrumutul are o durată limitată, condiții de prelungire și excepții pentru unele instrumente',
 ['Împrumutul este nelimitat în timp','Orice rezervare a altui elev garantează prelungirea','Toate instrumentele sunt disponibile exclusiv pentru acasă'],
 ('Ce înseamnă „cel mult șapte zile”?', 'Durata nu poate depăși șapte zile fără prelungire',['Durata trebuie să fie exact șapte zile','Durata trebuie să fie mai mare de șapte zile','Durata nu are limită'], 'Cel mult indică limita superioară; sunt posibile și împrumuturi mai scurte.')),
('Harta accesibilității','Voluntarii au verificat intrările a douăzeci de clădiri publice. Au notat existența rampelor, dar nu au evaluat accesibilitatea tuturor spațiilor interioare. Harta poate fi completată ulterior. Fragmentul nu indică numărul clădirilor care au rampă.',
 ['Numărul clădirilor cu rampă este cincisprezece.','Au fost verificate intrările a douăzeci de clădiri.','Au fost evaluate toate spațiile interioare.'],['N','A','F'],
 'Harta documentează intrările verificate și poate fi completată, fără o evaluare integrală a interioarelor',
 ['Harta garantează accesibilitatea fiecărui spațiu interior','Nu a fost verificată nicio intrare','Harta nu poate fi actualizată niciodată'],
 ('Ce generalizare nu este justificată?', 'O rampă la intrare garantează accesibilitatea întregii clădiri',['Verificarea a vizat intrările','Harta poate fi completată','Evaluarea interioarelor nu a fost integrală'], 'Accesul la intrare nu oferă informații suficiente despre toate spațiile interioare.')),
('Feedbackul anonim','Chestionarul permite răspunsuri anonime și este disponibil timp de o săptămână. Participarea nu este obligatorie. Organizatorii analizează răspunsurile primite, fără să afirme că ele reprezintă automat opiniile tuturor elevilor. Numărul răspunsurilor nu este precizat.',
 ['Participarea este voluntară.','Au răspuns exact o sută de elevi.','Toți elevii sunt obligați să completeze chestionarul.'],['A','N','F'],
 'Chestionarul colectează voluntar feedback anonim, cu limite privind generalizarea rezultatelor',
 ['Răspunsurile descriu obligatoriu opiniile fiecărui elev','Participarea este obligatorie','Identitatea fiecărui respondent este publicată'],
 ('De ce nu putem atribui automat rezultatele tuturor elevilor?', 'Participanții voluntari pot avea opinii diferite de cei care nu răspund',['Anonimatul face toate răspunsurile false','O săptămână este întotdeauna insuficientă','Toți elevii au obligatoriu aceeași opinie'], 'Participarea voluntară poate selecta un grup diferit de totalul elevilor. Textul nu garantează reprezentativitatea.')),
]
COMPLETIONS=[
 [('Pentru a compara două rezultate, folosim același ___ de evaluare','criteriu',['accident','decor','interval de odihnă']),('O afirmație susținută de date verificabile este mai bine ___','fundamentată',['ascunsă','colorată','grăbită'])],
 [('Dacă o instrucțiune poate fi interpretată în mai multe feluri, ea este ___','ambiguă',['exactă','obligatoriu falsă','univocă']),('O explicație care păstrează ideea principală, dar folosește alte cuvinte, este o ___','reformulare',['contradicție','măsurătoare','negare'])],
 [('Un rezultat care poate fi obținut din nou în aceleași condiții este ___','reproductibil',['definitiv imposibil','obligatoriu identic în orice condiții','secret']),('Pentru a transforma o observație într-o regulă generală, avem nevoie de dovezi ___','suplimentare',['decorative','inexistente','interzise'])],
 [('Un plan care stabilește ordinea sarcinilor importante realizează o ___','prioritizare',['anulare','duplicare','întârziere obligatorie']),('Două afirmații care nu pot fi adevărate simultan sunt ___','incompatibile',['identice','independente în mod necesar','obligatoriu adevărate'])],
 [('O concluzie derivată logic din premise este o ___','deducție',['decorație','preferință','întâmplare']),('Un exemplu care infirmă o afirmație universală este un ___','contraexemplu',['certificat','consens','rezumat'])],
 [('O condiție fără de care rezultatul nu poate apărea este o condiție ___','necesară',['accidentală','opțională','superficială']),('Un text care prezintă pe scurt ideile esențiale este un ___','rezumat',['catalog de prețuri','dialog obligatoriu','inventar complet'])],
 [('O decizie poate fi revizuită dacă apar informații ___','noi',['ascunse pentru totdeauna','imposibil de verificat în mod necesar','identice cu toate cele vechi']),('O comparație corectă între două consumuri cere unități de măsură ___','compatibile',['aleatorii','contradictorii','decorative'])],
 [('Dacă o regulă admite cazuri în care nu se aplică, acestea sunt ___','excepții',['confirmări universale','definiții identice','obligații generale']),('O afirmație care spune mai mult decât permit datele este o concluzie ___','excesivă',['demonstrată în întregime','inevitabil adevărată','minimală'])],
 [('Pentru a identifica o eroare, verificăm dacă rezultatul respectă ___','condițiile problemei',['culoarea paginii','numele autorului','ordinea alfabetică a titlurilor']),('Dacă două schimbări au loc simultan, atribuirea efectului uneia singure necesită ___','dovezi care separă efectele',['alegerea la întâmplare','ignorarea celeilalte schimbări','repetarea concluziei'])],
 [('O concluzie sigură trebuie să decurgă din informațiile ___','oferite',['imaginate','neprecizate','preferate']),('Alegerea unor cazuri care să reprezinte întregul grup cere o selecție ___','reprezentativă',['arbitrară în mod necesar','exclusiv după preferințe','fără nicio regulă'])],
]
ANALOGIES=[('rădăcină','arbore','fundație','clădire',['acoperiș','fereastră','zid'],'parte care susține → întreg susținut'),('cald','rece','rapid','lent',['grăbit','scurt','viteză'],'termen → opus'),('bibliotecă','cărți','muzeu','exponate',['bilete','program','vizitatori'],'instituție → obiecte pe care le păstrează și prezintă'),('redactor','text','montator video','film',['cameră','ecran','spectator'],'profesie → materialul pe care îl prelucrează'),('litru','volum','kilogram','masă',['distanță','presiune','timp'],'unitate → mărime măsurată'),('ploaie','umbrelă','soare puternic','parasolar',['cizme','pelerină','zăpadă'],'condiție → obiect de protecție potrivit'),('arbitru','meci','judecător','proces',['carte','hartă','laborator'],'rol de arbitrare → procedura supravegheată'),('întrebare','răspuns','problemă','soluție',['copertă','pauză','titlu'],'sarcină → rezolvarea ei'),('capitol','carte','scenă','piesă de teatru',['actor','decor','sală'],'parte → întreg'),('elev','învățare','cercetător','investigare',['copiere mecanică','odihnă','vânzare'],'persoană → activitate definitorie')]
PAIRS=[('unelte de lucru','ciocan și clește',['ciocan și lapte','clește și tramvai','mătase și cireș']),('unități de timp','secundă și minut',['minut și kilogram','secundă și litru','metru și kilogram']),('instrumente optice','microscop și telescop',['microscop și stilou','telescop și cheie','carte și bicicletă']),('materiale textile','bumbac și lână',['bumbac și fier','lână și sticlă','cupru și hârtie']),('surse scrise de informare','dicționar și atlas',['atlas și scaun','dicționar și clopot','lampă și ușă']),('corpuri geometrice','cub și sferă',['cub și triunghi','sferă și cerc','pătrat și dreptunghi']),('fenomene meteorologice','ploaie și ninsoare',['ploaie și râu','ninsoare și munte','lac și pădure']),('dispozitive de stocare a datelor','hard disk și memorie USB',['hard disk și mouse','memorie USB și imprimantă','monitor și tastatură']),('mijloace de transport pe apă','barcă și vapor',['barcă și tren','vapor și autobuz','avion și tramvai']),('subdiviziuni administrative ale unui oraș','cartier și sector',['cartier și continent','sector și ocean','țară și planetă'])]

def verbal(k):
    title,text,statements,values,main,wrongs,extra=TEXTS[k];qs=[]
    # Patru variante complete în locul formatului vechi cu trei răspunsuri.
    def label(v):return '; '.join(f'{i+1}: '+{'A':'adevărat','F':'fals','N':'nu se poate stabili'}[x] for i,x in enumerate(v))
    distractors=[]
    for i in range(3):
        v=values.copy();v[i]={'A':'N','N':'F','F':'A'}[v[i]];distractors.append(label(v))
    evidence=[]
    for i,(s,v) in enumerate(zip(statements,values)):
        evidence.append(f'Enunțul {i+1} („{s}”) este '+{'A':'adevărat pe baza fragmentului: este susținut explicit de informațiile prezentate.','F':'fals pe baza fragmentului: textul afirmă contrariul.','N':'nedeterminabil: fragmentul nu oferă date suficiente, deci nu îl declarăm nici adevărat, nici fals.'}[v])
    qs.append(item('verbal','Valori de adevăr pe baza unui text',f'Citește fragmentul și folosește numai informațiile din el:\n{text}\n\n'+ '\n'.join(f'{i+1}. {s}' for i,s in enumerate(statements))+'\nCare combinație este corectă?',label(values),distractors,
      ['Verificăm separat fiecare dintre cele trei enunțuri. Nu folosim informații din afara fragmentului.']+evidence+['Selectăm varianta care reproduce toate cele trei valori, în ordinea 1, 2, 3.'],
      'Adevărat = susținut de text; fals = contrazis de text; nedeterminabil = informații insuficiente.','Informația absentă nu este automat falsă. O valoare numerică neprecizată nu poate fi inventată.',
      table={'headers':['Enunț','Valoare față de text'],'rows':[[s,{'A':'Adevărat','F':'Fals','N':'Nu se poate stabili'}[v]] for s,v in zip(statements,values)]}))
    qs.append(item('verbal','Rezumat fără generalizare',f'Fragment:\n{text}\n\nCare este rezumatul cel mai fidel?',main,wrongs,
      ['Identificăm tema fragmentului și limitele informației oferite.',f'Rezumatul corect este: {main}.','Verificăm dacă rezumatul păstrează limitările, fără să transforme „unii” în „toți” sau „poate” în „garantează”.','Celelalte formulări elimină o limită explicită ori adaugă un rezultat care nu este demonstrat.'],
      'Un rezumat fidel păstrează atât ideea centrală, cât și limitările importante.','Un rezumat mai categoric decât textul schimbă sensul.'))
    question,answer,wrong,reason=extra
    qs.append(item('verbal','Inferență și limitarea concluziei',f'Pe baza fragmentului despre „{title.lower()}”:\n{text}\n\n{question}',answer,wrong,
       ['Recitim întrebarea pentru a vedea dacă se cere o concluzie permisă, o limită sau o inferență de evitat.',reason,f'Formularea care răspunde exact cerinței este: {answer}.','Verificăm că nu confundăm fapte distincte și nu adăugăm relații de cauzalitate nedemonstrate.'],
       'Concluzia trebuie să fie susținută de informația relevantă pentru cerință.','Asocierea a două fapte nu dovedește automat că unul este singura cauză a celuilalt.'))
    for sentence,answer,wrong in COMPLETIONS[k]:
        qs.append(item('verbal','Completare verbală în context',f'Completează propoziția cu formularea care păstrează sensul: „{sentence}.”',answer,wrong,
          ['Citirea întregii propoziții arată relația pe care trebuie să o exprimăm.',f'Completarea potrivită este „{answer}”.',f'Recitim propoziția completată: „{sentence.replace("___",answer)}.”','Celelalte variante fie schimbă relația, fie introduc informații fără legătură.'],
          'Completează după sensul întregii propoziții.','Un cuvânt apropiat tematic nu este suficient dacă propoziția rezultată nu exprimă relația cerută.'))
    a,b,c,d,wrong,relation=ANALOGIES[k]
    qs.append(item('verbal','Transferul unei relații verbale',f'Completează analogia: {a} : {b} = {c} : … .',d,wrong,
        [f'Relația primei perechi este: {relation}.',f'Păstrăm direcția relației și o aplicăm termenului „{c}”.',f'Obținem „{d}”.','Verificăm că rolul celui de-al patrulea termen corespunde rolului celui de-al doilea.'],
        'Identifică relația, apoi transfer-o fără să o inversezi.','Nu alege doar un obiect asociat; caută același tip de relație.'))
    category,answer,wrong=PAIRS[k]
    qs.append(item('verbal','Selectarea unei perechi din aceeași categorie',f'Care pereche este alcătuită exclusiv din {category}?',answer,wrong,
      [f'Categoria cerută este „{category}”.','Testăm separat fiecare membru al fiecărei perechi.',f'Ambele elemente din „{answer}” se încadrează în categoria cerută.','La celelalte perechi, cel puțin un element aparține unei alte categorii.'],
      'O pereche corectă trebuie să aibă ambele elemente în categoria cerută.','Faptul că un singur element se încadrează nu este suficient.'))
    return qs

def numeric(k):
    qs=[]
    def add(model,prompt,r,wrongs,unit,steps,rule,trap,op,alternative=''):
        r=F(r);wrong=list(map(F,wrongs));assert r not in wrong and len(set(wrong))==3
        proof={'kind':'research-numeric','operation':op,'result':str(r),'options':[str(r)]+list(map(str,wrong))}
        qs.append(item('numeric',model,prompt,fmt(r)+unit,[fmt(x)+unit for x in wrong],steps+[f'Rezultatul cerut este {fmt(r)}{unit}.'],rule,trap,alternative,proof))
    a=32+4*k;b=48+6*k;c=60+5*k;d=40+3*k
    add('Selectarea rândurilor relevante din tabel',f'Tabelul prezintă numărul de participanți la patru ateliere:\nAtelier A: {a} participanți.\nAtelier B: {b} participanți.\nAtelier C: {c} participanți.\nAtelier D: {d} participanți.\nCâți participanți au împreună atelierele B și C?',b+c,[a+b,c+d,a+d],' participanți',
      ['Cerința privește numai atelierele B și C; nu adunăm toate rândurile.',f'Citirea tabelului: B are {b}, C are {c} participanți.',f'Totalul cerut: {b} + {c} = {b+c}.'],'Selectează întâi rândurile cerute, apoi efectuează calculul.','Nu folosi un total care include alte ateliere.','table-sum')
    small=12+2*k;large=small*3
    add('Raport orientat din date numerice',f'Într-un grafic, grupa X are {small} de persoane, iar grupa Y are {large} de persoane. Care este raportul dintre numărul din X și numărul din Y, exprimat ca fracție?',F(1,3),[F(3),F(1,2),F(2,3)],'',
      [f'Ordinea cerută este X față de Y, deci scriem {small}/{large}.',f'Împărțim numărătorul și numitorul la {small}: obținem 1/3.',f'Control: {large} ÷ 3 = {small}, deci X este o treime din Y.'],'În raportul X/Y, pune X la numărător și Y la numitor.','Raportul invers, Y/X, ar fi 3 și ar răspunde altei întrebări.','oriented-ratio')
    before=80+20*k;after=before*F(5,4)
    add('Creștere procentuală față de baza inițială',f'Numărul vizitelor crește de la {before} la {fmt(after)}. Cu ce procent a crescut numărul vizitelor?',25,[20,75,125],'%',
       [f'Creșterea în valori absolute: {fmt(after)} − {before} = {fmt(after-before)}.',f'Baza este numărul inițial, {before}.',f'Procentul creșterii: {fmt(after-before)} ÷ {before} × 100 = 25%.'],'Procentul creșterii = diferența ÷ valoarea inițială × 100.','Diferența raportată la valoarea finală ar da alt procent.','growth',f'Regula de trei simplă: {before} vizite → 100%; {fmt(after-before)} vizite suplimentare → x%. x = {fmt(after-before)} × 100 ÷ {before} = 25%.')
    n1=10+k;n2=2*n1;v1=6;v2=9;r=8
    add('Medie ponderată a două grupuri',f'Într-o evaluare, {n1} persoane obțin fiecare nota {v1}, iar alte {n2} persoane obțin fiecare nota {v2}. Care este media tuturor notelor?',r,[F(15,2),7,9],'',
       [f'Primul grup contribuie cu {n1} × {v1} = {n1*v1} puncte.',f'Al doilea contribuie cu {n2} × {v2} = {n2*v2} puncte.',f'Suma este {n1*v1+n2*v2}, iar numărul persoanelor este {n1+n2}.',f'Media: {n1*v1+n2*v2} ÷ {n1+n2} = 8.'],'Ponderează fiecare notă cu numărul persoanelor care au obținut-o.','Media simplă a lui 6 și 9 ar ignora faptul că grupurile au mărimi diferite.','weighted', 'Metoda grupurilor egale: la fiecare persoană cu nota 6 corespund două persoane cu nota 9. Media acestui grup de trei persoane este (6 + 9 + 9) ÷ 3 = 8.')
    n=500+50*k;p=20;r=F(n)*F(4,5)*F(4,5)
    add('Scădere succesivă a aceleiași proporții',f'Un stoc inițial de {n} de materiale scade cu {p}% în prima etapă, apoi cu încă {p}% din stocul rămas în a doua etapă. Câte materiale rămân?',r,[F(n)*F(3,5),F(n)*F(4,5),F(n)*F(1,5)],' materiale',
      ['După o scădere de 20% rămâne 80% din stocul de la începutul etapei.',f'Etapa 1: {n} × 0,80 = {fmt(F(n)*F(4,5))}.',f'Etapa 2: {fmt(F(n)*F(4,5))} × 0,80 = {fmt(r)}.','Cele două procente au baze diferite, deci nu le adunăm ca și cum s-ar aplica ambele stocului inițial.'],'Pentru scăderi succesive, înmulțește factorii corespunzători fiecărei etape.','20% + 20% nu înseamnă aici o scădere totală de 40%.','successive')
    km=180+30*k;cons=6;price=8;r=F(km)*F(cons,100)*price
    add('Consum și cost cu unități',f'Un vehicul parcurge {km} km și consumă {cons} litri la 100 km. În această problemă, un litru costă {price} lei. Cât costă combustibilul pentru deplasare?',r,[F(km)*F(cons,100),r+8,r*2],' lei',
      [f'La 100 km se consumă {cons} litri.',f'La {km} km se consumă {km} × {cons} ÷ 100 = {fmt(F(km)*F(cons,100))} litri.',f'Costul este {fmt(F(km)*F(cons,100))} × {price} = {fmt(r)} lei.'],'Calculează întâi consumul în litri, apoi înmulțește cu prețul pe litru.','O valoare în litri nu răspunde unei întrebări despre lei.','fuel',f'Regula de trei simplă: 100 km → {cons} litri; {km} km → x litri. x = {km} × {cons} ÷ 100. Apoi înmulțești x cu {price} lei/litru.')
    fixed=40+10*k;unit=12;count=8+2*k;r=fixed+unit*count
    add('Cost fix și cost variabil',f'O activitate are un cost fix de {fixed} lei și un cost suplimentar de {unit} lei pentru fiecare participant. Participă {count} persoane. Care este costul total?',r,[unit*count,fixed+unit,r+fixed],' lei',
       [f'Costul fix de {fixed} lei se plătește o singură dată.',f'Costul variabil: {count} × {unit} = {count*unit} lei.',f'Total: {fixed} + {count*unit} = {r} lei.'],'Total = cost fix + cost unitar × număr de participanți.','Nu înmulți și costul fix cu numărul participanților.','fixed-variable')
    return qs

def logic(k):
    title=TEXTS[k][0].lower();qs=[]
    if k%2==0:
        prompt=f'La „{title}”, accesul este permis numai dacă există atât ecuson, cât și aprobare. O persoană are acces permis. Ce rezultă cu certitudine?'
        answer='Persoana are atât ecuson, cât și aprobare'
        wrong=['Persoana are ecuson, dar nu are aprobare','Persoana nu are ecuson, dar are aprobare','Persoana nu are nici ecuson, nici aprobare']
        steps=['Notăm E = are ecuson, A = are aprobare și P = are acces permis.','Expresia „numai dacă” introduce condiții necesare: P → (E și A).','Știm că P este adevărat, deci ambele condiții necesare trebuie îndeplinite.','Prin urmare, persoana are ecuson și aprobare; lipsa oricăreia ar contrazice regula.']
        op='necessary-both'
        rows=[['Da','Da','Posibil'],['Da','Nu','Nu este permis'],['Nu','Da','Nu este permis'],['Nu','Nu','Nu este permis']]
        table={'headers':['Ecusoane','Aprobare','Acces permis conform regulii'],'rows':rows}
    else:
        prompt=f'În verificarea pentru „{title}”, se aplică regula: „Dacă dosarul are semnătură și aviz, atunci este acceptat.” Dosarul are semnătură, dar nu are aviz. Ce putem concluziona numai din această regulă?'
        answer='Nu putem stabili dacă dosarul este acceptat'
        wrong=['Dosarul este obligatoriu acceptat','Dosarul este obligatoriu respins','Dosarul nu are semnătură']
        steps=['Condiția regulii conține două cerințe simultane: semnătură și aviz.','Dosarul are semnătură, dar nu are aviz, deci condiția compusă nu este îndeplinită.','Regula garantează acceptarea atunci când ambele cerințe sunt îndeplinite. Nu precizează ce se întâmplă în celelalte cazuri.','Sunt compatibile cu regula atât acceptarea, cât și respingerea acestui dosar. Concluzia este că acceptarea nu poate fi stabilită.','Nu adăugăm cuvântul „numai”: textul nu spune că sunt acceptate numai dosarele cu semnătură și aviz.']
        op='insufficient-conjunction'
        table={'headers':['Semnătură','Aviz','Acceptat','Regula este respectată'],'rows':[['Da','Nu','Da','Da'],['Da','Nu','Nu','Da']]}
    qs.append(item('logic','Condiții logice compuse',prompt,answer,wrong,steps,'P și Q cere îndeplinirea ambelor condiții; „numai dacă” indică necesitate.','Nu inversa o implicație și nu transforma o condiție suficientă în condiție necesară.',proof={'kind':'research-compound','operation':op},table=table))
    shift=k%3;matrix=[[(r+c+shift)%3+1 for c in range(3)] for r in range(3)];missing=matrix[2][2]
    symbol=['○','△','□'][k%3];names=['cercuri','triunghiuri','pătrate'];unit=names[k%3]
    labels={1:f'Un singur simbol {symbol}',2:f'Două simboluri {symbol}',3:f'Trei simboluri {symbol}',4:f'Patru simboluri {symbol}'}
    q=item('logic','Completarea unei matrice figurale',f'Matricea din setul {51+k} respectă această regulă: pe fiecare rând și pe fiecare coloană apar o dată un simbol, o dată două simboluri și o dată trei simboluri. Ce trebuie pus în celula cu semnul întrebării?',labels[missing],[labels[x] for x in range(1,5) if x!=missing],
       ['Regula cere ca numerele 1, 2 și 3 să apară câte o dată pe fiecare rând și pe fiecare coloană.',f'În ultimul rând sunt deja {matrix[2][0]} și {matrix[2][1]} simboluri; lipsește numărul {missing}.',f'În ultima coloană sunt deja {matrix[0][2]} și {matrix[1][2]} simboluri; lipsește tot {missing}.',f'Ambele verificări indică {missing} simboluri {symbol}.'],
       'Verifică regula și pe rând, și pe coloană.','Nu alege după aspectul unei singure celule; răspunsul trebuie să satisfacă ambele direcții.',proof={'kind':'research-matrix','matrix':matrix,'result':missing,'symbol':symbol})
    q['figure']={'kind':'matrix','cells':[[symbol*matrix[r][c] if (r,c)!=(2,2) else '?' for c in range(3)] for r in range(3)]};qs.append(q)
    # O repartizare cu soluție unică, diferită de un simplu lanț alfabetic.
    people=[f'Persoana {chr(65+k)}',f'Persoana {chr(66+k)}',f'Persoana {chr(67+k)}'];a,b,c=people
    solution=[b,a,c] if k%2==0 else [c,a,b]
    first=solution[0];last=solution[-1]
    answer=' → '.join(solution);other=[' → '.join(x) for x in itertools.permutations(people) if list(x)!=solution][:3]
    qs.append(item('logic','Repartizare în trei intervale',f'Pentru „{title}”, {a}, {b} și {c} ocupă câte un interval dintre primul, al doilea și al treilea, fără suprapuneri. {a} nu ocupă nici primul, nici al treilea interval. {first} este înaintea lui {last}. Care este ordinea?',answer,other,
       [f'{a} nu poate fi în primul sau al treilea interval, deci ocupă al doilea.',f'Pentru {first} și {last} rămân intervalele 1 și 3.',f'Condiția {first} înaintea lui {last} îl așază pe primul în intervalul 1 și pe celălalt în intervalul 3.',f'Ordinea unică este {answer}.'],
       'Fixează poziția impusă de excluderi, apoi aplică relația de ordine.','Nu uita că fiecare interval este ocupat de exact o persoană.',proof={'kind':'research-order','people':people,'middle':a,'before':[first,last]}))
    offset=2+k;factor=2+(k%2);x=4+k;r=x*factor+offset
    examples=[(v,v*factor+offset) for v in [1,2,3]]
    qs.append(item('logic','Descoperirea unei reguli de transformare',f'În codul „{title}”, regula este de forma „înmulțește cu o constantă întreagă pozitivă, apoi adaugă o a doua constantă întreagă”. Cele două constante rămân neschimbate în toate exemplele: '+ '; '.join(f'{a} → {b}' for a,b in examples)+f'. Ce rezultat corespunde numărului {x}?',str(r),[str(r-factor),str(r+factor),str(r+1)],
       [f'Când intrarea crește cu 1, rezultatul crește cu {factor}; acesta este factorul de înmulțire.',f'Din exemplul 1 → {factor+offset}, după înmulțirea 1 × {factor}, trebuie adăugat {offset}.',f'Controlăm celelalte exemple cu regula rezultat = intrare × {factor} + {offset}.',f'Pentru {x}: {x} × {factor} + {offset} = {r}.'],
       'Într-o regulă liniară precizată, diferența ieșirilor pentru intrări consecutive arată factorul.','Aplică întâi înmulțirea, apoi adunarea, exact în ordinea cerută.',proof={'kind':'research-function','examples':examples,'input':x,'result':r}))
    qs.append(item('logic','Deducție cu existență',f'Toți membrii echipei „{title}” au acces la arhivă. Unii membri ai acestei echipe sunt voluntari. Ce rezultă cu certitudine?',
       'Unii voluntari au acces la arhivă',['Niciun voluntar nu are acces la arhivă','Toate persoanele cu acces sunt voluntari','Toți voluntarii sunt membri ai echipei'],
       ['Prima premisă plasează fiecare membru al echipei în categoria persoanelor cu acces.','A doua premisă afirmă că există membri care sunt și voluntari.','Acești membri-voluntari au acces, deoarece regula se aplică tuturor membrilor.','Rezultă existența unor voluntari cu acces; nu rezultă o afirmație despre toți voluntarii.'],
       'Din „Toți A sunt B” și „Unii A sunt C” rezultă „Unii C sunt B”.','Nu transforma o concluzie despre unii voluntari într-o concluzie despre toți.',
       'Metoda mulțimilor: cercul membrilor este inclus în cercul celor cu acces. Marchează în cercul membrilor câteva persoane care sunt voluntari. Acestea sunt automat și în cercul accesului.',proof={'kind':'research-existence'}))
    target=2+k;alt=target+1
    table={'headers':['Loc posibil','Afirmația 1','Afirmația 2','Exact una adevărată'],'rows':[[str(target),'Adevărat','Adevărat','Nu'],[str(alt),'Fals','Adevărat','Da'],['Orice alt loc','Fals','Fals','Nu']]}
    qs.append(item('logic','Exact o afirmație adevărată',f'În clasamentul „{title}”, despre o persoană se fac două afirmații: 1. „Este pe locul {target}.” 2. „Este pe locul {target} sau pe locul {alt}.” Se știe că exact una este adevărată. Pe ce loc este persoana?',str(alt),[str(target),str(alt+1),'Nu se poate determina'],
       [f'Dacă persoana este pe locul {target}, ambele afirmații sunt adevărate, deci cazul este exclus.',f'Dacă este pe locul {alt}, prima este falsă, a doua adevărată: condiția este îndeplinită.','Pe orice alt loc, ambele afirmații sunt false, deci condiția nu este îndeplinită.',f'Singurul loc posibil este {alt}.'],
       'Testează cazurile și numără afirmațiile adevărate.','Exact una exclude atât zero afirmații adevărate, cât și două.',proof={'kind':'research-truth','target':target,'alternative':alt},table=table))
    return qs

tests=[]
for k in range(10):
    def rotate(a,n):return a[n%len(a):]+a[:n%len(a)]
    qs=rotate(verbal(k),k)+rotate(numeric(k),k*2)+rotate(logic(k),k)
    assert len(qs)==20
    for i,q in enumerate(qs):q['id']=f't{k+51}-q{i+1:02d}'
    tests.append(dict(id=51+k,title=TEXTS[k][0]+' · modele de aptitudini',durationSeconds=3600,questions=qs))
sorter="""let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{
const tests=JSON.parse(s);const c=new Intl.Collator('ro',{sensitivity:'base',numeric:false});
for(const t of tests)for(const q of t.questions){const rows=q.options.map((o,i)=>({text:o.replace(/[.!?]+$/,'')+'.',old:i}));rows.sort((a,b)=>c.compare(a.text,b.text));q.correct=rows.findIndex(r=>r.old===q.correct);q.options=rows.map(r=>r.text);if(q.proof?.options)q.proof.options=rows.map(r=>q.proof.options[r.old]);}
process.stdout.write(JSON.stringify(tests));});"""
tests=json.loads(subprocess.run(['node','-e',sorter],input=json.dumps(tests),text=True,capture_output=True,check=True).stdout)
(ROOT/'tests/exam-51-60.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2)+'\n')
print('Generate 51–60: 200 întrebări originale, fără figuri rotite, cu 10 matrice simple.')
