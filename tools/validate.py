#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate local Markdown targets, SVG artwork and CSV template headers."""
from pathlib import Path
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []
for file in ROOT.rglob('*.md'):
    content = file.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if target.startswith(('https://', 'http://', 'mailto:', '#')):
            continue
        path = target.split('#', 1)[0]
        if path and not (file.parent / path).exists():
            errors.append(f'{file.relative_to(ROOT)}: missing {target}')
    for target in re.findall(r'<img[^>]+src="([^"]+)"', content):
        if not target.startswith(('http://', 'https://')) and not (file.parent / target).is_file():
            errors.append(f'{file.relative_to(ROOT)}: missing image {target}')
for file in ROOT.rglob('*.svg'):
    ET.parse(file)
for file in (ROOT/'templates').glob('*.csv'):
    with file.open(newline='',encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    if len(rows) != 1 or len(set(rows[0])) != len(rows[0]):
        errors.append(f'{file.name}: templates must have one unique header row')
json.loads((ROOT/'templates/identity-record.json').read_text(encoding='utf-8'))
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print('Validated Markdown targets, artwork, header-only CSV templates and identity JSON.')
