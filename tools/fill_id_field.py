#!/usr/bin/env python3
# coding: utf-8
"""Fill id field in json video files
If a video file is found without id then it gets a id = max(id) + 1"""

import argparse
import collections
import json
import logging
import sys

sys.path.insert(0, '.')

from tools.utils import get_json_files
from tools.constants import JSON_FORMAT_KWARGS


def get_json_data(file_name):
    """Get data from json file and path as dict"""
    with open(file_name) as f_stream:
        try:
            data = json.load(f_stream)
        except ValueError:
            print('Json syntax error in file {}'.format(file_name))
            raise
    if 'file_name' in data:
        print('"File_name" is not a proper field in {}'.format(file_name))
        raise ValueError
    data['file_name'] = file_name
    return data


def update_id(data, data_id):
    """Update json file including new id"""
    file_name = data['file_name']
    del data['file_name']
    data['id'] = data_id
    with open(file_name, 'w') as f_stream:
        json.dump(data, f_stream, **JSON_FORMAT_KWARGS)


def main():
    """Fill id field in json video files"""

    logging.basicConfig(level=logging.WARNING)  # WARNING or DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to data repository")
    parser.add_argument('--db',
                        default='/tmp/db.json',
                        help="path to tinydb file")

    args = parser.parse_args()

    _, video_paths = get_json_files(args.path)

    # Retrieve data
    tb_video = [get_json_data(file_name) for file_name in sorted(video_paths)]

    # Query max id
    all_id = collections.Counter(video['id'] for video in tb_video
                                 if 'id' in video.keys())
    most_common, times_duplicate = all_id.most_common(1)[0]
    if times_duplicate > 1:
        raise ValueError('Duplicate id: {}'.format(most_common))
    max_id = max(all_id)
    logging.debug('Max id: {}'.format(max_id))

    # Update files
    video_without_id = [video for video in tb_video
                        if 'id' not in video.keys()]
    for video_id, video in enumerate(video_without_id, max_id + 1):
        update_id(video, video_id)


if __name__ == '__main__':
    main()
