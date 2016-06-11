import argparse
import json
import sys

from utils import get_json_files


def check_render_rest(data_root, verbose=False):
    _, video_paths = get_json_files(data_root)

    for file_path in video_paths:
        with open(file_path, encoding='UTF-8') as fp:
            blob = json.load(fp)

    # TODO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-v", "--verbose",
                        type=int,
                        help="increase output verbosity")
    args = parser.parse_args()

    check_render_rest(args.data_root, verbose=args.verbose)


if __name__ == '__main__':
    main()

