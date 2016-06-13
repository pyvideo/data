import json

from tools.constants import JSON_FORMAT_KWARGS


def reserialize(file_):
    with open(file_) as fp:
        data = json.load(fp)

    with open(file_, 'w') as fp:
        json.dump(data, fp, JSON_FORMAT_KWARGS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to edit")
    args = parser.parse_args()

    reserialize(args.file)


if __name__ == '__main__':
    main()

