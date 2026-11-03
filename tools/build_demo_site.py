#!/usr/bin/env python3
"""Build the static public explorer from frozen reports and authored tutorials."""
from pathlib import Path
import argparse,csv,json,html,re,shutil,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'
DEMO=ROOT/'examples/fictional-workflow'
BASE='https://mhdteto.github.io/authority-architecture-system/'

def inline(text):
    text=html.escape(text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    def link(m):
        url=html.unescape(m[2])
        if url.startswith('../'):
            url='https://github.com/mhdteto/authority-architecture-system/blob/main/'+url[3:]
        elif url.endswith('.md') and not url.startswith('http'):
            url=url[:-3]+'.html'
        if not url.startswith(('https://','http://','#')) and not re.fullmatch(r'[a-z-]+\.html',url):raise ValueError('Unsupported tutorial link '+url)
        return '<a href="'+html.escape(url,quote=True)+'">'+m[1]+'</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)

def markdown_subset(text):
    output=[];paragraph=[];code=None;listing=False
    def flush():
        if paragraph:output.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
    for line in text.splitlines():
        if line.startswith('```'):
            flush()
            if listing:output.append('</ul>');listing=False
            if code is None:code=[]
            else:output.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');code=None
            continue
        if code is not None:code.append(line);continue
        if not line.strip():
            flush()
            if listing:output.append('</ul>');listing=False
            continue
        heading=re.match(r'^(#{1,3}) (.+)',line)
        if heading:
            flush();level=len(heading[1]);output.append(f'<h{level}>'+inline(heading[2])+f'</h{level}>');continue
        item=re.match(r'^(?:- |\d+\. )(.+)',line)
        if item:
            flush()
            if not listing:output.append('<ul>');listing=True
            output.append('<li>'+inline(item[1])+'</li>');continue
        paragraph.append(line)
    flush()
    if listing:output.append('</ul>')
    if code is not None:raise ValueError('Unclosed code fence')
    return '\n'.join(output)

def build(output):
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    (output/'assets').mkdir(exist_ok=True);(output/'data').mkdir(exist_ok=True)
    for name in ['style.css','app.js']:shutil.copyfile(WEB/name,output/'assets'/name)
    data={name:json.loads((DEMO/'reports'/folder/'report.json').read_text()) for name,folder in [('identity','identity'),('evidence','evidence'),('citations','citations')]}
    with (WEB/'data/source-catalogue.csv').open(newline='') as source:data['sources']=list(csv.DictReader(source))
    assert len(data['sources'])==16
    for entry in data['sources']:
        assert entry['url'].startswith('https://') and entry['verification_url'].startswith('https://')
    serialized=json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template=(WEB/'index.html').read_text();assert template.count('{{DATA}}')==1
    (output/'index.html').write_text(template.replace('{{DATA}}',serialized))
    for name in ['identity','evidence','citations']:(output/'data'/f'{name}.json').write_text(json.dumps(data[name],indent=2,ensure_ascii=False)+'\n')
    shutil.copyfile(WEB/'data/source-catalogue.csv',output/'data/source-catalogue.csv')
    shutil.copytree(DEMO/'reports',output/'reports',dirs_exist_ok=True)
    for file in (output/'reports').rglob('*.html'):
        text=file.read_text();tag='<meta name="robots" content="noindex, follow">'
        if '<head>' in text:text=text.replace('<head>','<head>'+tag,1)
        else:text=text.replace('<meta charset="utf-8">','<meta charset="utf-8">'+tag,1)
        file.write_text(text)
    (output/'tutorials').mkdir(exist_ok=True)
    paths=['']
    for source in sorted((ROOT/'tutorials').glob('*.md')):
        if source.name=='README.md':continue
        title=source.read_text().splitlines()[0].lstrip('# ')
        page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+''' — Authority Explorer</title><meta name="description" content="A fictional, reproducible business workflow by Mohammed Teto. Exact commands, actual tool outputs and interpretation limits."><link rel="canonical" href="'''+BASE+'tutorials/'+source.stem+'''.html"><link rel="stylesheet" href="../assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="top"><div class="wrap top-inner"><a class="brand" href="../">Mohammed Teto · Authority Explorer</a><nav aria-label="Primary"><a href="../#tutorials">All tutorials</a><a href="https://github.com/mhdteto/authority-architecture-system/discussions">Community</a></nav></div></header><main class="wrap article" id="main"><a class="back" href="../#tutorials">← All tutorials</a>'''+markdown_subset(source.read_text())+'''</main><footer class="wrap footer"><span>Entirely fictional teaching data; actual code output.</span><a href="https://github.com/mhdteto/authority-architecture-system">Source repository</a></footer></body></html>'''
        (output/'tutorials'/(source.stem+'.html')).write_text(page);paths.append('tutorials/'+source.stem+'.html')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);sitemap=ET.Element('{'+ns+'}urlset')
    for path in paths:ET.SubElement(ET.SubElement(sitemap,'{'+ns+'}url'),'{'+ns+'}loc').text=BASE+path
    ET.ElementTree(sitemap).write(output/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (output/'.nojekyll').write_text('')
    (output/'README.txt').write_text('Public explorer by Mohammed Teto. Fictional scenario outputs are generated from the frozen source workflow. The separate real-source catalogue is pinned to source-map v1.0.0; checked-on dates are not current availability guarantees. Hosted HTML reports add only noindex metadata. No analytics, uploads or live AI queries.\n')
    print('Built explorer, three tutorials, four data downloads and five original-report sets:',output)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'_site');args=parser.parse_args();build(args.output)
