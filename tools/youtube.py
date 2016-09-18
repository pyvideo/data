import argparse
import copy
import json
import os
import sys
sys.path.insert(0, '.')
import time
import uuid
from urllib.parse import urlencode

import requests

from tools.constants import JSON_FORMAT_KWARGS
from tools.utils import slugify


ENV_VAR_API_KEY = 'GOOGLE_API_KEY'

YOUTUBE_VIDEO_TEMPLATE = 'https://www.youtube.com/watch?v={}'.format


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', '--api-key',
        help='Can also be specified via the environment variable GOOGLE_API_KEY'
    )
    parser.add_argument('-l', '--list')

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        parser.print_help()
        sys.exit(0)

    if args.list:
        fetch_list(api_key, args.list)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()

