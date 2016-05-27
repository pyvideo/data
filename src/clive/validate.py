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

from clive.pyvideo_schema import SCHEMAS
from clive.schemalib import ERROR, WARNING, get_version


def validate_item(fn, json_data):
    # FIXME: This is kind of cheating. Need a better way to distinguish data
    # types.
    type_ = 'category' if fn.endswith('category.json') else 'video'
    vers = get_version(json_data)
    return SCHEMAS[vers][type_].validate(json_data, 'TOP')


def validate_items(items):
    all_results = []
    for fn, data in items:
        all_results.extend(validate_item(data))

    return all_results
