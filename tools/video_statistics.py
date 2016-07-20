#!/usr/bin/env python3
# coding: utf-8
"""Read only program that prints statistics (in markdown) of all json files
in the repository:
- Fields
- Class
- Is the field empty
- Count"""

import argparse
import collections
import json
import logging
import sys
sys.path.insert(0, '.')

from tools.utils import get_json_files


def is_void(data):
    """Detect nulls in other types"""
    if data in ('', 0, []):
        return 'is empty'
    else:
        return 'have data'


def get_types(file_name):
    """Get field types (and lack of data) of json file"""
    with open(file_name) as f_stream:
        try:
            data = json.load(f_stream)
        except ValueError:
            print('Json syntax error in file {}'.format(file_name))
            raise
    return {(key, type(data[key]).__name__, is_void(data[key]))
            for key in data}


def markdown_statistics(file_names):
    """Statistics of json files files (class and lack of data)"""
    total = collections.Counter()
    for file_name in sorted(file_names):
        total.update(get_types(file_name))
    result = ["|Field|Class|Empty|Count|", "|---|---|---|---|"]
    for field, class_, void in sorted(total, key=str):
        result.append("|{}|{}|{}|{}|".format(field, class_, void, total[(
            field, class_, void)]))
    logging.debug('result: {}'.format(result))
    return '\n'.join(result)


def main():
    """Convert json file(s) to the project format standards"""
    logging.basicConfig(level=logging.WARNING)  # WARNING or DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to data repository")
    args = parser.parse_args()
    category_paths, video_paths = get_json_files(args.path)
    print('\n# Category statistics')
    print(markdown_statistics(category_paths))
    print('\n# Video statistics')
    print(markdown_statistics(video_paths))


if __name__ == '__main__':
    main()
