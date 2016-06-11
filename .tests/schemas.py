import argparse
import json
import os

import jsonschema

from utils import get_json_files


def check_schemas(data_root, schemas_dir):
    cateory_files, video_files = get_json_files(data_root)

    #with open(os.path.join(schemas_dir, 'category.json'), encoding='UTF-8') as fp:
    #    category_schema = json.load(fp)

    #for category in cateory_files:
    #    with open(category, encoding='UTF-8') as fp:
    #        blob = json.load(fp)
    #        validate(blob, category_schema)

    with open(os.path.join(schemas_dir, 'video.json'), encoding='UTF-8') as fp:
        video_schema = json.load(fp)

    for video in video_files:
        with open(video, encoding='UTF-8') as fp:
            blob = json.load(fp)
            try:
                jsonschema.validate(blob, video_schema)
            except jsonschema.exceptions.ValidationError as e:
                print(video)
                if True:
                    print(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-s", "--schemas-dir",
                        help="directory containing schema files") 
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()

    check_schemas(args.data_root, args.schemas_dir)


if __name__ == '__main__':
    main()

