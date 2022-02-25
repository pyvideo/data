"""Test to check reasonable file length.

While most filesystems should allow 255 bytes filenames, eCryptfs
needs to prepend some data to encrypted filenames, they recommend
limiting filenames to ~140 characters.
"""

import argparse
import sys
from pathlib import Path


def check_filename_length(data_root, verbose=False):
    too_long = []
    for file in Path(data_root).glob("**/*"):
        if len(file.name.encode("UTF-8")) >= 140:
            too_long.append(file)
    if too_long:
        print("Files that have an unreasonably long name:")
        for file in too_long:
            print(f" - {file}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root", help="directory to search for JSON files")
    parser.add_argument("-v", "--verbose", type=int, help="increase output verbosity")
    args = parser.parse_args()

    check_filename_length(args.data_root, verbose=args.verbose)


if __name__ == "__main__":
    main()
