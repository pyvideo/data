"""
This is a script to help parse out information contained in other parts of
gathered data. For example, let's say data for a conference was pulled from
YouTube. Youtube does not provide "speakers" in its API but a speaker's name
maybe contained in the title data that is provided by YouTube. This script will
aid in pulling the speaker's name from the title and adding it to the
speakers JSON array. Please note that modifications to this code are almost
certainly necessary for it to work properly for your use case.
"""
import glob
import json
import os
from pprint import pprint
import re
from pathlib import Path
import logging

PATTERNS = {'one' : r'\s*(?P<speakers>.*)\s*:\s*(?P<title>.*)\s*\|\s*(?P<event>.*)',
            'two' : r'\s*(?P<speakers>.*)\s*-\s*(?P<title>.*)\s*-\s*(?P<event>.*)' }

PYVIDEO_DATA = Path(os.environ['PYVIDEO_DATA'])
PAT = { key : re.compile(pattern) for key, pattern in PATTERNS.items() }
SOURCE_KEY = 'title'
CATEGORY = 'pydata-london-2019'


def parse(path):
    with open(path) as fp:
        try:
            data = json.load(fp)
        except ValueError:
            logging.error('Json syntax error in file {}'.format(path))
            raise

    source = data.get(SOURCE_KEY, '')
    match = None
    for pattern in PAT.values():
        match = pattern.match(source)
        if match:
            break

    parsed_title    = match.group('title').strip() if match else ''
    parsed_speakers = match.group('speakers').split(',') if match else []

    # UPDATE this placement code
    speakers = data.get('speakers', [])
    speakers.extend(parsed_speakers)
    data['speakers'] = speakers
    data['title2'] = data['title']
    data['title']    = parsed_title
    # DONE UPDATING

    # pprint(data)

    with open(path, 'w') as fp:
        json.dump(data, fp)


def main():
    videos = PYVIDEO_DATA / CATEGORY / 'videos'
    for path in videos.glob('*.json'):
        parse(path)


if __name__ == '__main__':
    main()

