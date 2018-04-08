"""
What is this tool
=================

This script allows you to pull down data from YouTube for a given playlist.

How to use this tool
====================

You'll need a Google API key:

    - Go to https://console.developers.google.com
    - Enable the "YouTube Data API v3" API
    - Under credentials, create an API key. (DON'T SHARE THIS KEY!)
    - Set an environmental variable named GOOGLE_API_KEY with your API key as its value

Get playlist ID to pull data from. For example, if you have a link to a
playlist like the following: 

    https://www.youtube.com/playlist?list=UUrJhliKNQ8g0qoE_zvL8eVg

The playlist ID would be the following: UUrJhliKNQ8g0qoE_zvL8eVg

Finally, (after setting the API key as an environment variable) you would
run this tool (from the root of the data repo) as follows:

    python tools/youtube.py -l UUrJhliKNQ8g0qoE_zvL8eVg

Running this command will generate a new category/event folder with associated
JSON files. The folder will be named something funky like:

    category-123456789.34567890

You will need to update this folder's name and files with the rest of
the appropriate information before submitting the change for a PR.

This tool can also format a category's or event's content in a more appropriate
style for our data repo. To use this feature, use the following:

    python youtube.py -p path/to/event

This can save you a lot of time when renaming thumbnails!

"""
import argparse
import copy
import json
import os
import re
import sys

import time
import uuid
from urllib.parse import urlencode

import requests

from constants import JSON_FORMAT_KWARGS
from utils import slugify


ENV_VAR_API_KEY = 'GOOGLE_API_KEY'

YOUTUBE_VIDEO_TEMPLATE = 'https://www.youtube.com/watch?v={}'.format
YOUTUBE_THUMBNAIL_URL_TEMPLATE = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format

URL_PATTERNS = {
    re.compile(r'https://www.youtube.com/watch\?v=(\S*)'),
    re.compile(r'http://youtu.be/(\S*)'),
}

class UrlStub:
    def __init__(self, stub, default_query_parts):
        self.stub = stub
        self.default_query_parts = default_query_parts

    def build(self, query_parts):
        parts = copy.deepcopy(self.default_query_parts)
        parts.update(query_parts)
        query_string = urlencode(parts)

        return self.stub + '?' + query_string


PLAY_LIST_ITEMS = UrlStub(
    stub='https://www.googleapis.com/youtube/v3/playlistItems',
    default_query_parts={
        'part': 'snippet',
        'maxResults': '50',
    },
)


BASE_VIDEO_BLOB = {
    'description': '',
    'speakers': [],
    'thumbnail_url': '',
    'title': '',
    'recorded': '',
    'videos': [],
}


def handle_errors(response_dict):
    if 'error' not in response_dict:
        return

    error = response_dict.get('error')

    raise RuntimeError(error.get('message'))


def get_response_dict_for_play_list(query_parts):
    url = PLAY_LIST_ITEMS.build(query_parts)
    response_dict = requests.get(url).json()
    handle_errors(response_dict)

    return response_dict


def fetch_list(api_key, play_list_id):
    query_parts = {
        'playlistId': play_list_id,
        'key': api_key,
    }

    response_dict = get_response_dict_for_play_list(query_parts)
    next_page_token = response_dict.get('nextPageToken')

    total_results = response_dict.get('pageInfo', {}).get('totalResults')
    print('Found {} results. Gathering them now .'.format(total_results), end='')

    items = response_dict.get('items', [])
    while next_page_token:
        query_parts.update({'pageToken': next_page_token})
        response_dict = get_response_dict_for_play_list(query_parts)
        items.extend(response_dict.get('items', []))
        next_page_token = response_dict.get('nextPageToken')
        print('.', end='', flush=True)

    print(' Done. Parsing results ...')

    # pull data from api structures
    snippets = []
    for item in items:
        snippet = item.get('snippet', {})
        video_id = snippet.get('resourceId', {}).get('videoId')
        snippets.append({
            'title': snippet.get('title'),
            'description': snippet.get('description'),
            'videos': [{
                'type': 'youtube',
                'url': YOUTUBE_VIDEO_TEMPLATE(video_id),
            }],
            'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url'),
        })

    # build pyvideo compliant data structures
    results = []
    for snippet in snippets:
        pyvideo_blob = copy.deepcopy(BASE_VIDEO_BLOB)
        pyvideo_blob.update(snippet)
        results.append(pyvideo_blob)

    print('Done parsing results. Writing files to disk ', end='')

    # make category dir
    category = 'category-{}'.format(time.time())
    os.makedirs(os.path.join(category, 'videos'))

    with open(os.path.join(category, 'category.json') , 'w') as fp:
        json.dump({'title': ''}, fp, **JSON_FORMAT_KWARGS)
        print('.', end='', flush=True)

    for result in results:
        title = result.get('title')
        file_name = slugify(title)
        file_name = os.path.join(category, 'videos', file_name)
        # add some randomness to the name if a file already exists with that name
        if os.path.exists(file_name + '.json'):
            file_name += '-{}.json'.format(str(uuid.uuid1())[:6])
        else:
            file_name += '.json'

        with open(file_name, 'w') as fp:
            json.dump(result, fp, **JSON_FORMAT_KWARGS)
        print('.', end='', flush=True)

    print(' Done.')


def get_api_key(api_key):
    if api_key:
        return api_key

    api_key = os.environ.get(ENV_VAR_API_KEY)
    return api_key


def parse_video_id(video_url):
    for pattern in URL_PATTERNS:
        match = pattern.match(video_url)
        if match:
            return match.group(1)


def normalize(path):
    videos_dir_path = os.path.join(path, 'videos')
    video_files = os.listdir(videos_dir_path)

    for video_file in video_files:
        video_file_path = os.path.join(videos_dir_path, video_file)
        with open(video_file_path) as fp:
            data = json.load(fp)

        # -- Normalize Data --
        # Get video id
        for video_obj in data['videos']:
            video_url = video_obj.get('url')
            if not video_url:
                continue

            video_id = parse_video_id(video_url)
            if video_id:
                break

        # Insert thumbnail url if video does not have one
        if video_id and 'thumbnail_url' not in data:
            data['thumbnail_url'] = YOUTUBE_THUMBNAIL_URL_TEMPLATE(video_id)

        with open(video_file_path, 'w') as fp:
            json.dump(data, fp, **JSON_FORMAT_KWARGS)
        print('.', end='', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', '--api-key',
        help='Can also be specified via the environment variable GOOGLE_API_KEY'
    )
    parser.add_argument('-l', '--list')
    parser.add_argument(
        '-p', '--path',
        help='Path to event to normalize.'
    )

    args = parser.parse_args()

    if args.list:
        api_key = get_api_key(args.api_key)
        if not api_key:
            print('Please set an API key!')
            parser.print_help()
            sys.exit(0)

        fetch_list(api_key, args.list)

    elif args.path:
        normalize(args.path)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()

