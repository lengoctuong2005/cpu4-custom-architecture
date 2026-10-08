"""Learning-only C/V arithmetic oracle; V is not a CPU4 architectural flag."""
import json
from pathlib import Path
s=lambda x:x if x<8 else x-16
ops=checks=0
for a in range(16):
 for b in range(16):
  for op in ('ADD','SUB'):
   value=a+b if op=='ADD' else a-b
   signed=s(a)+s(b) if op=='ADD' else s(a)-s(b)
   r=value&15; a3=a>>3; b3=b>>3; n=r>>3; z=int(r==0)
   v=((1^(a3^b3))&(a3^n)) if op=='ADD' else ((a3^b3)&(a3^n))
   assert v==int(not -8<=signed<=7)
   if op=='ADD':
    c=(a+b)>>4; assert c==int(a+b>=16)
   else:
    c=(a+(~b&15)+1)>>4; assert c==int(a>=b)
    tests=[(z==1,a==b),(z==0,a!=b),(c==0,a<b),(c==1,a>=b),
     (c==1 and z==0,a>b),(c==0 or z==1,a<=b),
     (n!=v,s(a)<s(b)),(n==v,s(a)>=s(b))]
    assert all(x==y for x,y in tests);checks+=len(tests)
    # Also verify greater-than / less-or-equal signed formulas.
    assert ((z==0 and n==v)==(s(a)>s(b)))
    assert ((z==1 or n!=v)==(s(a)<=s(b)))
   ops+=1
res={'arithmetic_cases':ops,'primary_comparison_checks':checks,'extra_signed_gt_le_checks':512,'status':'PASS','scope':'Python mathematical model, not RTL simulation'}
Path(__file__).resolve().parents[1].joinpath('build/verification/flags_math.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res))
