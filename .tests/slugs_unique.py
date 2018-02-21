import argparse
from collections import defaultdict
import glob
import json
import os
import sys

from tools.utils import get_json_files, slugify


def check_slugs_unique(data_root, verbose=False):
    category_paths, _ = get_json_files(data_root)

    paths_by_combo = defaultdict(list)

    for category_path in category_paths:
        with open(category_path, encoding='UTF-8') as fp:
            category_blob = json.load(fp)
            # slugs will be generated from titles, so titles can be used
            # as a stand-in for slugs when testing unique constraints.
            category_title = category_blob.get('title')

            head, _ = os.path.split(category_path)
            video_pattern = os.path.join(head, 'videos/*.json')
            for video_path in glob.iglob(video_pattern):
                with open(video_path, encoding='UTF-8') as fp:
                    video_blob = json.load(fp)
                    video_slug = video_blob.get('slug')
                    if not video_slug:
                        video_slug = slugify(video_blob.get('title'))

                    combo = (category_title, video_slug)
                    paths_by_combo[combo].append(video_path)

    keys = list(paths_by_combo.keys())
    for key in keys:
        if len(paths_by_combo[key]) <= 1:
            del paths_by_combo[key]

    if paths_by_combo:
        print('Duplicate slug combinations found:')
        for combo, paths in paths_by_combo.items():
            print('Combination {}'.format(combo))
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

    check_slugs_unique(args.data_root, verbose=args.verbose)


if __name__ == '__main__':
    main()

