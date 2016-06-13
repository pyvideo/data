import argparse

from tools.utils import get_json_files


def check_dir_structure(data_root, verbose=False):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-v", "--verbose",
                        type=int,
                        help="increase output verbosity")
    args = parser.parse_args()

    check_dir_structure(args.data_root, verbose=args.verbose)


if __name__ == '__main__':
    main()

