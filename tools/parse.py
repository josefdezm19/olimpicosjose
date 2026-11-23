import pdfplumber, glob, json, re, sys
pdf=pdfplumber.open(glob.glob('/mnt/user-data/uploads/b905b624-*.pdf')[0])
cols=[(0,60,'set'),(60,228,'ex'),(228,380,'load'),(380,540,'timing'),(540,900,'desc')]
days=[]; cur=None; curset=None
def col(x):
    for a,b,n in cols:
        if a<=x<b: return n
for pn in range(52,141):
    p=pdf.pages[pn-1]; H=p.height
    words=p.extract_words(keep_blank_chars=False, use_text_flow=False)
    links=[(l['top'],l['uri']) for l in p.hyperlinks if 'youtu' in l['uri']]
    # group by line top
    lines={}
    for w in words:
        if w['top']>H-50: continue  # footer
        key=round(w['top'])
        lines.setdefault(key,[]).append(w)
    for top in sorted(lines):
        ws=sorted(lines[top],key=lambda w:w['x0'])
        text=' '.join(w['text'] for w in ws)
        if text.startswith('weightlifting101.net') or re.fullmatch(r'\d+ / 166',text): continue
        m=re.match(r'Week (\d+), Day (\d+) – (.*)',text)
        if m:
            cur={'week':int(m[1]),'day':int(m[2]),'focus':m[3].rstrip('.'),'page':pn,'items':[]}; days.append(cur); curset=None; continue
        if text.startswith('Set Exercise'): continue
        if cur is None: continue
        first=ws[0]
        if col(first['x0'])=='set' and re.fullmatch(r'\d+',first['text']):
            curset={'n':int(first['text']),'ex':'','load':'','timing':'','desc':'','video':None,'_top':top,'_page':pn}
            cur['items'].append(curset); ws=ws[1:]
        if curset is None:
            print('ORPHAN',pn,text,file=sys.stderr); continue
        # desc keeps line breaks for lists
        parts={}
        for w in ws: parts.setdefault(col(w['x0']),[]).append(w['text'])
        for k,v in parts.items():
            s=' '.join(v)
            if k=='desc': curset['desc']+=('\n' if curset['desc'] else '')+s
            else: curset[k]+=(' ' if curset[k] else '')+s
    # assign links: link belongs to set whose start top <= link top on this page (last such)
    for t,u in links:
        cands=[s for d in days for s in d['items'] if s['_page']==pn and s['_top']<=t+3]
        if cands and not cands[-1]['video']: cands[-1]['video']=u
        elif not cands:
            # continuation from previous page
            pass
for d in days:
    for s in d['items']:
        s.pop('_top');s.pop('_page')
json.dump(days,open('raw.json','w'),indent=1,ensure_ascii=False)
print(len(days),[ (d['week'],d['day'],len(d['items'])) for d in days])
