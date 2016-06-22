import argparse
import json

import sys
sys.path.insert(0, '.')

from tools.constants import JSON_FORMAT_KWARGS
from tools.utils import get_json_files


def reserialize(file_):
    with open(file_) as fp:
        data = json.load(fp)

    with open(file_, 'w') as fp:
        json.dump(data, fp, **JSON_FORMAT_KWARGS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",
                        help="path to file(s) to reserialize")
    parser.add_argument("-a", "--all",
                        action="store_true",
                        help="reserialize all JSON files under path")
    args = parser.parse_args()

    if args.all:
        category_paths, video_paths = get_json_files(args.path)
        paths = category_paths + video_paths
        for path in paths:
            reserialize(path)
    else:
        reserialize(args.path)


if __name__ == '__main__':
    main()

