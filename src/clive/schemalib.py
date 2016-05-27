# Copyright (C) 2015, 2016  Sheila Miguez, Will Kahn-Greene
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['T', 'IntT', 'TextT', 'DateT', 'BoolT', 'ListOfT', 'DictOfT']

import re
import time
from collections import namedtuple

Result = namedtuple('Result', ('line', 'col', 'name', 'msg'))


class T:
    def __init__(self, required=False, *args, **kwargs):
        self.required = required

    def validate(self, val, depth):
        if self.required and val is None:
            return [Result(0, 0, depth, 'value required')]
        return []


class IntT(T):
    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))

        if val is None:
            return results

        if not isinstance(val, int) or isinstance(val, bool):
            results.append(Result(0, 0, depth, 'value is not a valid int: %r' % val))

        return results


class BoolT(T):
    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))
        if val is None:
            return results

        if not isinstance(val, bool):
            results.append(Result(0, 0, depth, 'value is not a valid bool: %r' % val))

        return results


SLUG_RE = re.compile(r'^[a-zA-Z0-9_-]+$')


class TextT(T):
    def __init__(self, required=False, slug=False, markdown=False, url=False,
                 *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.markdown = markdown
        self.slug = slug
        self.url = url

    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))
        if val is None:
            return results

        if not isinstance(val, str):
            results.append(Result(0, 0, depth, 'value is not a valid text value: %r' % val))

        # FIXME: markdown check here

        # FIXME: slug check here
        if self.slug and not SLUG_RE.match(val):
            results.append(Result(0, 0, depth, 'value is not a valid slug: %r' % val))

        # FIXME: url check here
        return results


class DateT(T):
    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))
        if val is None:
            return results

        try:
            time.strptime(val, '%Y-%m-%d')
        except ValueError:
            results.append(Result(0, 0, depth, 'value is not date in YYYY-MM-DD format: %r' % val))

        return results


class ListOfT(T):
    def __init__(self, subtype, required=False, *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.subtype = subtype

    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))
        if val is None:
            return results

        if not isinstance(val, (tuple, list)):
            results.append(Result(0, 0, depth, 'value is not a list: %r' % val))
            return results

        for i, item in enumerate(val):
            results.extend(
                self.subtype.validate(item, '%s[%s]' % (depth, i))
            )
        return results


class DictOfT(T):
    def __init__(self, keyvals, required=False, *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.keyval_dict = dict(keyvals)
        self.keyvals = keyvals

    # FIXME: Might want to make this more dict-like
    def __getitem__(self, name):
        return self.keyval_dict.__getitem__(name)

    def validate(self, val, depth):
        results = []
        results.extend(super().validate(val, depth))
        if val is None:
            return results

        if not isinstance(val, dict):
            results.append(Result(0, 0, depth, 'value is not a dict: %r' % val))
            return results

        # Verify values
        for key, item in sorted(val.items()):
            # For unknown keys, print an error
            if key not in self.keyval_dict.keys():
                results.append(Result(0, 0, depth, 'unknown key: %r' % key))
                continue

            results.extend(
                self[key].validate(item, '%s:%s' % (depth, key))
            )
        return results


def get_type(json_data):
    return json_data.get('schema_type', 'video')


def get_version(json_data):
    """Returns the schema version for this data object

    :returns: version as a string

    """
    return json_data.get('schema_version', '1')
