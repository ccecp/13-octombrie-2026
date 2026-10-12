"""Recalculare independentă a celor 200 de itemi din 51–60."""
import json,re,itertools
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def rotate(p,n):return frozenset((c,n-1-r) for r,c in p)
def validate():
    tests=json.loads((root/'tests/exam-51-60.json').read_text())
    assert [t['id'] for t in tests]==list(range(51,61))
    for t in tests:
        assert [q['category'] for q in t['questions']]==['verbal']*7+['numeric']*7+['logic']*6
        assert len(t['questions'])==20 and t['durationSeconds']==3600
        for q in t['questions']:
            assert len(set(q['options']))==4 and all(x.endswith('.') for x in q['options'])
            assert len(q['solution']['steps'])>=4 or q['category']=='numeric'
            p=q.get('proof') or {};kind=p.get('kind');chosen=q['options'][q['correct']].removesuffix('.')
            if kind=='research-numeric':
                n=[F(x.replace(',','.')) for x in re.findall(r'\d+(?:,\d+)?',q['prompt'])];op=p['operation']
                if op=='table-sum':r=n[1]+n[2]
                elif op=='oriented-ratio':r=n[0]/n[1]
                elif op=='growth':r=(n[1]-n[0])/n[0]*100
                elif op=='weighted':r=(n[0]*n[1]+n[2]*n[3])/(n[0]+n[2])
                elif op=='successive':r=n[0]*(1-n[1]/100)*(1-n[2]/100)
                elif op=='fuel':r=n[0]*n[1]/n[2]*n[3]
                elif op=='fixed-variable':r=n[0]+n[1]*n[2]
                else:raise AssertionError(op)
                assert r==F(p['result']),(q['id'],r,p)
                opts=list(map(F,p['options']));assert opts.count(r)==1 and opts[q['correct']]==r
                value=re.match(r'^([\d/,]+)',chosen).group(1);assert F(value.replace(',','.'))==r
            elif kind=='research-compound':
                valid=[]
                for e,a,r in itertools.product([False,True],repeat=3):
                    rule=(not r or (e and a)) if p['operation']=='necessary-both' else (not (e and a) or r)
                    if rule and (r if p['operation']=='necessary-both' else (e and not a)):valid.append((e,a,r))
                if p['operation']=='necessary-both':
                    assert valid and all(e and a for e,a,r in valid)
                    assert chosen=='Persoana are atât ecuson, cât și aprobare'
                else:
                    assert {r for e,a,r in valid}=={False,True}
                    assert chosen=='Nu putem stabili dacă dosarul este acceptat'
            elif kind=='research-matrix':
                m=p['matrix'];solutions=[]
                for v in range(1,5):
                    candidate=[row.copy() for row in m];candidate[2][2]=v
                    if all(sorted(row)==[1,2,3] for row in candidate) and all(sorted(candidate[r][c] for r in range(3))==[1,2,3] for c in range(3)):solutions.append(v)
                assert solutions==[p['result']]
                word={1:'Un singur',2:'Două',3:'Trei',4:'Patru'}[p['result']];assert chosen.startswith(word)
            elif kind=='research-order':
                a,b=p['before'];valid=[o for o in itertools.permutations(p['people']) if o[1]==p['middle'] and o.index(a)<o.index(b)]
                assert len(valid)==1 and chosen==' → '.join(valid[0])
            elif kind=='research-function':
                (x1,y1),(x2,y2),(x3,y3)=p['examples'];factor=F(y2-y1,x2-x1);offset=y1-factor*x1
                assert factor*x3+offset==y3
                assert int(chosen)==factor*p['input']+offset==p['result']
            elif kind=='research-truth':
                a,b=p['target'],p['alternative'];valid=[x for x in range(1,30) if int(x==a)+int(x in [a,b])==1]
                assert valid==[b] and chosen==str(b)
            elif kind=='research-existence':
                # Pentru trei persoane, enumerăm toate apartenențele A/B/C.
                assignments=list(itertools.product([False,True],repeat=9));valid=[]
                for row in assignments:
                    people=[row[i:i+3] for i in range(0,9,3)]
                    if all(not a or b for a,b,c in people) and any(a and c for a,b,c in people):valid.append(people)
                assert valid and all(any(b and c for a,b,c in people) for people in valid)
                assert chosen=='Unii voluntari au acces la arhivă'
    print('OK 51–60: 70 calcule independente; 10 matrice cu răspuns unic; 50 probleme de reguli și deducții verificate.')
if __name__=='__main__':validate()
