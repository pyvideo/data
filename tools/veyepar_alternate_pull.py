#!/usr/bin/env python
import argparse
import json
import os
import sys
from urllib.parse import urlparse
sys.path.insert(0, '.')

from pelican.utils import slugify
from requests import get

from tools.constants import JSON_FORMAT_KWARGS


def make_video_file(videos_dir, video_data):
    if video_data['veyepar_state'] < 11:
        return
    file_data = {}
    file_data['description'] = video_data['description']
    file_data['title'] = video_data['title']
    file_data['speakers'] = video_data['speakers']
    file_data['recorded'] = video_data['recorded'].split('T')[0]
    related_urls = []
    videos = []
    for item in video_data['videos']:
        if item['type'] == 'conf':
            related_urls.append(item['url'])
        elif item['type'] == 'archive':
            videos.append(dict(type=item['type'], url=item['url']))
        elif item['type'] == 'host':
            videos.append(dict(type='youtube', url=item['url']))
    file_data['videos'] = videos
    file_data['related_urls'] = related_urls
    file_data['thumbnail_url'] = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(
        video_data['source_url'].split('/')[-1])
    file_data['duration'] = video_data['duration']

    path = os.path.join(videos_dir, slugify(file_data['title']) + '.json')
    with open(path, 'w') as fp:
        json.dump(file_data, fp, **JSON_FORMAT_KWARGS)


def make_category(category, veyepar_url):
    parsed_url = urlparse(veyepar_url)
    if not parsed_url.path.endswith('.urls'):
        raise ValueError('veyepar url must be a json resource')

    # create necessary dirs
    category_dir = category.lower()
    videos_dir = os.path.join(category_dir, 'videos')
    if not os.path.exists(category_dir) or not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    talk_urls = get(veyepar_url).text.split('\n')[1:]

    for talk_url in talk_urls:
        video_data = get(talk_url).json()
        make_video_file(videos_dir, video_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--category')
    parser.add_argument(
            '-v', '--veyepar-url',
            help='e.g.: https://veyepar.tblwd.org/main/M/pyvid_json.urls?client=pyconza&show=pyconza2016')
    args = parser.parse_args()

    make_category(args.category, args.veyepar_url)

