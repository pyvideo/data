import argparse
from collections import defaultdict
import json
import sys

from tools.utils import get_json_files


def check_ids_unique(data_root, verbose=False):
    _, video_paths = get_json_files(data_root)

    paths_by_id = defaultdict(list)
    for file_path in video_paths:
        with open(file_path, encoding='UTF-8') as fp:
            blob = json.load(fp)
            id_ = blob.get('id')
            if id_:
                paths_by_id[id_].append(file_path)

    keys = list(paths_by_id.keys())
    for key in keys:
        if len(paths_by_id[key]) <= 1:
            del paths_by_id[key]

    if paths_by_id:
        print('Duplicate IDs found:')
        for id_, paths in paths_by_id.items():
            print('ID {}'.format(id_))
            for path in paths:
                print('\t', path)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-v", "--verbose",
                        type=int,
                        help="increase output verbosity")
    args = parser.parse_args()

    check_ids_unique(args.data_root, verbose=args.verbose)


if __name__ == '__main__':
    main()

