"""Bancă reproductibilă de itemi originali; adaptări de forme, nu subiecte oficiale."""
import json, itertools, math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def fmt(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    if 1000 % x.denominator == 0: return str(float(x)).replace('.', ',').rstrip('0').rstrip(',')
    return f'{x.numerator}/{x.denominator}'

def item(cat, model, prompt, answers, correct, steps, rule, trap, hint='', proof=None, historical=False):
    assert len(answers)==4 and len(set(map(str, answers)))==4
    assert 0<=correct<4
    return dict(category=cat, model=model, prompt=prompt, options=list(map(str,answers)), correct=correct,
        solution=dict(steps=steps, rule=rule, trap=trap), hint=hint, proof=proof,
        historical=historical)

def num(model,prompt,result,wrong,steps,rule,trap,unit='',hint=''):
    values=[F(result)]+[F(v) for v in wrong]
    assert len(set(values))==4, (model,values)
    return item('numeric',model,prompt,[fmt(v)+(' '+unit if unit else '') for v in values],0,
      steps+[f'Verificare: rezultatul cerut este {fmt(result)}'+(' '+unit if unit else '')+'.'],rule,trap,hint,
      proof=dict(kind='numeric',result=str(F(result)),options=[str(v) for v in values]))

NAMES=['Ana','Bogdan','Carmen','Dan','Elena','Florin','Gabriela','Horia','Ioana','Luca','Mara','Nora','Oana','Paul','Radu','Sonia','Tudor','Vlad','Daria','Emil']
TOPICS=['lectură','robotică','dezbatere','teatru','astronomie','fotografie','ecologie','scriere creativă','muzică','istorie locală','orientare profesională','jurnalism','arte digitale','șah','matematică aplicată','voluntariat','educație financiară','programare','biologie','comunicare']
ANALOGIES=[
 ('bibliotecă','cărți','arhivă','documente',['cititori','rafturi','secretari'],'loc–conținut'),
 ('termometru','temperatură','cronometru','timp',['distanță','presiune','viteză'],'instrument–mărime măsurată'),
 ('pictor','tablou','compozitor','compoziție muzicală',['pensulă','galerie','spectator'],'creator–operă'),
 ('rădăcină','copac','fundație','clădire',['acoperiș','fereastră','cameră'],'parte de susținere–întreg'),
 ('medic','spital','profesor','școală',['manual','examen','elev'],'profesie–loc de muncă tipic'),
 ('capitol','carte','act','piesă de teatru',['scenă de concert','actor','bilet'],'subdiviziune–operă'),
 ('busolă','orientare','dicționar','explicarea cuvintelor',['măsurarea timpului','numărarea paginilor','desenarea hărților'],'instrument–funcție'),
 ('sămânță','plantă','ou','pui',['cuib','pană','aripă'],'stadiu inițial–organism rezultat'),
 ('zi','săptămână','lună','an',['oră','minut','secol'],'unitate temporală–unitate mai mare care o include'),
 ('autor','roman','arhitect','proiect de clădire',['cititor','bibliotecă','cărămidă'],'creator–produs al creației'),
 ('cuțit','tăiere','ac','coasere',['măsurare','citire','vopsire'],'unealtă–acțiune'),
 ('aripă','pasăre','înotătoare','pește',['apă','cuib','solz'],'organ de deplasare–animal'),
 ('kilogram','masă','metru','lungime',['timp','volum','temperatură'],'unitate de măsură–mărime'),
 ('hartă','teritoriu','plan de clădire','clădire',['călător','busolă','constructor'],'reprezentare–obiect reprezentat'),
 ('dirijor','orchestră','antrenor','echipă',['minge','stadion','spectator'],'coordonator–grup coordonat'),
 ('perimetru','lungime','arie','suprafață',['viteză','masă','durată'],'măsură–caracteristică geometrică'),
 ('cheie','încuietoare','parolă','cont digital',['tastatură','ecran','fișier public'],'mijloc de acces–sistem protejat'),
 ('redactor','text','montor video','film',['microfon','sală','cititor'],'specialist în editare–material editat'),
 ('frunză','copac','pagină','carte',['creion','cititor','birou'],'parte–întreg'),
 ('întrebare','răspuns','problemă','soluție',['enunț','dificultate','număr'],'sarcină–rezolvare')]
LEX=[('preliminare','Datele preliminare vor fi verificate.','inițiale',['definitive','eronate','irelevante']),('succint','Raportul este succint.','concis',['confuz','detaliat','inexact']),('consecvent','Aplică regulile consecvent.','constant',['arbitrar','ocazional','superficial']),('pertinent','A formulat un argument pertinent.','relevant',['ambiguu','contradictoriu','secundar']),('explicit','Acordul trebuie să fie explicit.','clar exprimat',['implicit','neclar','presupus']),('fezabil','Planul este fezabil.','realizabil',['imposibil','obligatoriu','terminat']),('echitabil','A propus un criteriu echitabil.','corect și imparțial',['aleatoriu','identic în orice situație','preferențial']),('temporar','Programul este temporar.','limitat în timp',['definitiv','permanent','repetat zilnic']),('prioritar','Acesta este un obiectiv prioritar.','cu întâietate',['deja îndeplinit','fără importanță','opțional']),('coerent','Textul este coerent.','cu idei legate logic',['cu multe citate','foarte scurt','scris de mai mulți autori'])]
PAIRS=[('autobuz','tramvai','mijloace de transport'),('vioară','pian','instrumente muzicale'),('triunghi','pătrat','figuri geometrice plane'),('roman','nuvelă','specii literare epice'),('cupru','fier','metale'),('stejar','fag','arbori'),('kilometru','centimetru','unități de lungime'),('cerc','dreptunghi','figuri geometrice plane'),('vrabie','rândunică','păsări'),('psiholog','medic','profesii')]

def verbal(m,t):
    topic=TOPICS[t]; name=NAMES[t]; k=12+t; other=NAMES[(t+3)%20]
    if m==0:
        p=f'„Clubul de {topic} și-a prelungit programul în două zile ale săptămânii. Numărul participanților a crescut. Raportul nu stabilește cauza creșterii.”\nCare afirmație este susținută de text?'
        return item('verbal','Informație explicită',p,['Numărul participanților a crescut.','Programul s-a prelungit în fiecare zi.','Programul prelungit a provocat creșterea.','Fiecare participant a venit mai des.'],0,
        ['Citește cerința: se caută o afirmație susținută de text.','Textul afirmă direct creșterea numărului de participanți.','Nu avem o cauză demonstrată și nici informații despre frecvența fiecărei persoane.','Alege constatarea explicită, fără să o transformi într-o explicație cauzală.'],'Separă observația de explicația ei.','În fiecare zi este mai mult decât în două zile; totalul nu descrie fiecare persoană.',historical=True)
    if m==1:
        return item('verbal','Informație absentă',f'„Atelierul de {topic} este opțional. Toți cei înscriși au primit materialele. Unii au participat vineri.”\nCare afirmație NU poate fi stabilită din text?',
        ['Toți cei înscriși au primit materialele.',f'{name} a participat vineri.','Atelierul este opțional.','Cel puțin un participant înscris a venit vineri.'],1,
        ['Observă cuvântul NU: căutăm o informație absentă.',f'Textul nu menționează persoana {name}.','Nu putem transforma o informație despre unii participanți într-o informație despre o persoană precisă.','Celelalte variante reproduc informații explicite sau sensul lui unii.'],'Lipsa informației nu dovedește nici adevărul, nici falsitatea unei afirmații.','A alege o afirmație adevărată când se cere ce NU se poate stabili inversează cerința.',historical=True)
    if m in (2,3):
        a,b,c,d,w,rel=ANALOGIES[t if m==2 else (t+7)%20]
        return item('verbal','Analogie: '+rel,f'În fișa atelierului de {topic}, completează relația: {a} : {b} = {c} : …',[d]+w,0,
        [f'Identifică prima relație: {a} și {b} sunt legate prin {rel}.',f'Păstrează sensul și ordinea aceleiași relații pentru {c}.',f'Termenul corespunzător este {d}.','Verifică ambele perechi: trebuie să aibă aceeași relație, nu doar cuvinte din același domeniu.'],'La analogii, numește relația înainte de a căuta răspunsul.','O asociere tematică nu este suficientă; relația și direcția trebuie păstrate.',historical=True)
    if m==4:
        a,b,c=PAIRS[t%10]
        return item('verbal','Categorie comună',f'Pe fișa lui {name}, ce categorie comună, suficient de precisă, include atât „{a}”, cât și „{b}”?',[c,'obiecte sau concepte fără categorie comună','unități de timp','forme de comunicare verbală'],0,
        [f'Analizează separat sensul lui {a} și al lui {b}.',f'Ambele se încadrează în categoria {c}.','Categoria trebuie să fie valabilă pentru ambii termeni.','Respinge o categorie care descrie numai un termen sau un domeniu diferit.'],'Clasifică pe baza trăsăturilor esențiale comune.','Nu confunda asemănările accidentale cu apartenența la aceeași categorie.',historical=True)
    if m==5:
        word,s,good,w=LEX[t%10]
        return item('verbal','Sens în context',f'În raportul atelierului de {topic} apare enunțul „{s}”. Ce înseamnă „{word}”?',[good]+w,0,
        ['Citește enunțul întreg, nu doar cuvântul izolat.',f'În acest context, {word} are sensul {good}.','Înlocuiește mental cuvântul cu varianta aleasă.','Sensul propoziției trebuie să rămână același.'],'Sinonimul potrivit păstrează sensul contextual.','Nu alege un cuvânt doar pentru că are o conotație asemănătoare.')
    if m==6:
        return item('verbal','Corelație și cauzalitate',f'„Participanții la clubul de {topic} au avut rezultate mai bune. Așadar, clubul a produs rezultatele mai bune.” Care este problema argumentului?',
        ['O asociere este tratată ca dovadă suficientă a cauzei.','Premisa spune că nu există participanți.','Concluzia afirmă că rezultatele sunt identice.','Argumentul compară elevii cu profesorii.'],0,
        ['Premisa constată o asociere între participare și rezultate.','Concluzia adaugă o relație de cauzalitate.','Pot exista alte explicații: pregătire inițială, motivație sau sprijin suplimentar.','Prin urmare, asocierea singură nu demonstrează că participarea a produs diferența.'],'O corelație nu demonstrează singură o cauză.','Nu introduce în premisă informații care apar numai în concluzie.')
    if m==7:
        return item('verbal','Ideea principală',f'„Pentru clubul de {topic}, informațiile sunt publicate într-un singur loc. Astfel, participanții găsesc mai ușor programul, iar modificările nu mai circulă în versiuni diferite.” Care este ideea principală?',
        ['Centralizarea informațiilor facilitează accesul și reduce confuziile.','Programul nu se modifică niciodată.','Participanții nu trebuie să citească informațiile.','Toate cluburile folosesc aceeași platformă.'],0,
        ['Caută ideea care leagă cele două propoziții.','Prima descrie centralizarea; a doua explică avantajele ei.','Varianta corectă cuprinde atât accesul mai ușor, cât și reducerea confuziilor.','Celelalte variante introduc afirmații absolute sau informații absente.'],'Ideea principală acoperă mesajul întregului fragment.','Un detaliu inventat nu devine idee principală doar pentru că este plauzibil.')
    if m==8:
        return item('verbal','Rezumat fidel',f'„La atelierul de {topic}, înscrierea se face până joi. Dacă rămân locuri libere, se acceptă înscrieri și vineri.” Care rezumat păstrează exact informația?',
        ['Înscrierile sunt până joi, cu posibilă prelungire vineri dacă există locuri.','Înscrierile sunt obligatoriu doar vineri.','Oricine se poate înscrie vineri, indiferent de locuri.','Joi nu se acceptă înscrieri.'],0,
        ['Identifică regula generală: înscriere până joi.','Identifică excepția: vineri numai dacă rămân locuri.','Un rezumat fidel păstrează regula și condiția excepției.','Respinge rezumatele care elimină condiția sau inversează termenul.'],'La rezumat, păstrează condițiile și limitele afirmației.','Eliminarea expresiei dacă există locuri schimbă mesajul.')
    if m==9:
        return item('verbal','Referință pronominală',f'„Elevii au prezentat proiectul de {topic} în fața comisiei. Ei au răspuns apoi la întrebări.” La cine se referă „ei”?',
        ['La elevi','La comisie','La proiect','La întrebări'],0,
        ['Identifică antecedentele posibile: elevii, comisia, proiectul.','Pronumele ei este masculin plural și desemnează persoanele care au prezentat.','Elevii corespunde ca număr, gen și rol în succesiunea acțiunilor.','Comisia și proiectul sunt singular; întrebările nu sunt persoanele care răspund.'],'Urmărește acordul gramatical și continuitatea acțiunilor.','Apropierea unui cuvânt de pronume nu este suficientă pentru a-l face antecedent.')
    if m==10:
        return item('verbal','Sensul unei concesii',f'„Deși materialele pentru {topic} au sosit târziu, atelierul a început la ora stabilită.” Ce exprimă relația dintre cele două idei?',
        ['Atelierul a început la timp în ciuda întârzierii materialelor.','Atelierul a întârziat din cauza materialelor.','Materialele au sosit înainte de termen.','Ora atelierului nu fusese stabilită.'],0,
        ['Observă conectorul deși.','Acesta introduce un obstacol sau o situație contrară așteptării.','Continuarea spune că rezultatul a fost totuși începutul la timp.','Nu schimba rezultatul: textul nu afirmă întârzierea atelierului.'],'Deși exprimă concesie: rezultatul apare în pofida unui obstacol.','Nu interpreta o relație concesivă ca una cauzală.')
    if m==11:
        return item('verbal','Sensul unei restricții',f'„La sesiunea de {topic} sunt admiși numai elevii înscriși.” Ce reformulare păstrează sensul?',
        ['Orice elev admis este înscris.','Orice elev înscris este neapărat admis.','Niciun elev înscris nu este admis.','Toți elevii școlii sunt admiși.'],0,
        ['Cuvântul numai limitează categoria celor admiși.','Înscrierea este o condiție necesară pentru admitere.','Din faptul că cineva este admis rezultă că este înscris.','Nu rezultă automat că înscrierea garantează admiterea.'],'Numai introduce o condiție necesară.','Nu inversa sensul relației dintre înscriere și admitere.')
    if m==12:
        return item('verbal','Fapt și apreciere',f'Care enunț despre atelierul de {topic} este o apreciere subiectivă, nu o constatare verificabilă direct?',
        ['Atelierul a fost cel mai frumos eveniment al anului.',f'Au participat {k} elevi.','Atelierul a început la ora 10.','Activitatea a durat două ore.'],0,
        ['O constatare poate fi verificată prin numărare, program sau înregistrare.','Numărul participanților, ora și durata au criterii obiective de verificare.','Cel mai frumos exprimă o evaluare personală, în absența unor criterii precizate.','Alege enunțul a cărui apreciere poate diferi de la o persoană la alta.'],'Distinge datele observabile de judecățile de valoare.','Un enunț poate fi sincer fără să fie o constatare obiectivă.')
    if m==13:
        return item('verbal','Susținerea unei concluzii',f'Concluzie: „Mutarea atelierului de {topic} într-o sală mai mare ar rezolva problema locurilor insuficiente.” Ce informație susține cel mai direct concluzia?',
        ['Sala actuală are 20 de locuri, sunt 28 de înscriși, iar sala nouă are 35 de locuri.','Sala nouă are pereții albaștri.','Unii elevi preferă activitățile în aer liber.','Atelierul este organizat și anul viitor.'],0,
        ['Identifică problema exactă: capacitatea sălii.','Comparația 20 < 28 arată insuficiența sălii actuale.','Comparația 35 ≥ 28 arată că sala nouă poate găzdui înscrișii.','Celelalte informații nu stabilesc dacă există suficiente locuri.'],'O dovadă relevantă răspunde exact problemei concluziei.','Detaliile atractive despre sală nu demonstrează capacitatea ei.')
    if m==14:
        return item('verbal','Slăbirea unei generalizări',f'„Toți elevii care au participat la atelierul de {topic} au obținut punctaj maxim.” Ce informație contrazice direct afirmația?',
        [f'{name} a participat și nu a obținut punctaj maxim.','Un elev absent nu a obținut punctaj maxim.','Un elev absent a obținut punctaj maxim.','Unii participanți au obținut punctaj maxim.'],0,
        ['Afirmația privește toți participanții.','Pentru a o contrazice, trebuie un participant care nu îndeplinește rezultatul afirmat.',f'{name} este tocmai un asemenea contraexemplu.','Rezultatele absenților nu contrazic o regulă despre participanți.'],'O afirmație universală este respinsă de un singur contraexemplu relevant.','Contraexemplul trebuie să aparțină categoriei despre care se vorbește.')
    if m==15:
        return item('verbal','Presupunere necesară',f'„Vom trimite programul atelierului de {topic} exclusiv prin e-mail, astfel încât fiecare participant să-l poată consulta.” Ce presupunere este necesară acestui plan?',
        ['Fiecare participant are acces la e-mailul la care este trimis programul.','Fiecare participant preferă atelierul dimineața.','Programul are exact două pagini.','Toți participanții folosesc același model de telefon.'],0,
        ['Scopul este accesul fiecărui participant la program.','Mijlocul este exclusiv e-mailul.','Dacă o persoană nu poate accesa e-mailul respectiv, planul nu asigură accesul tuturor.','Preferințele, lungimea documentului și modelul telefonului nu sunt condiții necesare.'],'Testează o presupunere negând-o: dacă planul nu mai funcționează, ea poate fi necesară.','Nu confunda o condiție utilă cu una fără de care concluzia nu se susține.')
    if m==16:
        return item('verbal','Ordinea ideilor',f'Aranjează propozițiile într-o succesiune firească:\n1. În final, participanții au prezentat produsele.\n2. Mai întâi, au primit instrucțiunile.\n3. Apoi, au lucrat în echipe la tema de {topic}.',
        ['2–3–1','1–2–3','2–1–3','3–2–1'],0,
        ['Identifică marcatorii temporali: mai întâi, apoi, în final.','Instrucțiunile preced activitatea.','Lucrul în echipe precedă prezentarea produselor.','Ordinea este 2, 3, 1.'],'Marcatorii temporali și relația dintre acțiuni stabilesc succesiunea.','Ordinea tipăririi propozițiilor nu este neapărat ordinea evenimentelor.')
    if m==17:
        return item('verbal','Cuantificatori în text',f'„Majoritatea celor {k} elevi înscriși la {topic} au venit la prima întâlnire.” Care afirmație rezultă sigur?',
        ['Mai mult de jumătate dintre cei înscriși au venit.','Toți cei înscriși au venit.','Exact jumătate dintre cei înscriși au venit.','Niciun elev înscris nu a lipsit.'],0,
        ['Majoritatea înseamnă mai mult de jumătate din grup.','Termenul nu precizează numărul exact.','Poate fi vorba despre toți, dar textul nu garantează acest lucru.','Concluzia sigură păstrează limita minimă exprimată de majoritatea.'],'Nu transforma majoritatea în toți sau în exact jumătate.','O posibilitate nu este o concluzie obligatorie.')
    if m==18:
        return item('verbal','Comparație și concluzie',f'„Atelierul de {topic} are mai mulți înscriși decât clubul de teatru. Clubul de teatru are mai mulți înscriși decât clubul de șah.” Ce rezultă?',
        [f'Atelierul de {topic} are mai mulți înscriși decât clubul de șah.','Clubul de șah are mai mulți înscriși decât clubul de teatru.','Cele trei grupuri au același număr de înscriși.','Clubul de teatru are cei mai mulți înscriși.'],0,
        ['Notează A > B pentru prima comparație.','Notează B > C pentru a doua.','Prin tranzitivitate, A > C.','Nu știm numerele exacte, dar știm ordinea celor trei efective.'],'Relația mai mare decât se transmite printr-un lanț de comparații.','Nu ai nevoie de numere concrete pentru a compara extremitățile lanțului.')
    if m==19:
        return item('verbal','Concluzie excesivă',f'„Doi participanți la atelierul de {topic} au spus că preferă dimineața. Prin urmare, toți participanții preferă dimineața.” De ce concluzia este insuficient susținută?',
        ['Preferința a două persoane este extinsă nejustificat la întregul grup.','Textul dovedește că nimeni nu preferă dimineața.','Preferințele celor două persoane sunt identice cu programul.', 'Concluzia privește numai cele două persoane.'],0,
        ['Premisa conține informații despre două persoane.','Concluzia privește toți participanții.','Nu avem informații despre preferințele celorlalți.','Argumentul generalizează dintr-un grup restrâns fără justificare.'],'Mărimea și reprezentativitatea informației trebuie să susțină amploarea concluziei.','Nu confunda doi sau unii cu toți.')
    return item('verbal','Conector de cauză',f'„Atelierul de {topic} a fost mutat în interior deoarece ploua.” Ce relație exprimă „deoarece”?',
      ['Cauză','Comparație','Concesie','Succesiune fără cauză'],0,
      ['Identifică evenimentul: mutarea în interior.','Identifică explicația: ploaia.','Deoarece introduce motivul mutării.','Nu exprimă o comparație sau un rezultat în pofida unui obstacol.'],'Conectorii indică relația dintre idei.','Nu interpreta toți conectorii ca simple semne de ordine temporală.')

def numeric(m,t):
    a=t+2
    if m==0:
        rows=[(20+a,14+a),(18+a,23+a),(29+a,15+a),(20+a,18+a)]; sums=[sum(x) for x in rows]; best=sums.index(max(sums))
        return item('numeric','Totaluri în tabel','Împrumuturi de cărți (clasa A / clasa B):\n'+'\n'.join(f'{d}: {x} / {y}' for d,(x,y) in zip(['Luni','Marți','Miercuri','Joi'],rows))+'\nÎn ce zi este cel mai mare total?', ['Luni','Marți','Miercuri','Joi'],best,
        ['Adună valorile pe fiecare rând.', 'Totalurile, în ordinea zilelor, sunt: '+', '.join(map(str,sums))+'.',f'Compară totalurile: maximul este {max(sums)}.',f'Acest total aparține zilei { ["Luni","Marți","Miercuri","Joi"][best]}.'],'Compară totaluri corespunzătoare aceleiași unități.','Nu alege ziua cu maximul unei singure clase.', proof=dict(kind='maximum',values=sums,result=best),historical=True)
    if m==1:
        x=120+10*t;y=80+4*t;rate=F(1,2);r=(x-y)*rate
        return num('Tarif pe unitate',f'Ana parcurge {x} km, iar Bogdan {y} km. Tariful este 0,50 lei/km. Cu câți lei primește Ana mai mult?',r,[r+10,r*2,r+5],[f'Diferența de distanță: {x} − {y} = {x-y} km.',f'Diferența de plată: {x-y} × 0,50 = {fmt(r)} lei.'],'Înmulțește diferența de cantitate cu tariful comun.','Kilometrii și leii sunt unități diferite.',unit='lei')
    if m==2:
        initial=200+100*t;r=F(initial)*F(11,10)*F(9,10)
        return num('Procente succesive',f'Un produs de {initial} lei se scumpește cu 10%, apoi noul preț scade cu 10%. Prețul final este:',r,[initial,F(initial)*F(9,10),r+4],[f'Creșterea: {initial} × 1,10 = {fmt(F(initial)*F(11,10))} lei.',f'Reducerea se aplică noului preț: {fmt(F(initial)*F(11,10))} × 0,90 = {fmt(r)} lei.'],'La procente succesive, înmulțește factorii de modificare.','+10% și −10% nu se anulează: bazele sunt diferite.',unit='lei')
    if m==3:
        total=30+5*t;r=total*3//5
        return num('Raport parte–parte',f'Într-un grup de {total} elevi, raportul fete : băieți este 3 : 2. Câte fete sunt?',r,[total*2//5,r+2,r+5],[f'Raportul are 3 + 2 = 5 părți.',f'O parte: {total} ÷ 5 = {total//5}.',f'Fetele: 3 × {total//5} = {r}.'],'Adună părțile raportului înainte să calculezi o parte.','3 : 2 nu înseamnă că fetele sunt 3/2 din întreg.')
    if m==4:
        x=8;y=9;count=10+t;r=F(count*x+2*count*y,3*count)
        return num('Medie ponderată',f'{count} elevi au media 8, iar alți {2*count} au media 9. Media celor {3*count} elevi este:',r,[F(17,2),F(35,4),9],[f'Suma valorilor: {count} × 8 + {2*count} × 9 = {26*count}.',f'Împarte la efectivul total: {26*count} ÷ {3*count} = {fmt(r)}.'],'Ponderează fiecare medie cu numărul persoanelor.','Media simplă 8,5 ar fi valabilă pentru grupuri de aceeași mărime.')
    if m==5:
        d=6+2*t;r=d
        return num('Productivitate cu retragere',f'A termină o lucrare în {d} zile, B în {2*d} zile. Lucrează împreună {d//3} zile, apoi A se retrage. Câte zile suplimentare îi trebuie lui B?',r,[r-1,r+2,2*r],[f'A face zilnic 1/{d}; B face 1/{2*d}.',f'Împreună: 3/{2*d} din lucrare pe zi.',f'În {d//3} zile fac 1/2 din lucrare.',f'B realizează jumătatea rămasă în {2*d} ÷ 2 = {d} zile.'],'Lucrează cu fracții din lucrare pe unitatea de timp.','Nu scădea pur și simplu zilele lucrate din durata individuală.',unit='zile') if d%3==0 else numeric(22,t)
    if m==6:
        start=3+t;ds=[4,6,8,10];seq=[start]
        for d in ds:seq.append(seq[-1]+d)
        r=seq[-1]+12
        return num('Șir cu diferențe crescătoare','Diferențele cresc cu 2. Completează: '+', '.join(map(str,seq))+', …',r,[r-2,r+2,r+4],['Calculează diferențele: 4, 6, 8, 10.','Următoarea diferență este 12.',f'Următorul termen: {seq[-1]} + 12 = {r}.'],'Analizează diferențele când termenii nu cresc cu aceeași cantitate.','Regula privește diferențele, nu simpla repetare a ultimei creșteri.')
    if m==7:
        n=240+20*t;r=F(n,5)
        return num('Procent din întreg',f'Din {n} de înscriși, 20% aleg un atelier online. Câți sunt?',r,[r+10,F(n,4),n-r],[f'20% = 20/100 = 1/5.',f'Numărul cerut: {n} ÷ 5 = {fmt(r)}.'],'Procentul se aplică întregului indicat.','Restul de 80% reprezintă o altă categorie, nu răspunsul cerut.')
    if m==8:
        final=160+8*t;r=F(final)*F(5,4)
        return num('Preț inițial',f'După o reducere de 20%, prețul este {final} lei. Care a fost prețul inițial?',r,[F(final)*F(6,5),final+20,r+10],[f'Prețul final reprezintă 80% din cel inițial.',f'Inițialul: {final} ÷ 0,80 = {fmt(r)} lei.',f'Control: {fmt(r)} × 0,80 = {final}.'],'Pentru a recupera întregul, împarte partea la proporția ei.','A adăuga 20% prețului final nu anulează reducerea de 20%.',unit='lei')
    if m==9:
        r=3*(4+t)
        return num('Proporționalitate directă',f'4 dosare identice se verifică în 12 minute. La același ritm, câte minute necesită {4+t} dosare?',r,[r+3,r+6,r+9],['Un dosar necesită 12 ÷ 4 = 3 minute.',f'{4+t} dosare necesită {4+t} × 3 = {r} minute.'],'La ritm constant, timpul este direct proporțional cu numărul sarcinilor.','Nu folosi o proporție inversă când o singură persoană are mai multe sarcini.',unit='minute')
    if m==10:
        days=12+t;r=F(6*days,9)
        return num('Proporționalitate inversă',f'6 lucrători termină în {days} zile. În câte zile termină 9 lucrători cu același randament, lucrând simultan la aceeași lucrare?',r,[days,F(days)*F(3,2),r+2],[f'Volumul este 6 × {days} = {6*days} om-zile.',f'Cu 9 lucrători: {6*days} ÷ 9 = {fmt(r)} zile.'],'Pentru aceeași lucrare, numărul lucrătorilor și durata sunt invers proporționale.','Mai mulți lucrători reduc durata, în ipoteza randamentului identic.',unit='zile')
    if m==11:
        dist=180+18*t;r=F(dist*2,F(dist,60)+F(dist,90))
        return num('Viteză medie dus–întors',f'Un vehicul parcurge {dist} km cu 60 km/h și revine pe aceeași distanță cu 90 km/h. Fără opriri, viteza medie pe întregul drum este:',r,[75,70,80],[f'Distanța totală este {2*dist} km.',f'Timpul total este {dist}/60 + {dist}/90 = {fmt(F(dist,60)+F(dist,90))} ore.',f'Viteza medie = distanță totală ÷ timp total = {fmt(r)} km/h.'],'Viteza medie se calculează din distanța totală și timpul total.','Media aritmetică a vitezelor nu este potrivită pentru distanțe egale.',unit='km/h')
    if m==12:
        speed=40+2*t;time=F(3,2);r=speed*time
        return num('Distanță și conversie de timp',f'Un vehicul merge cu {speed} km/h timp de 1 oră și 30 de minute. Ce distanță parcurge?',r,[speed*2,speed+30,r+10],[f'1 oră și 30 de minute = 1,5 ore.',f'Distanța = viteză × timp = {speed} × 1,5 = {fmt(r)} km.'],'Transformă timpul în aceeași unitate cu cea folosită în viteză.','1 h 30 min înseamnă 1,5 h, nu 1,30 h.',unit='km')
    if m==13:
        x=12+t;y=x+6;r=x
        return num('Sumă și diferență',f'Două echipe au împreună {x+y} elevi. A doua are cu 6 mai mulți decât prima. Câți elevi are prima?',r,[r+3,r+6,x+y],[f'Scoate diferența din total: {x+y} − 6 = {2*x}.',f'Rămân două părți egale: {2*x} ÷ 2 = {x}.',f'Control: {x} + {x+6} = {2*x+6}.'],'Numărul mai mic este (suma − diferența) ÷ 2.','Împărțirea totalului la doi ignoră diferența.')
    if m==14:
        past=3+t
        return num('Vârste',f'Acum {past} ani, un copil avea 12 ani, iar părintele de trei ori vârsta lui. Ce vârstă are copilul acum?',12+past,[12,36+past,12+2*past],[f'Copilul avea 12 ani.',f'Adaugă timpul scurs: 12 + {past} = {12+past}.'],'Vârsta crește cu numărul anilor scurși.','Selectează datele relevante; vârsta părintelui nu este cerută.')
    if m==15:
        x=8+t;r=x+6
        return num('Media și valoarea lipsă',f'Trei valori au media {x+3}. Primele două sunt {x} și {x+3}. Care este a treia?',r,[x+3,x+9,3*(x+3)],[f'Suma celor trei valori: 3 × {x+3} = {3*(x+3)}.',f'Suma celor două cunoscute: {x} + {x+3} = {2*x+3}.',f'Valoarea lipsă: {3*(x+3)} − {2*x+3} = {r}.'],'Din medie și efectiv obții suma, apoi scazi valorile cunoscute.','Media nu este automat valoarea lipsă.')
    if m==16:
        x=30+t;y=25+t;both=10;r=x+y-both
        return num('Reuniunea a două grupuri',f'{x} elevi aleg engleza, {y} aleg franceza, iar 10 le aleg pe ambele. Câți aleg cel puțin una dintre cele două?',r,[x+y,r-10,r+5],[f'Adunarea simplă: {x} + {y} = {x+y}.','Elevii care aleg ambele limbi sunt numărați de două ori.',f'Scade o dată intersecția: {x+y} − 10 = {r}.'],'Reuniune = primul grup + al doilea − intersecție.','Cel puțin una îi include și pe cei care aleg ambele.')
    if m==17:
        x=5+t;r=x*2**5
        return num('Șir geometric','Fiecare termen este dublul precedentului. Completează: '+', '.join(str(x*2**i) for i in range(5))+', …',r,[r//2+2,r+5,r*2],['Regula precizată este înmulțirea cu 2.',f'Ultimul termen este {x*16}.',f'Următorul: {x*16} × 2 = {r}.'],'Păstrează raportul constant al șirului geometric.','Nu trece de la înmulțire la o diferență arbitrară.')
    if m==18:
        x=40+4*t;r=F(x)*F(5,4)
        return num('Creștere procentuală',f'Numărul participanților crește de la {x} la {fmt(r)}. Care este creșterea procentuală?',25,[20,30,125],[f'Creșterea absolută: {fmt(r)} − {x} = {fmt(r-x)}.',f'Raportează la inițial: {fmt(r-x)} ÷ {x} × 100 = 25%.'],'Creșterea procentuală se raportează la valoarea inițială.','125% este noul nivel față de inițial, nu creșterea.',unit='%')
    if m==19:
        n=100+20*t;r=F(n)*F(3,10)
        return num('Pondere complementară',f'Din {n} de dosare, 70% sunt complete. Câte sunt incomplete?',r,[F(n)*F(7,10),r+10,r+20],['Procentul incompletelor: 100% − 70% = 30%.',f'Număr: {n} × 0,30 = {fmt(r)}.'],'Folosește complementul dacă se cere categoria rămasă.','Nu calcula categoria menționată în enunț când se cere opusul ei.')
    if m==20:
        price=3+t;r=5*price+12
        return num('Cost fix și variabil',f'Un transport costă 12 lei taxă fixă și {price} lei pentru fiecare colet. Cât costă 5 colete?',r,[5*(price+12),r-12,r+5],[f'Cost variabil: 5 × {price} = {5*price} lei.',f'Adaugă o singură taxă fixă: {5*price} + 12 = {r} lei.'],'Total = cost fix + număr de unități × cost unitar.','Taxa fixă se plătește o dată, nu pentru fiecare colet.',unit='lei')
    if m==21:
        h=8+t;r=3*h
        return num('Scară de hartă',f'Pe o hartă, 1 cm reprezintă 3 km. Două localități sunt la {h} cm. Care este distanța reală?',r,[h,r+3,h*100],[f'Fiecărui centimetru îi corespund 3 km.',f'{h} × 3 = {r} km.'],'Aplică aceeași scară fiecărei unități măsurate.','Nu folosi o conversie cm–km directă; harta are o scară precizată.',unit='km')
    if m==22:
        d=4+t;r=F(2*d,3)
        return num('Productivitate simultană',f'A termină singură o lucrare în {d} zile, B în {2*d} zile. În cât timp o termină împreună, la ritm constant?',r,[d,F(3*d,2),F(d,2)],[f'Ritmuri: 1/{d} și 1/{2*d} din lucrare pe zi.',f'Ritmul comun este 3/{2*d}.',f'Timpul este inversul ritmului: {2*d}/3 = {fmt(r)} zile.'],'Adună ritmurile, apoi inversează pentru durata unei lucrări.','Nu aduna și nu media duratele individuale.',unit='zile')
    if m==23:
        n=1000+100*t;r=F(n)*F(2,5)*F(1,4)
        return num('Procent dintr-o parte',f'Un buget este de {n} lei. 40% se alocă materialelor, iar 25% din suma pentru materiale se folosește pentru hârtie. Cât costă hârtia?',r,[F(n,4),F(n)*F(2,5),r+20],[f'Materiale: {n} × 0,40 = {fmt(F(n)*F(2,5))} lei.',f'Hârtie: {fmt(F(n)*F(2,5))} × 0,25 = {fmt(r)} lei.'],'Citește baza fiecărui procent; al doilea poate viza doar o parte.','25% se aplică bugetului pentru materiale, nu bugetului total.',unit='lei')
    if m==24:
        total=50+10*t;r=total//5
        return num('Fracție și rest',f'Din {total} de cărți, 1/2 sunt romane și 3/10 sunt poezie. Restul sunt eseuri. Câte eseuri sunt?',r,[total//2,3*total//10,r+5],['Partea ocupată: 1/2 + 3/10 = 8/10.','Restul: 1 − 8/10 = 2/10 = 1/5.',f'Număr eseuri: {total} ÷ 5 = {r}.'],'Adună fracțiile folosind un numitor comun, apoi calculează restul.','Fracțiile au aceeași bază: totalul cărților.')
    if m==25:
        speed=60+6*t;r=F(speed,2)
        return num('Unități de timp',f'Un vehicul merge cu {speed} km/h. Ce distanță parcurge în 30 de minute?',r,[speed,speed*30,r+15],['30 de minute = 1/2 oră.',f'Distanța: {speed} × 1/2 = {fmt(r)} km.'],'Convertește minutele în ore înainte să folosești km/h.','Înmulțirea vitezei cu 30 ar trata minutele drept ore.',unit='km')
    if m==26:
        n=4+t;r=F(1,n)
        return num('Probabilitate simplă',f'Într-o urnă sunt {n} bile identice ca formă, numerotate distinct. Una singură este roșie. La extragere aleatoare, probabilitatea unei bile roșii este:',r,[F(2,n),F(1,n+1),F(n-1,n)],['Rezultate favorabile: 1 bilă roșie.',f'Rezultate posibile, echiprobabile: {n}.',f'Probabilitatea: 1/{n}.'],'Probabilitate = cazuri favorabile ÷ cazuri posibile echiprobabile.','Nu calcula probabilitatea bilelor care nu sunt roșii.')
    if m==27:
        a=5+t;b=a+2;r=2*(a+b)
        return num('Perimetru',f'O sală dreptunghiulară are lungimea {b} m și lățimea {a} m. Care este perimetrul?',r,[a*b,a+b,r+2],[f'Sunt două laturi de {b} m și două de {a} m.',f'Perimetru: 2 × ({b} + {a}) = {r} m.'],'Perimetrul este suma lungimilor laturilor.','Lungime × lățime reprezintă aria, nu perimetrul.',unit='m')
    if m==28:
        n=12+t;cap=5;r=math.ceil(n/cap)
        return num('Împărțire cu rotunjire în sus',f'{n} persoane sunt transportate în vehicule cu câte 5 locuri disponibile. Care este numărul minim de vehicule?',r,[r-1,r+1,r+2],[f'Împarte {n} la 5.',f'{r-1} vehicule oferă numai {(r-1)*5} locuri, insuficiente.',f'{r} vehicule oferă {r*5} locuri, suficiente.'],'Când restul reprezintă persoane care trebuie transportate, rotunjește în sus.','O fracție de vehicul nu poate fi folosită pentru persoanele rămase.')
    vals=[10+t,14+t,18+t,22+t,40+t];r=18+t
    return num('Mediană',f'Valorile ordonate sunt {", ".join(map(str,vals))}. Care este mediana?',r,[14+t,F(sum(vals),5),22+t],['Sunt 5 valori deja ordonate.','Poziția centrală este a treia.',f'A treia valoare este {r}.'],'La un număr impar de valori, mediana este valoarea centrală după ordonare.','Mediana nu este neapărat media aritmetică.')

def logic(m,t):
    A,B,C,D=NAMES[t],NAMES[(t+1)%20],NAMES[(t+2)%20],NAMES[(t+3)%20]
    topic=TOPICS[t]
    if m==0:
        return item('logic','Silogism cu excludere',f'Toți coordonatorii atelierului de {topic} sunt profesori. Niciun profesor nu este voluntar în proiectul X. Ce rezultă?',
        ['Niciun coordonator nu este voluntar în proiectul X.','Toți profesorii sunt coordonatori.','Unii coordonatori sunt voluntari în X.','Toți voluntarii în X sunt coordonatori.'],0,
        ['Coordonatori ⊆ profesori.','Profesorii nu au membri comuni cu voluntarii în X.','Nici subcategoria coordonatorilor nu poate avea membri comuni cu voluntarii.','Nu inversa incluziunea: nu toți profesorii trebuie să fie coordonatori.'],'O excludere a unei categorii se aplică și subcategoriilor ei.','Nu deduce existența unor membri dacă premisele nu o garantează.')
    if m==1:
        return item('logic','Modus tollens',f'Dacă dosarul lui {A} este aprobat, atunci este complet. Dosarul nu este complet. Ce rezultă?',
        ['Dosarul nu este aprobat.','Dosarul este aprobat.','Dosarul va fi completat mâine.','Dosarul este complet.'],0,
        ['Notează P = aprobat și Q = complet.','Regula este P → Q.','Avem nu Q. Dacă ar exista P, ar trebui Q, ceea ce contrazice informația.','Rezultă nu P: dosarul nu este aprobat.'],'Din P → Q și nu Q rezultă nu P.','Nu confunda această deducție cu inversarea condiției.')
    if m==2:
        return item('logic','Negarea unui cuantificator',f'Care este negarea exactă a afirmației „Toți evaluatorii atelierului de {topic} au verificat cel puțin un dosar”?',
        ['Cel puțin un evaluator nu a verificat niciun dosar.','Niciun evaluator nu a verificat niciun dosar.','Toți evaluatorii au verificat exact un dosar.','Cel puțin un evaluator a verificat toate dosarele.'],0,
        ['Structura este: pentru fiecare evaluator există un dosar verificat.','Negarea lui pentru fiecare este există cel puțin unul.','Pentru acel evaluator negăm existența unui dosar verificat: nu există niciunul.','Rezultă un evaluator care nu a verificat niciun dosar; nu trebuie să fie toți.'],'La negare, schimbă toți în cel puțin unul și neagă proprietatea.','Niciun evaluator este o afirmație mai puternică decât negarea exactă.')
    if m==3:
        opts=[[A,B,C,D],[D,A,C,B],[D,A,B,C],[D,B,C,A]]
        valid=lambda p:p.index(A)<p.index(B) and p.index(C)==p.index(B)+1 and p.index(D)<p.index(A)
        sol=[p for p in itertools.permutations([A,B,C,D]) if valid(p)];assert len(sol)==1
        return item('logic','Ordonare cu vecinătate',f'{A} prezintă înainte de {B}. {C} prezintă imediat după {B}. {D} prezintă înainte de {A}. Care este ordinea celor patru?', [' → '.join(o) for o in opts],2,
        [f'Pereche obligatorie consecutivă: {B} → {C}.',f'{A} trebuie înaintea perechii.',f'{D} trebuie înaintea lui {A}.',f'Ordinea unică: {D} → {A} → {B} → {C}.'],'Unește întâi blocurile consecutive, apoi aplică relațiile de ordine.','Imediat după este mai restrictiv decât undeva după.',proof=dict(kind='unique',solutions=[list(p) for p in sol],options=opts,result=2))
    if m==4:
        return item('logic','Repartizare imposibilă',f'{A}, {B}, {C} și {D} formează două echipe de câte două persoane. {A} nu poate fi cu {B}, iar {C} trebuie să fie cu {D}. Ce rezultă?',
        ['Nu există o repartizare care respectă toate condițiile.',f'{A} trebuie să fie cu {C}.',f'{B} trebuie să fie cu {D}.','Există două repartizări valide.'],0,
        [f'{C} și {D} ocupă complet prima echipă.',f'Rămân numai {A} și {B} pentru a doua.',f'Dar asocierea {A}–{B} este interzisă.','Cele două condiții, împreună cu mărimea echipelor, sunt incompatibile.'],'Aplică întâi perechea obligatorie și examinează persoanele rămase.','Nu rezolva o condiție ignorând-o pe cealaltă.')
    if m==5:
        pos=14+t;block=['○','△','△','□'];r=block[(pos-1)%4];opts=['○','△','□','Nu se poate determina']
        return item('logic','Bloc de simboluri repetat',f'Blocul ○, △, △, □ se repetă identic. Ce simbol se află pe poziția {pos}?',opts,opts.index(r),
        ['Blocul conține 4 poziții.',f'Împarte {pos} la 4; restul este {pos%4}.','Resturile 1, 2, 3 desemnează pozițiile respective; restul 0 desemnează poziția 4.',f'Simbolul cerut este {r}.'],'Folosește restul împărțirii la lungimea blocului.','La rest 0, poziția este ultima din bloc, nu prima.',proof=dict(kind='symbol',block=block,position=pos,result=r))
    if m==6:
        return item('logic','Modus ponens',f'Dacă {A} finalizează cursul, primește certificatul. {A} a finalizat cursul. Ce rezultă?',
        [f'{A} primește certificatul.',f'{A} nu primește certificatul.','Oricine primește certificatul a finalizat acest curs.','Toți participanții au finalizat cursul.'],0,
        ['Regula are forma P → Q.','Premisa afirmă P: cursul a fost finalizat.','Aplică regula și obține Q: primește certificatul.','Nu extinde informația la toți participanții și nu inversa regula.'],'Din P → Q și P rezultă Q.','Concluzia trebuie să se refere la persoana pentru care avem premisa.')
    if m==7:
        return item('logic','Afirmarea consecventului',f'Dacă {A} este coordonator, are acces la sală. {A} are acces la sală. Ce putem afirma despre statutul său?',
        ['Nu se poate determina dacă este coordonator.','Este obligatoriu coordonator.','Este obligatoriu necoordonator.','Niciun coordonator nu are acces.'],0,
        ['Regula spune că statutul de coordonator este suficient pentru acces.','Nu spune că numai coordonatorii au acces.','Accesul ar putea fi permis și altor persoane.','Din Q și P → Q nu rezultă nici P, nici nu P.'],'O condiție suficientă nu este automat necesară.','Afirmarea rezultatului nu dovedește condiția inițială.')
    if m==8:
        return item('logic','Disjuncție exclusivă',f'{A} participă fie la atelierul de {topic}, fie la cel de teatru, dar nu la ambele. Nu participă la teatru. Ce rezultă?',
        [f'Participă la atelierul de {topic}.','Nu participă la niciun atelier.','Participă la ambele ateliere.','Informația nu permite nicio concluzie.'],0,
        ['Enunțul cere participarea la exact unul dintre două ateliere.','Varianta teatru este eliminată.','Rămâne cealaltă variantă, care trebuie să fie adevărată.','Absența de la ambele ar încălca regula inițială.'],'Dacă exact una dintre două alternative este adevărată, negarea uneia impune cealaltă.','Fie… fie, dar nu ambele este exclusiv, nu facultativ.')
    if m==9:
        return item('logic','Negarea unei conjuncții',f'Care este negarea exactă a enunțului „{A} este prezent și {B} este prezent”?',
        [f'{A} este absent sau {B} este absent, inclusiv posibil amândoi.',f'{A} și {B} sunt amândoi absenți.',f'{A} este prezent sau {B} este prezent.',f'{A} și {B} sunt amândoi prezenți.'],0,
        ['Afirmația inițială cere prezența ambelor persoane.','Este falsă dacă lipsește cel puțin una.','Lipsa ambelor este posibilă, dar nu este obligatorie.','Negarea lui P și Q este nu P sau nu Q, cu sau inclusiv.'],'Legea lui De Morgan: nu(P și Q) = nu P sau nu Q.','Negarea nu impune absența ambelor persoane.')
    if m==10:
        return item('logic','Negarea unei disjuncții',f'Care este negarea exactă a afirmației „{A} participă la {topic} sau la teatru”, unde „sau” permite și participarea la ambele?',
        ['Nu participă nici la primul atelier, nici la teatru.','Participă la ambele.','Participă la primul, dar nu la teatru.','Participă la teatru, dar nu la primul.'],0,
        ['Disjuncția inclusivă este adevărată dacă există cel puțin o participare.','Ca să fie falsă, ambele participări trebuie să lipsească.','Negarea este nu P și nu Q.','Participarea la ambele face enunțul inițial adevărat.'],'Legea lui De Morgan: nu(P sau Q) = nu P și nu Q.','Nu confunda negarea lui sau cu alegerea unei singure alternative.')
    if m==11:
        return item('logic','Negarea unei implicații',f'Care situație face falsă regula „Dacă {A} este înscris, atunci primește materialele”?',
        ['Este înscris și nu primește materialele.','Nu este înscris și primește materialele.','Nu este înscris și nu primește materialele.','Este înscris și primește materialele.'],0,
        ['Regula promite materiale în cazul înscrierii.','Este încălcată numai când înscrierea există, dar materialele lipsesc.','Dacă înscrierea lipsește, regula nu decide distribuirea materialelor.','Situația falsificatoare are forma P și nu Q.'],'O implicație este falsă când antecedentul este adevărat și consecventul fals.','Regula nu spune numai cei înscriși primesc materiale.')
    if m==12:
        return item('logic','Silogism cu existență',f'Unii participanți la {topic} sunt profesori. Toți profesorii din acest grup au ecuson. Ce rezultă?',
        ['Unii participanți au ecuson.','Toți participanții sunt profesori.','Niciun participant nu are ecuson.','Toți cei cu ecuson sunt profesori.'],0,
        ['Unii garantează existența a cel puțin unui participant profesor.','Pentru acea persoană se aplică regula profesor → ecuson.','Există deci cel puțin un participant cu ecuson.','Nu extinde concluzia la toți participanții și nu inversa relația.'],'O existență dintr-o categorie poate fi transmisă către o categorie care o include.','Unii nu înseamnă toți.')
    if m==13:
        return item('logic','Condiții în lanț',f'Dacă {A} este coordonator, este membru al comisiei. Dacă este membru al comisiei, primește invitație. Nu a primit invitație. Ce rezultă?',
        ['Nu este coordonator.','Este coordonator.','Este membru al comisiei.','Toți invitații sunt coordonatori.'],0,
        ['Leagă regulile: coordonator → membru → invitație.','Lipsa invitației exclude statutul de membru.','Lipsa statutului de membru exclude statutul de coordonator.','Concluzia privește persoana menționată, nu toate persoanele invitate.'],'Aplică modus tollens înapoi prin lanțul condițiilor.','Nu porni de la invitație pentru a afirma automat coordonarea.')
    if m==14:
        return item('logic','Exact unul adevărat',f'Despre locul lui {A} în clasament, două afirmații sunt: 1. „Este pe locul 1.” 2. „Este pe locul 1 sau 2.” Exact una este adevărată. Pe ce loc este?',
        ['1','2','3','Nu se poate determina'],1,
        ['Dacă ar fi pe 1, ambele afirmații ar fi adevărate.','Dacă ar fi pe 2, prima ar fi falsă și a doua adevărată.','Pe orice alt loc, ambele ar fi false.','Singura posibilitate cu exact o afirmație adevărată este locul 2.'],'Testează variantele și numără valorile de adevăr.','Exact una elimină atât cazul cu zero, cât și cazul cu două afirmații adevărate.',proof=dict(kind='truth-position',result=2))
    if m==15:
        colors=2+t%4; target=2+t//4; r=colors*(target-1)+1
        return item('logic','Număr minim garantat',f'În sertarul lui {A} sunt șosete de {colors} culori, multe din fiecare culoare. Extragi fără să vezi. Câte trebuie extrase pentru a garanta {target} șosete de aceeași culoare?',
        [str(r-1),str(r),str(r+1),str(r+colors)],1,
        [f'În cel mai nefavorabil caz, extragi {target-1} din fiecare culoare.',f'Astfel poți avea {colors} × {target-1} = {r-1} șosete fără să atingi pragul.',f'Următoarea șosetă ridică una dintre culori la {target}.',f'Minimul garantat este {r}.'],'Principiul cutiei: depășește maximul posibil fără atingerea pragului.','Se cere garanție în cel mai rău caz, nu o posibilitate favorabilă.')
    if m==16:
        return item('logic','Calendar și periodicitate',f'Întâlnirea lui {A} este luni. Următoarea este peste {7+t} zile. Ce zi a săptămânii va fi?',
        ['luni','marți','miercuri','joi'] if t%7<4 else ['vineri','sâmbătă','duminică','luni'],
        t%7 if t%7<4 else t%7-4,
        ['Zilele săptămânii se repetă din 7 în 7.',f'{7+t} împărțit la 7 are restul {t%7}.',f'Avansează de luni cu {t%7} zile.',f'Ziua rezultată este { ["luni","marți","miercuri","joi","vineri","sâmbătă","duminică"][t%7]}.'],'Elimină săptămânile complete și folosește restul.','Peste o zi de luni înseamnă marți; nu număra ziua inițială drept prima zi scursă.')
    if m==17:
        return item('logic','Relație tranzitivă',f'{A} este mai înalt decât {B}. {B} este mai înalt decât {C}. {D} este mai scund decât {C}. Cine este cel mai înalt?',
        [A,B,C,D],0,
        [f'Prima regulă: {A} > {B}.',f'A doua: {B} > {C}.',f'A treia: {C} > {D}.',f'Lanțul este {A} > {B} > {C} > {D}.'],'Transformă comparațiile într-un lanț orientat.','Mai scund decât inversează ordinea față de mai înalt decât.')
    if m==18:
        opts=[[A,B,C,D],[B,A,C,D],[D,C,B,A],[C,A,B,D]]
        return item('logic','Ordine parțială: variantă posibilă',f'{A} trebuie înainte de {C}, iar {B} înainte de {A}. Care ordine respectă ambele reguli?', [' → '.join(o) for o in opts],1,
        [f'Combină regulile: {B} → {A} → {C}.',f'Poziția lui {D} nu este restricționată.',f'Varianta {B} → {A} → {C} → {D} respectă ambele reguli.','Se cere o ordine posibilă dintre variante, nu ordinea unică a tuturor persoanelor.'],'Verifică fiecare regulă în fiecare variantă.','Nu adăuga o condiție pentru persoana despre care enunțul nu spune nimic.')
    if m==19:
        return item('logic','Repartizare pe roluri',f'{A}, {B} și {C} au, fiecare, un rol diferit: moderator, secretar, observator. {A} nu este moderator și nu este secretar. {B} nu este moderator. Cine este moderator?',
        [A,B,C,'Nu se poate determina'],2,
        [f'{A} nu poate avea primele două roluri, deci este observator.',f'{B} nu este moderator și nu mai poate fi observator, deci este secretar.',f'Rolul rămas pentru {C} este moderator.','Verifică: fiecare persoană are un singur rol și toate rolurile sunt diferite.'],'Rezolvă mai întâi persoana cu cele mai multe excluderi.','Nu permite același rol la două persoane când rolurile sunt distincte.')
    if m==20:
        return item('logic','Condiție necesară',f'Accesul lui {A} este permis numai dacă are legitimație. Accesul i-a fost permis. Ce rezultă?',
        ['Are legitimație.','Nu are legitimație.','Oricine are legitimație primește acces.','Legitimația este singura condiție posibilă.'],0,
        ['Numai dacă introduce o condiție necesară.','Acces permis → legitimație.','Premisa confirmă accesul permis.','Aplică regula și deduci legitimația; nu deduci că legitimația singură garantează accesul.'],'În P numai dacă Q, direcția este P → Q.','Necesar nu înseamnă suficient.')
    if m==21:
        return item('logic','Numărare de ordini posibile',f'{A}, {B} și {C} prezintă fiecare o dată. Singura regulă este că {A} trebuie înainte de {B}. Câte ordini sunt posibile?',
        ['1','2','3','6'],2,
        ['Trei persoane pot fi ordonate în 3 × 2 × 1 = 6 moduri.',f'Exact jumătate au {A} înainte de {B}.',f'Ordini valide: {A}–{B}–{C}, {A}–{C}–{B}, {C}–{A}–{B}.','Rezultă 3 ordini.'],'Enumeră sistematic posibilitățile și elimină-le pe cele care încalcă regula.','Nu calcula toate permutările fără să aplici restricția.')
    if m==22:
        return item('logic','Suficiența informației',f'{A}, {B}, {C} au punctaje diferite. Știm numai că {A} are mai mult decât {B} și mai mult decât {C}. Ce se poate determina sigur?',
        [f'{A} are cel mai mare punctaj.',f'{B} are cel mai mic punctaj.',f'{C} are cel mai mic punctaj.',f'{B} are mai mult decât {C}.'],0,
        [f'{A} depășește fiecare dintre celelalte două persoane.','Așadar, maximul este determinat.','Nu avem comparația dintre celelalte două persoane.','Nu putem stabili minimul sau ordinea completă.'],'Separă partea determinată a ordinii de partea încă necunoscută.','Informația suficientă pentru maxim poate fi insuficientă pentru minim.')
    return item('logic','Bicondițional',f'{A} primește ecuson dacă și numai dacă este înscris. Nu a primit ecuson. Ce rezultă?',
      ['Nu este înscris.','Este înscris.','Nu se poate determina înscrierea.','Toți cei înscriși nu primesc ecuson.'],0,
      ['Dacă și numai dacă exprimă două reguli: înscris → ecuson și ecuson → înscris.','Pentru prima regulă avem lipsa consecventului: nu ecuson.','Prin modus tollens rezultă nu înscris.','Concluzia privește persoana dată, nu întregul grup.'],'Bicondiționalul permite ambele direcții ale relației.','Nu trata dacă și numai dacă drept o simplă asociere posibilă.')

TITLES=['Reperele de bază','Sens și proporții','Concluzii și condiții','Date și argumente','Analogie și ordine','Procente și deducții','Text și productivitate','Reguli și comparații','Precizie și repartizare','Sinteză și calcule','Condiții necesare','Grafice, tabele și relații','Argumente și contraexemple','Medii și tipare','Decizii din informații','Quantificatori și ritmuri','Cauze și restricții','Ordine și probabilități','Verificare și inferență','Simulare de sinteză']

ALTERNATIVES={
 'Procente succesive':'Poți gândi în factori: o creștere de 10% înseamnă înmulțire cu 1,10, iar o reducere de 10% înseamnă înmulțire cu 0,90. Produsul lor este 0,99. Așadar, prețul final este 99% din prețul inițial, adică o scădere totală de 1%.',
 'Raport parte–parte':'Metoda segmentelor: desenează mental trei segmente egale pentru fete și două pentru băieți. Întregul conține cinci segmente. Împarte numărul total de elevi la cinci și ia trei asemenea părți pentru fete. Controlul se face adunând fetele și băieții și verificând raportul.',
 'Medie ponderată':'Imaginează-ți că ai scris nota fiecărui elev pe câte un bilețel. Media întregului grup este suma tuturor bilețelelor împărțită la numărul lor. Grupul mai numeros contribuie cu mai multe bilețele, deci are o influență mai mare asupra mediei finale.',
 'Productivitate cu retragere':'Metoda unei lucrări împărțite în unități: alege drept întreg un număr de unități egal cu durata individuală a echipei mai lente. Aceasta face o unitate pe zi, iar echipa mai rapidă face două. Împreună fac trei unități pe zi. Scade ce au făcut împreună, apoi atribuie restul echipei lente.',
 'Productivitate simultană':'Metoda unităților: alege ca volum al lucrării durata echipei mai lente, exprimată în unități. Echipa lentă face o unitate pe zi, iar cealaltă două. Împreună fac trei. Împarte volumul ales la trei pentru a afla durata. Această metodă și metoda fracțiilor dau același rezultat.',
 'Preț inițial':'Regula de trei simplă: prețul final corespunde lui 80%, iar prețul inițial lui 100%. Scrie final / 80 = inițial / 100. Prin înmulțire în cruce, inițial = final × 100 / 80. Verifică aplicând din nou reducerea la prețul inițial obținut.',
 'Procent din întreg':'Regula de trei simplă: întregul corespunde lui 100%, iar partea cerută lui 20%. Înmulțești întregul cu 20 și împarți la 100. Deoarece 20/100 = 1/5, poți folosi și împărțirea directă la cinci.',
 'Proporționalitate inversă':'Metoda om-zile: o zi lucrată de o persoană este o unitate de muncă. Pentru aceeași lucrare, produsul dintre persoane și zile rămâne constant. Întâi calculezi volumul din situația cunoscută, apoi îl împarți la noul număr de lucrători.',
 'Viteză medie dus–întors':'Pentru două distanțe egale poți folosi formula 2 × v₁ × v₂ / (v₁ + v₂). Formula rezultă din distanța totală împărțită la timpul total; nu trebuie aplicată automat când distanțele diferă. Verifică dacă rezultatul se află între cele două viteze.',
 'Sumă și diferență':'Metoda segmentelor: desenează mental două segmente egale, apoi adaugă șase unități unuia dintre ele. Totalul cuprinde două segmente plus șase. Scoți cele șase unități și împarți restul la doi pentru a găsi segmentul mai mic.',
 'Reuniunea a două grupuri':'Metoda mulțimilor: imaginează două cercuri care se suprapun. Zona comună este inclusă în fiecare cerc. Când aduni efectivele, o numeri de două ori. Scazi intersecția o singură dată pentru a rămâne cu fiecare persoană numărată exact o dată.',
 'Negarea unui cuantificator':'Poți testa afirmația cu un contraexemplu. Pentru a respinge „toți au verificat măcar un dosar”, ai nevoie de un singur evaluator care nu a verificat niciunul. Nu ai nevoie ca întregul grup să fi procedat astfel. Negarea exactă este minimul logic care face afirmația inițială falsă.',
 'Modus tollens':'Gândește prin contradicție: presupune că dosarul ar fi aprobat. Regula ar impune să fie complet. Dar știm că este incomplet. Presupunerea duce la o contradicție, deci aprobarea nu poate fi adevărată.',
 'Afirmarea consecventului':'Construiește două scenarii compatibile: persoana este coordonator și are acces; sau persoana nu este coordonator, dar primește acces din alt motiv. Ambele respectă regula dată. Cum există două scenarii cu statut diferit, statutul nu poate fi determinat.',
 'Negarea unei conjuncții':'Verifică cele patru cazuri: ambii prezenți, doar primul prezent, doar al doilea prezent, ambii absenți. Afirmația inițială este adevărată numai în primul caz. Negarea trebuie să acopere celelalte trei, adică absența cel puțin a unei persoane.',
 'Negarea unei disjuncții':'Construiește cazurile: participare la primul, la al doilea, la ambele sau la niciunul. Disjuncția inclusivă este adevărată în primele trei situații. Numai absența ambelor participări o face falsă.',
 'Negarea unei implicații':'Tabelul de adevăr are patru cazuri pentru P și Q. P adevărat și Q adevărat respectă regula; P fals și Q adevărat nu o încalcă; P fals și Q fals nu o încalcă. Numai P adevărat și Q fals o încalcă. Acesta este cazul căutat.',
 'Repartizare pe roluri':'Metoda tabelului: pune persoanele pe rânduri și rolurile pe coloane. Taie celulele interzise. Când pe un rând rămâne un singur rol, îl atribui și îl elimini pentru celelalte persoane. Repetă până când toate rolurile sunt stabilite.',
 'Ordonare cu vecinătate':'Metoda blocurilor: tratează cele două persoane care trebuie să fie consecutive ca pe un singur bloc. Așază celelalte persoane în raport cu blocul, respectând fiecare condiție. La sfârșit, desfă blocul și verifică toate regulile pe ordinea completă.'
}

def original_first(qs):
    qs[0]=item('verbal','Informație explicită','„În semestrul al doilea, biblioteca a prelungit programul în două zile ale săptămânii. Numărul împrumuturilor a crescut față de semestrul întâi. Raportul nu stabilește cauza acestei creșteri.”\nCare afirmație este susținută de text?',
      ['Creșterea împrumuturilor a fost provocată de programul prelungit.','Programul bibliotecii a fost prelungit în fiecare zi.','În semestrul al doilea au fost mai multe împrumuturi.','Toți elevii au împrumutat mai multe cărți.'],2,
      ['Se cere o informație susținută de text, nu o presupunere.','Textul spune explicit că numărul împrumuturilor a crescut.','Raportul nu stabilește cauza, deci nu putem atribui creșterea programului prelungit.','Creșterea totalului nu arată că fiecare elev a împrumutat mai mult; două zile nu înseamnă fiecare zi.'],'Caută dovada exactă în text.','Nu transforma asocierea în cauză și totalul în proprietatea fiecărui elev.',historical=True)
    qs[1]=item('verbal','Informație absentă','„Atelierul de lectură este opțional. Toți elevii înscriși au primit materialele. Unii dintre ei au participat și la întâlnirea de vineri.”\nCare afirmație NU poate fi stabilită din text?',
      ['Elevii înscriși au primit materialele.','Maria a participat la întâlnirea de vineri.','Participarea la atelier este opțională.','Cel puțin un elev înscris a participat vineri.'],1,
      ['Observă NU: se caută o informație pe care nu o avem.','Prima și a treia variantă sunt exprimate direct în text.','Unii implică existența cel puțin a unui participant vineri.','Maria nu este menționată. Nu putem decide dacă a participat sau nu.'],'Informația absentă nu este automat falsă.','Nu alege o afirmație explicită atunci când cerința solicită ce NU se poate stabili.',historical=True)
    qs[2]=verbal(2,0);qs[2]['prompt']='Completează relația: Bibliotecă : cărți = arhivă : …'
    qs[3]=verbal(2,1);qs[3]['prompt']='Completează relația: Termometru : temperatură = cronometru : …'
    qs[4]=item('verbal','Categorie comună','Din lista „autobuz, caiet, tramvai, creion, bibliotecă, profesor”, care pereche este formată din două mijloace de transport?',
      ['Autobuz și tramvai','Bibliotecă și profesor','Caiet și creion','Tramvai și bibliotecă'],0,
      ['Se cere o categorie precisă: mijloace de transport.','Autobuzul și tramvaiul transportă persoane.','Caietul și creionul au o categorie comună, dar sunt rechizite.','În celelalte perechi nu există două mijloace de transport.'],'Categoria cerută trebuie să includă ambii termeni.','O pereche cu o altă categorie comună nu răspunde cerinței.',historical=True)
    qs[5]['prompt']='În enunțul „Datele preliminare vor fi verificate înaintea raportului final”, cuvântul „preliminare” înseamnă:'
    qs[7]=item('numeric','Totaluri în tabel','Cărți împrumutate (clasa A / clasa B):\nLuni: 24 / 18\nMarți: 19 / 27\nMiercuri: 31 / 16\nJoi: 22 / 20\nÎn ce zi este cel mai mare total?',
      ['Luni','Marți','Miercuri','Joi'],2,['Luni: 24 + 18 = 42.','Marți: 19 + 27 = 46.','Miercuri: 31 + 16 = 47. Joi: 22 + 20 = 42.','Maximul este 47, corespunzător zilei de miercuri.'],'Calculează totalurile pe rânduri, apoi compară.','Nu compara doar una dintre clase.',proof=dict(kind='maximum',values=[42,46,47,42],result=2),historical=True)
    qs[8]=num('Tarif pe unitate','Distanțe parcurse:\nLuni: Ana — 120 km; Bogdan — 80 km.\nMarți: Ana — 150 km; Bogdan — 110 km.\nFiecare primește 0,50 lei/km. Cu câți lei este mai mare suma totală primită de Ana?',40,[20,30,80],
      ['Ana: 120 + 150 = 270 km.','Bogdan: 80 + 110 = 190 km.','Diferența: 270 − 190 = 80 km.','Diferența de plată: 80 × 0,50 = 40 lei.'],'Adună ambele zile pentru fiecare persoană, apoi aplică tariful.','20 lei este diferența unei singure zile; 80 este diferența în kilometri.',unit='lei')
    qs[15]['prompt']='Dacă dosarul lui Radu este aprobat, atunci este complet. Dosarul lui Radu nu este complet. Ce rezultă obligatoriu?'
    qs[16]['prompt']='Care este negarea exactă a afirmației „Toți evaluatorii au verificat cel puțin un dosar”?'
    return qs

def rotate(q,t,i):
    offset=(t*3+i)%4
    q['options']=q['options'][offset:]+q['options'][:offset]
    q['correct']=(q['correct']-offset)%4
    if q.get('proof') and q['proof']['kind']=='numeric':
        q['proof']['options']=q['proof']['options'][offset:]+q['proof']['options'][:offset]
    q['id']=f't{t+1:02}-q{i+1:02}'
    return q

def build():
    manifest=[];seen=set();models=set()
    for t in range(20):
        # Combinațiile de subtipuri variază, nu doar valorile din aceeași machetă.
        vs=list(range(7)) if t==0 else [(t*5+j*2+j//3)%21 for j in range(7)]
        ns=list(range(7)) if t==0 else [(t*7+j*4)%30 for j in range(7)]
        ls=list(range(6)) if t==0 else [(t*5+j*3)%24 for j in range(6)]
        qs=[verbal(m,t) for m in vs]+[numeric(m,t) for m in ns]+[logic(m,t) for m in ls]
        if t==0:qs=original_first(qs)
        assert len(qs)==20
        for i,q in enumerate(qs):
            q['solution']['alternative']=ALTERNATIVES.get(q['model'],'')
            if q['model']=='Totaluri în tabel' and t>0:
                q['chart']={'title':'Împrumuturi pe zile — clasele A și B împreună','labels':['Luni','Marți','Miercuri','Joi'],'values':q['proof']['values']}
            rotate(q,t,i)
            assert q['prompt'] not in seen, ('duplicate',t,q['prompt'])
            seen.add(q['prompt']);models.add(q['model'])
        test=dict(id=t+1,title=TITLES[t],durationSeconds=3600,questions=qs)
        (ROOT/'tests'/f'test-{t+1:02}.json').write_text(json.dumps(test,ensure_ascii=False,indent=2)+'\n')
        manifest.append(dict(id=t+1,title=TITLES[t],file=f'tests/test-{t+1:02}.json',models=list(dict.fromkeys(q['model'] for q in qs))))
    (ROOT/'tests'/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(seen)} itemi unici; {len(models)} familii; 20 teste generate.')
if __name__=='__main__':build()
