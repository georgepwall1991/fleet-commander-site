#!/usr/bin/env python3
"""Validate the new acquisition routes and their actual local dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://georgepwall1991.github.io/fleet-commander-site/'
ROUTES=['','space-roguelite/','frontier-runs-guide/','fleet-builds-extraction/','press/']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.text=[];self.schema=[];self.in_schema=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));self.in_schema=tag=='script' and a.get('type')=='application/ld+json' if tag=='script' else self.in_schema
 def handle_endtag(self,tag):
  if tag=='script':self.in_schema=False
 def handle_data(self,data):
  self.text.append(data)
  if self.in_schema:self.schema.append(json.loads(data))
sitemap={e.text for e in ET.parse(ROOT/'sitemap.xml').iter() if e.tag.endswith('}loc')}
titles=[]
for route in ROUTES:
 path=ROOT/route/'index.html';p=Page();p.feed(path.read_text());tags=p.tags;text=' '.join(p.text)
 assert sum(t=='h1' for t,a in tags)==1,route
 assert any(t=='link' and a.get('rel')=='canonical' and a.get('href')==BASE+route for t,a in tags),route
 assert any(t=='meta' and a.get('name')=='description' and a.get('content') for t,a in tags),route
 assert any(t=='meta' and a.get('property')=='og:image' for t,a in tags),route
 assert p.schema and BASE+route in sitemap,route
 assert 'upcoming' in text.lower() and '1.2.0' in text,route
 for tag,a in tags:
  if tag=='img':assert a.get('alt'),(route,a)
  if tag=='video':assert a.get('preload')=='none' and 'controls' in a,(route,a)
  for field in ('href','src','poster'):
   ref=a.get(field,'');u=urlparse(ref)
   if not ref or u.scheme or u.netloc or ref.startswith('#'):continue
   target=(path.parent/unquote(u.path)).resolve()
   if target.is_dir():target=target/'index.html'
   assert target.is_file(),(route,ref)
print('PASS: five Frontier routes, canonical URLs, metadata, schema, sitemap, native media dependencies and upcoming labels')
