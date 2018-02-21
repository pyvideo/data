import argparse
import difflib
import json
import sys

from tools.constants import JSON_FORMAT_KWARGS
from tools.utils import get_json_files


def check_render_rest(data_root, verbose=False):
    category_paths, video_paths = get_json_files(data_root)

    file_paths = category_paths + video_paths

    error_by_path = {}
    for file_path in file_paths:
        with open(file_path, encoding='UTF-8') as fp:
            serialized_blob = fp.read()
            re_serialized_blob = json.dumps(
                json.loads(serialized_blob),
                **JSON_FORMAT_KWARGS
            )
            if serialized_blob.strip() != re_serialized_blob.strip():
                error_by_path[file_path] = (serialized_blob, re_serialized_blob)

    if error_by_path:
        for path, blobs in error_by_path.items():
            print('Incorrect serialization order in {}'.format(path), flush=True)
            blobs = tuple(blob.splitlines(keepends=True) for blob in blobs)
            if verbose:
                print(''.join(difflib.ndiff(*blobs)), end="")
        sys.exit(1)


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

