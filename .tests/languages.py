import argparse
from collections import defaultdict
import json
import sys

from tools.utils import get_json_files

# Copied from pelicanconf.py in https://github.com/pyvideo/pyvideo
VIDEO_LANGUAGE_NAMES = {
    'ita': 'Italian',
    'zho': 'Chinese',
    'por': 'Portuguese',
    'ukr': 'Ukrainian',
    'deu': 'German',
    'eng': 'English',
    'rus': 'Russian',
    'fra': 'French',
    'spa': 'Spanish',
    'eus': 'Basque',
    'cat': 'Catalan',
    'glg': 'Galician',
    'kor': 'Korean',
    'lit': 'Lithuanian',
    'jpn': 'Japanese',
    'slk': 'Slovak',
    'pol': 'Polish',
    'heb': 'Hebrew',
    'tha': 'Thai',
    'ces': 'Czech',
}



def check_ids_unique(data_root, verbose=False):
    _, video_paths = get_json_files(data_root)

    bad_lang_by_path = {}
    for file_path in video_paths:
        with open(file_path, encoding='UTF-8') as fp:
            blob = json.load(fp)
            lang = blob.get('language')
            if lang and lang not in VIDEO_LANGUAGE_NAMES:
                bad_lang_by_path[file_path] = lang

    if bad_lang_by_path:
        print('Incorrect languages found:')
        for path, lang in bad_lang_by_path.items():
            print('{} {}'.format(lang, path))
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

