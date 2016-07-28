import os
import glob
import re

from jinja2 import Markup
import six


def get_json_files(root, exclude=None):
    exclude = exclude if exclude else set()

    category_pattern = os.path.join(root, '**/category.json')
    video_pattern = os.path.join(root, '**/videos/*.json')

    category = [path for path in glob.iglob(category_pattern) if path not in exclude]
    video = [path for path in glob.iglob(video_pattern) if path not in exclude]

    return category, video


def slugify(value, substitutions=()):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    Took from Django sources.
    Taken from Pelican sources.
    """
    # TODO Maybe steal again from current Django 1.5dev
    value = Markup(value).striptags()
    # value must be unicode per se
    import unicodedata
    from unidecode import unidecode
    # unidecode returns str in Py2 and 3, so in Py2 we have to make
    # it unicode again
    value = unidecode(value)
    if isinstance(value, six.binary_type):
        value = value.decode('ascii')
    # still unicode
    value = unicodedata.normalize('NFKD', value).lower()

    # backward compatible covert from 2-tuples to 3-tuples
    new_subs = []
    for tpl in substitutions:
        try:
            src, dst, skip = tpl
        except ValueError:
            src, dst = tpl
            skip = False
        new_subs.append((src, dst, skip))
    substitutions = tuple(new_subs)

    # by default will replace non-alphanum characters
    replace = True
    for src, dst, skip in substitutions:
        orig_value = value
        value = value.replace(src.lower(), dst.lower())
        # if replacement was made then skip non-alphanum
        # replacement if instructed to do so
        if value != orig_value:
            replace = replace and not skip

    if replace:
        value = re.sub('[^\w\s-]', '', value).strip()
        value = re.sub('[-\s]+', '-', value)
    else:
        value = value.strip()

    # we want only ASCII chars
    value = value.encode('ascii', 'ignore')
    # but Pelican should generally use only unicode
    return value.decode('ascii')

