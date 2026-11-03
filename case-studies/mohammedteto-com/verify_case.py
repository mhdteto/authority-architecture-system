# SPDX-License-Identifier: MIT
"""Verify archived real observations offline; never invent a before/after result."""
import hashlib,json
from pathlib import Path
from collect import load_checker,Metadata
BASE=Path(__file__).resolve().parent/'2026-11-03'
manifest=json.loads((BASE/'SHA256SUMS.json').read_text())
for name,expected in manifest.items():
    assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==expected,name
archive=json.loads((BASE/'http-archive.json').read_text())
assert archive['kind'].startswith('archived real public HTTP')
checker=load_checker()
metadata=json.loads((BASE/'metadata.json').read_text())
for slug in ['home','method','tools']:
    original=json.loads((BASE/slug/'report.json').read_text())
    replay=checker.analyze(original['input_url'],lambda url:archive['responses'][url],original['collected_at'])
    replay['transport']=original['transport']
    assert replay==original,slug
    assert (BASE/slug/'report.html').read_text()==checker.render_html(replay)
    parser=Metadata();parser.feed(archive['responses'][original['page']['url']]['body'])
    assert all(metadata[slug][key]==value for key,value in parser.data.items()),slug
print('PASS: archive hashes, three real reports, HTML and metadata reproduce offline.')
