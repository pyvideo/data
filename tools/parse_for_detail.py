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


PAT = re.compile(r'^DjangoCon EU 2013: (.*) -.*$')
SOURCE_KEY = 'title'
CATEGORY = 'djangocon-eu-2013'


def parse(path):
    with open(path) as fp:
        try:
            data = json.load(fp)
        except ValueError:
            logging.error('Json syntax error in file {}'.format(path))
            raise

    source = data.get(SOURCE_KEY, '')
    match = PAT.match(source)
    parsed_content = match.group(1).strip() if match else ''

    # UPDATE this placement code
    speakers = data.get('speakers', [])
    speakers.append(parsed_content)
    data['speakers'] = speakers
    # DONE UPDATING

    with open(path, 'w') as fp:
        json.dump(data, fp)


def main():
    video_pattern = os.path.join(CATEGORY, 'videos/*.json')
    for path in glob.iglob(video_pattern):
        parse(path)


if __name__ == '__main__':
    main()

