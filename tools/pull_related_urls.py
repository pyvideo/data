import argparse
import logging
import json
import re
import sys
sys.path.insert(0, '.')

from tools.constants import JSON_FORMAT_KWARGS
from tools.utils import get_json_files

RE_URL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


def pull_links_from_string(string):
    urls = RE_URL.findall(string)
    return urls


def pull_links_from_file(file_):
    with open(file_) as fp:
        try:
            data = json.load(fp)
        except ValueError:
            logging.error('Json syntax error in file {}'.format(file_))
            raise

    description = data.get('description') or ''
    summary = data.get('summary') or ''
    related_urls = data.get('related_urls') or []

    description_links = pull_links_from_string(description)
    summary_links = pull_links_from_string(summary)
    links = description_links + summary_links

    if links:
        # hack cause I don't want to spend time finding a better regex
        links = [link.strip('>') for link in links]
        related_urls += links
        data['related_urls'] = sorted(set(related_urls))

        with open(file_, 'w') as fp:
            json.dump(data, fp, **JSON_FORMAT_KWARGS)


def main():
    """Pull related urls from summary and description of video JSON"""
    logging.basicConfig(level=logging.WARNING)
    parser = argparse.ArgumentParser()
    parser.add_argument("path",
                        help="path to file(s) to reserialize")
    parser.add_argument("-a", "--all",
                        action="store_true",
                        help="reserialize all JSON files under path")
    args = parser.parse_args()

    if args.all:
        category_paths, video_paths = get_json_files(args.path)
        paths = video_paths
        for path in paths:
            pull_links_from_file(path)
    else:
        pull_links_from_file(args.path)


if __name__ == '__main__':
    main()

