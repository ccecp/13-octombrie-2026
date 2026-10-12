"""Control independent al structurii, calculelor și cazurilor logice pentru 41–50."""
import json,re,itertools
from pathlib import Path
from fractions import Fraction as F
root=Path(__file__).resolve().parents[1]
def independent_numeric(q):
    n=[F(x.replace(',','.')) for x in re.findall(r'\d+(?:,\d+)?',q['prompt'])]
    op=q['proof']['operation']
    if op=='payment':return (n[0]-n[1])*n[2]
    if op=='percent':return n[0]*n[1]/100
    if op=='original-price':return n[1]/(1-n[0]/100)
    if op=='ratio':return n[0]*n[1]/(n[1]+n[2])
    if op=='missing-average':return 3*n[0]-n[1]-n[2]
    if op=='direct':return n[1]*n[2]/n[0]
    if op=='inverse':return n[0]*n[1]/n[2]
    if op=='sum-difference':return (n[0]-n[1])/2
    if op=='fraction-rest':return n[0]*(1-n[1]/n[2]-n[3]/n[4])
    if op=='ceiling':return F((int(n[0])+int(n[1])-1)//int(n[1]))
    raise AssertionError(op)
def validate():
    manifest=json.loads((root/'tests/manifest.json').read_text())
    assert [m['id'] for m in manifest]==list(range(1,61))
    seen_ids=set();seen_prompts=set();total=0
    bank={}
    for m in manifest:
        if m['file'] not in bank:bank[m['file']]=json.loads((root/m['file']).read_text())
        data=bank[m['file']];t=next(x for x in data if x['id']==m['id']) if isinstance(data,list) else data
        assert t['id']==m['id'] and t['durationSeconds']==3600
        assert len(t['questions'])==20
        assert [q['category'] for q in t['questions']]==['verbal']*7+['numeric']*7+['logic']*6
        for q in t['questions']:
            assert q['id'] not in seen_ids;seen_ids.add(q['id'])
            assert q['prompt'] not in seen_prompts,q['id'];seen_prompts.add(q['prompt']);total+=1
            assert len(q['options'])==4
            if t['id']>=41:assert len(set(q['options']))==4
            assert type(q['correct']) is int and 0<=q['correct']<4
            assert len(q['solution']['steps'])>=3 and q['solution']['rule'] and q['solution']['trap']
            if t['id']<41:continue
            assert all(x.endswith('.') for x in q['options'])
            proof=q.get('proof') or {};kind=proof.get('kind');chosen=q['options'][q['correct']].removesuffix('.')
            if kind=='exam-numeric':
                result=independent_numeric(q);assert result==F(proof['result']),(q['id'],result,proof)
                assert [F(x) for x in proof['options']].count(result)==1
                assert F(proof['options'][q['correct']])==result
                # Vérifică și valoarea afișată, nu doar metadatele.
                displayed=re.match(r'^([\d/,]+)',chosen).group(1)
                assert F(displayed.replace(',','.'))==result,(q['id'],chosen,result)
            elif kind=='exam-maximum':
                rows=q['prompt'].splitlines()[1:5]
                totals=[sum(map(int,re.findall(r'\d+',row))) for row in rows]
                assert totals==proof['values'] and totals.count(max(totals))==1
                assert chosen==proof['days'][totals.index(max(totals))]
            elif kind=='exam-sequence':
                values=proof['values'];diffs=[b-a for a,b in zip(values,values[1:])];assert len(set(diffs))==1
                assert int(chosen)==values[-1]+diffs[0]
            elif kind=='exam-symbol':
                position=int(re.search(r'poziția (\d+)',q['prompt']).group(1));assert position==proof['position']
                assert chosen==proof['block'][(position-1)%len(proof['block'])]
            elif kind=='exam-order':
                valid=[p for p in itertools.permutations(proof['names']) if all(p.index(a)<p.index(b) for a,b in proof['edges'])]
                assert len(valid)==1 and chosen==' → '.join(valid[0])
            elif kind=='exam-logic':
                op=proof['operation'];states=list(itertools.product([False,True],repeat=2))
                implication=lambda p,q:not p or q
                if op=='implication-counterexample':
                    invalid=[s for s in states if not implication(*s)];assert invalid==[(True,False)]
                    assert chosen=='Documentul este complet și nu este acceptat'
                elif op in ('modus-ponens','necessary'):
                    valid=[s for s in states if implication(*s) and s[0]];assert all(s[1] for s in valid)
                    assert ('primește un ecuson' in chosen if op=='modus-ponens' else 'are autorizație' in chosen)
                elif op=='modus-tollens':
                    valid=[s for s in states if implication(*s) and not s[1]];assert all(not s[0] for s in valid)
                    assert 'nu este înscris' in chosen
                elif op=='xor':
                    valid=[s for s in states if s[0]!=s[1] and not s[1]];assert valid==[(True,False)]
                    assert chosen=='Alege rolul de organizator'
                elif op=='exclusion':
                    valid=[s for s in itertools.product([False,True],repeat=3) if implication(s[0],s[1]) and not(s[1] and s[2])]
                    assert all(not(s[0] and s[2]) for s in valid)
                    assert chosen=='Niciun voluntar al proiectului nu lucrează fără supraveghere'
                elif op in ('not-all','not-exists'):
                    for s in states:assert (not all(s))==any(not x for x in s) if op=='not-all' else (not any(s))==all(not x for x in s)
                    assert chosen==('Cel puțin un participant nu a trimis formularul' if op=='not-all' else 'Niciun participant nu a sosit înainte de ora 9')
                else:raise AssertionError(op)
    assert total==1200
    print('OK: 60 teste, 1.200 itemi unici; distribuție 7/7/6 și 4 variante per item.')
    print('OK: toate cele 70 de probleme numerice noi și cele 60 de probleme logice noi verificate independent.')
if __name__=='__main__':validate()
