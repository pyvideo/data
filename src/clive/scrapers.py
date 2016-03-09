# Copyright (C) 2016  Sheila Miguez, Will Kahn-Greene
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
import subprocess
from datetime import datetime
from urllib.parse import urlparse

from slugify import slugify


def is_youtube(url):
    parsed = urlparse(url)
    return parsed.netloc.startswith(
        ('www.youtube.com', 'youtube.com', 'youtu.be'))


class ScraperError(Exception):
    pass


class Scraper(object):
    def scrape(self, url):
        """Takes a url and returns list of dicts or None if not handled"""
        raise NotImplemented


class YoutubeScraper(object):
    def transform_item(self, item):
        """Converts youtube-dl output to richard fields"""
        return {
            'title': item.get('fulltitle', item['title']),
            'summary': item['description'],
            'description': '',
            'category': '',
            'quality_notes': '',
            'language': '',
            'copyright_text': '',
            'thumbnail_url': item['thumbnail'],
            'duration': item['duration'],
            'source_url': item['webpage_url'],
            'recorded': datetime.strptime(item['upload_date'], '%Y%m%d'),
            'slug': slugify(item['fulltitle'], to_lower=True, max_length=50),
            'tags': item.get('categories', []) + item.get('tags', []),
            'speakers': [],
            'videos': [{
                'length': 0,
                'url': item['webpage_url'],
                'type': 'youtube'
            }]
        }

    def scrape(self, url):
        """Scrapes a url by passing it through youtube-dl"""
        if not is_youtube(url):
            return

        # FIXME: Sometimes youtube-dl takes a *long* time to run. This
        # needs to give indication of progress.
        try:
            output = subprocess.check_output(
                ['youtube-dl', '-j', url],
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as cpe:
            raise ScraperError('youtube-dl said "{0}".'.format(cpe.output))
        except OSError:
            raise ScraperError('youtube-dl not installed or not on PATH.')

        # Each line is a single JSON object.
        items = []
        for line in output.splitlines():
            # FIXME: Do we know for a fact that it's utf-8?
            items.append(json.loads(line.decode('utf-8')))

        items = [self.transform_item(item) for item in items]

        return items


def scrape_videos(url):
    """Scrapes a url for video data. Returns list of dicts.

    :arg url: The url to fetch data from

    :returns: list of dicts

    >>> scrape_videos('https://www.youtube.com/user/PyConDE/videos')
    [...]

    """
    # FIXME: generate list of available scrapers.
    # FIXME: run url through all available scrapers.
    return YoutubeScraper().scrape(url)
