import argparse
import json
import sys
import textwrap

import docutils
from docutils.parsers import rst

import sys
sys.path.insert(0, '.')
from tools.utils import get_json_files

# Presence of these keys in a docutils node's attributes is an
# indicator of a possible render error. They will be used as
# as part of a litmus test to determine if a document contains
# render errors
ERROR_ATTRS = ('type', 'line', 'level')

# Lowest error level that qualifies a ReST blob as invalid
INVALID_ERROR_LEVEL = 2


class InvalidReSTError(Exception):
    pass


class ReSTValidatorVisitor(docutils.nodes.SparseNodeVisitor):
    def dispatch_visit(self, node):
        if isinstance(node, docutils.nodes.system_message):
            attributes = getattr(node, 'attributes', {})
            contains_errors = all(attr in attributes for attr in ERROR_ATTRS)
            if contains_errors:
                raise InvalidReSTError(str(node), attributes.get('level'))


def validate_rest(text):
    components=(docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(components).get_default_values()
    document = docutils.utils.new_document('', settings)
    rst.Parser().parse(text, document)

    try:
        document.walk(ReSTValidatorVisitor(document))
        return False, None
    except InvalidReSTError as e:
        return e.args[0], e.args[1]


def check_render_rest(data_root, verbose=False):
    _, video_paths = get_json_files(data_root)

    fields = ('description', 'summary')

    error_by_path = {}
    valid = True
    for file_path in video_paths:
        with open(file_path, encoding='UTF-8') as fp:
            blob = json.load(fp)

            for field in fields:
                # A description or summary maybe None.
                # Ensure text is a string.
                text = blob.get(field) or ''
                error, level = validate_rest(text)
                if error and level >= INVALID_ERROR_LEVEL:
                    valid = False

                if error:
                    msg = 'ReST validation error (level {level}):\n\tFile: {fp}\n\tKey: {key}\n\tError:\n{error}'
                    print(msg.format(fp=file_path, key=field, level=level, error=textwrap.indent(error,'\t\t')), flush=True)
                    if verbose:
                        print('\t', error, sep='', flush=True)

    if not valid:
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

