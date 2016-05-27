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

import importlib
import os
import sys
import traceback
from textwrap import dedent

import click

from clive import __version__
from clive.lib import load_json_data, save_json_data
from clive.scrapers import scrape_videos
from clive.validate import ERROR, WARNING, validate_item


USAGE = '%prog [options] [command] [command-options]'
VERSION = 'clive ' + __version__


def click_run():
    sys.excepthook = exception_handler
    cli(obj={})


@click.group()
def cli():
    pass


@cli.command()
@click.option('--errorsonly/--no-errorsonly', default=False, help='Only print errors.')
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def validate(ctx, errorsonly, paths):
    """Validates JSON file data located in PATHS."""
    if not paths:
        raise click.UsageError('No files or directories specified.')

    errors_count = 0
    warnings_count = 0

    for path in paths:
        data = load_json_data(path)
        click.echo('Looking at %d items...' % len(data))
        for fn, item in data:
            results = validate_item(fn, item)
            if results:
                errors = [res for res in results if res.level == ERROR]
                errors_count += len(errors)

                for err in errors:
                    click.echo(
                        '%(fn)s ERROR:%(name)s:%(msg)s' % {
                            'fn': fn, 'name': err.name, 'msg': err.msg
                        },
                        err=True
                    )

                if not errorsonly:
                    warnings = [res for res in results if res.level == WARNING]
                    warnings_count += len(warnings)

                    for warn in warnings:
                        click.echo(
                            '%(fn)s WARN:%(name)s:%(msg)s' % {
                                'fn': fn, 'name': warn.name, 'msg': warn.msg
                            }
                        )

    # FIXME: Validate things that need to be unique across the
    # dataset here.

    # FIXME: Validate file format? i.e. 2-space indents? Sort order?

    if not errorsonly:
        print('%d warnings found.' % warnings_count)
    print('%d errors found.' % errors_count)

    print('Done!')
    ctx.exit(code=1 if errors_count else 0)


@cli.command()
@click.option('--transform', '-t', type=str, multiple=True)
@click.argument('url', nargs=1)
@click.argument('path', nargs=1)
@click.pass_context
def fetch(ctx, transform, url, path):
    """Scrapes video data at URL and saves it as JSON files in the PATH
    directory.

    """
    error_count = 0
    path = os.path.abspath(path)

    # Summarize what we're going to do to the user.
    click.echo('Fetching videos from:     %s' % url)
    click.echo('Saving video data to:     %s' % path)
    click.echo('Applying transforms from: %s' % ', '.join(transform))
    click.echo('')
    click.confirm('Do you want to continue?', abort=True)

    if not os.path.exists(path):
        click.echo('Creating %s...' % path)
        os.makedirs(path)

    # Scrape the data from wherever.
    click.echo('Fetching data... (this can take a long time)')
    # FIXME: Add some kind of progress bar here
    data = scrape_videos(url)

    click.echo('Found %d items.' % len(data))
    for tr in transform:
        # FIXME: We might want to change how this works so that it's more
        # flexible.
        click.echo('Applying transform %s' % tr)
        module, name = tr.rsplit('.', 1)
        module = importlib.import_module(module)
        tr_callable = getattr(module, name)
        data = tr_callable(data)

    # FIXME: Go through and fix the slugs so they're unique for this data set?

    # Save the data to the path specified.
    data = [
        (os.path.join(path, item['slug'] + '.json'), item)
        for item in data
    ]
    save_json_data(data)

    print('Done!')
    ctx.exit(code=1 if error_count else 0)


def exception_handler(exc_type, exc_value, exc_tb):
    click.echo(dedent("""\
    Oh no! Clive has thrown an error while trying to do stuff. Please write
    up a bug report with the specifics so that we can fix it.

    https://github.com/pyvideo/pyvideo-data/issues

    Here is some information you can copy and paste into the bug report:

    """))
    click.echo('---')
    click.echo('Clive: %s' % repr(__version__))
    click.echo('Python: %s' % repr(sys.version))
    click.echo('Command line: %s' % repr(sys.argv))
    click.echo()
    click.echo(
        ''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    click.echo('---')
