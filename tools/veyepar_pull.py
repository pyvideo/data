#!/usr/bin/env python
import argparse
import json
import os
from urllib.request import urlopen
import sys
sys.path.insert(0, '.')

from pelican.utils import slugify

from tools.constants import JSON_FORMAT_KWARGS


def make_video_file(videos_dir, video_data):
    if video_data['fields']['state'] < 11:
        return
    file_data = {}
    file_data['description'] = video_data['fields']['description']
    file_data['title'] = video_data['fields']['name']
    file_data['speakers'] = video_data['fields']['authors'].split(',')
    file_data['recorded'] = video_data['fields']['start'].split('T')[0]
    file_data['videos'] = [{
        'type': 'youtube',
        'url': video_data['fields']['host_url'],
    }]
    file_data['thumbnail_url'] = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(
        file_data['videos'][0]['url'].split('/')[-1])
    duration_chunks = list(map(int, video_data['fields']['duration'].split(':')))
    duration = sum(60 ** i * j for i, j in enumerate(reversed(duration_chunks)))
    file_data['duration'] = duration

    path = os.path.join(videos_dir, slugify(file_data['title']) + '.json')
    with open(path, 'w') as fp:
        json.dump(file_data, fp, **JSON_FORMAT_KWARGS)


def make_category(category, veyepar_url):
    if not veyepar_url.endswith('.json'):
        raise ValueError('veyepar url must be a json resource')

    # create necessary dirs
    category_dir = category.lower()
    videos_dir = os.path.join(category_dir, 'videos')
    if not os.path.exists(category_dir) or not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    with urlopen(veyepar_url) as fp:
        data = fp.read()

    data = data.decode()
    data = json.loads(data)

    for video_data in data:
        make_video_file(videos_dir, video_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--category')
    parser.add_argument(
            '-v', '--veyepar-url',
            help='e.g.: https://example.com/main/C/pyconza/S/pyconza2016.json')
    args = parser.parse_args()

    make_category(args.category, args.veyepar_url)

