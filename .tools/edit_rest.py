import argparse
import json
import os
from subprocess import call
import tempfile


EDITOR = os.environ.get('EDITOR', 'vim')


def get_edited_text(original_text):
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(original_text.encode())
        tf.flush()
        call([EDITOR, tf.name])

        with open(tf.name) as fp:
            return fp.read()


def edit_rest(file_, key):
    key = 'description' if key.strip().startswith('d') else 'summary'

    with open(file_) as fp:
        data = json.load(fp)

    data[key] = get_edited_text(data[key])

    with open(file_, 'w') as fp:
        json.dump(data,
                  fp,
                  indent=4,
                  sort_keys=True,
                  separators=(', ', ': '))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to edit")
    parser.add_argument("key", help="key's value to edit (summary or description)")
    args = parser.parse_args()

    edit_rest(args.file, args.key)


if __name__ == '__main__':
    main()

