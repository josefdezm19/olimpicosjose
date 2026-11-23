import json,re
d=json.load(open('raw.json'))
def fix(s): return re.sub(r'(\w)- (Up|Extensions?)\b',r'\1-\2',s).strip()
def paras(desc):
    lines=desc.split('\n'); out=[]; buf=''
    for i,l in enumerate(lines):
        l=l.strip()
        if re.match(r'^[A-Z]\. ',l) or l.startswith('- '):
            if buf: out.append(buf); buf=''
            out.append(l); continue
        if buf and (buf.endswith('.') or buf.endswith(':')) and len(lines[i-1].strip())<44:
            out.append(buf); buf=l
        else:
            buf=(buf+' '+l).strip() if buf else l
    if buf: out.append(buf)
    return out
CORE=['Roll-Outs','L-sit','Leg Raises','Chinese Plank','GHD','Sit-Ups','Sidebends','Forward Crawls']
def cat(ex,load):
    if any(k in ex for k in CORE): return 'core'
    if ('1RM' in load and 'Squat' in ex) or ('Press' in ex and 'moderate' in load) or ('Pull' in ex and '% BW' in load and '+' not in ex): return 'fuerza'
    if '% BW' in load or 'TECHNICAL' in load: return 'olimpico'
    return 'tecnica'
out=[]
for day in d:
    items=[]
    for s in day['items']:
        ex=fix(s['ex']); load=fix(s['load'])
        items.append({'n':s['n'],'ex':ex,'load':load,'timing':s['timing'],'desc':paras(fix(s['desc'])),'video':s['video'],'cat':cat(ex,load)})
    out.append({'w':day['week'],'d':day['day'],'focus':day['focus'],'items':items})
js='const PROGRAM='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';'
open('data.js','w').write(js)
print(len(js))
import collections
print(collections.Counter(i['cat'] for x in out for i in x['items']))
for x in out[:1]:
    for i in x['items']: print(i['cat'],i['ex'],i['desc'])
