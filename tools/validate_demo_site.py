#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate generated static pages and run the three published tutorial commands."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import csv,json,re,subprocess,sys,tempfile,shutil,hashlib

ROOT=Path(__file__).resolve().parents[1]
SITE=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'_site').resolve()

class Page(HTMLParser):
    def __init__(self):super().__init__();self.h1=0;self.ids=[];self.links=[];self.canon=[];self.description=[];self.tab_names=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='h1':self.h1+=1
        if d.get('id'):self.ids.append(d['id'])
        if tag in ['a','script','link'] and (d.get('href') or d.get('src')):self.links.append(d.get('href',d.get('src')))
        if tag=='link' and d.get('rel')=='canonical':self.canon.append(d['href'])
        if tag=='meta' and d.get('name')=='description':self.description.append(d['content'])
        if 'data-tab' in d:self.tab_names.append(d['data-tab'])

for p in [SITE/'index.html',*sorted((SITE/'tutorials').glob('*.html'))]:
    text=p.read_text();doc=Page();doc.feed(text)
    assert doc.h1==1 and len(doc.canon)==1 and len(doc.description)==1,p
    assert len(doc.ids)==len(set(doc.ids)),p
    expected='https://mhdteto.github.io/authority-architecture-system/'+p.relative_to(SITE).as_posix().replace('index.html','')
    assert doc.canon==[expected],p
    for target in doc.links:
        u=urlsplit(target)
        if u.scheme or u.netloc:continue
        if u.path:
            resolved=(p.parent/unquote(u.path)).resolve()
            if u.path.endswith('/'):resolved/= 'index.html'
            assert resolved.is_file(),(p,target)
        elif u.fragment:assert u.fragment in doc.ids or u.fragment in doc.tab_names,(p,target)
    assert 'fictional' in text.lower(),p

identity=json.loads((SITE/'data/identity.json').read_text())
assert identity['profile_count']==4
assert identity['status_counts']=={'approved_alias':2,'manual_review':3,'match':6,'mismatch':2,'missing':3}
evidence=json.loads((SITE/'data/evidence.json').read_text())
assert evidence['claims'][0]['independent_support_publishers']==1
assert evidence['claims'][1]['independent_support_publishers']==0
assert evidence['claims'][2]['statuses']==['missing evidence']
citations=json.loads((SITE/'data/citations.json').read_text())
assert len(citations['answers'])==6 and len(citations['groups'])==2
for group in citations['groups']:
    answers=[a for a in citations['answers'] if all(a[k]==group[k] for k in ['engine','model','interface','language','market'])]
    assert len(answers)==group['answer_count']
    cited=sum(bool(a['citation_urls']) for a in answers)
    assert cited==group['cited_answer_count'] and cited/len(answers)==group['cited_answer_rate']
with (SITE/'data/source-catalogue.csv').open(newline='') as source:sources=list(csv.DictReader(source))
assert len(sources)==16 and len({s['market'] for s in sources})==7
assert sum(s['market']=='France' for s in sources)==2
assert sum(s['name'].startswith('ORCID') for s in sources)==1
assert (SITE/'data/source-catalogue.csv').read_bytes()==(ROOT/'web/data/source-catalogue.csv').read_bytes()

original=ROOT/'examples/fictional-workflow/reports'
for p in original.rglob('*'):
    if not p.is_file():continue
    served=SITE/'reports'/p.relative_to(original)
    if p.suffix=='.html':assert served.read_text().replace('<meta name="robots" content="noindex, follow">','')==p.read_text()
    else:assert served.read_bytes()==p.read_bytes()

with tempfile.TemporaryDirectory() as temp:
    demo=Path(temp).resolve()/'workflow'
    shutil.copytree(ROOT/'examples/fictional-workflow',demo)
    for path in sorted((ROOT/'tutorials').glob('*.md')):
        if path.name=='README.md':continue
        commands=re.findall(r'```sh\n([^`]+)```',path.read_text())
        assert len(commands)==1,path
        args=commands[0].strip().split();assert args.pop(0)=='python3'
        subprocess.run([sys.executable,*args],cwd=demo,check=True)
    for p in original.rglob('*'):
        if p.is_file():assert (demo/'reports'/p.relative_to(original)).read_bytes()==p.read_bytes(),p

print('Explorer validation PASS: four pages, five panels, 16 real source entries, separate fictional counts, local links, hosting-only metadata and three exact tutorial commands.')
