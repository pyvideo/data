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

import re
import time
from collections import namedtuple

Result = namedtuple('Result', ('line', 'col', 'name', 'msg'))


class T:
    def __init__(self, required=False, *args, **kwargs):
        self.required = required

    def validate(self, val, depth, results):
        if self.required and val is None:
            results.append(Result(0, 0, depth, 'value required'))


class IntT(T):
    def validate(self, val, depth, results):
        super().validate(val, depth, results)
        if val is None:
            return

        if not isinstance(val, int):
            results.append(Result(0, 0, depth, 'value is not a valid int: %r' % val))


class BoolT(T):
    def validate(self, val, depth, results):
        super().validate(val, depth, results)
        if val is None:
            return

        if val not in (True, False):
            results.append(Result(0, 0, depth, 'value is not a valid bool: %r' % val))


SLUG_RE = re.compile(r'^[a-zA-Z0-9_-]+$')


class TextT(T):
    def __init__(self, required=False, slug=False, markdown=False, url=False,
                 *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.markdown = markdown
        self.slug = slug
        self.url = url

    def validate(self, val, depth, results):
        super().validate(val, depth, results)
        if val is None:
            return

        if not isinstance(val, str):
            results.append(Result(0, 0, depth, 'value is not a valid text value: %r' % val))
            return

        # FIXME: markdown check here

        # FIXME: slug check here
        if self.slug and not SLUG_RE.match(val):
            results.append(Result(0, 0, depth, 'value is not a valid slug: %r' % val))
            return

        # FIXME: url check here


class DateT(T):
    def validate(self, val, depth, results):
        super().validate(val, depth, results)
        if val is None:
            return
        try:
            time.strptime(val, '%Y-%m-%d')
        except ValueError:
            results.append(Result(0, 0, depth, 'value is not date in YYYY-MM-DD format: %r' % val))


class ListOfT(T):
    def __init__(self, subtype, required=False, *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.subtype = subtype

    def validate(self, val, depth, results):
        super().validate(val, depth, results)
        if not isinstance(val, (tuple, list)):
            results.append(Result(0, 0, depth, 'value is not a list: %r' % val))
            return

        for i, item in enumerate(val):
            self.subtype.validate(item, '%s[%s]' % (depth, i), results)


class DictOfT(T):
    def __init__(self, keyvals, required=False, *args, **kwargs):
        super().__init__(required=required, *args, **kwargs)
        self.keyvals = keyvals
        self.all_keys = set(self.keyvals.keys())

    def validate(self, val, depth, results):
        if not isinstance(val, dict):
            results.append(Result(0, 0, depth, 'value is not a dict: %r' % val))

        # Verify all keys are known
        if not set(val.keys()).issubset(self.all_keys):
            results.append(Result(0, 0, depth, 'unknown keys: %s' % repr(set(val.keys()) - self.all_keys)))

        # Verify values
        for key, item in val.items():
            self.keyvals[key].validate(item, '%s:%s' % (depth, key), results)


REQS = {
    'video': DictOfT({
        # FIXME: This is a leftover from pyvideo. Do we need this?
        'id': IntT(),

        # FIXME: This could be inferred from the directory.
        'category': TextT(required=True),

        # FIXME: This has to be unique across the data-set. That's tricky.
        'slug': TextT(required=True, slug=True),

        'title': TextT(required=True),
        'summary': TextT(required=True, markdown=True),
        'description': TextT(markdown=True),
        'quality_notes': TextT(markdown=True),
        'language': TextT(required=True),
        'copyright_text': TextT(required=True),
        'thumbnail_url': TextT(url=True),
        'duration': IntT(),
        'videos': ListOfT(
            DictOfT({
                'length': IntT(),
                'url': TextT(required=True, url=True),

                # FIXME: This needs thinking.
                'type': TextT(required=True)
            })
        ),
        'source_url': TextT(url=True),
        'recorded': DateT(),
        'tags': ListOfT(TextT()),
        'speakers': ListOfT(TextT()),
    }),

    'category': DictOfT({
        'title': TextT(required=True),
        'description': TextT(markdown=True),
        'url': TextT(url=True),
        'start_date': DateT(),

        # FIXME: This has to be unique across the data-set. Can we just use the
        # directory name?
        'slug': TextT(required=True, slug=True),
    })
}


def validate_item(fn, json_data):
    # FIXME: This is kind of cheating. Need a better way to distinguish data
    # types.
    type_ = 'category' if fn.endswith('category.json') else 'video'
    results = []
    REQS[type_].validate(json_data, 'TOP', results)
    return results


def validate_items(items):
    all_results = []
    for fn, data in items:
        all_results.extend(validate_item(data))

    return all_results
