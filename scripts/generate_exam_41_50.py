"""Simulări originale 41–50: structură 7/7/6, dificultate moderată."""
import json, itertools, subprocess
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]

# Pentru fiecare text: informație explicită, contradicție, informație absentă, idee principală.
TEXTS=[
('Biblioteca deschisă', 'Biblioteca școlii a prelungit programul în zilele de marți și joi. Modificarea a fost solicitată de elevii care participă la activități după ore. Împrumutul cărților a rămas gratuit. Numărul vizitelor a crescut în prima lună, dar raportul nu arată dacă elevii au citit mai multe cărți.',
 ('Când a fost prelungit programul?', 'Marți și joi', ['În fiecare zi','Luni și miercuri','Numai vineri'], 'Prima propoziție numește explicit cele două zile: marți și joi.'),
 ('Care afirmație contrazice textul?', 'Împrumutul cărților a devenit contra cost', ['Elevii au cerut modificarea programului','Numărul vizitelor a crescut','Programul a fost prelungit în două zile'], 'Textul spune că împrumutul a rămas gratuit; plata împrumutului ar contrazice această informație.'),
 ('Ce informație nu poate fi stabilită din text?', 'Dacă elevii au citit mai multe cărți', ['Cine a solicitat schimbarea','Dacă împrumutul a rămas gratuit','În ce zile s-a prelungit programul'], 'Raportul nu măsoară numărul cărților citite. Mai multe vizite nu înseamnă automat mai multe cărți citite.'),
 ('Care este rezumatul fidel?', 'Programul bibliotecii a fost adaptat, iar vizitele au crescut', ['Biblioteca a introdus taxe pentru toate serviciile','Lectura tuturor elevilor s-a dublat după schimbare','Programul bibliotecii a fost redus la cererea elevilor'], 'Textul descrie adaptarea programului și creșterea vizitelor; nu confirmă un efect asupra lecturii.')),
('Atelierul de robotică', 'Atelierul de robotică primește elevi de clasa a IX-a și a X-a. Experiența anterioară nu este obligatorie. La prima întâlnire, participanții lucrează în perechi și testează senzori. Construirea unui robot complet este planificată pentru finalul semestrului. Textul nu precizează costurile materialelor.',
 ('Cine poate participa la atelier?', 'Elevii de clasa a IX-a și a X-a', ['Doar elevii de clasa a XII-a','Doar elevii cu experiență anterioară','Numai profesorii de informatică'], 'Prima propoziție indică cele două clase eligibile.'),
 ('Care afirmație este infirmată de text?', 'Experiența anterioară este obligatorie', ['La prima întâlnire se testează senzori','Participanții lucrează în perechi','Robotul complet este planificat pentru finalul semestrului'], 'Enunțul spune expres că experiența anterioară nu este obligatorie.'),
 ('La ce întrebare nu oferă textul un răspuns?', 'Cât costă materialele', ['Când este planificat robotul complet','Cum lucrează participanții la prima întâlnire','Dacă experiența anterioară este obligatorie'], 'Costurile materialelor nu sunt precizate; celelalte trei informații sunt menționate.'),
 ('Care formulare surprinde ideea principală?', 'Atelierul oferă o pregătire treptată, inclusiv elevilor fără experiență', ['Atelierul admite exclusiv specialiști în robotică','Participanții construiesc un robot complet la prima întâlnire','Toți elevii școlii participă obligatoriu la atelier'], 'Sunt acceptați începători, prima activitate este limitată, iar produsul complet este prevăzut ulterior.')),
('Expoziția de fotografie', 'Expoziția cuprinde fotografii realizate de elevi în timpul unor plimbări prin oraș. Organizatorii au selectat lucrările după claritatea imaginii și relevanța temei, fără să ia în calcul prețul aparatului. Accesul publicului este gratuit. Nu este menționat numărul vizitatorilor.',
 ('Ce criterii au fost folosite pentru selecție?', 'Claritatea imaginii și relevanța temei', ['Prețul aparatului și vârsta elevului','Popularitatea autorului și numărul vizitatorilor','Viteza realizării și dimensiunea aparatului'], 'Textul numește două criterii, claritatea și relevanța, și exclude prețul aparatului.'),
 ('Care afirmație contrazice fragmentul?', 'Prețul aparatului a fost criteriu de selecție', ['Accesul publicului este gratuit','Fotografiile au fost realizate de elevi','Lucrările au fost realizate în oraș'], 'Organizatorii nu au luat în calcul prețul aparatului; varianta afirmă exact contrariul.'),
 ('Ce nu putem afla din fragment?', 'Câți vizitatori a avut expoziția', ['Cine a realizat fotografiile','Dacă accesul publicului este gratuit','După ce criterii s-au selectat lucrările'], 'Numărul vizitatorilor lipsește din fragment.'),
 ('Care este ideea centrală?', 'Expoziția valorifică fotografii ale elevilor, selectate după calitatea și tema lucrării', ['Expoziția compară prețurile aparatelor elevilor','Expoziția este rezervată exclusiv fotografilor profesioniști','Expoziția impune o taxă tuturor vizitatorilor'], 'Rezumatul păstrează autorii și criteriile selecției, fără să introducă informații noi.')),
('Mișcare după ore', 'Clubul sportiv organizează două antrenamente pe săptămână pentru elevii înscriși. În zilele ploioase, activitățile se desfășoară în sală. Participarea la un turneu este opțională și necesită o înscriere separată. Textul nu precizează câți elevi s-au înscris la turneu.',
 ('Ce se întâmplă în zilele ploioase?', 'Activitățile se desfășoară în sală', ['Antrenamentele sunt anulate întotdeauna','Elevii sunt înscriși automat la turneu','Numărul antrenamentelor se dublează'], 'Textul indică sala drept loc alternativ în zilele ploioase.'),
 ('Care afirmație este contrară textului?', 'Participarea la turneu este obligatorie', ['Clubul organizează două antrenamente pe săptămână','Înscrierea la turneu se face separat','Pe ploaie, activitățile se desfășoară în sală'], 'Participarea la turneu este opțională, deci nu obligatorie.'),
 ('Ce informație lipsește?', 'Numărul elevilor înscriși la turneu', ['Caracterul opțional al turneului','Locul activităților în zilele ploioase','Numărul antrenamentelor săptămânale'], 'Nu există o valoare pentru numărul elevilor înscriși la turneu.'),
 ('Care este rezumatul potrivit?', 'Clubul oferă antrenamente regulate și participare opțională la turneu', ['Clubul anulează toate activitățile când plouă','Fiecare elev înscris la club participă obligatoriu la turneu','Turneul înlocuiește toate antrenamentele săptămânale'], 'Sunt păstrate cele două aspecte principale: antrenamentele regulate și opțiunea distinctă pentru turneu.')),
('Colectarea selectivă', 'În curtea școlii au fost amplasate recipiente separate pentru hârtie și plastic. Elevii voluntari explică modul de utilizare. După o lună, cantitatea de hârtie colectată separat a crescut. Raportul nu stabilește dacă volumul total al deșeurilor școlii a scăzut.',
 ('Ce rol au elevii voluntari?', 'Explică modul de utilizare a recipientelor', ['Calculează prețul tuturor materialelor','Înlocuiesc toate recipientele zilnic','Interzic folosirea hârtiei în școală'], 'A doua propoziție precizează explicit rolul voluntarilor.'),
 ('Care afirmație contrazice textul?', 'Hârtia și plasticul sunt colectate în același recipient', ['Cantitatea de hârtie colectată separat a crescut','Elevii voluntari oferă explicații','Recipientele au fost amplasate în curte'], 'Textul menționează recipiente separate, nu un singur recipient comun.'),
 ('Ce concluzie nu este justificată de raport?', 'Volumul total al deșeurilor a scăzut', ['Hârtia colectată separat a crescut','Sunt recipiente pentru hârtie și plastic','Voluntarii explică utilizarea recipientelor'], 'Creșterea colectării separate nu demonstrează reducerea cantității totale de deșeuri.'),
 ('Care este ideea principală?', 'Colectarea separată este sprijinită prin recipiente și explicații ale voluntarilor', ['Colectarea separată a eliminat complet toate deșeurile','Școala a renunțat definitiv la utilizarea plasticului','Voluntarii au interzis accesul elevilor în curte'], 'Rezumatul descrie măsurile concrete și nu transformă un rezultat limitat într-o afirmație absolută.')),
('Programul de mentorat', 'Fiecare profesor debutant din program este sprijinit de un mentor. Întâlnirile au loc bilunar și pot fi individuale sau de grup. Participanții discută situații de la clasă, fără a publica numele elevilor. Raportul nu compară rezultatele acestui program cu cele ale altor programe.',
 ('Ce se discută la întâlniri?', 'Situații de la clasă', ['Datele bancare ale elevilor','Exclusiv rezultatele altor programe','Numai prețul materialelor didactice'], 'Textul indică situațiile de la clasă drept obiect al discuțiilor.'),
 ('Care afirmație este infirmată de fragment?', 'Numele elevilor sunt publicate în cadrul discuțiilor', ['Fiecare debutant din program are un mentor','Întâlnirile pot fi individuale','Sunt posibile întâlniri de grup'], 'Fragmentul precizează că numele elevilor nu sunt publicate.'),
 ('Ce nu se poate stabili din raport?', 'Dacă programul este mai eficient decât alte programe', ['Cine este sprijinit de mentori','Dacă întâlnirile pot fi de grup','Dacă se publică numele elevilor'], 'Nu există o comparație cu alte programe; superioritatea eficienței nu poate fi dedusă.'),
 ('Care este rezumatul fidel?', 'Programul sprijină debutanții prin întâlniri de mentorat care protejează identitatea elevilor', ['Programul demonstrează că toate celelalte programe sunt inutile','Programul publică numele elevilor pentru fiecare situație','Programul sprijină exclusiv profesorii cu vechime mare'], 'Sunt păstrate beneficiarii, forma de sprijin și protejarea identității.')),
('Revista elevilor', 'Revista școlii apare trimestrial. Articolele sunt redactate de elevi și revizuite de o echipă editorială înainte de publicare. Autorii pot propune subiecte noi, dar fiecare text trebuie să respecte limita de spațiu. Fragmentul nu precizează tirajul revistei.',
 ('Ce se întâmplă înainte de publicare?', 'Articolele sunt revizuite de echipa editorială', ['Autorii sunt obligați să cumpere revista','Revista se distribuie zilnic','Toate propunerile sunt respinse automat'], 'Revizuirea este etapa explicit menționată înainte de publicare.'),
 ('Care afirmație contrazice textul?', 'Revista apare în fiecare săptămână', ['Autorii pot propune subiecte noi','Elevii redactează articolele','Textele trebuie să respecte limita de spațiu'], 'Trimestrial înseamnă o dată la trei luni, nu săptămânal.'),
 ('Ce informație nu este oferită?', 'Numărul exemplarelor tipărite', ['Cine redactează articolele','Dacă autorii pot propune subiecte','Existența limitei de spațiu'], 'Tirajul reprezintă numărul exemplarelor, iar acesta nu este precizat.'),
 ('Care este ideea centrală?', 'Revista publică articole ale elevilor, după revizuire și cu respectarea limitei de spațiu', ['Articolele sunt publicate fără nicio verificare','Revista exclude orice propunere nouă de subiect','Revista publică exclusiv texte ale profesorilor'], 'Rezumatul combină corect autorii și condițiile de publicare.')),
('Laboratorul renovat', 'După renovare, laboratorul poate fi rezervat de profesorii școlii printr-un calendar comun. Rezervarea trebuie făcută cu cel puțin o zi înainte. Echipamentele portabile pot fi folosite și în alte săli, cu acordul responsabilului. Textul nu indică valoarea investiției.',
 ('Cu cât timp înainte trebuie făcută rezervarea?', 'Cu cel puțin o zi înainte', ['Cu exact o lună înainte','Doar după folosirea laboratorului','Fără niciun termen'], 'Expresia cel puțin stabilește un minim de o zi, nu un termen exact unic.'),
 ('Care afirmație este contrară textului?', 'Echipamentele portabile nu pot fi folosite niciodată în alte săli', ['Este folosit un calendar comun','Profesorii școlii pot rezerva laboratorul','Utilizarea în alte săli cere acordul responsabilului'], 'Textul permite folosirea în alte săli, dacă există acordul responsabilului.'),
 ('Ce nu poate fi aflat din fragment?', 'Valoarea investiției în renovare', ['Cine poate rezerva laboratorul','Condiția folosirii echipamentelor în alte săli','Termenul minim al rezervării'], 'Costul renovării nu este indicat.'),
 ('Care rezumat păstrează sensul?', 'Folosirea laboratorului și a echipamentelor este organizată prin rezervări și acorduri', ['Laboratorul este rezervat exclusiv responsabilului','Renovarea a eliminat orice regulă de utilizare','Toate echipamentele trebuie să rămână permanent în laborator'], 'Regulile de rezervare și de utilizare a echipamentelor formează tema comună a textului.')),
('Clubul de lectură', 'Clubul de lectură se întâlnește lunar. Membrii aleg cartea următoare prin vot, dintre trei propuneri. La discuții pot participa și elevii care nu au terminat lectura. Organizatorii recomandă lectura integrală, dar nu o impun ca regulă de acces. Textul nu arată care carte a obținut cele mai multe voturi.',
 ('Cum este aleasă cartea următoare?', 'Prin vot, dintre trei propuneri', ['Exclusiv prin tragere la sorți','Numai de către bibliotecar','Prin alegerea obligatorie a celei mai lungi cărți'], 'Procesul de selecție este descris explicit: vot între trei propuneri.'),
 ('Care afirmație contrazice fragmentul?', 'Doar elevii care au terminat lectura pot participa', ['Clubul se întâlnește lunar','Lectura integrală este recomandată','Membrii votează cartea următoare'], 'Fragmentul permite participarea celor care nu au terminat lectura.'),
 ('Ce informație nu poate fi stabilită?', 'Titlul cărții care a primit cele mai multe voturi', ['Dacă întâlnirile sunt lunare','Dacă lectura integrală este obligatorie pentru acces','Numărul propunerilor supuse votului'], 'Nu este indicat rezultatul votului și nici titlul cărții câștigătoare.'),
 ('Care este ideea principală?', 'Clubul organizează discuții accesibile și alegerea participativă a lecturilor', ['Clubul exclude toți elevii care nu termină cartea','Organizatorii interzic lectura integrală','Toate cărțile sunt impuse fără consultarea membrilor'], 'Accesul la discuții și votul membrilor susțin ambele componente ale rezumatului.')),
('Grădina școlii', 'Elevii au amenajat o grădină cu plante aromatice și flori. Echipele udă plantele prin rotație, iar în zilele cu ploaie suficientă udarea este suspendată. Observațiile despre creștere sunt notate săptămânal. Nu sunt oferite date despre recolta finală.',
 ('Cum este organizată udarea?', 'Prin rotația echipelor', ['Doar de o singură echipă permanentă','Exclusiv în zilele cu ploaie suficientă','Fără implicarea elevilor'], 'Textul indică rotația echipelor drept regulă de organizare.'),
 ('Care afirmație este contrară textului?', 'Udarea continuă obligatoriu și când plouă suficient', ['Grădina cuprinde flori','Observațiile sunt notate săptămânal','Sunt cultivate plante aromatice'], 'În zilele cu ploaie suficientă udarea este suspendată, deci nu continuă obligatoriu.'),
 ('Ce informație lipsește din fragment?', 'Cantitatea recoltei finale', ['Frecvența notării observațiilor','Prezența florilor în grădină','Regula aplicată când plouă suficient'], 'Nu sunt oferite date privind recolta; nu putem inventa o cantitate.'),
 ('Care este rezumatul fidel?', 'Elevii îngrijesc organizat grădina și înregistrează periodic observații', ['Elevii au abandonat grădina după prima ploaie','Observațiile sunt făcute doar la recolta finală','Plantele sunt udate fără a ține cont de ploaie'], 'Rezumatul păstrează îngrijirea organizată, adaptarea la ploaie și observațiile periodice.')),
]
ANALOGIES=[
('termometru','temperatură','barometru','presiune atmosferică',['direcție','masă','viteză'],'instrument → mărimea măsurată'),
('pictor','tablou','compozitor','melodie',['atelier','pensulă','public'],'creator → produsul creației'),
('pagină','carte','treaptă','scară',['balustradă','etaj','ușă'],'parte → întreg'),
('cheie','încuietoare','parolă','cont',['document','ecran','tastatură'],'mijloc de acces → sistem protejat'),
('medic','spital','bibliotecar','bibliotecă',['carte','cititor','raft'],'profesie → loc de muncă tipic'),
('foarfecă','tăiere','ac','coasere',['desenare','măsurare','ștergere'],'instrument → acțiune'),
('hartă','teritoriu','portret','persoană',['culoare','ramă','tablou'],'reprezentare → ceea ce reprezintă'),
('minut','oră','lună','an',['calendar','săptămână','zi'],'unitate temporală → unitate mai mare care o include'),
('sămânță','plantă','ou','pui',['cuib','pană','sol'],'stadiu inițial → organism rezultat'),
('ceas','timp','odometru','distanță',['masă','temperatură','volum'],'instrument → mărimea măsurată'),
]
CATEGORIES=[
('busolă și termometru','instrumente de măsurare',['alimente','mijloace de transport','piese de mobilier']),
('vioară și flaut','instrumente muzicale',['aparate de iluminat','materiale de construcție','unelte agricole']),
('stejar și fag','arbori',['animale','metale','obiecte de mobilier']),
('triunghi și pătrat','poligoane',['corpuri geometrice','instrumente muzicale','unități de timp']),
('fier și cupru','metale',['combustibili','materiale textile','plante']),
('roman și nuvelă','specii literare epice',['instrumente optice','unități de lungime','vehicule']),
('autobuz și tramvai','mijloace de transport',['aparate de măsurare','produse alimentare','unelte de scris']),
('măr și pară','fructe',['cereale','legume rădăcinoase','metale']),
('litru și mililitru','unități de volum',['unități de lungime','unități de masă','unități de timp']),
('dicționar și enciclopedie','lucrări de referință',['instrumente de laborator','mijloace de transport','specii de arbori']),
]
WORDS=[
('Rezultatul este provizoriu până la verificarea documentelor','provizoriu','temporar',['definitiv','eronat','obligatoriu']),
('Procedura este transparentă: criteriile sunt publicate și explicate','transparentă','deschisă și ușor de verificat',['imposibil de înțeles','secretă','schimbată zilnic']),
('Raportul este concis: prezintă esențialul în puține cuvinte','concis','scurt și concentrat',['ambiguu','foarte lung','incomplet în mod necesar']),
('Cele două măsuri sunt complementare și se susțin reciproc','complementare','care se completează reciproc',['care se exclud obligatoriu','identice în toate privințele','lipsite de legătură']),
('Echipa a fost prudentă și a verificat riscurile înainte să decidă','prudentă','atentă la riscuri',['grăbită','indiferentă','neinformată']),
('O eroare minoră nu schimbă concluzia principală a raportului','minoră','de mică importanță',['decisivă','intenționată','inevitabilă']),
('Planul este fezabil cu resursele și timpul disponibile','fezabil','posibil de realizat',['deja realizat','imposibil','obligatoriu']),
('Răspunsul este explicit: nu lasă concluzia doar să fie dedusă','explicit','exprimat clar și direct',['ascuns','contradictoriu','nesigur']),
('Programul este flexibil și permite ajustări ale orelor','flexibil','adaptabil',['fix și imposibil de modificat','nefuncțional','obligatoriu']),
('Dovezile sunt relevante pentru întrebarea investigată','relevante','legate de problema analizată',['contrare în mod necesar','insuficiente în orice situație','lipsite de legătură']),
]

def item(cat,model,prompt,answer,wrong,steps,rule,trap,alternative='',proof=None,chart=None,table=None):
    options=[answer]+wrong
    assert len(set(options))==4,(model,options)
    q=dict(category=cat,model=model,prompt=prompt,options=options,correct=0,
           solution=dict(steps=steps,rule=rule,trap=trap,alternative=alternative),hint='',proof=proof,historical=False)
    if chart:q['chart']=chart
    if table:q['solution']['truthTable']=table
    return q

def verbal(k):
    title,text,*tasks=TEXTS[k];qs=[]
    models=['Informație explicită din text','Afirmație contrazisă de text','Informație care lipsește','Ideea principală a textului']
    for j,(question,answer,wrong,reason) in enumerate(tasks):
        qs.append(item('verbal',models[j],f'Citește fragmentul și răspunde numai pe baza lui:\n\n{text}\n\n{question}',answer,wrong,
          ['Identificăm cerința: '+question,'Separăm ceea ce textul afirmă de ceea ce doar am putea presupune.',reason,
           'Recitim cele patru variante. Alegem singura formulare care răspunde cerinței fără să adauge sau să inverseze informații.'],
          'Pentru întrebările despre text, folosește exclusiv informațiile din fragment.',
          'O presupunere plauzibilă nu devine informație confirmată. Recomandat nu înseamnă obligatoriu, iar lipsa informației nu înseamnă că afirmația este falsă.'))
    a,b,c,d,wrong,relation=ANALOGIES[k]
    qs.append(item('verbal','Analogie verbală',f'Completează analogia, păstrând același tip de relație: {a} → {b}; {c} → … .',d,wrong,
       [f'Citind prima pereche, identificăm relația: {relation}.',f'Aplicăm aceeași relație termenului „{c}”.',f'Termenul care păstrează relația este „{d}”.','Nu alegem un cuvânt doar pentru că este asociat temei; trebuie să îndeplinească același rol ca al doilea termen din prima pereche.'],
       'La analogii, păstrează atât relația, cât și direcția ei.','Asocierea obișnuită dintre două cuvinte nu este suficientă dacă tipul relației diferă.'))
    pair,answer,wrong=CATEGORIES[k]
    qs.append(item('verbal','Categorie comună',f'Care este categoria comună cea mai potrivită pentru {pair}?',answer,wrong,
       [f'Analizăm ambele elemente ale perechii: {pair}.','Căutăm o categorie care se aplică fiecăruia, nu doar unuia dintre ele.',f'Ambele aparțin categoriei „{answer}”.','Celelalte variante nu includ corect ambele elemente.'],
       'Categoria comună trebuie să cuprindă ambele elemente.','Nu confunda o utilizare accidentală sau o asociere cu apartenența la o categorie.'))
    sentence,word,answer,wrong=WORDS[k]
    qs.append(item('verbal','Sensul unui cuvânt în context',f'„{sentence}.” Ce sens are aici cuvântul „{word}”?',answer,wrong,
      ['Citirea propoziției întregi arată contextul în care este folosit cuvântul.',f'În acest context, „{word}” înseamnă „{answer}”.',f'Înlocuim mental cuvântul cu „{answer}” și verificăm dacă sensul propoziției se păstrează.','Respingem variantele care schimbă sensul sau introduc o condiție suplimentară.'],
      'Sensul cerut este cel din propoziție, nu orice sens posibil al cuvântului.','Un sinonim aparent apropiat poate adăuga o idee care nu există în enunț.'))
    return qs

def fmt(x):
    x=F(x)
    if x.denominator==1:return str(x.numerator)
    if 1000%x.denominator==0:return ('%.3f'%float(x)).rstrip('0').rstrip('.').replace('.',',')
    return f'{x.numerator}/{x.denominator}'

def numeric(k):
    qs=[]
    def add(model,prompt,result,wrongs,unit,steps,rule,trap,alternative='',kind=None,chart=None):
        r=F(result);wrong=list(map(F,wrongs));assert r not in wrong and len(set(wrong))==3
        proof=dict(kind='exam-numeric',operation=kind,result=str(r),options=[str(r)]+[str(x) for x in wrong])
        qs.append(item('numeric',model,prompt,fmt(r)+unit,[fmt(x)+unit for x in wrong],steps+[f'Răspunsul cerut este {fmt(r)}{unit}.'],rule,trap,alternative,proof,chart))
    # Două întrebări din tabele, în forma exemplelor publice din 2021.
    a=[120+13*k,90+7*k,150+11*k,110+5*k];b=[80+6*k,180+9*k,130+8*k,90+4*k]
    names=['Luni','Marți','Miercuri','Joi'];totals=[x+y for x,y in zip(a,b)];i=totals.index(max(totals));assert totals.count(max(totals))==1
    table='\n'.join(f'{day}: echipa A — {x} km; echipa B — {y} km.' for day,x,y in zip(names,a,b))
    qs.append(item('numeric','Compararea totalurilor din tabel',f'Tabelul arată distanțele parcurse în patru zile, în săptămâna {k+1}:\n{table}\nÎn ce zi au parcurs cele două echipe împreună distanța cea mai mare?',names[i],[n for n in names if n!=names[i]],
      ['Cerința „împreună” ne cere să adunăm distanțele celor două echipe pentru fiecare zi.']+[f'{n}: {x} + {y} = {z} km.' for n,x,y,z in zip(names,a,b,totals)]+[f'Comparăm totalurile: maximul este {max(totals)} km, în ziua de {names[i].lower()}.'],
      'Pentru un total comun, adună valorile din același rând, apoi compară totalurile.','Cea mai mare valoare pentru o singură echipă nu garantează cel mai mare total.',proof={'kind':'exam-maximum','values':totals,'days':names},chart={'title':'Total zilnic, în km','labels':names,'values':totals}))
    x=240+20*k;y=160+10*k;rate=F(1,2);result=(x-y)*rate
    add('Diferență de sume din tabel',f'Într-o deplasare, echipa A parcurge {x} km, iar echipa B parcurge {y} km. Ambele primesc 0,50 lei pentru fiecare kilometru. Cu câți lei primește echipa A mai mult decât echipa B?',result,[x-y,(x+y)*rate,x*rate],' lei',
        [f'Distanța suplimentară este {x} − {y} = {x-y} km.',f'Fiecare kilometru suplimentar aduce 0,50 lei: {x-y} × 0,50 = {fmt(result)} lei.',f'Control: A primește {fmt(x*rate)} lei, B primește {fmt(y*rate)} lei; diferența este {fmt(result)} lei.'],
        'La același tarif, diferența de sume este diferența de distanțe înmulțită cu tariful.','Se cere diferența dintre sume, nu suma totală încasată de echipa A.',kind='payment')
    total=200+20*k;p=[15,20,25,30,40,15,20,25,30,40][k];r=F(total*p,100)
    if k%2==0:
        add('Procent dintr-un total',f'Din {total} de participanți la o activitate, {p}% aleg atelierul de fotografie. Câți participanți aleg acest atelier?',r,[total-r,r+10,r-10],' participanți',
           [f'Întregul este {total} de participanți și corespunde lui 100%.',f'1% reprezintă {total} ÷ 100 = {fmt(F(total,100))} participanți.',f'{p}% reprezintă {fmt(F(total,100))} × {p} = {fmt(r)} participanți.'],
           'Partea = întregul × procentul ÷ 100.','Nu calcula procentul din partea rămasă; baza procentului este totalul inițial.',f'Regula de trei simplă: 100% → {total}; {p}% → x. Atunci x = {total} × {p} ÷ 100 = {fmt(r)}.',kind='percent')
    else:
        price=400+40*k;disc=20;final=price*F(4,5)
        add('Preț înainte de reducere',f'După o reducere de {disc}%, un aparat costă {fmt(final)} lei. Cât costa înainte de reducere?',price,[final,final*F(6,5),price+40],' lei',
          [f'După reducere rămâne 100% − {disc}% = 80% din prețul inițial.',f'Cei {fmt(final)} lei reprezintă 80%, deci 1% reprezintă {fmt(final)} ÷ 80 = {fmt(final/80)} lei.',f'Prețul inițial: {fmt(final/80)} × 100 = {price} lei.',f'Control: reducerea este {fmt(price*F(1,5))} lei, iar {price} − {fmt(price*F(1,5))} = {fmt(final)} lei.'],
          'Preț inițial = preț redus ÷ procentul rămas exprimat ca fracție.','Adăugarea a 20% din prețul redus folosește altă bază și nu anulează reducerea.',kind='original-price')
    unit=8+2*k;total=5*unit;r=3*unit
    add('Împărțire în raport',f'Într-un grup de {total} de elevi, raportul dintre fete și băieți este 3 : 2. Câte fete sunt?',r,[2*unit,r+unit,total],' fete',
        ['Trei părți reprezintă fetele, iar două părți băieții: în total sunt 3 + 2 = 5 părți egale.',f'O parte are {total} ÷ 5 = {unit} elevi.',f'Fetele au trei părți: 3 × {unit} = {r}.',f'Control: băieții sunt {2*unit}; totalul este {r} + {2*unit} = {total}.'],
        'Adună părțile raportului, află o parte, apoi ia numărul de părți cerut.','Raportul 3 : 2 nu înseamnă că fetele reprezintă 3/2 din întreg.',
        f'Metoda segmentelor: întregul este alcătuit din cinci segmente egale. Trei sunt pentru fete și două pentru băieți. Fiecare segment reprezintă {unit} elevi, deci cele trei segmente reprezintă {r} fete.',kind='ratio')
    avg=14+k;v1=avg-3;v2=avg+1;r=3*avg-v1-v2
    add('Valoare lipsă din medie',f'Media aritmetică a trei rezultate este {avg}. Primele două rezultate sunt {v1} și {v2}. Care este al treilea rezultat?',r,[avg,r+3,r-3],'',
        [f'Media este suma împărțită la 3. Prin urmare, suma rezultatelor este 3 × {avg} = {3*avg}.',f'Primele două rezultate au suma {v1} + {v2} = {v1+v2}.',f'Al treilea rezultat este {3*avg} − {v1+v2} = {r}.',f'Control: ({v1} + {v2} + {r}) ÷ 3 = {avg}.'],
        'Suma valorilor = media × numărul valorilor.','Media nu este automat valoarea lipsă.',kind='missing-average')
    if k%3==0:
        n=4+k;cost=15*n;target=n+3;r=15*target
        add('Cost proporțional',f'{n} caiete identice costă {cost} lei. La același preț pe caiet, cât costă {target} caiete?',r,[cost,r+15,r-15],' lei',
           [f'Prețul unui caiet este {cost} ÷ {n} = 15 lei.',f'Pentru {target} caiete plătim {target} × 15 = {r} lei.','Mai multe caiete la același preț unitar înseamnă un cost total proporțional mai mare.'],
           'Află prețul unei unități, apoi înmulțește cu numărul unităților cerute.','Nu păstra costul total inițial când se schimbă numărul de caiete.',f'Regula de trei simplă: {n} caiete → {cost} lei; {target} caiete → x lei. x = {cost} × {target} ÷ {n} = {r}.',kind='direct')
    elif k%3==1:
        workers=4+k;days=12;more=2*workers;r=6
        add('Durată și număr de lucrători',f'{workers} lucrători termină o lucrare în {days} zile. În câte zile o termină {more} lucrători, dacă au aceeași productivitate, lucrează simultan și nu se încurcă reciproc?',r,[3,12,24],' zile',
           [f'Volumul lucrării este {workers} × {days} = {workers*days} zile de muncă ale unui lucrător.',f'Împărțim volumul la {more} lucrători: {workers*days} ÷ {more} = 6 zile.',f'Control: {more} × 6 = {workers*days}, același volum de muncă.'],
           'Pentru aceeași lucrare, număr de lucrători × durată este constant.','Dublarea numărului de lucrători înjumătățește timpul, nu îl dublează.', 'Metodă rapidă: numărul lucrătorilor s-a dublat, deci timpul scade de două ori: 12 ÷ 2 = 6 zile.',kind='inverse')
    else:
        total=66+4*k;diff=10;r=(total-diff)//2
        add('Sumă și diferență',f'Două cutii conțin împreună {total} de creioane. Prima cutie are cu {diff} creioane mai mult decât a doua. Câte creioane are a doua cutie?',r,[r+diff,total//2,total-diff],' creioane',
           [f'Scoatem din total surplusul de {diff} creioane al primei cutii: {total} − {diff} = {total-diff}.',f'Acum cele două părți sunt egale, deci a doua cutie are {total-diff} ÷ 2 = {r} creioane.',f'Prima are {r} + {diff} = {r+diff}; controlul sumei: {r} + {r+diff} = {total}.'],
           'Cantitatea mai mică = (suma − diferența) ÷ 2.','Împărțirea directă a totalului la 2 ar ignora diferența.',f'Metoda segmentelor: desenează două segmente egale și adaugă la primul un segment de {diff}. După eliminarea surplusului, cele două segmente egale au împreună {total-diff} creioane.',kind='sum-difference')
    if k%2==0:
        n=96+12*k;a=F(1,3);b=F(1,4);r=F(n)*(1-a-b)
        add('Fracții și rest',f'Dintr-un stoc de {n} de dosare, se verifică dimineața 1/3 din stocul inițial și după-amiaza încă 1/4 din același stoc inițial. Câte dosare rămân neverificate?',r,[F(n,3),F(n,4),F(n)*F(7,12)],' dosare',
          [f'Dimineața se verifică {n} ÷ 3 = {n//3} dosare.',f'După-amiaza se verifică {n} ÷ 4 = {n//4} dosare. Ambele fracții au aceeași bază: stocul inițial.',f'În total sunt verificate {n//3} + {n//4} = {n*7//12} dosare.',f'Rămân {n} − {n*7//12} = {fmt(r)} dosare.'],
          'Când fracțiile se referă la același întreg, le aduni și scazi rezultatul din 1.','Nu aplica a doua fracție restului; enunțul precizează același stoc inițial.',f'Metoda fracțiilor: 1 − 1/3 − 1/4 = 12/12 − 4/12 − 3/12 = 5/12. Restul este {n} × 5/12 = {fmt(r)} dosare.',kind='fraction-rest')
    else:
        seats=30;people=121+10*k;r=(people+seats-1)//seats
        add('Număr minim de vehicule',f'Pentru {people} de persoane se folosesc microbuze cu câte {seats} de locuri pentru pasageri. Care este numărul minim de microbuze, dacă fiecare persoană trebuie să aibă loc?',r,[r-1,r+1,r+2],' microbuze',
          [f'Cu {r-1} microbuze avem {(r-1)*seats} locuri, mai puține decât {people}.',f'Cu {r} microbuze avem {r*seats} locuri, suficiente pentru toate persoanele.','Dacă împărțirea nu este exactă, este necesar încă un vehicul pentru persoanele rămase.'],
          'Numărul minim de vehicule este câtul împărțirii rotunjit în sus.','Nu rotunji la numărul întreg cel mai apropiat; chiar și o singură persoană rămasă cere un loc suplimentar.',kind='ceiling')
    return qs

NAMES=['Ana','Bogdan','Carla','Dorin','Elena','Filip','Gabriela','Horia','Irina','Lucian']
def logic(k):
    name=NAMES[k];title=TEXTS[k][0].lower();qs=[]
    def add(model,prompt,answer,wrong,steps,rule,trap,alternative='',proof=None,table=None):
        qs.append(item('logic',model,prompt,answer,wrong,steps,rule,trap,alternative,proof,table=table))
    if k%2==0:
        add('Regulă condițională aplicată',f'În activitatea „{title}”, orice persoană înscrisă primește un ecuson. {name} este înscrisă în activitate. Ce rezultă cu certitudine?',f'{name} primește un ecuson',[f'{name} nu primește ecuson','Nicio persoană nu primește ecuson','Toate persoanele cu ecuson sunt înscrise'],
          ['Notăm P = persoana este înscrisă și Q = persoana primește ecuson.','Regula spune: dacă P, atunci Q.',f'Despre {name} știm că P este adevărat. Aplicăm regula și obținem Q.',f'Prin urmare, {name} primește ecuson. Regula nu afirmă și direcția inversă.'],
          'Din P → Q și P rezultă Q.','Nu transforma o regulă într-o echivalență: primirea ecusonului nu dovedește, singură, înscrierea.',proof={'kind':'exam-logic','operation':'modus-ponens','result':True})
    else:
        add('Regulă condițională și absența consecinței',f'În activitatea „{title}”, orice persoană înscrisă primește un ecuson. {name} nu primește ecuson. Dacă regula este respectată, ce rezultă?',f'{name} nu este înscris în activitate',[f'{name} este înscris în activitate','Nimeni nu este înscris în activitate','Nu se poate stabili nimic despre înscriere'],
          ['Notăm P = înscris și Q = primește ecuson. Regula este P → Q.',f'Dacă {name} ar fi înscris, ar trebui să primească ecuson.',f'Dar {name} nu primește ecuson. Ipoteza înscrierii ar contrazice regula.',f'Rezultă că {name} nu este înscris în activitate. Nu tragem o concluzie despre toate persoanele.'],
          'Din P → Q și nu Q rezultă nu P.','Concluzia privește persoana dată, nu întregul grup.',proof={'kind':'exam-logic','operation':'modus-tollens','result':False})
    table={'headers':['P: document complet','Q: document acceptat','Regula P → Q'],'rows':[['Adevărat','Adevărat','Adevărată'],['Adevărat','Fals','Falsă'],['Fals','Adevărat','Adevărată'],['Fals','Fals','Adevărată']]}
    add('Situația care încalcă o regulă',f'Pentru înscrierea la „{title}” se aplică regula: „Dacă documentul este complet, atunci este acceptat.” Care situație încalcă regula?',
        'Documentul este complet și nu este acceptat',['Documentul este complet și este acceptat','Documentul nu este complet și este acceptat','Documentul nu este complet și nu este acceptat'],
        ['Separăm condiția P: documentul este complet, de consecința Q: documentul este acceptat.','Regula promite acceptarea atunci când documentul este complet.','Pentru a încălca această promisiune, documentul trebuie să fie complet, dar să nu fie acceptat.','Dacă documentul nu este complet, regula nu precizează dacă va fi acceptat. Nu putem adăuga condiția „numai documentele complete sunt acceptate”.','În tabel, doar rândul P adevărat, Q fals face regula falsă.'],
        'O regulă „Dacă P, atunci Q” este falsă numai în situația P și nu Q.','Nu confunda „dacă este complet, este acceptat” cu „este acceptat numai dacă este complet”.',
        'Metoda promisiunii: ți se promite acceptarea documentului complet. Prezinți un document complet, dar el este respins. Tocmai acest caz dovedește încălcarea regulii.',proof={'kind':'exam-logic','operation':'implication-counterexample','result':[True,False]},table=table)
    if k%2==0:
        add('Negarea afirmației universale',f'Care este negarea exactă a afirmației „Toți participanții la activitatea «{title}» au trimis formularul”?',
          'Cel puțin un participant nu a trimis formularul',['Cel puțin un participant a trimis formularul','Niciun participant nu a trimis formularul','Toți participanții au trimis două formulare'],
          ['Afirmația inițială atribuie aceeași proprietate tuturor participanților.','Pentru a o face falsă, este suficient un singur participant fără această proprietate.','Negăm „toți” prin „cel puțin unul” și negăm „a trimis” prin „nu a trimis”.','Nu este necesar ca nimeni să nu fi trimis; afirmația „niciunul” ar spune mult mai mult.'],
          'Negarea lui „Toți au P” este „Cel puțin unul nu are P”.','Nu înlocui „toți” cu „niciunul”: sunt afirmații contrare, nu negații exacte.',proof={'kind':'exam-logic','operation':'not-all','result':True})
    else:
        add('Negarea afirmației existențiale',f'Care este negarea exactă a afirmației „Cel puțin un participant la «{title}» a sosit înainte de ora 9”?',
          'Niciun participant nu a sosit înainte de ora 9',['Cel puțin un participant a sosit după ora 9','Toți participanții au sosit exact la ora 9','Toți participanții au sosit înainte de ora 9'],
          ['Afirmația inițială cere existența măcar a unei persoane care a sosit înainte de ora 9.','Negarea trebuie să excludă orice persoană cu această proprietate.','Prin urmare, nimeni nu a sosit înainte de ora 9.','Nu rezultă că toți au sosit exact la 9; sunt posibile și sosiri mai târzii.'],
          'Negarea lui „Există cel puțin unul cu P” este „Nu există niciunul cu P”.','Un participant sosit mai târziu nu exclude existența altuia sosit înainte de ora 9.',proof={'kind':'exam-logic','operation':'not-exists','result':True})
    # Ordonare: numai o variantă respectă toate condițiile.
    names=[f'Echipa {chr(65+k)}',f'Echipa {chr(66+k)}',f'Echipa {chr(67+k)}',f'Echipa {chr(68+k)}'];a,b,c,d=names
    answer=' → '.join([a,b,c,d]);wrong=[' → '.join(v) for v in ([b,a,c,d],[a,c,b,d],[a,b,d,c])]
    add('Ordonare după condiții',f'La prezentările pentru „{title}”, cele patru echipe au poziții distincte. {a} prezintă înaintea echipei {b.split()[-1]}; {b} înaintea echipei {c.split()[-1]}; {c} înaintea echipei {d.split()[-1]}. Care este ordinea de la prima la ultima?',answer,wrong,
       [f'Din prima condiție avem {a} înainte de {b}.',f'Adăugăm a doua condiție: {a} → {b} → {c}.',f'A treia condiție așază {d} după {c}, deci ordinea completă este {answer}.','Verificăm toate cele trei condiții în ordinea aleasă. Celelalte variante inversează cel puțin o pereche obligatorie.'],
       'Relațiile „înainte de” se pot lega într-un lanț.','Nu ordona după alfabet doar din obișnuință; verifică fiecare condiție.',proof={'kind':'exam-order','names':names,'edges':[[a,b],[b,c],[c,d]],'result':names})
    if k%3==0:
        add('Deducție între categorii',f'Toți voluntarii proiectului „{title}” au instruire. Nicio persoană cu instruire nu lucrează fără supraveghere. Ce rezultă cu certitudine?',
          'Niciun voluntar al proiectului nu lucrează fără supraveghere',['Orice persoană supravegheată este voluntar','Toate persoanele cu instruire sunt voluntari','Toți voluntarii lucrează fără supraveghere'],
          ['Notăm V = voluntari, I = persoane cu instruire și F = persoane care lucrează fără supraveghere.','Prima premisă spune că V este inclus în I.','A doua spune că I și F nu au membri comuni.','Fiind în I, voluntarii nu pot fi în F. Rezultă că niciun voluntar nu lucrează fără supraveghere.'],
          'Dacă A este inclus în B, iar B nu se intersectează cu C, nici A nu se intersectează cu C.','Incluziunea nu permite inversarea: toate persoanele cu instruire nu sunt neapărat voluntari.',
          'Metoda mulțimilor: imaginează cercul voluntarilor în interiorul cercului celor instruiți. Cercul celor care lucrează fără supraveghere este separat de cercul instruirii; este deci separat și de voluntari.',proof={'kind':'exam-logic','operation':'exclusion','result':True})
    elif k%3==1:
        add('Alegere exclusivă',f'La „{title}”, {name} alege exact unul dintre două roluri: organizator sau fotograf. Nu alege rolul de fotograf. Ce rezultă?',
          'Alege rolul de organizator',['Alege ambele roluri','Nu alege niciun rol','Nu se poate determina rolul ales'],
          ['Expresia „exact unul” cere un rol și interzice alegerea ambelor.','Rolul de fotograf este exclus de a doua informație.','Rămâne rolul de organizator, care trebuie ales.','A nu alege niciunul ar încălca cerința „exact unul”.'],
          'Dacă trebuie aleasă exact una dintre două posibilități, eliminarea uneia impune cealaltă.','„Exact unul” nu permite nici zero alegeri, nici două.',proof={'kind':'exam-logic','operation':'xor','result':True},
          table={'headers':['Organizator','Fotograf','Exact un rol ales'],'rows':[['Da','Da','Nu'],['Da','Nu','Da'],['Nu','Da','Da'],['Nu','Nu','Nu']]})
    else:
        add('Condiție necesară',f'La „{title}”, accesul în sala tehnică este permis numai persoanelor cu autorizație. {name} are acces permis. Ce rezultă?',
          f'{name} are autorizație',[f'{name} nu are autorizație','Oricine are autorizație are automat acces permis','Nicio persoană nu are autorizație'],
          ['Cuvântul „numai” stabilește o condiție necesară: acces permis → autorizație.',f'Despre {name} știm că are acces permis.','Aplicăm regula în direcția ei și obținem existența autorizației.','Nu rezultă automat accesul pentru orice persoană autorizată: pot exista și alte condiții.'],
          '„P numai dacă Q” înseamnă P → Q.','Nu inversa relația: condiția necesară nu este automat suficientă.',proof={'kind':'exam-logic','operation':'necessary','result':True})
    if k%2==0:
        start=2+k;step=3+k;values=[start+i*step for i in range(5)];r=start+5*step
        add('Șir cu regulă precizată',f'În codul pentru „{title}”, fiecare termen se obține adunând aceeași valoare la termenul precedent. Șirul începe: '+', '.join(map(str,values))+'. Care este termenul următor?',str(r),[str(r-step),str(r+step),str(r+1)],
          [f'Diferența dintre primii doi termeni este {values[1]} − {values[0]} = {step}.',f'Verificăm diferențele următoare: toate sunt {step}.',f'Adunăm aceeași valoare la ultimul termen: {values[-1]} + {step} = {r}.','Enunțul precizează regula, deci nu căutăm alte tipare posibile.'],
          'La un șir cu diferență constantă, termenul următor este ultimul termen plus diferența.','Nu aduna poziția termenului; adună diferența dintre termeni.',proof={'kind':'exam-sequence','values':values,'result':r})
    else:
        block=['○','△','□'];pos=17+2*k;answer=block[(pos-1)%3]
        add('Bloc repetat de simboluri',f'Etichetele activității „{title}” repetă identic blocul ○, △, □. Pozițiile sunt numărate de la 1. Ce simbol este pe poziția {pos}?',answer,[x for x in block if x!=answer]+['Nu se poate determina'],
          ['Blocul are trei poziții: 1 = ○, 2 = △, 3 = □.',f'Împărțim {pos} la 3: câtul este {pos//3}, restul este {pos%3}.','Restul 1 indică primul simbol, restul 2 al doilea, iar restul 0 ultimul simbol.',f'Pentru poziția cerută rezultă simbolul {answer}.'],
          'Folosește restul împărțirii poziției la lungimea blocului.','Restul 0 indică ultima poziție a blocului, nu o poziție inexistentă.',proof={'kind':'exam-symbol','block':block,'position':pos,'result':answer})
    return qs

tests=[]
for k in range(10):
    # Ordini diferite în interiorul celor trei secțiuni, păstrând distribuția.
    def rotate(a,n):return a[n%len(a):]+a[:n%len(a)]
    qs=rotate(verbal(k),k)+rotate(numeric(k),2*k)+rotate(logic(k),k)
    assert len(qs)==20
    for i,q in enumerate(qs):q['id']=f't{k+41}-q{i+1:02d}'
    tests.append(dict(id=41+k,title=TEXTS[k][0]+' · simulare de examen',durationSeconds=3600,questions=qs))
sorter="""let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{
const tests=JSON.parse(s);const collator=new Intl.Collator('ro',{sensitivity:'base',numeric:false});
for(const t of tests)for(const q of t.questions){
 const rows=q.options.map((o,i)=>({text:o.replace(/[.!?]+$/,'')+'.',old:i}));
 rows.sort((a,b)=>collator.compare(a.text,b.text));
 q.correct=rows.findIndex(r=>r.old===q.correct);q.options=rows.map(r=>r.text);
 if(q.proof?.options)q.proof.options=rows.map(r=>q.proof.options[r.old]);
}
process.stdout.write(JSON.stringify(tests));});"""
tests=json.loads(subprocess.run(['node','-e',sorter],input=json.dumps(tests),text=True,capture_output=True,check=True).stdout)
(ROOT/'tests/exam-41-50.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2)+'\n')
print('Generate: 10 teste, 200 itemi originali, 7 verbali + 7 numerici + 6 logici.')
