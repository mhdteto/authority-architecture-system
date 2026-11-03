#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Collect a bounded first-party technical case, with archived public responses."""
import argparse
from datetime import datetime,timezone
import hashlib,importlib.util,json
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'examples/fictional-workflow/tools/search-ai-discoverability-checker/check.py'
PAGES={'home':'https://mohammedteto.com/','method':'https://mohammedteto.com/method/','tools':'https://mohammedteto.com/open-source-tools/'}

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data={'html_lang':None,'titles':[],'descriptions':[],'h1':[],'hreflang':[]}
        self.active=None;self.parts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.data['html_lang']=a.get('lang')
        if tag in ('title','h1'):self.active=tag;self.parts=[]
        if tag=='meta' and a.get('name','').lower()=='description':self.data['descriptions'].append(a.get('content',''))
        if tag=='link' and a.get('hreflang'):self.data['hreflang'].append({'language':a['hreflang'],'url':a.get('href','')})
    def handle_data(self,data):
        if self.active:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag==self.active:
            self.data['titles' if tag=='title' else 'h1'].append(' '.join(''.join(self.parts).split()))
            self.active=None

def load_checker():
    spec=importlib.util.spec_from_file_location('checker',SOURCE)
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    return checker

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True)
    args=parser.parse_args()
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=False)
    checker=load_checker();responses={};stamp=datetime.now(timezone.utc).isoformat()
    def transport(url):
        if url not in responses:
            raw=checker.live_transport(url)
            # Archive only public content and diagnostic headers, never cookies.
            allowed={'content-type','x-robots-tag','link','location','content-encoding','content-length'}
            responses[url]={'status':raw['status'],'headers':{k:v for k,v in raw['headers'].items() if k in allowed},'body':raw['body']}
        return responses[url]
    metadata={}
    for slug,url in PAGES.items():
        report=checker.analyze(url,transport,stamp)
        report['transport']='live public HTTP(S)'
        target=out/slug;target.mkdir()
        (target/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        (target/'report.html').write_text(checker.render_html(report))
        m=Metadata();m.feed(responses[report['page']['url']]['body'])
        metadata[slug]={'url':url,'collected_at':stamp,**m.data}
    sitemaps={}
    for url,response in responses.items():
        if 'xml' not in response['headers'].get('content-type',''):continue
        try:
            doc=ET.fromstring(response['body'])
            sitemaps[url]={'root':doc.tag.split('}')[-1],'locations':[e.text for e in doc.iter() if e.tag.split('}')[-1]=='loc']}
        except ET.ParseError as exc:sitemaps[url]={'parse_error':str(exc)}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
    (out/'sitemap-observation.json').write_text(json.dumps(sitemaps,indent=2)+'\n')
    archive={'kind':'archived real public HTTP responses; not synthetic teaching data','collected_at':stamp,'responses':responses}
    (out/'http-archive.json').write_text(json.dumps(archive,indent=2,ensure_ascii=False)+'\n')
    manifest={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
    (out/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Archived',len(responses),'public HTTP responses for three page observations at',stamp)

if __name__=='__main__':main()
