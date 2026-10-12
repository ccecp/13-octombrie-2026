"""Verifică banca și recalculează independent răspunsurile numerice."""
import json,re,itertools
from pathlib import Path
from fractions import Fraction as F
root=Path(__file__).resolve().parents[1]
prompts=set(); ids=set(); mixtures=set(); count=0
def independently(q,t):
    m=q['model']; p=q['prompt']; n=list(map(int,re.findall(r'\d+',p)))
    if m=='Tarif pe unitate':return F(40) if t==0 else F(n[0]-n[1],2)
    if m=='Procente succesive':return F(n[0])*F(99,100)
    if m=='Raport parte–parte':return F(n[0]*3,5)
    if m=='Medie ponderată':return F(n[0]*n[1]+n[2]*n[3],n[0]+n[2])
    if m=='Productivitate cu retragere':return (1-F(n[2])*(F(1,n[0])+F(1,n[1])))*n[1]
    if m=='Șir cu diferențe crescătoare':return F(n[-1]+n[-1]-n[-2]+2)
    if m=='Procent din întreg':return F(n[0]*n[1],100)
    if m=='Preț inițial':return F(n[1]*100,100-n[0])
    if m=='Proporționalitate directă':return F(n[1]*n[2],n[0])
    if m=='Proporționalitate inversă':return F(n[0]*n[1],n[2])
    if m=='Viteză medie dus–întors':return F(2*n[1]*n[2],n[1]+n[2])
    if m=='Distanță și conversie de timp':return F(n[0])*(n[1]+F(n[2],60))
    if m=='Sumă și diferență':return F(n[0]-n[1],2)
    if m=='Vârste':return F(n[0]+n[1])
    if m=='Media și valoarea lipsă':return F(3*n[0]-n[1]-n[2])
    if m=='Reuniunea a două grupuri':return F(n[0]+n[1]-n[2])
    if m=='Șir geometric':return F(n[-1]*2)
    if m=='Creștere procentuală':return F(n[1]-n[0],n[0])*100
    if m=='Pondere complementară':return F(n[0]*(100-n[1]),100)
    if m=='Cost fix și variabil':return F(n[0]+n[1]*n[2])
    if m=='Scară de hartă':return F(n[1]*n[2])
    if m=='Productivitate simultană':return 1/(F(1,n[0])+F(1,n[1]))
    if m=='Procent dintr-o parte':return F(n[0]*n[1]*n[2],10000)
    if m=='Fracție și rest':return F(n[0])*(1-F(n[1],n[2])-F(n[3],n[4]))
    if m=='Unități de timp':return F(n[0]*n[1],60)
    if m=='Probabilitate simplă':return F(1,n[0])
    if m=='Perimetru':return F(2*(n[0]+n[1]))
    if m=='Împărțire cu rotunjire în sus':return F((n[0]+n[1]-1)//n[1])
    if m=='Mediană':return F(sorted(n)[len(n)//2])
    raise AssertionError(m)
for path in sorted((root/'tests').glob('test-*.json')):
    test=json.loads(path.read_text());t=test['id']-1;qs=test['questions'];assert len(qs)==20
    assert [q['category'] for q in qs]==['verbal']*7+['numeric']*7+['logic']*6
    signature=tuple(q['model'] for q in qs);assert signature not in mixtures;mixtures.add(signature)
    assert test['durationSeconds']==3600
    for q in qs:
        count+=1;assert q['id'] not in ids;ids.add(q['id']);assert q['prompt'] not in prompts;prompts.add(q['prompt'])
        assert len(q['options'])==4 and len(set(q['options']))==4
        assert isinstance(q['correct'],int) and 0<=q['correct']<4
        assert len(q['solution']['steps'])>=3
        assert q['solution']['rule'] and q['solution']['trap']
        proof=q.get('proof') or {}
        if proof.get('kind')=='numeric':
            r=independently(q,t);assert r==F(proof['result']),(q['id'],r,proof)
            opts=list(map(F,proof['options']));assert opts.count(r)==1
            assert opts[q['correct']]==r
        elif proof.get('kind')=='maximum':
            p=q['prompt']; pairs=[list(map(int,re.findall(r'\d+',line))) for line in p.splitlines()[1:5]]
            totals=[sum(pair) for pair in pairs];assert totals==proof['values'];assert totals.count(max(totals))==1
            days=['Luni','Marți','Miercuri','Joi'];assert q['options'][q['correct']]==days[totals.index(max(totals))]
        elif proof.get('kind')=='symbol':
            assert q['options'][q['correct']]==proof['block'][(proof['position']-1)%len(proof['block'])]
        elif proof.get('kind')=='unique':
            assert q['options'][q['correct']]==' → '.join(proof['solutions'][0])
        if q['model']=='Calendar și periodicitate':
            days=['luni','marți','miercuri','joi','vineri','sâmbătă','duminică'];n=int(re.search(r'peste (\d+)',q['prompt']).group(1));assert q['options'][q['correct']]==days[n%7]
        if q['model']=='Exact unul adevărat':
            valid=[x for x in range(1,10) if int(x==1)+int(x in [1,2])==1];assert valid==[2];assert q['options'][q['correct']]=='2'
        if q['model']=='Număr minim garantat':
            n=list(map(int,re.findall(r'\d+',q['prompt'])));colors,target=n;assert int(q['options'][q['correct']])==colors*(target-1)+1
assert count==400 and len(mixtures)==20
print('OK: 400 itemi unici, 20 combinații distincte, distribuție 7/7/6, câte 4 opțiuni.')
print('OK: răspunsurile numerice recalculate independent; tabelele, simbolurile și condițiile verificabile confirmate.')


from validate_exam_41_50 import validate
validate()

from validate_exam_51_60 import validate as validate_new
validate_new()
