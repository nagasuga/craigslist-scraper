from datetime import datetime
import json
import re
import urllib.parse

import feedparser
import dateutil.parser
import requests

from .models import Entry


class Craigslist(object):
    def __init__(self, city='losangeles'):
        self.url = 'http://%s.craigslist.org/search/sss' % city
        self.params = {
            'format': 'rss',
            'query': '',
        }
        self.raw_data = None

    def call(self, query):
        params = self.params
        params.update({
            'query': query,
        })
        self.raw_data = requests.get(url=self.url, params=params).text
        return self

    def iter(self):
        data = feedparser.parse(self.raw_data)
        for raw_entry in data['entries']:
            entry = self.parse(raw_entry)
            yield entry

    def parse(self, raw_entry):
        matched = re.search(r'^.*\/(\d+)\.html$', raw_entry['id'])
        entry_id = matched.group(1)
        updated = dateutil.parser.parse(raw_entry['updated'])
        published = dateutil.parser.parse(raw_entry['published'])
        image = raw_entry.get('enc_enclosure', {}).get('resource')
        title = re.sub(r'(.*) \&\#x\d{4};\d+$', r'\1', raw_entry['title'])
        return Entry(updated=updated,
                     summary=raw_entry['summary'],
                     url=raw_entry['link'],
                     title=title,
                     id=entry_id,
                     published=published,
                     image=image)
