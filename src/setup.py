#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click',
    'youtube-dl',
    'awesome-slugify',
]

setup(
    name='clive',
    version='0.1.0',
    description='Data tools for pyvideo-data.',
    long_description=readme + '\n\n' + history,
    url='https://github.com/pyvideo/pyvideo-data',
    packages=[
        'clive',
    ],
    package_dir={
        'clive': 'clive'
    },
    include_package_data=True,
    install_requires=requirements,
    license='AGPLv3',
    zip_safe=False,
    entry_points="""
        [console_scripts]
        clive-cmd=clive.cmdline:click_run
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
