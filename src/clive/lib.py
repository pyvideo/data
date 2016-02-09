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

import json
import os


def load_json_data(path):
    """Parses and returns all video files for a path

    :arg path: a file or directory
    :returns: list of (filename, data) tuples for all .json files

    """
    if not path or not os.path.exists(path):
        return []

    if os.path.isfile(path):
        if not path.endswith('.json'):
            all_files = []
        else:
            all_files = [path]

    else:
        all_files = []

        for root, dirs, files in os.walk(path):
            all_files.extend(
                [os.path.join(root, fn) for fn in files if fn.endswith('.json')]
            )

    data = []

    for fn in sorted(all_files):
        with open(fn, 'r') as fp:
            data.append((fn, json.load(fp)))

    return data


def save_json_data(data_items):
    """Takes list of (fn, data) tuples and saves them all to disk

    :arg data_items: list of (fn, data) tuples to save

    """

    for fn, data in data_items:
        with open(fn, 'w') as fp:
            # FIXME: We really want an explicit sorting of the keys and not
            # sort alphabetically. Maybe switch sort_keys to False and then use
            # an OrderedDict, build the dicts by hand and then dump?
            json.dump(data, fp, indent=2, sort_keys=True)
