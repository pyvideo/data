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

"""
Extracts videos using the pyvideo API and puts them in JSON files
by category.

Usage::

    python bin/extract_videos.py

"""

import json
import os
import sys

try:
    from steve import restapi
    from steve import richardapi
except ImportError:
    print('Requires: steve')
    print('Run: pip install steve')
    raise


API_URL = 'http://pyvideo.org/api/v2/'


def get_video_id(richard_url):
    return int(richard_url.split('/video/')[1].split('/')[0])


def main(args):
    categories = richardapi.get_all_categories(API_URL)
    data_path = os.path.join(os.getcwd(), 'data')

    try:
        os.mkdir(data_path)
    except OSError:
        pass

    for cat in categories:
        print('Working on %s...' % cat['title'])
        # make the category directory
        path = os.path.join(data_path, cat['slug'])
        try:
            os.mkdir(path)
        except OSError:
            pass

        # save category data
        with open(os.path.join(path, 'category.json'), 'w') as fp:
            fp.write(
                json.dumps({
                    'title': cat['title'],
                    'description': cat['description'],
                    'url': cat['url'],
                    'slug': cat['slug'],
                    'start_date': cat['start_date']
                })
            )

        videos_path = os.path.join(path, 'videos')
        try:
            os.mkdir(videos_path)
        except OSError:
            pass

        # pull down the video data
        for video_url in cat['videos']:
            print('   %s' % video_url)
            video_id = get_video_id(video_url)
            try:
                video = richardapi.get_video(
                    api_url=API_URL,
                    auth_token=None,
                    video_id=video_id
                )
            except restapi.Http4xxException:
                # If we get this, then the video is in draft. Let's just skip
                # it.
                print('      404')
                continue

            # if this video is a "draft", then skip it
            if video['state'] == 2:
                print '   ... skipping: draft'
                continue

            # ditch embed because that's gross
            del video['embed']

            # if the language is None, then set it to English which is
            # probably right.
            if not video['language']:
                video['language'] = 'English'

            # ditch the slug because we don't need those anymore.
            slug = video['slug']
            del video['slug']

            # ditch the id because we don't need that anymore, either.
            del video['id']

            # delete added and updated since we don't need those anymore.
            del video['added']
            del video['updated']

            # ditch state
            del video['state']

            video_fn = os.path.join(videos_path, slug) + '.json'
            with open(video_fn, 'w') as fp:
                fp.write(json.dumps(video))

    return


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
