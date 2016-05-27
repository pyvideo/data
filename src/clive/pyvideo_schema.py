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

from clive.schemalib import *


SCHEMAS = {
    # Version 1. Published XXX.
    '1': {
        'video': DictOfT([
            # FIXME: This is a leftover from pyvideo. Do we need this?
            ('id', IntT()),

            # FIXME: This could be inferred from the directory.
            ('category', TextT(required=True)),

            # FIXME: This has to be unique across the data-set. That's tricky.
            ('slug', TextT(required=True, slug=True)),

            ('title', TextT(required=True)),
            ('summary', TextT(required=True, is_reST=True)),
            ('description', TextT(is_reST=True)),
            ('quality_notes', TextT(is_reST=True)),
            ('language', TextT(required=True)),
            ('copyright_text', TextT(required=True)),
            ('thumbnail_url', TextT(url=True)),
            ('duration', IntT()),
            ('videos', ListOfT(
                DictOfT([
                    ('length', IntT()),
                    ('url', TextT(required=True, url=True)),

                    # FIXME: This needs thinking.
                    ('type', TextT(required=True)),
                ]))
            ),
            ('source_url', TextT(url=True)),
            ('tags', ListOfT(TextT())),
            ('speakers', ListOfT(TextT())),
            ('recorded', DateT()),
        ]),

        'category': DictOfT([
            ('title', TextT(required=True)),
            ('description', TextT(is_reST=True)),
            ('url', TextT(url=True)),
            ('start_date', DateT()),

            # FIXME: This has to be unique across the data-set. Can we just use the
            # directory name?
            ('slug', TextT(required=True, slug=True)),
        ]),
    }
}
