#!/usr/bin/env python3
"""Check crawlable pages, download destinations, local assets and honest claims."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import argparse
import json
import re
import xml.etree.ElementTree as ET

BASE = 'https://georgepwall1991.github.io/fleet-commander-site/'
ROUTES = ['', 'no-ads/', 'offline/', 'garden/', 'faq/', 'press/']


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.schemas = []
        self.schema = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema = ''

    def handle_data(self, data):
        if self.schema is not None:
            self.schema += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None


def check(root):
    failures = []
    sitemap = ET.parse(root / 'sitemap.xml')
    locs = [e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if len(locs) != len(set(locs)):
        failures.append('duplicate sitemap URLs')
    for route in ROUTES:
        path = root / 'gemgame' / route / 'index.html'
        if not path.is_file():
            failures.append(f'missing {path.relative_to(root)}')
            continue
        raw = path.read_text()
        page = Page()
        try:
            page.feed(raw)
        except (ValueError, AssertionError) as exc:
            failures.append(f'{route}: invalid HTML/JSON: {exc}')
            continue
        url = BASE + 'gemgame/' + route
        canonical = [a.get('href') for t,a in page.tags if t == 'link' and a.get('rel') == 'canonical']
        if canonical != [url] or url not in locs:
            failures.append(f'{route}: canonical/sitemap mismatch')
        if sum(t == 'h1' for t,_ in page.tags) != 1:
            failures.append(f'{route}: needs one main heading')
        if not page.schemas:
            failures.append(f'{route}: missing structured data')
        if not any(t == 'meta' and a.get('name') == 'description' and a.get('content') for t,a in page.tags):
            failures.append(f'{route}: missing description')
        if any(t == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', '') for t,a in page.tags):
            failures.append(f'{route}: blocked from indexing')
        if not any(t == 'a' and 'apps.apple.com/app/id6761720994' in a.get('href', '') for t,a in page.tags):
            failures.append(f'{route}: missing correct download link')
        if re.search(r'handcrafted|hand-designed|no energy|full offline play|you decide when.*session ends', raw, re.I):
            failures.append(f'{route}: stale or unbounded feature claim')
        for tag, attrs in page.tags:
            if tag == 'img' and ('alt' not in attrs or not attrs.get('width') or not attrs.get('height')):
                failures.append(f'{route}: image lacks alt or dimensions')
            refs = [attrs[k] for k in ('href', 'src', 'poster') if k in attrs]
            # Generated source elements use one srcset image per format.
            if 'srcset' in attrs:
                refs += [x.strip().split()[0] for x in attrs['srcset'].split(',')]
            for ref in refs:
                parsed = urlparse(urljoin(url, ref))
                if parsed.netloc != 'georgepwall1991.github.io' or not parsed.path.startswith('/fleet-commander-site/'):
                    continue
                target = root / unquote(parsed.path.removeprefix('/fleet-commander-site/'))
                if parsed.path.endswith('/'):
                    target /= 'index.html'
                if not target.is_file():
                    failures.append(f'{route}: broken local reference {ref}')
    if failures:
        raise SystemExit('\n'.join('FAIL: ' + f for f in failures))
    print('GemGame acquisition check passed: six pages, canonical URLs, sitemap, structured data, download CTAs, local links/assets and claim boundaries')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    check(parser.parse_args().root.resolve())
