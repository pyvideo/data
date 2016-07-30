#!/usr/bin/env python3
# coding: utf-8
"""Fill id field in json video files
If a video file is found without id then it gets a id = max(id) + 1"""

import argparse
import json
import logging
import sys

sys.path.insert(0, '.')

import tinydb

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

    category_paths, video_paths = get_json_files(args.path)

    # Create DB
    db = tinydb.TinyDB(args.db)
    db.purge()  # Erase all content
    tb_video = db.table('video')
    tb_category = db.table('category')
    db_query = tinydb.Query()

    # Retrieve data
    tb_category.insert_multiple(get_json_data(file_name)
                                for file_name in sorted(category_paths))
    tb_video.insert_multiple(get_json_data(file_name)
                             for file_name in sorted(video_paths))

    # Query max id
    max_id = max(video['id']
                 for video in tb_video.search(db_query.id.exists()))

    # Update files
    [update_id(video, video_id)
     for video_id, video in enumerate(
         tb_video.search(~db_query.id.exists()), max_id + 1)]


if __name__ == '__main__':
    main()
