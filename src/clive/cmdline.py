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

import sys
import traceback
from textwrap import dedent

import click

from clive import __version__
from clive.lib import load_json_data
from clive.validate import validate_item


USAGE = '%prog [options] [command] [command-options]'
VERSION = 'clive ' + __version__


def click_run():
    sys.excepthook = exception_handler
    cli(obj={})


@click.group()
def cli():
    pass


@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def validate(ctx, paths):
    if not paths:
        raise click.UsageError('No files or directories specified.')

    error_count = 0

    for path in paths:
        data = load_json_data(path)
        print('Looking at %d items...' % len(data))
        for fn, item in data:
            try:
                validate_item(fn, item)
            except ValueError as ve:
                click.echo('Error: %s:' % fn, err=True)
                click.echo(ve, err=True)
                error_count += 1

    # FIXME: Validate things that need to be unique across the
    # dataset here.

    # FIXME: Validate file format? i.e. 2-space indents? Sort order?

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
